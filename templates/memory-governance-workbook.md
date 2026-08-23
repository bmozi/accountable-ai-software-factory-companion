# Memory Governance Workbook

Use this workbook with Chapter 6 to prevent a memory system from treating
semantic similarity as authority. Complete it for each class of record the
factory may retrieve or use to change future behavior.

## Memory-class inventory

| Memory class | Example | Source of truth | Owner | Retention | May guide future action |
| --- | --- | --- | --- | --- | --- |
| Source record | Specification or policy |  |  |  | Yes, within authority |
| Session history | Tool calls and messages |  |  |  | No, inspection only |
| Decision record | Approved tradeoff |  |  |  | Yes, within scope |
| Observation | One retrospective finding |  |  |  | Experimental only |
| Candidate learning | Proposed reusable guidance |  |  |  | Bounded test only |
| Validated practice | Reinforced guidance |  |  |  | Yes, within scope |
| Retired learning | Superseded guidance |  |  |  | No |

## Learning record

**Identifier:**  
**State:** record / observation / candidate / validated / retired  
**Created by:**  
**Created at:**  
**Reviewed by:**  
**Next review:**

### Claim

State one bounded lesson. Avoid words such as “always” unless the evidence and
scope justify them.

### Applicability

- Systems:
- Work classes:
- Risk classes:
- Languages or platforms, if material:
- Preconditions:
- Known exclusions:

### Evidence

| Evidence | Date | Supports or contradicts | Strength | Limitation |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Reinforcement

What later outcome would count as reinforcement? Repetition alone is not
enough if every instance shares the same hidden cause or evaluator.

### Contradiction

What evidence would weaken or retire the learning? Record unresolved
contradictions rather than averaging them into false confidence.

### Confidence

Choose low, medium, or high and explain the basis. Confidence should reflect
evidence quality and applicability, not a model's linguistic certainty.

### Decay and review

- Time-based review interval:
- Event that forces immediate review:
- Conditions under which influence decays:
- Retirement authority:

### Retrieval policy

- Queries or work classes for which this record is eligible:
- Minimum authority and freshness:
- Contradictions that must be shown alongside it:
- Whether the record may alter prompts, tests, policy, or execution:

## Promotion test

Before promoting a candidate learning to validated practice, answer:

1. Was it tested on work beyond the event that created it?
2. Did the test include a baseline and countermetric?
3. Were producer and evaluator sufficiently independent?
4. Did it improve the intended outcome without unacceptable harm?
5. Is the applicable scope explicit?
6. Are exceptions and contradictions preserved?
7. Can the organization reverse the change?
8. Has an authorized human approved persistent influence?

Any “no” keeps the learning experimental.

## Worked fictional example

**Observation:** A fictional factory repeatedly spent two fix iterations on
tasks where the first attempted fix produced no file change.

**Candidate learning:** If a fix iteration produces no material diff and no
new evidence, stop the loop and request human adjudication.

**Scope:** Repository-change tasks using diff-producing tools. Excludes
investigation tasks where a no-change result may be correct.

**Test:** Compare thirty eligible Work Orders before and after the rule. Track
unproductive iterations, false stops, successful completion, and reviewer
intervention time.

**Possible contradiction:** Some generators update external state without a
repository diff. The rule must inspect declared side effects before stopping.

**Decision:** Promote only for repository-only tasks if it reduces wasted
iterations without materially increasing false stops.
