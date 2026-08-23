# Execution Authority and Evidence Contract

## Execution envelope

Every attempt receives a machine-enforced envelope:

```yaml
subject: execution-identity
work_order_version: immutable-reference
resource_scope: declared repositories and environments
capabilities: explicit read/write/execute operations
prohibited_effects: protected paths, secrets, release, policy mutation
budgets: wall_time, model_usage, cost, retries, side_effects
stop_conditions: no_progress, ambiguity, policy_denial, budget, cancellation
escalation_owner: named role or queue
```

Treat the prompt as task context, not the access-control system. Check authority
at every effectful adapter. Record denied attempts because a boundary that is
never tested cannot be distinguished from an unused boundary.

The single execution-owner path should work before delegation is introduced.
If delegation is later justified, the parent remains responsible for
integration; child capabilities and aggregate budgets cannot exceed the parent;
cancellation propagates; and nested delegation remains off until lineage,
budget conservation, and cancellation are proven.

## Evidence package

Each acceptance criterion receives its own verdict:

```json
{
  "criterion_id": "stable-id",
  "candidate_digest": "immutable-digest",
  "source": {"identity": "verifier", "version": "version"},
  "result": "pass | fail | unresolved | error",
  "blocking": true,
  "observed_at": "timestamp",
  "expires_at": "timestamp-or-null",
  "artifact_refs": ["durable-reference"],
  "limitations": ["known limitation"]
}
```

Aggregation is a policy decision, not a rewriting of evidence. Preserve a
passing test beside a failing security rule or unresolved human review. A
blocking criterion passes only when an authorized, current source evaluates the
current candidate digest. Producer testimony may inform the inventory but is
not decisive evidence for its own boundary.

## Disposition contract

The decision record identifies:

- the actor and authority exercised;
- Work Order version and candidate digest;
- evidence-package digest and unresolved items;
- applicable policy version and exception, if any;
- approve, reject, revise, stop, or escalate;
- rationale and expiry;
- the next accountable owner.

Never encode “human in the loop” as the design. Name the particular decision,
the competent authority, the evidence presented, and what happens when the
person is unavailable or disagrees.
