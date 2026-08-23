# Factory Architecture Decision Guide

**Version:** 0.1 working draft
**Relationship:** Chapters 3, 5–11, and 13–18

## Purpose

Use this guide to choose among credible architectures. It is not a maturity
score whose highest answer is always “more factory.” The right design may be a
human-owned assisted process, a deterministic workflow, a stateless bounded
agent, a purchased platform, a federated service, or a deliberate stop.

Complete the guide for one work class. Different work classes in the same
organization should produce different answers.

## 1. Decide whether factory machinery is justified

Ask:

- Is the work frequent enough to learn from repetition?
- Can eligibility and intended outcome be stated?
- Does execution cross a shared artifact, authority, budget, or external-effect
  boundary?
- Can important claims be evaluated independently?
- Is there a competent consequence owner?
- Can the work stop, recover, or retreat?
- Would durable state materially improve handoffs, investigation, or audit?

Prefer ordinary human-owned delivery when work is rare, deeply novel, difficult
to evaluate, or dominated by judgment that cannot yet be encoded. Prefer a
narrow deterministic workflow when the steps and decisions are already stable.
Build a factory path when adaptive execution is valuable and its consequence
requires durable accountability.

## 2. Choose the execution form

| Form | Choose when | Avoid or constrain when | Evidence before expansion |
| --- | --- | --- | --- |
| Human with AI assistant | Ambiguity and integrated human context dominate | Decisions disappear into local practice | Ordinary delivery quality and review |
| Deterministic workflow with model steps | Route and transitions are stable | Exceptions and discovery dominate | Replay, transition, and recovery tests |
| Single bounded agent | Work is coupled and context continuity matters | Independent challenge is absent | Boundary and separate-evidence tests |
| Owner-led bounded delegation | Work decomposes and one owner can integrate | Shared mutation or scarce review dominates | Budget, cancellation, lineage, and comparison |
| Autonomous peers/swarm | Search value is high and outputs remain proposals | Effects require strong attribution or reversal | Containment, conservation, synthesis, and outcome evidence |

Decision rule: add coordination only when measured search, independence, or
latency benefits repay the integration, capacity, and recovery cost.

## 3. Choose the state and memory form

| Form | What it preserves | What it risks |
| --- | --- | --- |
| Stateless attempt | Clean execution boundary | Repeated discovery |
| Durable Work Order only | Intent, state, ownership, and recovery | Formalization overhead |
| Documentation retrieval | Shared maintained knowledge | Stale or context-insensitive guidance |
| Session continuity | Local reasoning context | Conversation mistaken for authority |
| Curated operational memory | Scoped reusable observation | Poisoning, contradiction, and maintenance |
| Validated practice | Broad behavioral influence | Fossilization and self-protection |

Decision rule: use the least influential persistence mechanism that solves the
observed problem. Do not create learning authority merely because storage is
available.

## 4. Choose the evidence architecture

For each claim, classify consequence, reproducibility, producer incentive,
uncertainty, and cost of error.

- Use schema and static checks for stable structural claims.
- Use deterministic tests for executable behavior.
- Use independent model or expert review for interpretation and correlated
  blind spots.
- Use policy evaluation for permissions and floors.
- Use bounded runtime observation for operational and outcome claims.
- Preserve unresolved disagreement when no source can decide.

Decision rule: increase independence when producer and evaluator incentives or
assumptions are likely to correlate and the consequence justifies the cost.
Reduce ceremonial checks that never change a disposition, unless they protect
a deliberately accepted invariant.

## 5. Choose the control placement

| Placement | Centralize here | Keep local here |
| --- | --- | --- |
| Central control plane | Identity, audit integrity, protected floors, shared tenant invariants | Domain eligibility and consequence |
| Team-local control | Work-class rules and operating context | Cross-organizational safeguards |
| Delivery-platform control | Repeatable enforcement near effects | Contested business judgment |
| Independent assurance | High-consequence challenge and review | Fast routine operation |
| Federated model | Common invariants plus explicit local authority | Requires clear conflict and appeal design |

Decision rule: place a decision with the actor possessing the necessary domain
knowledge, independence, incentive, and authority. Platform ownership alone is
not competence.

## 6. Choose build, buy, assemble, or remain conventional

Score each capability—not the entire factory—against differentiation, security
sensitivity, change rate, internal competence, vendor maturity, integration
cost, evidence portability, delegated authority, degraded operation, and exit.

- **Buy** coherent commodity capability whose boundary and exit can be tested.
- **Build** differentiating judgment or protected authority the organization can
  sustainably operate.
- **Assemble** when the organizational contract must remain stable across
  replaceable components.
- **Remain conventional** when the machinery adds more support and governance
  cost than the work-class consequence justifies.

Decision rule: the organization may delegate execution but retains a named
owner for the consequence and a portable account of why consequential work was
allowed.

## 7. Choose the adoption pace

Expand one authority dimension only after the current one demonstrates:

- correct admission and refusal;
- enforceable capability and budget boundaries;
- evidence that informs disposition;
- interruption and duplicate-effect recovery;
- acceptable human and operational load;
- observable outcomes and countermetrics;
- an exercised stop or retreat path.

Possible decisions are stop, continue unchanged, repair, narrow, extend to
collect evidence, or expand one dimension. Calendar progress and executive
attention do not substitute for the obligation.

## Architecture decision record

For each material choice record:

```text
Work class and consequence:
Decision:
Credible alternatives:
Why the selected architecture fits now:
Evidence supporting the choice:
Strongest objection and when it is correct:
Risks and countermetrics:
Authority granted and withheld:
Failure/degraded mode:
Evidence that would reverse this decision:
Review date and owner:
```

The most important field is evidence that would reverse the decision. An
architecture that cannot lose an argument has become identity rather than
engineering.

## Anti-pattern diagnostic

Mark **observed**, **possible**, or **not evident**. For every observed pattern,
name a decision owner and one falsifiable corrective experiment.

| Anti-pattern | Recognition signal | Corrective question |
| --- | --- | --- |
| Paper Factory | Controls exist in documents but no denial can be demonstrated | Which transition or effect does this control stop? |
| Transcript Database | Current intent must be reconstructed from conversation | What is the authoritative durable version? |
| Prompt Constitution | Prompts carry permissions the environment does not enforce | Which external mechanism holds the boundary? |
| Autonomous Theater | Agent count rises while integration remains invisible human work | What outcome did delegation improve after coordination cost? |
| Self-Grading Factory | Producer supplies the decisive verdict | Which evidence source can contradict production? |
| Approval Laundromat | Humans approve summaries they cannot inspect | What decision and evidence can this reviewer competently own? |
| Mechanical Oracle | A repeatable rule is treated as timeless truth | What outcome, override, or drift reopens the rule? |
| Governance Monolith | Central platform owns remote domain decisions | Which decisions belong with consequence owners? |
| Human Exception Queue | Ambiguity accumulates in an understaffed review queue | Which repeated judgment should be clarified, automated, or refused? |
| Universal Paved Road | Unlike consequences receive one workflow and authority | Which work-class differences justify another path? |
| Green Dashboard Factory | Activity improves while displaced harm is omitted | Which outcome and countermetric can reverse expansion? |
| Memory Landfill | Guidance accumulates without contradiction or expiry | What has been retired, and why? |
| Learning Coup | Small improvements gradually weaken controls | Which boundary can improvement never change itself? |
| Vendor-Owned Decision Chain | Artifacts export but decisions and evidence do not | Can the organization reconstruct and migrate one release? |
| Pilot That Cannot Fail | Every result supports continuation | Which precommitted result forces stop or reduction? |
| Infinite Retry | Repeated activity substitutes for progress or reconciliation | What ceiling and indeterminate state halt repetition? |
| Ever-Growing Estate | Creation is funded while ownership and retirement are not | Who operates, measures, and retires the resulting capability? |
| Permanent Emergency | Exceptional authority lacks expiry and review | When does the capability revoke, and who verifies closure? |

## Facilitation sequence

1. Have advocates state the proposed architecture and evidence.
2. Assign another group to present the strongest credible alternative.
3. Identify conditions under which each side is correct.
4. Walk one happy path, one refusal, one interruption, and one harmful outcome.
5. Complete the anti-pattern diagnostic.
6. Record the narrowest decision that enables learning without granting
   unnecessary authority.
7. Set a review trigger based on evidence, not only a date.

Disagreement is useful output. Preserve minority objections and the evidence
that would resolve them.
