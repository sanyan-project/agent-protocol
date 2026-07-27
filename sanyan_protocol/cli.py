from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .audit import InvalidRecord, audit_record, load_record


PACKAGE_ROOT = Path(__file__).resolve().parent


def _health_record() -> dict[str, object]:
    return {
        "schema_version": "1.0-alpha",
        "task_id": "SYNTHETIC-HEALTH-001",
        "executor": "executor-demo",
        "reviewer": "reviewer-demo",
        "risk": "low",
        "human_approved": False,
        "stages": ["observe", "orient", "decide", "act", "reflect", "persist"],
        "claims": [{"text": "The installed package declares its audit module.", "citation": "__init__.py:1"}],
        "outcome": "completed",
        "stop_condition": "Stop after the installed-package smoke test runs once.",
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sanyan-audit")
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit", help="audit one protocol record")
    audit.add_argument("--record", type=Path, required=True)
    audit.add_argument("--root", type=Path, required=True)
    commands.add_parser("health", help="run the shipped synthetic protocol check")
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(arguments)
    try:
        if args.command == "health":
            report = audit_record(_health_record(), PACKAGE_ROOT)
        else:
            report = audit_record(load_record(args.record), args.root)
        print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
        return 0 if report["verdict"] == "PASS" else 1
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(json.dumps({"verdict": "ERROR", "error": str(exc)}, ensure_ascii=True, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
