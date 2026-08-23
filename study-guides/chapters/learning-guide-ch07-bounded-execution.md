# Learning Guide — Chapter 7: Bounded Execution

> **Learning Objectives** — After completing this chapter, you will be able to:
>
> 1. Define an execution envelope across tools, data, authority, time, and cost.
> 2. Analyze how isolation, ceilings, and concurrency affect reversibility.
> 3. Evaluate whether a stated boundary is advisory or independently enforced.
> 4. Construct and test an envelope matrix for one work class.

## Study Guide

### Key Terms

- **Execution envelope:** The enforced limits within which work may proceed.
- **Isolation:** Separation that limits interference and blast radius.
- **Budget:** A ceiling on time, cost, attempts, or resources.
- **Concurrency:** Work that overlaps and can contend for state or authority.
- **Graduated authority:** Capability expanded by dimension after evidence supports it.

### Review Questions

1. Which dimensions belong in an execution envelope?
2. How does isolation buy reversibility?
3. Why does concurrency change risk rather than only speed?
4. What distinguishes an advisory limit from an enforced boundary?

### Discussion Questions

1. Which execution limits should be universal and which should vary by work class?
2. When does strict isolation cost more than the risk it reduces?

### Exercises

**Exercise 7.1 (Core): Build an envelope matrix.** Inventory tools, data, writes, environments, budgets, retries, and release authority.
*Deliverable:* A completed envelope matrix.
*Assessment:* Every boundary names its enforcement mechanism and change owner.

**Exercise 7.2 (Core): Test a stop.** Trigger a safe prohibited action or budget ceiling.
*Deliverable:* A stop receipt and operator-view capture.
*Assessment:* State, reason, evidence, and authorized next actor remain visible.

**Exercise 7.3 (Challenge): Admit controlled scale-up.** Propose one authority or concurrency increase.
*Deliverable:* An admission case.
*Assessment:* Evidence, quota, rollback, tenant impact, and revocation condition are explicit.
