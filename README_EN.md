# Sanyan Agent Collaboration Protocol v1.0-alpha

> Human-AI Agent collaboration engineering reference
> **⚠️ alpha: mechanisms deployed, execution rate under validation.**

## Status

| Metric | Target | Actual | Gap |
|:--|:--|:--|:--|
| Self-audit ratio | ≤5:1 | 15:1 | 🔴 Pending |
| Pending closure | >80% | ~11% | 🔴 Backlog |
| OODA completion | >95% | Untracked | 🟡 New |

**This document describes the target state under construction**, not current reality. Hard gates deployed 2026-05-29; execution metrics need time.

## Team

- **Sanyan Lead** (Human) — Final decision-maker. Threshold-based intervention.
- **SiSi** (AI Agent) — Execution core. Code / Ops / Content / Decisions
- **TianPing** (AI Agent) — Independent auditor. First-order audit + self-audit
- **Jian** (AI Agent) — Cloud observer. Engine monitoring + concept discovery (WIP)

### Intervention Protocol

| Trigger | Action |
|:--|:--|
| External audit 🔴 alert | Lead must intervene |
| Quality score drops 2 weeks | Lead notified, optional intervention |
| Major direction change | Lead must confirm |
| Normal operations | Lead not involved; SiSi+TianPing auto-run |

## Execution Gates (SiSi)

### OODA State Machine
Every task: [OODA:Observe]→[OODA:Orient]→[OODA:Decide]→[OODA:Act]→[OODA:Reflect]→[OODA:Persisted]

### Sanyan 4-Step
Essence → (Concept Match) → Simplest → Chain → Inverse

### Guardrail Regex
Code assertions must carry file:line. Auto-validated.

### Reflection JSON
Structured post-task reflection.

## Audit Gates (TianPing)

### ASE Audit System
26+ audits. Each produces verdict + evidence + pending items.

### Pre-audit Gate
Mandatory read of audit_memory.json + error_patterns.json before each audit.

### Self-Audit (Hard Gate)
Every 5 ASE audits → forced self-audit. Ratio > 5:1 → alert.

### External Perspective Simulator
Every 50 rounds: switch to "stranger" perspective audit.

## Observability

### Quality Score
SiSi 5-dim × TianPing 4-dim = composite health score.

### Failure Ritual
Fail → 5Why → pattern match → Guardrail update → TianPing confirm.

### Dashboard (6 metrics)
OODA rate · Guardrail rate · Reflection rate · Self-audit ratio · Memory rate · External audit rating.

## Assets (12 files)

guardrail_checker.py · external_auditor.py · meta_audit.py · health_check.py · error_patterns.json · quality_score.json · failure_ritual.json · memory_health.json · reflection_template.json · concept_driven.json · external_view_simulator.json · dashboard_v0.md

## How to Use

```bash
python health_check.py  # One-click health check
```

MIT License. Reference freely.

## Version

v1.0-alpha · 2026-05-29 · Initial (mechanisms deployed, metrics pending)
