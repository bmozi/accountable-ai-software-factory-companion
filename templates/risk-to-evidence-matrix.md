# Risk-to-Evidence Matrix

## Instructions

For each material claim a change makes, choose evidence based on consequence,
uncertainty, reversibility, and exposure. Do not assign evidence only by file
type or estimated effort.

## Risk Dimensions

Rate each dimension low, medium, or high:

- customer or user consequence;
- security and privacy exposure;
- financial or regulatory consequence;
- operational blast radius;
- reversibility and recovery time;
- novelty or ambiguity;
- evaluator uncertainty;
- cross-system coupling.

Any high dimension may raise the evidence floor even when the implementation is
small.

## Evidence Selection

| Claim | Risk drivers | Structural | Behavioral | Adversarial | Independent judgment | Operational |
| --- | --- | --- | --- | --- | --- | --- |
| Build artifact is well formed | Low consequence | Required | Optional | No | No | No |
| Existing public behavior is preserved | Customer impact | Required | Required | As indicated | Reviewer | Canary where possible |
| Authorization boundary is correct | Security, high consequence | Required | Required | Required | Security owner | Staged observation |
| Migration preserves data | Irreversibility, operational impact | Required | Required | Failure simulation | Data owner | Rehearsal and monitored rollout |
| Performance objective is met | Scale and cost | Required | Load test | Fault and saturation tests | Performance owner as needed | Production telemetry |

## Disagreement Rule

Define before execution what happens when evidence disagrees. Default:

1. a blocking deterministic failure cannot be overruled by model confidence;
2. conflicting deterministic results stop for environment or test diagnosis;
3. model-review disagreement remains visible and routes by risk;
4. an approval does not erase failed evidence; it records an authorized
   exception with owner and expiration;
5. operational harm triggers rollback even if pre-release evidence passed.

## Worked Fictional Example

A one-line change expands a service account's permissions. Implementation size
is tiny. Consequence and blast radius are high. Required evidence includes
policy validation, authorization tests, negative tests proving denied actions
remain denied, security review independent of the producer, staged deployment,
and monitored rollback criteria. Lines changed do not determine evidence.
