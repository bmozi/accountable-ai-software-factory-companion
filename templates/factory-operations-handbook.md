# Factory Operations Handbook

**Relationship:** Chapters 12, 14, 17, and 18

## Service definition

Operate the factory as an internal production service. For every supported work
class publish:

- eligibility and intake contract;
- authority offered and explicitly withheld;
- evidence and approval floor;
- normal, degraded, and stopped modes;
- data, tenant, provider, and retention boundaries;
- support hours and escalation route;
- recovery and outcome owners;
- service objectives and exclusions;
- deprecation and exit policy.

The application team owns the consequence of its software unless a different
decision is explicit. The platform team owns factory-service failures. Evidence,
control, security, and release owners retain their respective decisions.

## Service-level indicators

Use indicators that describe accountable flow, not machine busyness:

| Indicator | Definition | Why it matters |
| --- | --- | --- |
| Admission decision latency | Time from sufficient request to admit/refuse | Shows whether eligibility is operable |
| Actionable stop rate | Stops that name cause, preserved work, and next owner | Distinguishes safe refusal from opaque failure |
| Evidence freshness/completeness | Required current criteria with authorized verdicts | Measures decision readiness |
| Reconciliation age | Time an effect remains indeterminate | Exposes hidden recovery debt |
| Duplicate-effect rate | Repeated unintended effects per operation | Tests idempotency and receipt integrity |
| Operator-control latency | Time for cancel/revoke/stop to take effect | Measures whether authority is practically controllable |
| Retry amplification | Attempts and spend after the first repeated equivalent failure | Exposes loops that convert failure into unproductive activity |
| Spend-containment latency | Time and cost from budget or velocity breach to stopped attributable work | Tests whether financial guardrails act rather than merely report |
| Decision queue age | Time evidence-complete work waits for competent authority | Reveals human capacity as a constraint |
| Recovery time by class | Time to resume, repair, roll back, or close | Separates failure modes |
| Outcome disposition coverage | Releases receiving effective/ineffective/insufficient/harmful result | Closes the value loop |
| Exception age and return rate | Duration and closure of paved-road exceptions | Prevents permanent shadow paths |

## Suggested objectives and error budgets

Do not copy universal targets. Establish a baseline and choose objectives by
consequence. A low-risk draft service may optimize speed. A release-bearing
service may prioritize complete evidence and control latency.

Define error budgets for failures that justify narrowing or stopping authority:

- un-attributed effects;
- release without required disposition;
- stale evidence used in a decision;
- cross-tenant data or budget breach;
- cancellation that fails to contain active work;
- background activity that continues after its spend ceiling;
- indeterminate effects older than the response objective;
- exceptions past expiry;
- harmful outcomes without the prescribed response.

Some events should have a budget of zero even when the service tolerates
ordinary failures. Zero does not mean impossible; it means one occurrence
triggers investigation and an authority decision.

## Operating modes

| Mode | Allowed behavior | Entry trigger | Exit authority |
| --- | --- | --- | --- |
| Normal | Declared work classes and authority | Objectives healthy | Service policy |
| Constrained | Lower concurrency, narrower providers or work | Capacity, evidence, or reviewer pressure | Service owner within policy |
| Draft-only | Produce isolated candidates; no release | Control/evidence degradation | Control and service owners |
| Read-only | Inspect and advise; no mutation | Integrity, identity, or provider uncertainty | Security/control owner |
| Drain | Admit no new work; finish or stop existing work | Upgrade, incident, or retirement | Incident/change authority |
| Stopped | No factory execution | Protected promise at risk | Named recovery authority |

Degraded operation is a product feature. Users must see the mode, reason,
permitted actions, expected next update, and owner. Do not silently lower the
evidence floor to preserve throughput.

## Incident command

Classify incidents by lost promise, not only infrastructure symptom:

1. intent or state integrity;
2. authority or tenant boundary;
3. evidence or decision integrity;
4. duplicate, unknown, or harmful effect;
5. provider/capacity availability;
6. outcome or learning failure.

The incident record should contain affected Work Orders and tenants, last known
good policy and artifact versions, authorities revoked, operations and receipts,
indeterminate effects, evidence invalidated, releases exposed, communication
owner, and criteria for resumption.

Recovery does not end when the worker restarts. Close or explicitly transfer
every indeterminate effect, re-establish evidence freshness, review decisions
made under degradation, and decide what observations may become learning.

## Upgrade and change management

Treat changes to the factory as consequential software changes:

1. identify affected work classes and protected promises;
2. version model/provider, tool, policy, schema, state, evidence, and adapter
   contracts;
3. replay representative traces and the failure acceptance suite;
4. canary one authority dimension and tenant segment;
5. define abort, rollback, and data migration reconciliation;
6. observe operator load and outcome countermetrics;
7. promote through an authority external to the change producer.

Never combine provider replacement, state migration, evidence-policy change,
and authority expansion in one rollout if you need to learn which change caused
the result.

## Retirement and exit

Retiring a work class or provider requires more than disabling intake:

- stop new admission and drain or disposition active work;
- export durable Work Orders, evidence, decisions, receipts, and outcomes;
- reconcile unresolved side effects;
- revoke identities, credentials, integrations, and callbacks;
- dispose of workspaces, caches, and provider-held data under policy;
- preserve required audit and learning records;
- notify tenants and name the replacement or manual path;
- test that the retired capability can no longer act;
- assign ownership of software and obligations that outlive the factory path.

The final receipt of control is the ability to stop safely.

## Weekly operating review

Review the worst and oldest cases, not only averages:

- refused and abandoned work;
- longest decision and reconciliation age;
- largest budget variance;
- fastest spend acceleration and repeated-error clusters;
- orphaned or unexpectedly active background work;
- overrides and expiring exceptions;
- provider and tenant concentration;
- evidence disagreement;
- operator-control failures;
- harmful and insufficient-evidence outcomes;
- recurring support work;
- proposed, contradicted, and retired learning.

End with explicit decisions: preserve, repair, narrow, expand one dimension,
run an experiment, change an objective, or stop.
