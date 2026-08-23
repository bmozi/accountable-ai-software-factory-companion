# Machine-Readable Accountability Contracts

These JSON Schemas make four book concepts concrete without prescribing a
vendor, agent framework, database, or deployment system:

1. [`work-order.schema.json`](work-order.schema.json)
2. [`evidence-record.schema.json`](evidence-record.schema.json)
3. [`factory-receipt.schema.json`](factory-receipt.schema.json)
4. [`outcome-observation.schema.json`](outcome-observation.schema.json)

The schemas are teaching contracts, not production compliance claims. Extend
them for identity, records, privacy, safety, legal, accessibility, operational,
and domain obligations before use on consequential work.

## Run the examples

```bash
python3 tools/validate_artifact.py examples/artifacts/*.json
```

The dependency-free validator checks selected cross-field invariants in
addition to basic structure. The JSON Schema files are suitable for editors,
CI tools, and fuller validators that support Draft 2020-12.

## Design rules

- `schemaVersion` changes when machine interpretation changes.
- every artifact has a durable identity;
- candidate-bound records use a SHA-256 digest;
- evidence names one criterion and preserves limitations;
- disposition identifies an authorized actor separately from the producer;
- receipts distinguish known, indeterminate, and reconciled effects; and
- outcome observations can narrow or retire authority.
