# Recovery and Reconciliation Protocol

## Why recovery is part of correctness

An execution service will eventually stop after requesting an effect but before
recording the response. On restart, “retry the step” may duplicate the effect;
“mark it failed” may hide a completed effect. The correct interim result is
often **indeterminate**.

## Durable execution protocol

1. Admit a Work Order version before execution.
2. Acquire a time-bounded lease using compare-and-set.
3. Allocate an operation ID before every effectful request.
4. Persist intent-to-act before sending the request.
5. Make the downstream operation idempotent where possible.
6. Persist the observed response as a side-effect receipt.
7. On timeout or process loss, do not infer completion from silence.
8. Reconcile the desired state, durable receipts, and independently observed
   target state.
9. Retry only when the operation class and evidence make retry safe.
10. Escalate unresolved effects to a named operator with the full trace.

```text
reconcile(work_order):
  desired = durable_desired_state(work_order)
  observed = inspect_target_state(work_order)
  receipts = durable_receipts(work_order)

  if observed satisfies desired and attribution is valid:
      record reconciled completion
  else if no effect occurred and retry policy proves retry-safe:
      schedule a bounded retry with the same operation identity
  else if repair is deterministic and authorized:
      propose or execute the bounded repair
  else:
      mark indeterminate and escalate
```

## Required restart drill

In a non-production environment, terminate the worker at each boundary:

- before intent-to-act is persisted;
- after persistence but before the external request;
- after the request but before the response;
- after response but before receipt persistence;
- after receipt persistence but before state projection.

For each point, prove that restart yields one of: no effect, one attributable
effect, a safe bounded retry, a deterministic repair, or an explicit
indeterminate escalation. It must never yield an unrecorded duplicate or a
fabricated success.

## Reconciler boundaries

Reconciliation is not permission to improvise. The reconciler may observe,
compare, retry a preclassified safe operation, execute an authorized repair, or
escalate. It may not broaden intent, mint new authority, waive evidence, or
reinterpret a harmful outcome as completion.
