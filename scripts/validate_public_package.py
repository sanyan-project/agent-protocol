from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    ".github",
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PROTOCOL.md",
    "README.md",
    "README_EN.md",
    "SECURITY.md",
    "WHITEPAPER.md",
    "docs",
    "examples",
    "health_check.py",
    "public-files.txt",
    "pyproject.toml",
    "sanyan_protocol",
    "scripts",
    "tests",
}
FORBIDDEN = (
    "D:" + "/360MoveData",
    "/Users" + "/",
    "黄" + "sir",
    "audit_" + "memory.json",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}"),
)


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key!r}")
        value[key] = item
    return value


def main() -> int:
    actual = {path.name for path in ROOT.iterdir() if path.name != ".git"}
    if actual != REQUIRED:
        raise SystemExit(f"public boundary mismatch: missing={sorted(REQUIRED-actual)} extra={sorted(actual-REQUIRED)}")
    expected_files = {
        line.strip()
        for line in (ROOT / "public-files.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    actual_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
        and path.suffix != ".pyc"
        and not any(part.endswith(".egg-info") for part in path.relative_to(ROOT).parts)
    }
    if expected_files != actual_files:
        raise SystemExit(f"file allowlist mismatch: missing={sorted(expected_files-actual_files)} extra={sorted(actual_files-expected_files)}")
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_symlink():
            raise SystemExit(f"symlink not allowed: {path.relative_to(ROOT)}")
        if path.is_dir():
            continue
        if path.stat().st_size > 1_000_000:
            raise SystemExit(f"file exceeds public size limit: {path.relative_to(ROOT)}")
        if path.suffix not in {".json", ".md", ".py", ".toml", ".txt", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN:
            if marker in text:
                raise SystemExit(f"private marker {marker!r} in {path.relative_to(ROOT)}")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            raise SystemExit(f"credential-like text in {path.relative_to(ROOT)}")
        if path.suffix == ".json":
            try:
                json.loads(text, object_pairs_hook=unique_object)
            except (json.JSONDecodeError, ValueError, RecursionError) as exc:
                raise SystemExit(f"invalid JSON in {path.relative_to(ROOT)}: {type(exc).__name__}") from exc
    print("public-package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
