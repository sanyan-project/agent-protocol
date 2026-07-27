from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Mapping


REQUIRED_STAGES = ("observe", "orient", "decide", "act", "reflect", "persist")
RECORD_FIELDS = {
    "schema_version",
    "task_id",
    "executor",
    "reviewer",
    "risk",
    "human_approved",
    "stages",
    "claims",
    "outcome",
    "stop_condition",
}
CLAIM_FIELDS = {"text", "citation"}
CITATION = re.compile(r"(?P<path>[^:\n]+):(?P<line>[1-9][0-9]{0,6})\Z")
MAX_CITATION_LINE = 1_000_000
MAX_RECORD_BYTES = 1_000_000


class InvalidRecord(ValueError):
    """Raised when the input cannot be interpreted as a protocol record."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise InvalidRecord(f"duplicate JSON key: {key!r}")
        value[key] = item
    return value


def load_record(path: Path) -> dict[str, Any]:
    if path.stat().st_size > MAX_RECORD_BYTES:
        raise InvalidRecord(f"record exceeds {MAX_RECORD_BYTES} byte limit")
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except RecursionError as exc:
        raise InvalidRecord("record nesting exceeds the supported limit") from exc
    if not isinstance(value, dict):
        raise InvalidRecord("record root must be an object")
    return value


def _schema_errors(record: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    fields = set(record)
    if fields != RECORD_FIELDS:
        if missing := RECORD_FIELDS - fields:
            errors.append(f"missing fields: {sorted(missing)}")
        if extra := fields - RECORD_FIELDS:
            errors.append(f"unknown fields: {sorted(extra)}")
    if record.get("schema_version") != "1.0-alpha":
        errors.append("schema_version must be 1.0-alpha")
    for field in ("task_id", "executor", "reviewer"):
        if not isinstance(record.get(field), str) or not str(record.get(field)).strip():
            errors.append(f"{field} must be a non-empty string")
    if record.get("risk") not in {"low", "medium", "high"}:
        errors.append("risk must be low, medium, or high")
    if not isinstance(record.get("human_approved"), bool):
        errors.append("human_approved must be boolean")
    for field in ("outcome", "stop_condition"):
        if not isinstance(record.get(field), str):
            errors.append(f"{field} must be a string")
    stages = record.get("stages")
    if not isinstance(stages, list) or not all(isinstance(item, str) for item in stages):
        errors.append("stages must be a list of strings")
    claims = record.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
    else:
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict) or set(claim) != CLAIM_FIELDS:
                errors.append(f"claims[{index}] must contain exactly text and citation")
                continue
            for field in CLAIM_FIELDS:
                if not isinstance(claim[field], str) or not claim[field].strip():
                    errors.append(f"claims[{index}].{field} must be a non-empty string")
    return errors


def _citation_error(citation: str, root: Path) -> str | None:
    match = CITATION.fullmatch(citation)
    if not match:
        return "citation must use relative/path:positive-line"
    try:
        relative = Path(match.group("path"))
        if relative.is_absolute() or ".." in relative.parts:
            return "citation path must stay inside the audit root"
        resolved_root = root.resolve()
        candidate = (resolved_root / relative).resolve()
        if candidate != resolved_root and not candidate.is_relative_to(resolved_root):
            return "citation path escapes the audit root"
        if not candidate.is_file():
            return "citation target is not a regular file"
        target_line = int(match.group("line"))
        if target_line > MAX_CITATION_LINE:
            return "citation line exceeds the supported limit"
        with candidate.open(encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                if number == target_line:
                    return None if line.strip() else "citation target line is blank"
        return "citation line is beyond end of file"
    except (OSError, UnicodeError, ValueError):
        return "citation target could not be read as UTF-8 text"


def _normalized_role(value: str) -> str:
    return unicodedata.normalize("NFKC", value).strip().casefold()


def _check(check_id: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"id": check_id, "passed": passed, "evidence": evidence}


def audit_record(record: Mapping[str, Any], root: Path) -> dict[str, Any]:
    schema_errors = _schema_errors(record)
    if schema_errors:
        raise InvalidRecord("; ".join(schema_errors))
    if not root.resolve().is_dir():
        raise InvalidRecord("audit root must be an existing directory")

    stages = tuple(record["stages"])
    state_passed = stages == REQUIRED_STAGES
    role_passed = _normalized_role(record["executor"]) != _normalized_role(record["reviewer"])

    citation_errors: list[str] = []
    for index, claim in enumerate(record["claims"]):
        if error := _citation_error(claim["citation"], root):
            citation_errors.append(f"claims[{index}]: {error}")
    citations_passed = not citation_errors

    authority_passed = record["risk"] != "high" or record["human_approved"] is True
    closeout_passed = bool(str(record["stop_condition"]).strip()) and record["outcome"] in {
        "completed",
        "stopped",
        "blocked",
    }

    checks = [
        _check("state_machine_complete", state_passed, "six required stages in fixed order"),
        _check("role_identifiers_differ", role_passed, "normalized executor and reviewer identifiers differ"),
        _check(
            "citations_exist",
            citations_passed,
            "all citations resolve to non-empty lines" if citations_passed else "; ".join(citation_errors),
        ),
        _check("high_risk_human_authority", authority_passed, "high-risk work requires human_approved=true"),
        _check("closeout_recorded", closeout_passed, "outcome and stop condition are explicit"),
    ]
    passed = all(item["passed"] for item in checks)
    return {
        "protocol_version": "1.0-alpha",
        "task_id": record["task_id"],
        "verdict": "PASS" if passed else "FAIL",
        "checks": checks,
        "passed": sum(1 for item in checks if item["passed"]),
        "failed": sum(1 for item in checks if not item["passed"]),
    }
