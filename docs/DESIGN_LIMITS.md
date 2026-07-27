# Design limits

The current audit proves structure and file-line existence only. It does not
prove semantic entailment, reviewer identity, context independence, model
diversity, business completion, or safety of real-world actions.

Only claims explicitly listed in `claims[]` are checked; the tool cannot detect
an omitted factual statement elsewhere in an agent response. Reports do not
bind a workspace identity, file hash, or durable content snapshot, so they
describe the files at audit time rather than providing later tamper evidence.

Future work should add a signed or platform-provided reviewer identity before
making identity claims, and task-specific assertions before making quality
claims. General AI judging should remain advisory unless anchored to external,
reproducible evidence.
