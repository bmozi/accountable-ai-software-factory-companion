# Provider, Tenant, Quota, and Capacity Design

Use this design instrument with Chapters 7–8 and the economics interlude.

## The conservation rule

Capacity is not a single maximum-agent setting. An admitted attempt must fit
inside every relevant constraint:

```text
admissible capacity = minimum(
  host headroom,
  provider/account allowance,
  tenant entitlement,
  work-order remaining budget,
  workspace conflict ceiling,
  evidence and reviewer capacity,
  risk-policy ceiling
)
```

The minimum is the current binding constraint. Record it so operators can
distinguish deliberate conservation from a stalled system.

## Capacity ledger

Create a durable reservation before starting work:

| Dimension | Limit | Reserved | Consumed | Released | Binding reason |
| --- | ---: | ---: | ---: | ---: | --- |
| Provider requests or tokens |  |  |  |  |  |
| Tenant daily cost |  |  |  |  |  |
| Work Order cost, time, or actions |  |  |  |  |  |
| Host memory, CPU, or workspaces |  |  |  |  |  |
| Concurrent writes |  |  |  |  |  |
| Evidence executions |  |  |  |  |  |
| Reviewer decisions |  |  |  |  |  |
| Release exposure |  |  |  |  |  |

Checking a remaining balance independently inside concurrent workers is not
conservation. Two workers can both see the same balance. Reserve atomically,
consume against the reservation, and release only what was unused.

## Tenant fairness

Define fairness for the service rather than assuming first-come-first-served is
neutral. Options include reserved shares, weighted fair queues, risk classes,
deadlines, and bounded borrowing of unused capacity.

For each tenant record:

- identity and data partition;
- supported work classes and maximum authority;
- provider and model eligibility;
- concurrent attempt and write ceilings;
- daily and per-Work-Order budget;
- burst allowance and cooldown;
- evidence and human-review entitlement;
- priority and emergency policy;
- retention, export, deletion, and incident notification; and
- who may change the entitlement and how the tenant can appeal.

An emergency tenant should not receive an undocumented bypass. Give it an
explicit class with stronger attribution, expiry, and retrospective review.

## Provider-specific policy

Providers differ in context handling, tool semantics, rate limits, data terms,
regional availability, identity support, observability, and interruption
behavior. A stable factory port should expose these differences rather than
pretend they do not exist.

| Provider property | Admission consequence | Runtime signal | Degraded response |
| --- | --- | --- | --- |
| Data or region restriction | Exclude incompatible Work Orders | Policy denial | Route only if another approved provider exists |
| Rate or concurrency ceiling | Reserve before launch | Throttle and queue age | Reduce concurrency; do not retry-storm |
| Tool or control limitation | Reduce granted authority | Capability unavailable | Read-only, draft-only, or stop |
| Response lost after effect | Require operation identity | Indeterminate receipt | Reconcile before retry |
| Model or version change | Revalidate affected work classes | Contract or version drift | Pin, canary, narrow, or stop |
| Outage | Preserve durable work and leases | Health and error budget | Queue, use an approved substitute, follow a manual path, or stop |

Provider portability is a controlled migration capability, not the claim that
all models behave identically. Preserve Work Orders, decisions, evidence,
receipts, outcomes, and learning outside provider-specific state. Re-run the
acceptance suite for every provider and work-class combination.

## Learned sizing

Begin with static conservative estimates. Once durable telemetry exists,
estimate resource need from bounded recent samples. Prefer a high percentile
for resources whose exhaustion can destabilize the service. Reject corrupt,
cross-tenant, or incomparable observations.

A sizing recommendation may:

- hold or reduce a ceiling when evidence is weak;
- propose a one-step increase below a hard maximum;
- name the evidence window and confidence; and
- declare rollback triggers such as provider throttling, error growth,
  operator-control latency, host pressure, cost, or reviewer backlog.

It may not mint budget, reinterpret authority, override real-time pressure, or
make its own recommendation permanent.

## Required drills

1. Simultaneous children compete for one remaining budget reservation.
2. One tenant bursts while another has deadline-bound eligible work.
3. Provider throttling causes queue pressure; confirm bounded backoff rather
   than synchronized retry.
4. A provider becomes unavailable after partial work; confirm the replacement
   path cannot inherit unverified completion.
5. Host headroom crosses the stop threshold during fan-out.
6. Human-review capacity, not compute, becomes binding.
7. Learned sizing recommends scale-up; inject a rollback signal.

Report admitted, queued, refused, cancelled, partial, migrated, and completed
attempts with their binding constraints. Throughput without the denominator of
refused and delayed work hides the fairness decision.
