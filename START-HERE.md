# Start Here

## Use the book as the operating guide

This repository is the laboratory for *The Accountable AI Software Factory*;
it is not a parallel edition of the book. Before changing the teaching core,
read the chapter paired with the responsibility you are changing in
[`BOOK-TO-COMPANION-MAP.md`](BOOK-TO-COMPANION-MAP.md). The code demonstrates
selected mechanisms. The book explains why they exist, how they interact, what
they cannot prove, and who remains accountable for the result.

## Thirty-minute reader journey

### 1. Run the teaching core — five minutes

```bash
./reference-factory/run-reader-journey.sh
```

Do not ask only whether the tests are green. Identify the promise each failure
protects and the actor who must decide what happens next. If you cannot explain
those two things using the book's decision model, the exercise is not complete.

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

- **Complete implementation path:** follow
  [`implementation/minimum-viable-accountable-factory.md`](implementation/minimum-viable-accountable-factory.md).
- **Builder:** complete the twenty-four obligations in
  [`05-acceptance-test-suite.md`](reference-factory/05-acceptance-test-suite.md),
  then validate the [`example artifacts`](examples/artifacts/).
- **Architect:** use
  [`factory-architecture-decision-guide.md`](templates/factory-architecture-decision-guide.md)
  and [`provider-tenant-capacity-design.md`](templates/provider-tenant-capacity-design.md).
- **Security reviewer:** use
  [`factory-threat-model.md`](templates/factory-threat-model.md).
- **Engineering leader:** use
  [`ninety-day-pilot-workbook.md`](templates/ninety-day-pilot-workbook.md)
  and [`comparative-pilot-protocol.md`](templates/comparative-pilot-protocol.md).
- **Executive sponsor:** use
  [`factory-outcome-scorecard.md`](templates/factory-outcome-scorecard.md),
  [`factory-balance-sheet.md`](templates/factory-balance-sheet.md), and the
  [`accountable-factory diagnostic`](assessment/accountable-factory-diagnostic.md).
- **Learning-system owner:** use
  [`memory-governance-workbook.md`](templates/memory-governance-workbook.md).
- **Team or educator:** choose a path in
  [`learning-paths/README.md`](learning-paths/README.md) and use the
  [`chapter workbook`](study-guides/chapter-workbook.md) or the eighteen
  [`individual learning guides`](study-guides/chapters/README.md).
- **Red team:** run all twelve drills in the
  [`failure laboratory`](exercises/failure-laboratory.md).

## Completion standard

Running the script is setup, not completion. A completed reader exercise leaves
five things another accountable operator can inspect:

1. the book principle and chapter governing the change;
2. the contract or decision artifact you changed;
3. one failed test proving the unsafe path stops;
4. the named actor authorized to disposition the remaining uncertainty; and
5. the outcome and countermetric that determine whether authority continues.
