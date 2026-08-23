# Accountable Factory Architecture Decision Starters

Each record is a starting decision, not a universal rule. Add local forces,
evidence, dissent, expiry, and the result that would reverse it.

## ADR-001 — One owner before coordinated agents

- **Decision:** Begin with one accountable owner; add bounded workers only
  where independence or latency has measured value.
- **Protects:** coherence, shared budget, integration, cancellation.
- **Watch for:** hidden handoffs, duplicated work, correlated assumptions.
- **Reverse when:** controlled comparison shows a different topology improves
  total justified outcomes without unacceptable coordination cost.

## ADR-002 — Deterministic machinery around probabilistic work

- **Decision:** Use schemas, state machines, policies, and tests where meaning
  is stable; use models for interpretation and candidate production.
- **Protects:** reproducibility, inspectability, enforceable boundaries.
- **Watch for:** stale deterministic rules that automate harm.
- **Reverse when:** the rule cannot represent material context and bounded
  interpretation produces a better evidenced decision.

## ADR-003 — Durable state for consequential work

- **Decision:** Preserve authoritative Work Order state and guarded transitions.
- **Protects:** restart, concurrency, audit, and recovery.
- **Watch for:** wrong desired state, corrupt records, privacy over-retention.
- **Reverse when:** work is disposable, side-effect free, and cheaper to restart
  than recover.

## ADR-004 — Independent evidence for consequential claims

- **Decision:** Match evaluator independence to claim consequence and preserve
  disagreement.
- **Protects:** against producer self-approval and repeated blind spots.
- **Watch for:** ceremonial independence, shared context, evaluator gaming.
- **Reverse when:** low-consequence claims are better served by deterministic or
  sampled verification.

## ADR-005 — Federated work classes behind a common contract

- **Decision:** Centralize protected identity, state, evidence meaning, and
  control floors while allowing bounded local execution paths.
- **Protects:** common accountability without making the platform a tollbooth.
- **Watch for:** paper federation, incompatible semantics, central review queues.
- **Reverse when:** scale and consequence make one simpler operating model
  demonstrably more reliable.

## ADR-006 — Own the contract; replace components

- **Decision:** Retain authoritative intent, decisions, evidence, outcomes, and
  exit records even when execution is purchased.
- **Protects:** accountability and provider portability.
- **Watch for:** costly integration and lowest-common-denominator interfaces.
- **Reverse when:** a provider preserves the complete decision chain at lower
  total obligation.

## ADR-007 — Translate prototypes before production admission

- **Decision:** Treat prototype code as a new candidate; do not presume reuse.
- **Protects:** against hidden assumptions crossing the production boundary.
- **Watch for:** unnecessary rewrites and ceremonial translation.
- **Reverse when:** the artifact already satisfies the declared production
  contract on equivalent evidence.

## ADR-008 — Reconcile indeterminate effects before retry

- **Decision:** Give consequential operations semantic identities; after a lost
  response, observe authoritative state before attempting the effect again.
- **Protects:** against duplicate releases, payments, messages, and mutations.
- **Watch for:** providers that cannot expose effect state or support idempotency.
- **Reverse when:** the action is proven side-effect free and retry is cheaper
  than reconciliation.

## ADR-009 — Mechanical gates before scarce human judgment

- **Decision:** Automate stable checks and reserve informed people for values,
  ambiguity, irreversibility, exceptions, and consequence.
- **Protects:** review capacity and meaningful oversight.
- **Watch for:** automation bias, deskilling, or suppressed escalation.
- **Reverse when:** a mechanical check cannot represent the decision and a
  competent human path remains viable.

## ADR-010 — Advisory release before autonomous consequence

- **Decision:** Begin with the narrowest mode that tests real consequence and
  expand one authority dimension at a time.
- **Protects:** learning speed without premature autonomy.
- **Watch for:** permanent pilots, rubber stamps, and shadow automation.
- **Reverse when:** recovery, human-load, and outcome evidence justify a
  specific broader authority.

## Record template

- Identifier and title:
- Status and owner:
- Work class and consequence:
- Context and forces:
- Considered alternatives:
- Decision and authority boundary:
- Required evidence:
- Failure and degraded behavior:
- Dissent and unresolved questions:
- Review or expiry date:
- Reversal trigger:
