#!/usr/bin/env python3
"""Run the fictional Meridian Ledger failure-oriented factory journey.

© 2026 John Briggs — MIT licensed; see ../../LICENSE-CODE.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from reference_factory import ContractViolation, Factory


def show(step: str, detail: object) -> None:
    print(f"\n[{step}]\n{json.dumps(detail, indent=2, sort_keys=True)}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="accountable-factory-") as temp:
        database = Path(temp) / "factory.db"
        factory = Factory(database)
        show("1 exploration envelope", {
            "purpose": "learn whether conflict explanation helps specialists",
            "authority": "synthetic data, isolated draft only",
            "expires": "14 days",
            "production_effects": "prohibited",
        })

        intent = {
            "promise": "show source conflict and a supported advisory recommendation",
            "criteria": ["contract", "explanation", "prohibited-write"],
            "prohibitions": ["no source mutation", "no automatic match", "no customer message"],
            "owner": "Elena Park",
        }
        work = factory.admit(intent)
        show("2 admitted Work Order", work.__dict__)
        running = factory.transition(work.id, work.version, "RUNNING", "Luis Ortega")
        digest = factory.record_candidate(work.id, running.version, b"meridian-advisory-v1")
        candidate = factory.transition(work.id, running.version, "CANDIDATE", "Luis Ortega")
        verifying = factory.transition(work.id, candidate.version, "VERIFYING", "evidence-plane")

        try:
            factory.verdict(digest, "contract", "producer-self-review", "pass", producer=True)
        except ContractViolation as error:
            show("3 evaluator-independence failure", {"stopped": str(error)})

        factory.verdict(digest, "contract", "contract-verifier", "pass")
        factory.verdict(digest, "prohibited-write", "policy-verifier", "pass")
        factory.verdict(digest, "explanation", "example-evaluator", "pass")
        factory.verdict(digest, "explanation", "operator-evaluator", "fail")
        statuses = {criterion: factory.evidence_status(digest, criterion) for criterion in intent["criteria"]}
        show("4 conflicting evidence", statuses)
        assert not factory.evidence_satisfies(digest, intent["criteria"])

        decision = factory.transition(work.id, verifying.version, "DECISION_REQUIRED", "evidence-plane")
        factory.record_event(work.id, "disposition", {"decision": "repair", "owner": "Elena Park"})
        approved = factory.transition(work.id, decision.version, "APPROVED", "Elena Park")
        show("5 accountable disposition", {
            "state": approved.state,
            "boundary": "illustrative human disposition; conflict remains visible",
        })

        operation_id = "meridian-canary-release-001"
        factory.begin_operation(work.id, operation_id)
        factory.mark_indeterminate(operation_id)
        factory.db.close()

        restarted = Factory(database)
        before = restarted.operation_status(operation_id)
        after = restarted.reconcile(operation_id, "canary-cohort-001")
        show("6 restart reconciliation", {"before": before, "after": after, "duplicate_effect": False})
        for kind, body in [
            ("provider_substitution_exercise", {"result": "decision record portable; degraded adapter used"}),
            ("outcome", {"specialist_disposition": "improved", "total_queue": "unchanged", "status": "mixed"}),
            ("authority_narrowed", {"to": "original advisory cohort", "reason": "mixed outcome"}),
            ("learning_rejected", {"proposal": "ignore explanation failures", "reason": "weakens promise"}),
            ("retirement", {"exploration_prototype": "deleted", "production_slice": "renewed one quarter"}),
        ]:
            restarted.record_event(work.id, kind, body)
        show("7 outcome, learning, and retirement", restarted.events(work.id)[-5:])
        print("\nJourney complete: the system expanded no authority its evidence did not earn.")
        restarted.db.close()


if __name__ == "__main__":
    main()
