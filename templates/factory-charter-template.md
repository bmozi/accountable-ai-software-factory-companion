# Factory Charter Template

**Version:**<br>
**Owner:**<br>
**Approval date:**<br>
**Next review:**<br>
**Applies to:**<br>
**Supersedes:**

Complete this charter for one bounded work class. If an answer is unknown,
write `UNRESOLVED`, name the decision owner, and keep the affected authority
disabled. Do not use an empty field to imply permission.

## 1. Business Purpose

What organizational outcome should the factory improve? Name the customer or
operator consequence, not merely the desired engineering activity.

> Example: Reduce the elapsed time to resolve low-risk dependency updates while
> maintaining or improving change-failure rate and reviewer load.

**Factory promise:** What artifact or decision-ready result does an accepted
attempt produce?

**Explicit non-promises:** What does acceptance not guarantee—for example,
completion, merge, release, or production fitness?

## 2. Eligible Work

List work classes the factory may accept. Define them narrowly enough that an
intake function can decide eligibility consistently.

| Work class | Included | Explicitly excluded |
| --- | --- | --- |
| Example: patch-level dependency update | Existing supported dependency, no API migration | Major versions, authentication libraries, payment code |

**Unknown eligibility behavior:** Reject / Needs clarification / Human triage

**Re-entry rule:** What must change before rejected or clarified work may be
submitted again?

## 3. Consequence Ownership

| Decision | Named role | Required information | Response time |
| --- | --- | --- | --- |
| Accept work |  |  |  |
| Approve design exception |  |  |  |
| Approve merge |  |  |  |
| Approve deployment |  |  |  |
| Own production consequence |  |  |  |
| Authorize rollback |  |  |  |
| Change factory policy |  |  |  |

**Unavailable-owner fallback:** Identify the alternate role or required stop
state for every time-bound decision.

## 4. Authority Envelope

| Dimension | Permitted | Prohibited | Enforcement mechanism | Expansion authority |
| --- | --- | --- | --- | --- |
| Data read |  |  |  |  |
| Tools |  |  |  |  |
| Repository writes |  |  |  |  |
| Environment access |  |  |  |  |
| External communication |  |  |  |  |
| Merge |  |  |  |  |
| Deploy |  |  |  |  |
| Memory update |  |  |  |  |
| Policy change |  |  |  |  |

Prompt instructions alone are not an enforcement mechanism for consequential
authority. Name the repository permission, sandbox, identity, network rule,
budget service, approval gate, or other control that actually refuses the
action.

## 5. Required Evidence

For each accepted work class, define the claim that must be established and the
evidence that can establish it.

| Claim | Evidence | Independent from producer | Blocking | Disagreement rule |
| --- | --- | --- | --- | --- |
| Example: public behavior is unchanged | Contract and regression tests | Yes | Yes | Any failure stops merge |
| Example: no critical known vulnerability introduced | Dependency and security scan | Yes | Yes | Scanner error is insufficient evidence, not a pass |

### Exception contract

- Who may authorize an exception?
- Which evidence classes may never be excepted?
- What compensating control is required?
- When does the exception expire?
- Who verifies rollback or remediation?
- How will the receipt preserve the failed or missing evidence?

## 6. Budgets and Bounds

- Maximum elapsed time:
- Maximum model or compute cost:
- Maximum tool actions:
- Maximum fix iterations:
- Maximum files or services changed:
- Maximum concurrent work orders:
- Maximum subagents per work order:
- Shared provider or tenant ceiling:
- Budget-exhaustion behavior:

## 7. Stop and Escalate

| Condition | Required stop state | Escalation owner | Evidence package |
| --- | --- | --- | --- |
| Ambiguous intent | Needs clarification |  | Work order and ambiguity |
| Authority exceeded | Blocked |  | Requested action and policy |
| Evidence disagreement | Needs adjudication |  | Full conflicting results |
| No-op retry | Partial completion |  | Attempts and unchanged diff |
| Budget exhausted | Partial completion |  | Cost, actions, current state |
| Owner unavailable | Awaiting decision or cancelled |  | Decision requested and deadline |
| Provider interrupted after possible side effect | Recovery required |  | Last confirmed action and uncertain side effects |
| Rollback unavailable | Blocked |  | Reversibility assessment |

Every accepted attempt must produce one durable terminal state. Define the
allowed states and the operator action associated with each:

| Terminal state | Meaning | Next owner | May be retried? |
| --- | --- | --- | --- |
| Completed |  |  |  |
| Rejected at intake |  |  |  |
| Needs clarification |  |  |  |
| Blocked by authority |  |  |  |
| Evidence failed |  |  |  |
| Partially completed |  |  |  |
| Cancelled |  |  |  |
| Interrupted |  |  |  |
| Recovery required |  |  |  |

## 8. Release and Recovery

- Release path:
- Canary or staged exposure:
- Required monitoring:
- Rollback owner and mechanism:
- Maximum detection and recovery objective:
- Behavior when rollback cannot be proven:
- Authority to stop one attempt, a delegation wave, or the complete service:

## 9. Learning Policy

- Who may create an observation?
- What evidence promotes an observation to candidate learning?
- Who may approve a validated practice?
- Which learnings decay or require scheduled review?
- How are contradictions handled?
- Which parts of the factory may not be modified through the improvement path?

## 10. Success and Countermetrics

| Desired outcome | Baseline | Target | Countermetric | Stop threshold |
| --- | ---: | ---: | --- | ---: |
|  |  |  |  |  |

## Charter Review Test

The charter is incomplete if a reasonable operator cannot tell:

1. whether work belongs in the factory;
2. what the factory may do;
3. what evidence “done” requires;
4. when it must stop;
5. who owns the next decision;
6. what production consequence will determine whether the work helped.

## Boundary Exercise

Before approval, walk the charter through these cases and record the expected
state, evidence, and next owner:

1. clean eligible work;
2. confident model review plus failing deterministic test;
3. work discovered to touch an excluded component;
4. unavailable consequence owner;
5. useful partial result at budget exhaustion;
6. expired exception;
7. interruption after a possible side effect;
8. proposed learning that weakens a protected control.

| Scenario | Expected state | Evidence preserved | Next owner | Observed result matches? |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Worked Example: Patch-Level Dependency Update

This abbreviated example shows the required specificity. Replace it with the
organization's own values and evidence.

- **Purpose:** reduce elapsed time for routine supported dependency updates
  without increasing reviewer load, escaped defects, or change-failure rate.
- **Promise:** produce a review-ready patch, evidence package, and truthful
  terminal state within forty-five minutes.
- **Non-promises:** acceptance does not guarantee that an update is possible,
  safe to merge, or authorized for release.
- **Eligible:** patch release of an already approved runtime dependency with no
  declared breaking change, API migration, or protected-component impact.
- **Excluded:** major or minor releases; authentication, authorization,
  payment, cryptography, build-chain, or unsupported dependencies.
- **Authority:** read the repository and approved registries; write only an
  isolated branch; run approved build, test, and scan tools; no merge, deploy,
  secret access, external messaging, memory promotion, or policy change.
- **Evidence:** lockfile integrity, clean build, existing unit, integration, and
  contract tests, dependency and license scan, changed-behavior review, and
  human merge approval. A scanner error is missing evidence, not a clean scan.
- **Bounds:** forty-five minutes, two repair attempts, one dependency, and a
  declared file limit. All delegated work draws from the same attempt budget.
- **Stop:** ambiguous version intent, excluded component, migration required,
  failed required evidence, unapproved transitive dependency, unavailable
  rollback, repeated no-op repair, or exhausted budget.
- **Escalation:** return the work order, diff, tool versions, complete evidence,
  attempted repairs, consumed budget, and smallest unresolved question to the
  dependency owner.
- **Release:** human-approved merge followed by the normal staged deployment
  and service rollback path.
- **Learning:** record the outcome as an observation. No dependency or policy
  rule changes until reviewed by the factory-policy owner.
- **Measures:** lead time and active reviewer minutes; countermetrics are
  rejection and rework, change failure, escaped dependency defects, and
  exceptions.
