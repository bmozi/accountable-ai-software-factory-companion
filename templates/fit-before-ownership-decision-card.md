# Fit-Before-Ownership Decision Card

**Version:** 1.0
**Book relationship:** Chapter 17, *The New Economics of Ownership*
**Use:** Build, buy, assemble, replace-a-slice, buy-to-learn, or retire decisions

## The rule

> Requirements first. Ownership second.

Ownership cost is a valid comparison among options that can produce the
required outcome at the required consequence and evidence floor. It is not a
reason to lower that floor.

## 1. Fix the bar before discussing vendors or implementation

- Required outcome:
- Intended users and affected people:
- Non-negotiable functional requirements:
- Non-negotiable safety, security, privacy, legal, or regulatory constraints:
- Evidence required before release or reliance:
- Authority, explanation, appeal, and remedy that must remain available:
- Integration and authoritative-data boundaries:
- Degraded mode, recovery, and stopping requirements:
- Decision owner:

## 2. Name complete options

Include the current path or doing nothing. Describe each option together with
the integrations, workarounds, people, and operating processes it requires.

- Current/do nothing:
- Buy:
- Assemble:
- Build:
- Replace one slice:
- Buy to learn:
- Retire:

## 3. Apply the requirements gate

Use **Pass**, **Fail**, or **Unknown**. A failed non-negotiable requirement
removes the option. An unknown requires investigation or a bounded experiment;
it does not become a pass because the option is convenient.

| Requirement | Option A | Option B | Option C | Evidence or open question |
| --- | --- | --- | --- | --- |
| Required outcome |  |  |  |  |
| Functional fit |  |  |  |  |
| Consequence and evidence floor |  |  |  |  |
| Authority, appeal, and remedy |  |  |  |  |
| Integration and data boundaries |  |  |  |  |
| Degraded mode and recovery |  |  |  |  |
| Record continuity and exit |  |  |  |  |

## 4. Price every seam

When an option misses a requirement, the compensation belongs to that option's
architecture and total cost.

| Fit gap | Compensation | Owner | Coupled systems | Break trigger | Detection and recovery | Recurring load | Removal path |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

If a required compensation has no owner, the option does not pass.

## 5. Compare ownership among the survivors

For each surviving option, record ranges and confidence rather than fabricated
precision.

- acquisition and implementation;
- integration and migration;
- operation, support, reliability, and on-call;
- security, privacy, compliance, and evidence;
- training, adoption, and change management;
- vendor management and renewal exposure;
- internal staffing and opportunity cost;
- roadmap, compatibility, and technical debt;
- incident, recovery, and failure-tail exposure;
- strategic control, differentiation, and learning;
- exit, data disposition, migration, and retirement.

## 6. Record the decision and its reversal

- Selected option:
- Why it passed the requirements gate:
- Ownership obligation accepted:
- Seam obligations accepted:
- Strongest counterargument:
- Evidence still missing:
- Bounded experiment or replacement-slice test:
- Reversal trigger:
- Exit or retirement path:
- Reassessment date:
- Accountable executive:

## Worked fictional example

Alder & Finch evaluates a workflow product that meets most of a regulated
review process. The missing requirements are attributable evidence and a
recoverable record of disputed decisions. Buying appears cheapest until the
team records two compensations: a parallel evidence store and manual
reconciliation after vendor updates. Those seams require permanent internal
ownership.

An AI-built replacement slice shows that the differentiating decision record
is feasible, but it does not prove that the organization should operate the
whole product. The company buys the commodity workflow, builds the bounded
evidence and explanation layer, preserves an exit contract, and schedules a
replacement exercise. Fit chooses the viable architecture; ownership analysis
chooses which viable obligation to carry.

## Misuse test

Stop and reset the decision if anyone:

- changes a requirement only after seeing a preferred product;
- compares a vendor demonstration with an internal production obligation;
- calls glue code or a manual workaround free;
- treats a prototype as proof of operability;
- assumes internal ownership creates coherence automatically;
- treats vendor ownership as transfer of organizational accountability;
- scores cost before deciding whether the option is viable.
