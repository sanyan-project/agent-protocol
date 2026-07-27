# Protocol contract v1.0-alpha

An audit record is one JSON object with exactly these fields:

| Field | Contract |
|---|---|
| `schema_version` | `1.0-alpha` |
| `task_id` | Non-empty string |
| `executor` | Non-empty role identifier |
| `reviewer` | Non-empty role identifier different from `executor` |
| `risk` | `low`, `medium`, or `high` |
| `human_approved` | Boolean; must be true for `high` risk |
| `stages` | Exactly `observe`, `orient`, `decide`, `act`, `reflect`, `persist` |
| `claims` | Non-empty list of `{text, citation}` objects |
| `outcome` | `completed`, `stopped`, or `blocked` |
| `stop_condition` | Non-empty explanation of why the run ended or should stop |

Each citation uses `relative/path:line`. Absolute paths, `..` traversal, unknown
files, non-regular files, line zero, lines beyond EOF, and blank target lines
fail closed. Line numbers are bounded to 1,000,000 and cited files must be UTF-8
text. Duplicate JSON object keys are rejected. Role identifiers are compared
after trimming, Unicode NFKC normalization, and case folding. The audit root is explicit; it is never inferred from user
configuration or conversation history.

Record files are limited to 1,000,000 bytes. Excessive JSON nesting is returned
as a structured input error rather than escaping as a runtime traceback.

Exit code is `0` for `PASS`, `1` for a valid record that fails a gate, and `2`
for malformed input or invocation errors. Reports contain gate results but do
not persist source-file contents.
