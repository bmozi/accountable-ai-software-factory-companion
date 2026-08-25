# From a Governed Delivery Loop to an Accountable Factory

Do not build factory infrastructure merely because agents can perform more
steps. Graduate from Book 2's governed delivery loop only when the
responsibility boundary has outgrown one team, one repository, and one
reviewable decision.

## The graduation test

Stay with the Book 2 loop if one team can still answer all of these questions
from its repository and normal delivery system:

- What was requested, prohibited, and accepted?
- What could the agent read, change, execute, or publish?
- What exact candidate did the checks evaluate?
- Who reviewed the remaining uncertainty?
- Who made the **SHIP**, **REVISE**, or **STOP** decision?
- What did the team learn before the next session?

Move into Book 3's factory model when one or more of these conditions makes
those answers unstable:

- several teams, repositories, agents, or providers can affect the same work;
- work and authority must survive across sessions, queues, or service
  boundaries;
- a side effect may have happened even though its response was lost;
- admission, verification, release, and outcome ownership belong to different
  actors;
- evidence must remain bound to an exact candidate after handoffs;
- disagreement requires a durable, attributable disposition; or
- observed outcomes can narrow, suspend, or retire future authority.

## Translate one Book 2 result

Bring one completed Book 2 evidence packet into the laboratory. Do not bring a
fictional success story; use a real bounded change with its sensitive details
removed.

| Book 2 evidence | Factory responsibility to investigate | Laboratory starting point |
| --- | --- | --- |
| Work Order and SPEC | Durable admitted promise | [`work-order-template.md`](templates/work-order-template.md) and the book's intent chapters |
| Agent scope and permissions | Enforceable execution authority | [`02-execution-authority-and-evidence.md`](reference-factory/02-execution-authority-and-evidence.md) and the book's authority model |
| Test and review output | Evidence bound to an exact candidate | [`risk-to-evidence-matrix.md`](templates/risk-to-evidence-matrix.md) and the book's proof-boundary guidance |
| **SHIP / REVISE / STOP** record | Attributable disagreement and release disposition | [`decision-rights-matrix.md`](templates/decision-rights-matrix.md), [`human-judgment-placement.md`](templates/human-judgment-placement.md), and the book's decision-rights treatment |
| Rollback plan | Reconciliation before retry | [`03-recovery-and-reconciliation.md`](reference-factory/03-recovery-and-reconciliation.md) and the book's recovery reasoning |
| Metrics and learning record | Owned outcome and governed learning | [`factory-outcome-scorecard.md`](templates/factory-outcome-scorecard.md), [`memory-governance-workbook.md`](templates/memory-governance-workbook.md), and the book's outcome chapters |

For each row, write down what is lost when the work crosses the new boundary.
Then run [`./reference-factory/run-reader-journey.sh`](reference-factory/run-reader-journey.sh)
and identify the failure obligation that protects that loss.

## Completion decision

Leave this exercise with one of two justified decisions:

- **STAY WITH THE LOOP:** the Book 2 practice still contains the responsibility;
  strengthen it before adding orchestration.
- **GRADUATE TO THE FACTORY:** name the first responsibility that must become
  durable, its human owner, the evidence it requires, and the unsafe path its
  first failing test must stop.

The repository can make the boundary visible. *The Accountable AI Software
Factory* is required to reason about the full operating model, the tradeoffs
between responsibilities, and the organizational authority needed to operate
it.
