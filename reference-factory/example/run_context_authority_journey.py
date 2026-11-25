#!/usr/bin/env python3
"""Run an offline context, authority and learning extension to the teaching core.

Version 1, 2026-11-25. Fictional actors and records; no model or network calls.
© 2026 John Briggs — MIT licensed; see ../../LICENSE-CODE.
"""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from accountable_factory import ContractViolation, Factory, PolicyEngine, sha256_digest


ROOT = Path(__file__).resolve().parents[2]
NOW = "2026-11-25T12:00:00Z"
SOURCE_OWNER = "meridian-policy-owner"


@dataclass(frozen=True)
class SourceVersion:
    source_id: str
    version: str
    text: str

    @property
    def digest(self) -> str:
        return sha256_digest(self.text.encode("utf-8"))


@dataclass(frozen=True)
class AdvisoryView:
    """A lesson-only reference to one source version, not an authority grant."""

    source_id: str
    source_version: str
    source_digest: str
    advice: str


class LessonContext:
    """Small in-memory registry for this exercise, separate from the core schema.

    The fixed owner is a fictional fixture identity, not real authentication.
    There is no connector, tenant isolation, transitive lineage or durable store.
    """

    def __init__(self) -> None:
        self.history: dict[tuple[str, str], SourceVersion] = {}
        self.current: dict[str, SourceVersion] = {}

    def admit(self, source: SourceVersion, actor: str) -> None:
        if actor != SOURCE_OWNER:
            raise ContractViolation("source admission requires the lesson's policy owner")
        if not source.source_id.strip() or not source.version.strip() or not source.text.strip():
            raise ContractViolation("source identity, version and text are required")
        key = (source.source_id, source.version)
        previous = self.history.get(key)
        if previous is not None and previous != source:
            raise ContractViolation("a source version cannot be rewritten")
        if previous is not None and self.current.get(source.source_id) != previous:
            raise ContractViolation("an old source cannot silently become current again")
        self.history[key] = source
        self.current[source.source_id] = source

    def derive(self, source_id: str, advice: str) -> AdvisoryView:
        source = self.current.get(source_id)
        if source is None or not advice.strip():
            raise ContractViolation("current source and nonempty advice are required")
        return AdvisoryView(source.source_id, source.version, source.digest, advice)

    def check_current(self, view: AdvisoryView) -> None:
        source = self.current.get(view.source_id)
        if source is None:
            raise ContractViolation("current source is unavailable")
        if (source.version, source.digest) != (view.source_version, view.source_digest):
            raise ContractViolation("source changed; derive and review new advice")


def advisory_content(view: AdvisoryView) -> bytes:
    """Bind this lesson's exact advice and source reference to candidate bytes."""
    document = {
        "advice": view.advice, "sourceId": view.source_id,
        "sourceVersion": view.source_version, "sourceDigest": view.source_digest,
    }
    return (json.dumps(document, sort_keys=True) + "\n").encode("utf-8")


def work_order(suffix: str) -> dict[str, Any]:
    work = json.loads((ROOT / "examples/artifacts/work-order.valid.json").read_text())
    work["id"] = f"WO-CONTEXT-{suffix}"
    return work


def prepare_candidate(
    factory: Factory, work: dict[str, Any], content: bytes, *, omit_last_check: bool = False
) -> str:
    """Use the existing factory for intent, candidate and independent evidence."""
    factory.admit(work, work["owner"])
    running = factory.start(work["id"], work["version"], work["owner"])
    digest = factory.record_candidate(work["id"], running.version, content, work["producerId"])
    factory.begin_verification(work["id"], "lesson-evaluator")
    criteria = work["evidenceFloor"][:-1] if omit_last_check else work["evidenceFloor"]
    for number, criterion in enumerate(criteria, 1):
        evidence = {
            "schemaVersion": "1.0", "kind": "EvidenceRecord",
            "id": f"EV-{work['id']}-{number}", "workOrderId": work["id"],
            "candidateDigest": digest, "criterionId": criterion,
            "producerId": work["producerId"],
            "evaluator": {"actorId": "lesson-evaluator", "type": "deterministic", "independence": "separate-method"},
            "method": "Fictional independent fixture check", "result": "pass",
            "decisive": True, "observedAt": NOW,
            "limitations": ["Scripted teaching evidence, not a real evaluation service"],
        }
        factory.record_evidence(evidence, "lesson-evaluator")
    return digest


def approve(factory: Factory, work: dict[str, Any], digest: str) -> None:
    factory.request_decision(work["id"], digest, "lesson-evaluator")
    factory.decide(
        work["id"], digest, work["consequenceOwner"], "approve",
        "Fictional reviewer accepts this candidate and declared scope",
    )


def apply_local_advisory(
    factory: Factory, work_id: str, content: bytes, view: AdvisoryView,
    context: LessonContext, output: Path, actor: str,
) -> dict[str, Any]:
    """Compose current checks before one local file effect; not a core API.

    The lesson supplies a new temporary directory. This wrapper is not a file
    sandbox, distributed lock, authenticated identity service or production tool.
    """
    work = factory.load(work_id)
    digest = sha256_digest(content)
    trace = factory.trace(work_id)
    if work.state != "APPROVED" or actor != work.document["releaseOwner"]:
        raise ContractViolation("a named release owner and approved Work Order are required")
    if not any(
        decision["candidate_digest"] == digest and decision["decision"] == "approve"
        for decision in trace["dispositions"]
    ):
        raise ContractViolation("approval does not cover this candidate")
    context.check_current(view)
    if content != advisory_content(view):
        raise ContractViolation("candidate does not bind this exact advisory and source")
    factory.assert_capability(work_id, "writes", "isolated-workspace", actor)
    operation_id = f"OP-{work_id}"
    factory.begin_release(work_id, operation_id, actor)
    # Exclusive creation makes a repeated lesson write explicit rather than
    # silently replacing a file. Failure/recovery after this point needs review.
    with output.open("xb") as handle:
        handle.write(content)
    effect_ref = sha256_digest(output.read_bytes())
    factory.complete_operation(operation_id, effect_ref, actor)
    return factory.create_receipt(
        work_id, digest, operation_id, actor, ["writes:isolated-workspace"],
        "advisory", "one temporary fictional advisory file", "remove the temporary fixture",
        f"RC-{work_id}",
    )


def expect_blocked(operation: Callable[[], Any]) -> str:
    try:
        operation()
    except ContractViolation as exc:
        return str(exc)
    raise AssertionError("The deliberately unsafe lesson operation was not blocked")


def run(directory: Path) -> dict[str, Any]:
    """Create a new isolated lesson directory and return inspectable outcomes."""
    directory.mkdir(parents=True, exist_ok=False)
    factory = Factory(directory / "factory.db", PolicyEngine.from_file(ROOT / "policies/default-policy.json"))
    context = LessonContext()
    original = SourceVersion("meridian-reconciliation-rule", "1", "Show unresolved source conflicts to a specialist.")
    replacement = SourceVersion("meridian-reconciliation-rule", "2", "Show conflicts and require a ledger cross-check.")
    context.admit(original, SOURCE_OWNER)
    old_view = context.derive(original.source_id, "Show the source conflict.")
    context.admit(replacement, SOURCE_OWNER)
    corrected_block = expect_blocked(lambda: context.check_current(old_view))
    current_view = context.derive(replacement.source_id, "Show the conflict and request a ledger cross-check.")
    context.check_current(current_view)
    content = advisory_content(current_view)
    try:
        missing = work_order("MISSING-CHECK")
        missing_digest = prepare_candidate(factory, missing, content, omit_last_check=True)
        missing_block = expect_blocked(lambda: factory.request_decision(missing["id"], missing_digest, "lesson-evaluator"))
        missing_trace = factory.trace(missing["id"])

        revoked = work_order("REVOKED")
        revoked_digest = prepare_candidate(factory, revoked, content)
        approve(factory, revoked, revoked_digest)
        factory.revoke_capability(revoked["id"], "writes", "isolated-workspace", revoked["owner"])
        revoked_file = directory / "revoked-advisory.json"
        revoked_block = expect_blocked(lambda: apply_local_advisory(factory, revoked["id"], content, current_view, context, revoked_file, revoked["releaseOwner"]))

        current = work_order("CURRENT")
        current_digest = prepare_candidate(factory, current, content)
        approve(factory, current, current_digest)
        receipt = apply_local_advisory(factory, current["id"], content, current_view, context, directory / "advisory.json", current["releaseOwner"])
        factory.begin_observation(current["id"], current["consequenceOwner"])
        observation = copy.deepcopy(json.loads((ROOT / "examples/artifacts/outcome.valid.json").read_text()))
        observation.update({"id": "OUT-CONTEXT-LOCAL", "receiptId": receipt["id"], "observedAt": NOW})
        observation["limitations"] = ["Fictional exercise data; no reader or customer outcome was measured"]
        factory.record_outcome(observation, current["consequenceOwner"])
        scope = {"workClass": current["workClass"], "sourceVersion": "2", "use": "local-exercise"}
        learning_id = "LRN-CONTEXT-LOCAL"
        factory.propose_learning(current["id"], learning_id, "Recheck context and authority after a review wait", scope, current["learningOwner"])
        candidate_influence = factory.learning_can_influence(learning_id, scope, NOW)
        producer_block = expect_blocked(lambda: factory.promote_learning(learning_id, [receipt["id"], observation["id"]], "2026-12-31T00:00:00Z", current["producerId"]))
        factory.promote_learning(learning_id, [receipt["id"], observation["id"]], "2026-12-31T00:00:00Z", current["learningOwner"])
        admitted_influence = factory.learning_can_influence(learning_id, scope, NOW)
        factory.retire_learning(learning_id, current["learningOwner"], "A later correction requires a new validation decision")
        retired_influence = factory.learning_can_influence(learning_id, scope, NOW)
        report = {
            "lesson": "context-authority-and-learning", "version": 1,
            "classification": "fictional offline teaching extension",
            "sourceCorrection": {"oldView": "blocked", "reason": corrected_block, "newView": "current", "historicalVersions": len(context.history)},
            "missingCheck": {"verification": "incomplete", "reason": missing_block, "receiptCreated": bool(missing_trace["receipts"]), "state": missing_trace["state"]},
            "revocationDuringApproval": {"decision": "blocked", "reason": revoked_block, "effectCreated": revoked_file.exists()},
            "freshScope": {"workOrderId": current["id"], "effectCreated": True, "receipt": receipt},
            "learning": {"candidateCanInfluence": candidate_influence, "producerPromotion": producer_block, "reviewedCanInfluence": admitted_influence, "retiredCanInfluence": retired_influence},
            "observedOutcome": "insufficient; fictional data does not establish benefit",
            "trace": factory.trace(current["id"]),
            "limits": ["Context history is in-memory and direct-source only", "Actors are fixture strings, not authenticated identities", "No concurrent authorization/effect atomicity or production safety claim", "Learning admission is scripted owner judgment, not proof the claim is true"],
        }
        (directory / "lesson-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return report
    finally:
        factory.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Keep artifacts in a new directory; never overwrite")
    args = parser.parse_args()
    if args.output_dir is not None:
        report = run(args.output_dir)
    else:
        with tempfile.TemporaryDirectory(prefix="context-authority-lesson-") as temporary:
            report = run(Path(temporary) / "journey")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("Lesson complete: stale context and revoked action blocked; fresh bounded advisory recorded; incomplete evidence withheld release.")


if __name__ == "__main__":
    main()
