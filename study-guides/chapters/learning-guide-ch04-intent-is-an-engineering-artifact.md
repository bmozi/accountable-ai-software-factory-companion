# Learning Guide — Chapter 4: Intent Is an Engineering Artifact

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Explain why intent must persist beyond a prompt or conversation.
> 2. Analyze outcomes, constraints, prohibitions, and unresolved decisions separately.
> 3. Evaluate whether an intent artifact creates a safe stopping condition.
> 4. Construct an intent statement and MUST-NOT boundary for a real request.

## Study Guide

### Key Terms

- **Intent artifact:** A durable record of desired outcome and governing boundaries.
- **Constraint:** A condition the solution must satisfy.
- **Prohibition:** A reasonable action or assumption that is explicitly disallowed.
- **Decision right:** Authority assigned to a named role for an unresolved choice.
- **Safe stop:** A preserved state that prevents unauthorized invention or action.

### Review Questions

1. How is intent broader than a requirement?
2. Why do prohibitions reveal hidden architecture?
3. What should happen when material intent remains unresolved?
4. How can two readers test whether an intent artifact is executable?

### Discussion Questions

1. When does additional clarification become delay rather than risk reduction?
2. Which product decisions should never be inferred from historical code alone?

### Exercises

**Exercise 4.1 (Core): Write outcome-first intent.** Remove implementation language from a current request and state the changed condition sought.
*Deliverable:* An intent artifact with outcome, constraints, and owner.
*Assessment:* The outcome is observable and does not prescribe an unjustified implementation.

**Exercise 4.2 (Core): Build the MUST-NOT set.** Identify five damaging but reasonable assumptions.
*Deliverable:* A prohibition and decision-right table.
*Assessment:* Each item has a reason, owner, and stop behavior.

**Exercise 4.3 (Challenge): Test translation.** Give the artifact to two independent readers and compare their permitted next actions.
*Deliverable:* A translation test report.
*Assessment:* Divergent material actions trigger a documented revision or stop.
