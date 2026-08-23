# Factory Capability and Maturity Assessment

Primary chapters: 2 and 18

Use this assessment to identify the weakest responsibility that could invalidate
the rest of the factory. Do not average rows into a maturity score. A strong
generation capability cannot compensate for absent authority, recovery, or
outcome ownership.

## Evidence scale

| Level | Meaning |
|---|---|
| 0 — Assumed | The responsibility is absent or exists only as an expectation. |
| 1 — Described | Prose names the desired behavior, but enforcement or repeatability is unproven. |
| 2 — Demonstrated | A bounded test shows the mechanism works on the normal and stop paths. |
| 3 — Operated | Repeated use has produced receipts, exceptions, recovery evidence, and named ownership. |
| 4 — Governed | Outcomes determine whether the capability is preserved, expanded, narrowed, or retired. |

## Assessment

| Responsibility | Level | Evidence inspected | Most consequential gap | Owner | Next bounded test |
|---|---:|---|---|---|---|
| Work eligibility |  |  |  |  |  |
| Executable intent and prohibitions |  |  |  |  |  |
| Durable work state |  |  |  |  |  |
| Context and memory provenance |  |  |  |  |  |
| Tool, data, write, and environment authority |  |  |  |  |  |
| Budgets, quotas, concurrency, and stopping |  |  |  |  |  |
| Claim-level independent evidence |  |  |  |  |  |
| Approval and exception control |  |  |  |  |  |
| Release, observation, and rollback |  |  |  |  |  |
| Restart reconciliation and recovery |  |  |  |  |  |
| Human judgment placement |  |  |  |  |  |
| Outcome and countermetric measurement |  |  |  |  |  |
| Governed learning and retirement |  |  |  |  |  |
| Factory product and service ownership |  |  |  |  |  |

## Disposition

- Weakest consequential responsibility:
- Authority that must not expand until it improves:
- Evidence required for expansion:
- Named decision owner:
- Review date:

## Worked fictional example

A platform team rates automated dependency updates at level 3 for generation
and testing but level 1 for recovery: interrupted runs can be repeated, yet the
team cannot prove whether an external change occurred before interruption. The
overall decision is not “level 3 maturity.” The team holds release authority at
its current boundary and tests restart reconciliation before adding concurrency.
