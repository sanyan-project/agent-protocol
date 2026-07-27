# Contributing

Keep the protocol deterministic and the public examples synthetic.

Before opening a pull request, run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_public_package.py
python health_check.py
```

New hard gates need both passing and failing tests. Do not weaken a gate to make
a real failure disappear. Do not submit customer data, real conversations,
credentials, private paths, internal audit logs, or identifiable incidents.
