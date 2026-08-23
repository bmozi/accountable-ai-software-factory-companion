# Domain and State Contract

## Minimal durable records

Implement these as tables, documents, or event-derived projections. Field names
are illustrative; the invariants are the contract.

| Record | Required meaning |
| --- | --- |
| Work Order | Immutable ID; intent version; eligibility; criteria; prohibitions; risk; owners; evidence requirements; budgets; outcome contract |
| Attempt | Work Order version; execution identity; authority envelope; lease; start/end; terminal disposition; parent lineage if any |
| Candidate | Attempt ID; immutable artifact digest; changed scope; producer claims; provenance |
| Criterion verdict | Candidate digest; criterion ID; evidence source/version; pass/fail/unresolved/error; freshness; blocking class |
| Decision | Actor; authority; policy version; inputs; approve/reject/revise/stop/escalate; rationale; expiry if exceptional |
| Side-effect receipt | Operation ID; requested effect; target; before/after knowledge; completed/failed/indeterminate; observed timestamp |
| Release receipt | Candidate digest; environment; release authority; exposure; rollback reference; resulting identity |
| Outcome observation | Release identity; metric and countermetric window; data owner; limitations; effective/ineffective/insufficient/harmful |
| Learning proposal | Source observations; proposed influence; scope; confidence; contradictions; expiry; experiment; disposition |

All consequential records carry tenant or organizational scope, creation time,
schema version, and actor identity. Updates preserve prior decision history.

## Illustrative state machine

```text
DRAFT -> READY -> ADMITTED -> RUNNING -> CANDIDATE -> VERIFYING
      -> DECISION_REQUIRED -> APPROVED -> RELEASED -> OBSERVING

From controlled points:
  -> BLOCKED -> READY | CANCELLED
  -> REVISE -> READY
  -> REJECTED | FAILED | CANCELLED | PARTIAL

Outcome terminals after observation:
  EFFECTIVE | INEFFECTIVE | INSUFFICIENT_EVIDENCE | HARMFUL
```

Do not copy these labels blindly. Define a smaller machine if your work class
needs less. Preserve these invariants:

1. generated is not verified;
2. verified is not approved;
3. approved is not released;
4. released is not effective;
5. observed is not learned;
6. learning is not authority;
7. an artifact or intent change invalidates dependent decisions unless their
   contract explicitly survives the change;
8. a stale version cannot advance state;
9. terminal does not always mean success;
10. uncertainty is representable without guessing.

## Transition function

Implement transitions as a deterministic function outside the model:

```text
transition(record_id, expected_version, requested_state, actor, evidence_refs)
  current = load_for_update(record_id)
  reject if current.version != expected_version
  reject unless policy.allows(actor, current.state, requested_state)
  reject unless required_evidence(current, requested_state) is valid
  append TransitionRequested and TransitionAccepted atomically
  update projection and increment version
```

A model may propose `requested_state` and explain why. It must not bypass the
version, policy, or evidence checks.
