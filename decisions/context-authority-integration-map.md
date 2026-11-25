# Context, authority and learning: curriculum integration map

John Briggs · companion update, 25 November 2026 · unreleased 1.2.1 content.
This is a reader-facing extension of the existing laboratory, not a new book
edition or a production architecture specification.

## What the reader gains

Explain why useful information, permission to act and proof of a result are
three different responsibilities. In the fictional Meridian Ledger case, an
approved-looking change must stop if its guidance becomes stale or its actor
loses permission. A useful outcome may support a proposed lesson without giving
that lesson authority to change future work.

The [interactive guide](../diagrams/interactive-guide/index.html) lets you choose
a reader question and follow its responsibility, chapter, exercise and expected
evidence. The [connected lesson](../reference-factory/06-context-authority-and-learning.md)
then executes selected failures using the existing teaching factory and an
explicit miniature source-version model. Neither requires a model provider,
cloud account or Merlin installation.

## Keep the three responsibilities of the publications distinct

| Resource | Its responsibility | Evidence boundary |
|---|---|---|
| Book | Explain architectural choices, organizational judgment, consequence ownership and when authority is earned | A code example cannot replace the operating argument |
| Public companion | Give readers bounded contracts, runnable failure examples, diagrams and operating instruments | A passing local exercise is evidence about that teaching mechanism only |
| First-party implementation lessons | Motivate transferable patterns and questions, with scope and unavailable evidence stated | A private project does not establish universal benefit, product superiority or production controls in the teaching example |

This update adapts responsibility-level lessons already represented by the
[sanitized pattern cards](../merlin/sanitized-pattern-cards.md). It does not copy
private implementation diagrams, prompts, tool inventories, security mechanisms,
customer material or protected reference photographs into the public laboratory.

## Chapter-by-chapter connection

| Question | Read in the book | Inspect or run | What demonstrates learning |
|---|---|---|---|
| What makes this a factory rather than a collection of assistants? | Chapters 2 and5 | [Visual guide](../diagrams/interactive-guide/index.html), [original trace](../reference-factory/04-canonical-proof-trace.md) | Name intent, consequence owner, evidence, disposition, recovery and outcome separately |
| Can a retrieved note become organizational policy? | Chapter 6 | [Memory workbook](../templates/memory-governance-workbook.md), connected lesson's source correction | A changed source makes the recorded dependent advice unusable; revised advice still needs an allowed use |
| Does a trusted source authorize a write? | Chapters 7 and11 | Connected lesson's revoked-authority path; [execution contract](../reference-factory/02-execution-authority-and-evidence.md) | Revoked execution authority stops the effect despite readable, current guidance |
| Does a green interface mean verification completed? | Chapters 9 and10 | Connected lesson's missing-check path; [evidence rules](../reference-factory/05-acceptance-test-suite.md) | Missing required evidence withholds disposition and canonical receipt; the trace names the next owner |
| What survives a lost response or restart? | Chapter 12 | [Original recovery exercise](../reference-factory/03-recovery-and-reconciliation.md) and original reader journey | Reconcile the actual effect before retry; the optional source-version model makes no durability guarantee |
| Who makes the consequential judgment? | Chapter 13 | [Judgment placement](../templates/human-judgment-placement.md) | Identify a competent authorized decision maker, not merely an approval field |
| Did the output actually help? | Chapter 15 | [Outcome scorecard](../templates/factory-outcome-scorecard.md), canonical journey's synthetic observation | Separate synthetic test observation, release acceptance and measured real-world benefit |
| When may a lesson influence later work? | Chapter 16 | Connected lesson's proposed/admitted learning; [improvement experiment](../templates/continuous-improvement-experiment.md) | Candidate influence is absent until a separate authorized admission; record contrary evidence and review conditions |
| How can teams reuse this safely? | Chapters 14,17 and18 | [Architecture decision guide](../templates/factory-architecture-decision-guide.md), [ninety-day workbook](../templates/ninety-day-pilot-workbook.md) | Choose one bounded work class, name failure and stopping behavior, and state the evidence needed before expanding authority |

The seven guide boundaries—Intent, Context, Authority, Execution, Verification,
Outcomes and Validated learning—are responsibility views. They do not require
seven agents, services or sequential approvals. Governance applies throughout.
One accountable owner may integrate bounded assistance; independent evaluation
and authorized disposition remain separate responsibilities.

## An evidence ladder for the lesson

1. **Conceptual view:** selecting a scenario explains the expected boundary. It
   does not query a source, issue a grant or execute a tool.
2. **Local mechanism:** running the Python lesson shows actual teaching-core
   decisions and a small in-memory source-version check on fictional records.
3. **Reader understanding:** explain the stopped path, legitimate alternative
   and responsible next owner; change one contract and observe the consequence.
4. **Operational evaluation:** separately provide authentic identity, complete
   source/use coverage, durable transactions, target-specific idempotency,
   appropriate checks, retention and human judgment for a real deployment.

The update supplies the first two levels and an exercise for the third. It does
not claim a human-reader study, production safety, comparative performance or ROI.
The fourth level is deliberately not supplied by the companion.

## Compatibility and maintenance

The original twenty-four acceptance obligations, four public artifact schemas,
nineteen templates, nine pattern cards and five canonical Mermaid views remain
stable. The printed book-only lesson and `companion/...` paths are unchanged.
This extension adds its own tests; it does not relabel them as new published
A01–A24 obligations or a claim that the book's first edition has changed.

Keep one teaching implementation authoritative. The extension calls the existing
factory for execution authority, evidence, outcomes and learning; its small
source-version model is explicitly local and separate. Add an adapter or core
contract only when a specific exercise needs one, with failure tests and review.

Review additions as a complete reader path: chapter map, example behavior,
stopping explanation, next owner, licensing, bundle contents and visual output.
Use the repository validator, both documented journeys, unit tests and an
unpack-and-run check. Keep generated databases, screenshots and reports out of
reader source directories. Browser checks do not substitute for observations
with independent human readers.

This source update remains unreleased until a separate tagged-release process.
Do not alter the existing release metadata to imply retailer publication or a
new manuscript edition. Preserve the public correction process in
[CONTRIBUTING](../CONTRIBUTING.md) and [ERRATA](../ERRATA.md).

©2026 John Briggs. Written content: [CC BY-NC-SA 4.0](../LICENSE-CONTENT).
Executable examples carry their separate [MIT notice](../LICENSE-CODE).
