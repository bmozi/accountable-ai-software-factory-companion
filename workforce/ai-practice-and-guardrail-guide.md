# AI Practice and Guardrail Guide

## Purpose

Use this guide before distributing broader AI authority to an engineering team.
It helps a person and organization answer three questions:

1. Where is our demonstrated AI operating practice today?
2. Which protections does the organization supply, and which decisions remain
   with the engineer?
3. What evidence would justify the next expansion of authority?

This is not an employee ranking, certification, or performance score. Assess a
person in relation to a specific work class and operating environment. Someone
may be ready to direct documentation changes and unready to authorize a data
migration. That is ordinary risk differentiation, not a judgment of worth.

## Part 1: Locate the Current Practice

Choose the highest level for which behavior is repeatable and evidenced. Do not
select a level because a tool can technically perform it.

### Level 1: Assisted exploration

The engineer uses AI to explain, search, brainstorm, or draft. No machine action
has production consequence.

Evidence to look for:

- sensitive information is handled according to policy;
- generated claims are checked before reuse;
- drafts are clearly distinguished from approved work;
- the engineer can name important limitations of the tool.

### Level 2: Supervised production

AI creates bounded candidate changes. The engineer inspects the work and
ordinary delivery controls remain authoritative.

Evidence to look for:

- intent, prohibitions, and success conditions are explicit;
- repository, data, tool, and budget scope are narrow;
- generated tests do not serve as the only evaluation;
- the engineer can stop, discard, and reproduce the attempt;
- authorship and AI contribution remain attributable.

### Level 3: Governed delegation

The system performs multi-step work inside a defined execution envelope and
produces evidence for an accountable disposition.

Evidence to look for:

- work-order state survives sessions and interruption;
- authority is bound to identity and work;
- producer and decisive evaluator are sufficiently independent;
- timeouts, retries, and partial side effects have a recovery contract;
- exceptions route to a named owner;
- the engineer can explain why the work was allowed to advance.

### Level 4: Managed factory operation

Several work classes use shared contracts, controls, evidence, service
objectives, outcome measurement, and governed learning.

Evidence to look for:

- maturity and authority differ by work class;
- the platform exposes normal, constrained, read-only, drain, and stopped modes;
- provider, tenant, reviewer, release, and risk capacity are managed;
- outcome and human-load countermetrics influence expansion;
- validated learning cannot approve its own authority;
- retirement and provider exit are exercised rather than merely documented.

## Part 2: Divide the Responsibility Clearly

Complete this table for one work class.

| Responsibility | Supplied by factory | Supplied by team | Engineer must decide | Evidence |
| --- | --- | --- | --- | --- |
| Approved tools and models |  |  |  |  |
| Data and repository scope |  |  |  |  |
| Intent and prohibitions |  |  |  |  |
| Budget and stopping limits |  |  |  |  |
| Required tests and evaluation |  |  |  |  |
| Security and privacy checks |  |  |  |  |
| Exception and escalation path |  |  |  |  |
| Recovery and rollback |  |  |  |  |
| Release decision |  |  |  |  |
| Outcome observation |  |  |  |  |
| Learning and retention |  |  |  |  |

Any blank is an unowned responsibility. Do not solve it by writing “engineer
uses judgment.” Name the information, competence, time, and authority that make
the judgment viable.

## Part 3: Create the Guardrail Card

For the selected work class, record:

- **Allowed purpose:**
- **Excluded purposes:**
- **Allowed repositories, data, environments, and tools:**
- **Maximum time, cost, attempts, and parallel work:**
- **Actions requiring human approval:**
- **Required independent evidence:**
- **Conditions that force a stop:**
- **Indeterminate-state recovery owner:**
- **Rollback or compensation path:**
- **Outcome owner and observation window:**
- **Retention and deletion rules:**
- **Where the engineer can ask for help:**

The guardrail card should be reflected in enforcement where practical. A rule
that exists only in training material is guidance, not a mechanical boundary.

## Part 4: Run a Formation Exercise

Choose a reversible, frequent, useful task. Before using AI, ask the engineer
to identify:

1. one ambiguity in the request;
2. one action the system must not take;
3. one producer claim requiring independent evidence;
4. one condition that should stop the attempt;
5. one failure that could make retry unsafe;
6. the person who owns the release consequence;
7. the outcome that would show the change helped.

Run the task. Review the decision chain, not prompt elegance. If the attempt
stops safely and exposes a missing decision, treat that as useful performance.

## Part 5: Decide Whether Authority Should Change

Use one disposition:

- **Preserve:** the current level fits the work and evidence.
- **Expand one dimension:** increase only tool, data, duration, parallelism, or
  release authority whose supporting evidence is clear.
- **Narrow:** reduce authority because behavior, context, or consequence changed.
- **Improve the factory:** the person performed appropriately, but the shared
  path, training, evidence, or recovery support was inadequate.
- **Stop the work class:** consequence exceeds current organizational capability.

Never make greater authority a reward for activity volume. Require observed
judgment, evidence quality, safe stopping, recovery competence, and acceptable
outcomes.

## Manager and Platform Commitments

The organization should not ask employees to carry institutional risk alone.
Before encouraging use, leaders commit to:

- provide a safe approved path and an honest description of its limits;
- protect time for learning, review, and recovery;
- distinguish experimentation from production authority;
- avoid punishing correct refusal or visible stopping;
- supply competent security, privacy, product, and operational escalation;
- measure burdens transferred to engineers and reviewers;
- investigate whether a failure reflects the person, the work contract, the
  platform, the incentive, or the missing institution;
- update training and controls when evidence changes.

## Review Record

- Work class:
- Participant and role:
- Current level and evidence:
- Factory protections available:
- Missing protections:
- Guardrail card version:
- Disposition:
- One next learning objective:
- One factory improvement owner:
- Review date and next review:

The desired result is not universal autonomy. It is shared capability whose
authority remains proportionate to demonstrated practice and organizational
support.
