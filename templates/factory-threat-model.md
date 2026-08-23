# Accountable Factory Threat-Model Workbook

**Version:** 0.1 working draft
**Relationship:** Chapters 7, 10–12, and 17

## Purpose

This workbook treats the factory as an authority-bearing production system.
The question is not only whether a model can be manipulated. It is whether any
participant—human, model, tool, provider, integration, memory, or compromised
dependency—can cause an effect without the required intent, authority,
evidence, attribution, or recovery path.

Complete it for one supported work class and one deployment boundary. A generic
enterprise threat model is too broad to decide what this factory may do.

## 1. Declare the protected promises

Record the promises that must survive compromise, error, interruption, and
operator pressure:

| Promise | Consequence if broken | Owner | Detection | Stop/repair |
| --- | --- | --- | --- | --- |
| Admitted intent cannot be silently rewritten |  |  |  |  |
| Execution cannot exceed its capability envelope |  |  |  |  |
| Producer claims cannot become decisive evidence |  |  |  |  |
| Release requires authorized disposition |  |  |  |  |
| Unknown effects cannot trigger blind retries |  |  |  |  |
| Tenant data and capacity cannot cross boundaries |  |  |  |  |
| Learning cannot weaken its own controls |  |  |  |  |

## 2. Map trust boundaries

For every boundary, record identity, data, allowed effects, enforcement point,
evidence, and failure behavior:

- requester to intake;
- intake to durable Work Order;
- Work Order to execution adapter;
- model to tool gateway;
- workspace to repository and network;
- producer to evidence source;
- evidence to decision authority;
- decision to release adapter;
- release to runtime observation;
- observation to learning proposal;
- tenant to shared control plane;
- factory to model, CI, repository, and cloud providers;
- operator and administrator to protected controls.

Do not write “trusted internal service.” Name the mechanism and the consequence
of its compromise.

## 3. Adversary and failure inventory

Consider deliberate attack and ordinary failure together. Both can cross the
same authority boundary.

| Actor or condition | Plausible action | Required prevention | Required detection | Recovery authority |
| --- | --- | --- | --- | --- |
| Malicious requester | Encodes prohibited objective inside ordinary work | Eligibility and consequence review | Intake refusal and anomaly record | Work-class owner |
| Untrusted repository content | Redirects model or tool use | Source precedence and external capability checks | Denied operation and source attribution | Execution owner |
| Compromised model/provider | Exfiltrates context or fabricates completion | Data minimization, tool mediation, receipts | Egress, policy, and evidence discrepancy | Security/control owner |
| Overprivileged tool | Performs wider effect than requested | Capability attenuation and target validation | Side-effect receipt comparison | Tool owner |
| Producer/evaluator collusion | Converts claims into passes | Independent identity and evidence policy | Criterion-source audit | Evidence owner |
| Stale evidence | Authorizes changed artifact or policy | Digest and version binding | Freshness rejection | Evidence owner |
| Duplicate delivery | Repeats external effect | Operation identity and idempotency | Duplicate receipt | Release owner |
| Lost response | Makes completion unknowable | Indeterminate state and reconciliation | Desired/observed mismatch | Operator |
| Malicious tenant | Consumes shared capacity or reads another tenant | Scoped identity, quotas, data partition | Cross-scope and fairness telemetry | Platform owner |
| Privileged administrator | Changes protected policy without review | Separation, multi-party authorization, audit | Control-change alert | Governance owner |
| Poisoned learning | Broadens a local or adversarial conclusion | Provenance, scope, contradiction, experiment | Recurrence/countermetric review | Learning authority |
| Provider outage or policy change | Removes capability during work | Degraded-mode contract and portable records | Provider health and contract drift | Service owner |

## 4. Misuse and abuse cases

Walk at least these scenarios in a safe environment:

1. Place a tool instruction in a repository document that conflicts with the
   Work Order. Confirm it cannot grant authority.
2. Ask a worker to reveal or transmit data outside the declared resource scope.
3. Replace a candidate after evidence passes. Confirm every dependent verdict
   becomes unusable.
4. Reuse an operation identifier with different effect parameters. Confirm a
   conflict rather than a second effect.
5. Exhaust one tenant's budget while another tenant has eligible work. Confirm
   the first cannot consume the second's reservation.
6. Revoke a provider or tool capability during execution. Confirm stop,
   partial-state preservation, and named escalation.
7. Attempt to approve an exception using the same identity that requested it.
8. Submit a learning proposal that lowers the evidence floor which evaluates
   learning. Confirm rejection and audit.

## 5. Threat disposition

For each material threat choose one:

- prevent mechanically;
- reduce likelihood or consequence;
- detect and recover;
- transfer contractually while retaining an accountable owner;
- accept for this work class, with rationale and expiry;
- exclude the work class from factory authority.

“Human review” is incomplete. State which human, which decision, what evidence,
what response time, and what happens when the reviewer is unavailable.

## 6. Evidence and review gate

The threat model is ready for pilot use only when:

- every protected promise has an owner and test;
- every effectful adapter has an identity and receipt strategy;
- uncertainty and partial completion have explicit states;
- administrator and learning paths are inside the model;
- tenant and provider failure are exercised;
- at least one independent security reviewer records objections;
- residual risks are accepted by the consequence owner, not only the builder.

Revisit the model after a new work class, authority dimension, provider,
tenant, tool, memory influence, or release environment is introduced.
