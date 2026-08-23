# Executable Teaching Core

This standard-library Python example demonstrates a durable Work Order,
compare-and-set transitions, artifact-bound evidence, separation of producer
claims from verdicts, idempotent operation identities, and restart
reconciliation. It is intentionally incomplete: it has no model, authentication,
sandbox, policy engine, deployment adapter, tenant isolation, or production
hardening.

Run:

```bash
python3 -m unittest -v test_reference_factory.py
```

Or run the tests and complete canonical journey from the parent directory:

```bash
../run-reader-journey.sh
```

Use the acceptance suite in the parent directory to extend it. Do not grant the
example production authority merely because its teaching tests pass.
