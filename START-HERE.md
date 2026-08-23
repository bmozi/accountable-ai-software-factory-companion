# Start Here

## Thirty-minute reader journey

### 1. Run the teaching core — five minutes

```bash
./reference-factory/run-reader-journey.sh
```

Do not ask only whether the tests are green. Identify the promise each failure
protects and the actor who must decide what happens next.

### 2. Read the three contracts — ten minutes

1. [`01-domain-and-state-contract.md`](reference-factory/01-domain-and-state-contract.md)
2. [`02-execution-authority-and-evidence.md`](reference-factory/02-execution-authority-and-evidence.md)
3. [`03-recovery-and-reconciliation.md`](reference-factory/03-recovery-and-reconciliation.md)

Mark one place where your current AI-assisted workflow relies on a transcript,
convention, or model promise instead of an enforceable boundary.

### 3. Change one contract — ten minutes

Choose one reversible work class. Add a criterion, prohibition, budget, or
authority rule to the fictional Work Order. Write the failing test before
changing the teaching core.

### 4. Leave with one decision artifact — five minutes

Complete the first sections of
[`factory-charter-template.md`](templates/factory-charter-template.md) and
[`work-order-template.md`](templates/work-order-template.md). If you cannot
name the outcome owner, release owner, evidence floor, and stopping boundary,
do not connect the workflow to production.

## Next paths

- **Builder:** complete the twenty-four obligations in
  [`05-acceptance-test-suite.md`](reference-factory/05-acceptance-test-suite.md).
- **Architect:** use
  [`factory-architecture-decision-guide.md`](templates/factory-architecture-decision-guide.md).
- **Security reviewer:** use
  [`factory-threat-model.md`](templates/factory-threat-model.md).
- **Engineering leader:** use
  [`ninety-day-pilot-workbook.md`](templates/ninety-day-pilot-workbook.md).
- **Executive sponsor:** use
  [`factory-outcome-scorecard.md`](templates/factory-outcome-scorecard.md).
