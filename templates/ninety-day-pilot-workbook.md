# Ninety-Day Factory Pilot Workbook

## Pilot Rule

Choose one frequent, bounded, reversible work class. The pilot tests an
operating model, not whether an agent can generate code in a demonstration.

## Before Day One

### Select the Work Class

The first work class should have:

- clear eligibility;
- enough frequency to observe repeated behavior;
- low or moderate consequence;
- reliable automated evidence;
- a known human owner;
- reversible release;
- an existing baseline.

Avoid critical authorization, irreversible data migration, novel architecture,
and poorly understood legacy behavior as the first authority-bearing pilot.

### Establish the Baseline

Measure at least:

- elapsed lead time;
- active human time;
- review time and queue time;
- completion and abandonment;
- rework;
- escaped defects or failed changes;
- recovery time;
- security findings;
- customer or operator outcome;
- developer confidence and cognitive load;
- cost per accepted change.

### Precommit Decisions

**Success means:**<br>
**Failure means:**<br>
**Stop immediately if:**<br>
**Authority may expand only if:**<br>
**Decision owner:**

## Days 1–15: Observe and Define

- map the current path from request to production;
- identify the actual constraint;
- write the factory charter;
- define work-order, evidence, and escalation schemas;
- establish privacy, security, and disclosure boundaries;
- run the agent read-only or in suggestion mode;
- record where the proposed model disagrees with real work.

**Gate:** Do not grant write authority until the team can explain the current
process and evaluate suggested outcomes consistently.

## Days 16–30: Draft-Only Production

- allow candidate branches or changes in an isolated environment;
- require human merge and deployment;
- enforce mechanical evidence independently;
- record no-op loops, retries, disagreements, and missing context;
- compare accepted and rejected candidates;
- revise the charter rather than relying on operator memory.

**Gate:** Expand only if the system stops correctly, the evidence package is
usable, and reviewer load is understood.

## Days 31–60: Bounded Team Use

- include several operators and reviewers;
- enforce identity and per-tool authority;
- test rollback and recovery deliberately;
- introduce memory only for a clearly governed record class;
- begin one controlled improvement experiment;
- measure outcomes and countermetrics weekly;
- interview participants about hidden work and trust.

**Gate:** Do not treat higher throughput as success if rework, instability,
review burden, or customer outcome worsens beyond the precommitted threshold.

## Days 61–90: Prove or Reduce Authority

- compare with the baseline and account for changes in work mix;
- inspect failure tails, not only averages;
- review every override and exception;
- test whether validated learning improves later work;
- decide whether to preserve, narrow, expand, or stop the pilot;
- publish the decision and evidence internally;
- update the operating model before buying broader automation.

## Weekly Evidence Log

| Week | Eligible work | Accepted | Rejected | Partial | Human time | Rework | Failed changes | Key learning |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |  |  |  |

## Authority Ledger

| Date | Dimension changed | Previous authority | New authority | Evidence | Approver | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Day-Ninety Decision

- [ ] Stop and document why
- [ ] Continue at current authority
- [ ] Narrow work or authority
- [ ] Expand one authority dimension
- [ ] Prepare a second work-class pilot

The decision memo must report desired outcomes, countermetrics, failures,
participant experience, costs, unresolved risks, and what evidence remains
missing. “The demo worked” is not a decision criterion.
