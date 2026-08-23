# Learning Guide — Chapter 9: Deterministic Machinery Around Probabilistic Work

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Distinguish probabilistic interpretation from deterministic enforcement.
> 2. Analyze factory decisions by responsibility and mechanism.
> 3. Evaluate where repeated judgment can become a mechanical control.
> 4. Construct a responsibility map that records versioned decision machinery.

## Study Guide

### Key Terms

- **Probabilistic work:** Interpretation or generation whose result is not mechanically fixed.
- **Deterministic control:** A repeatable rule implemented in executable machinery.
- **State machine:** Named states and permitted transitions enforced by code.
- **Idempotency:** Safe repetition without duplicated consequence.
- **Versioned policy:** A rule tied durably to the decision it governed.

### Review Questions

1. Which tasks are models particularly suited to perform?
2. Which decisions should be moved into deterministic machinery?
3. Why can a deterministic rule still be wrong?
4. Why must evidence record policy and tool versions?

### Discussion Questions

1. What repeated judgment in your organization is ready to become a control?
2. When does mechanizing a decision conceal necessary human interpretation?

### Exercises

**Exercise 9.1 (Core): Map responsibilities.** Classify decisions as interpretation, proposal, enforcement, execution, evaluation, approval, or recording.
*Deliverable:* A responsibility map.
*Assessment:* Mechanism choice matches decision type and consequence.

**Exercise 9.2 (Core): Extract one control.** Replace one repeated model judgment with a schema, policy, or test.
*Deliverable:* A control specification and examples.
*Assessment:* Passing, failing, and ambiguous cases are reproducible.

**Exercise 9.3 (Challenge): Version a consequence.** Design how an approval becomes stale when artifact, evidence, or policy changes.
*Deliverable:* A stale-decision protocol.
*Assessment:* No prior decision silently authorizes a materially changed candidate.
