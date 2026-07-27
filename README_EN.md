# GateLedger

[中文](README.md) | [English](README_EN.md)

[![CI](https://github.com/sanyan-project/gate-ledger/actions/workflows/ci.yml/badge.svg)](https://github.com/sanyan-project/gate-ledger/actions/workflows/ci.yml)
[![Python 3.10–3.12](https://img.shields.io/badge/Python-3.10--3.12-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![MIT License](https://img.shields.io/badge/License-MIT-E8D7B5.svg)](LICENSE)

![Two independent agent paths pass through an audit gate and converge on an evidence scale](docs/assets/repository-cover.jpg)

> **v1.0-alpha · runnable reference · not production-ready**

**Turn role separation, evidence citations, human authority, and stop conditions into deterministic gates that fail closed.**

GateLedger is a runnable audit protocol for workflows where one agent executes
and another role reviews. It reads a structured task record plus workspace
evidence and turns these rules into deterministic, fail-closed checks:

- executor and reviewer must differ;
- the record must contain Observe, Orient, Decide, Act, Reflect, and Persist in order;
- every factual claim must cite a real, non-empty `file:line` inside the authorized workspace;
- high-risk work must record human approval;
- outcome and stop condition must be explicit;
- one failed hard gate makes the audit verdict `FAIL`.

It does not claim autonomous self-evolution or prove that a reviewer is truly
independent or correct. The current release is a deterministic protocol core
with a fully synthetic public example.

## Quick start

Python 3.10, 3.11, or 3.12 is required. There are no third-party runtime dependencies.

```bash
python health_check.py
```

The JSON report should contain `verdict: PASS` with all five hard gates passing.

The key result is:

```json
{"failed": 0, "passed": 5, "protocol_version": "1.0-alpha", "verdict": "PASS"}
```

Audit a specific record:

```bash
python -m sanyan_protocol.cli audit \
  --record examples/audit_record.json \
  --root examples/workspace
```

## Install and test

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/validate_public_package.py
```

After installation:

```bash
sanyan-audit health
```

## What the gates prove

| Gate | Deterministically checked | Not proven |
|---|---|---|
| State machine | Six stages are complete and ordered | Reasoning quality inside each stage |
| Role separation | Normalized executor and reviewer identifiers differ | Independent models or contexts |
| Citations | File is inside the root; line exists and is non-empty | Semantic entailment of the full claim |
| Human authority | High-risk record declares human approval | Approver identity |
| Closeout | Outcome and stop condition are recorded | Business success |

See [PROTOCOL.md](PROTOCOL.md) for the data contract. [WHITEPAPER.md](WHITEPAPER.md)
explains the design and clearly labels older numbers as an unverified historical
snapshot.

The fully synthetic record and regression suite cover the passing path plus
missing stages, same-role self-review, absent human approval, path traversal,
absolute paths, unknown files, out-of-range citations, and blank lines.
[GitHub CI](https://github.com/sanyan-project/gate-ledger/actions/workflows/ci.yml)
has passed the same checks on Python 3.10, 3.11, and 3.12.

## Safety and scope

Do not commit customer data, real chats, credentials, private repository paths,
or internal audit logs. Public examples must be synthetic. Run sensitive audits
locally in an authorized environment and never attach their inputs to public
issues.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Licensed
under the [MIT License](LICENSE).
