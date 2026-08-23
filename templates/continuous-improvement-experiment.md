# Continuous-Improvement Experiment Record

## Proposal

**Proposal identifier:**<br>
**Proposer:**<br>
**Date:**<br>
**Affected factory capability:**<br>
**Affected authority dimension:**<br>
**Required approver:**

### Observed Problem

Describe the outcome, frequency, and evidence. Separate the raw event from the
interpretation.

### Proposed Explanation

What mechanism may be causing the problem? What competing explanations remain?

### Proposed Change

State the smallest change capable of testing the explanation.

### Expected Benefit

Name the outcome and expected direction. Do not use activity as the only
benefit.

### Possible Harm

List quality, security, stability, cost, human-load, fairness, and learning
risks.

## Experiment Design

| Element | Definition |
| --- | --- |
| Eligible work |  |
| Excluded work |  |
| Baseline |  |
| Treatment |  |
| Primary outcome |  |
| Countermetrics |  |
| Sample or duration |  |
| Confounders |  |
| Abort conditions |  |
| Rollback |  |
| Evidence owner |  |

## Authority Review

- Does the proposal change what the factory may read, write, execute, merge,
  deploy, remember, or approve?
- Does it change an evidence threshold or evaluator?
- Does it affect the improvement mechanism itself?
- Does it touch a protected control boundary?
- Can the proposer or beneficiary approve the change alone?

If the proposal changes the system that evaluates or approves improvement, it
requires independent governance outside the ordinary improvement path.

## Results

| Measure | Baseline | Treatment | Difference | Confidence and limitation |
| --- | ---: | ---: | ---: | --- |
|  |  |  |  |  |

Record failures, excluded cases, overrides, and missing data. A clean average
must not hide a harmful tail.

## Decision

- [ ] Reject
- [ ] Revise and retest
- [ ] Retain as bounded experiment
- [ ] Promote to validated practice
- [ ] Retire an existing practice

**Rationale:**

**Approved scope:**

**Next review or decay event:**

**Rollback owner:**

## Learning Update

Link the observation, experiment evidence, approval, new or changed learning,
and any superseded guidance. Preserve the rejected hypothesis so the factory
does not repeatedly rediscover and retry it without new evidence.
