# Book-to-Companion Curriculum Map

The companion is an implementation laboratory for *The Accountable AI Software
Factory: Building Governed, Verifiable Software at AI Speed*. It deliberately
does not restate the book's argument, Meridian Ledger consequence chain,
architectural objections, economic reasoning, or authority-expansion logic.

Use the book to decide what a responsibility means and when it is justified.
Use the companion to make that decision concrete, executable, and falsifiable.

| Read in the book | Decision the book teaches | Use in the companion | Proof that you learned it |
|---|---|---|---|
| Chapter 3, The Factory Contract | What the factory promises, prohibits, owns, and stops | `templates/factory-charter-template.md`; `reference-factory/01-domain-and-state-contract.md` | An ineligible request is refused without creating hidden work |
| Chapter 4, Intent Is an Engineering Artifact | How purpose becomes versioned claims, constraints, assumptions, and countermetrics | `templates/work-order-template.md` | A second operator can distinguish required outcomes from implementation suggestions |
| Chapter 5, Work Orders and the Decision Chain | Why intent, attempts, artifacts, evidence, decisions, effects, and outcomes require durable lineage | `reference-factory/01-domain-and-state-contract.md`; `04-canonical-proof-trace.md` | The complete decision can be reconstructed without a chat transcript |
| Chapter 6, Memory Must Earn Its Influence | How observations become candidate learning without silently becoming policy | `templates/memory-governance-workbook.md`; `templates/continuous-improvement-experiment.md` | A useful lesson remains quarantined until separately admitted |
| Chapter 7, Bounded Execution | Which authority dimensions must be enforced outside a prompt | `reference-factory/02-execution-authority-and-evidence.md`; `templates/factory-threat-model.md` | A prohibited capability is denied even when the producer requests it persuasively |
| Chapter 8, One Agent, Many Agents, and the Cost of Handoffs | When delegation repays its lineage, budget, cancellation, and integration costs | `templates/factory-architecture-decision-guide.md`; `templates/provider-tenant-capacity-design.md` | One integrating owner and conserved authority remain visible across every child |
| Chapter 9, Deterministic Machinery Around Probabilistic Work | Where interpretation belongs and where repeatable enforcement belongs | `reference-factory/example/`; `05-acceptance-test-suite.md` | A model claim cannot bypass a deterministic transition or evidence floor |
| Chapter 10, The Evidence Plane | How evidence becomes artifact-bound, criterion-specific, independent, and proportionate | `templates/risk-to-evidence-matrix.md`; `reference-factory/02-execution-authority-and-evidence.md` | Changing the candidate invalidates stale verdicts and preserves disagreement |
| Chapter 11, The Control Plane | Why the production path cannot mint its own authority | `templates/decision-rights-matrix.md`; `templates/factory-threat-model.md` | Grant, denial, exception, revocation, and expiry have attributable owners |
| Chapter 12, Observability, Provenance, and Recovery | Why interruption requires reconciliation rather than blind retry | `reference-factory/03-recovery-and-reconciliation.md`; `MERLIN-PUBLIC-LESSONS.md` | A lost response produces reattachment, proven-safe retry, repair, or explicit indeterminate escalation |
| Chapter 13, Humans Are the Judgment Architecture | Which decisions require competence, legitimacy, attention, and consequence ownership | `templates/human-judgment-placement.md` | “Human in the loop” becomes a named decision with authority and absence behavior |
| Chapter 14, The Factory as an Internal Product | How supported paths, refusals, exits, and recovery shape adoption | `templates/factory-operations-handbook.md` | A stopped user receives evidence, a next owner, and a supported route forward |
| Chapter 15, Measure Outcomes, Not Machine Activity | How primary outcomes, countermetrics, baselines, and obligations govern continuation | `templates/factory-outcome-scorecard.md`; `templates/comparative-pilot-protocol.md` | Faster production cannot hide rework, harm, human load, or continuing cost |
| Chapter 16, The Factory That Improves the Factory | How improvement proposes changes without granting itself influence | `templates/continuous-improvement-experiment.md` | A learning proposal can be narrowed, rejected, expired, or reversed independently |
| Chapter 17, Build, Buy, or Assemble | Which components may be replaceable and which accountability capabilities remain owned | `PUBLIC-IMPLEMENTATIONS-TO-STUDY.md`; `templates/factory-architecture-decision-guide.md` | Replacing a component preserves intent, authority, evidence, recovery, and export contracts |
| Chapter 18, The First Ninety Days | How authority expands only after local evidence and can contract again | `templates/ninety-day-pilot-workbook.md`; `templates/factory-maturity-assessment.md` | The day-ninety decision can expand, hold, narrow, redesign, or stop using precommitted evidence |

## Why the repository is not the whole method

Code can demonstrate a state transition. It cannot decide whether the state
model expresses a legitimate organizational promise. A test can show that an
evidence requirement fired. It cannot decide whether the requirement is
proportionate to customer consequence. A human approval field can exist while
oversight remains ceremonial. A successful release can still create a harmful
outcome or an unjustified continuing obligation.

The book supplies the interpretation needed to prevent these mechanisms from
becoming accountability theater. The companion supplies the material needed to
test whether the interpretation survives implementation.

## Reader completion test

For every artifact you adapt, be able to answer:

1. Which book principle does this mechanism implement?
2. Which failure or consequence makes the mechanism necessary?
3. What evidence proves the boundary works on an unhappy path?
4. Who is authorized to decide when evidence remains incomplete or conflicts?
5. Which outcome or countermetric can reduce or retire the authority later?

If any answer is missing, the factory may run, but the learning exercise is not
complete.
