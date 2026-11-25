# Context, current authority and learning after a review wait

**Version:** 1.0 · **Updated:** 2026-11-25 · **Author:** John Briggs

**Relationship:** Chapters 5–7, 10–12 and 15–16. This is an additional laboratory
for the book's architecture, not a replacement for its reasoning or the existing
[twenty-four acceptance obligations](05-acceptance-test-suite.md).

## What you will learn

A useful reference and permission to act answer different questions. This lesson
helps you check both after a review wait, inspect missing evidence, and decide
what an organization may learn. Think of an advisory note as a reference card
and an approval as permission for one specific proposed result. Updating the
card does not renew permission, and permission does not make the card correct.

In the fictional Meridian Ledger case, a reconciliation specialist needs an
advisory explaining conflicting records. A policy correction adds a ledger
cross-check while a candidate is under review. Another candidate's local write
permission is revoked after approval. The safe result is to stop those uses,
then admit and review a fresh bounded candidate rather than reuse old permission.
No payment, customer record or production system is changed.

## Run the lesson

From the companion repository root:

```bash
PYTHONPATH=. python3 -m unittest discover -s reference-factory/example -p 'test_context_authority_journey.py' -v
PYTHONPATH=. python3 reference-factory/example/run_context_authority_journey.py
```

The lesson requires only Python 3.10 or newer and its standard library. It
requires no model, API key, cloud account or additional package. The default
command creates a temporary SQLite database and one advisory file, prints the
report, then removes its temporary directory. Windows PowerShell readers can
set `$env:PYTHONPATH = "."` and use the equivalent `python` commands.

To retain evidence, choose a directory that does not already exist:

```bash
PYTHONPATH=. python3 reference-factory/example/run_context_authority_journey.py --output-dir /tmp/meridian-context-lesson
```

For PowerShell, use a new relative path such as `--output-dir .\context-lesson`.
Existing directories are refused. Inspect `lesson-report.json`, `advisory.json`
and `factory.db`. The last contains ordinary canonical teaching-factory Work
Orders, evidence, decisions, revocations, operations, receipt and learning records.
The context registry itself is in memory and does **not** survive a restart.

## Follow the decision chain

| Boundary | What the script does | Evidence to inspect | What this does not establish |
|---|---|---|---|
| Intent | Admits three distinct fictional Work Orders for missing evidence, revoked authority and a valid bounded result | `workOrderId`, declared criteria and canonical trace | Legitimate organizational policy or real user need |
| Context | Preserves source versions 1 and 2; refuses old advice after correction; derives advice with the new version | `sourceCorrection.oldView`, `newView`, `historicalVersions`; candidate contains source ID/version/digest and exact advice | Semantic truth, enterprise connectors or complete dependency lineage |
| Authority | Approves an exact candidate, then revokes its isolated-workspace capability; checks again before effect | `revocationDuringApproval.decision`, `effectCreated`; durable denial event | Real authentication, a distributed authorization guarantee or global revocation coverage |
| Execution | Uses a separately reviewed, permitted candidate to create one local advisory file | `freshScope.receipt`, candidate/effect digests and read-back bytes | Production release or independent verification of the advice's meaning |
| Verification | Deliberately omits one required criterion on another Work Order | `missingCheck.verification`, `state`, `receiptCreated` | A partial check cannot justify a passed evidence floor |
| Outcomes | Records explicitly fictional insufficient outcome data | `observedOutcome` and trace state `INSUFFICIENT` | Measured reader/customer benefit, time saved or ROI |
| Learning | Proposes a scoped lesson, rejects producer promotion, allows the named learning owner to admit it, then retires it | `learning.candidateCanInfluence`, `reviewedCanInfluence`, `retiredCanInfluence` | Automated discovery of truth or a scientifically validated organizational practice |

The complete main journey includes separate unsafe cases and a legitimate-use
control. The tests additionally change a source after approval, attempt to reuse
its old candidate approval, reopen the database after revocation, change the
candidate, and attempt release as the producer. The lesson must block those
invalid uses while the freshly scoped, reviewed candidate can still complete.

### Why the missing-check result has no receipt

The canonical teaching factory requires every declared evidence-floor criterion
to be present before asking for disposition, and passing before ordinary
approval. Therefore the missing-check case remains `VERIFYING`; it has no release
and no `FactoryReceipt`. The lesson report says **verification incomplete** and
`receiptCreated: false`. It is a lesson report, not a substitute receipt schema.

A production design might also produce a terminal failure manifest. That is a
separate contract decision; do not fabricate a successful release receipt to
make a dashboard look complete. In this companion, the current core contract
remains unchanged.

### What owner-reviewed learning means here

The core records a learning candidate with no influence. Only the named learning
owner may promote it with existing evidence references, scope and expiry; a later
retirement removes influence without deleting history. The script supplies that
owner decision. Fixture strings are not authenticated people, and the decision
is not a test of the claim's semantic truth.

The recorded insufficient outcome cannot support a claim of improved business
performance. The narrow lesson concerns observed local boundary behavior:
recheck context and permission after a wait. A real owner must assess contrary
examples, applicability, validation method, costs and outcome evidence before
allowing broader influence. Review/admission is a responsibility, not a magic
conversion of an observation into fact.

## Read the implementation at the right level

[The lesson script](example/run_context_authority_journey.py) composes the existing
`accountable_factory` implementation. Work Orders, evidence, independent
candidate disposition, revocation, operations, receipts and learning use the
canonical core. No new artifact kind or alternative factory state machine is
introduced.

`LessonContext`, `SourceVersion` and `AdvisoryView` are deliberately small,
lesson-only objects. They demonstrate one direct source reference and a current
version check. Exact advice plus source identity/version/digest are bound into
the candidate bytes; a changed candidate requires a new disposition. The wrapper
checks source currency, current write capability and the named release owner
before exclusive creation of the local file. These checks do not form an atomic
transaction with an external effect.

This is not a production context service, file sandbox, policy engine, authority
issuer, durable source registry, federated memory system or signing scheme.
It does not establish tenant isolation, transitive correction propagation,
concurrent approval consumption, expiry of real credentials, or authenticity of
an arbitrary source. Changing the source text cannot establish the correctness
of advice merely by changing a hash. An interrupted file effect needs explicit
recovery; the separate [recovery laboratory](03-recovery-and-reconciliation.md)
teaches indeterminate effects and reconciliation.

## Change one contract and explain the consequence

1. Add a third source version. Identify which advice and candidate must be
   reconsidered. Preserve old bytes and decisions rather than relabeling them.
2. Omit a different evidence criterion. Explain why a missing check differs from
   a failed check and why neither is a passed approval requirement.
3. Try a different actor for policy admission, release or learning promotion.
   Identify which named role must decide and what authentication a real system
   would need to bind to that role.
4. Narrow the admitted learning scope, then query a different scope. Explain why
   useful advice in one work class does not earn universal influence.
5. Consider a revocation that races with a remote effect. State the unresolved
   outcome and what fencing, consistency or reconciliation contract your chosen
   platform would need. Do not claim this local lesson solves that race.

**Completion:** point to an actual denied use, an actual permitted local result,
the absent receipt for incomplete evidence, and a separately owned learning
admission/retirement. Explain what each proves and what still needs human judgment.
A green test alone is not a complete answer to the book's architectural question.

## Related instruments and correction path

- [Chapter-to-companion map](../BOOK-TO-COMPANION-MAP.md)
- [Memory governance workbook](../templates/memory-governance-workbook.md)
- [Factory architecture decision guide](../templates/factory-architecture-decision-guide.md)
- [Interactive architecture guide](../diagrams/interactive-guide/index.html)
- [Learning paths](../learning-paths/README.md)

Report an ordinary error through the repository's correction process; use the
private reporting path in [SECURITY](../SECURITY.md) for sensitive findings.
This prose is governed by [LICENSE-CONTENT](../LICENSE-CONTENT); executable
lesson code carries the [MIT license](../LICENSE-CODE). No unpublished manuscript,
private implementation, production credential or third-party booklet material is
needed to complete this exercise.
