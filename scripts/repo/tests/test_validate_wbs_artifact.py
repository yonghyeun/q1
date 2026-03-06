from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_wbs_artifact  # noqa: E402


class ValidateWbsArtifactTests(unittest.TestCase):
    def write_payload(self, payload: dict) -> Path:
        temp_dir = TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "artifact.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_valid_handoff_packet_passes(self) -> None:
        payload = {
            "packet_id": "H-2026-03-06-001",
            "run_id": "RUN-2026-03-06-A",
            "seq": 1,
            "slice_id": "MVP-TS-INSERT",
            "parent_wbs": "mvp-wbs/v1",
            "owner_role": "impl",
            "handoff_from": "operator",
            "handoff_to": "impl",
            "goal": "타임스탬프 삽입 구현",
            "inputs": ["docs/product/mvp-spec.md:61"],
            "contracts": ["docs/product/contracts/domain.ts"],
            "acceptance_criteria": ["버튼 클릭 시 링크가 삽입된다"],
            "owned_paths": ["apps/web/src/features/timestamp/**"],
            "required_tests": ["unit"],
            "validator_rules": ["inputs_resolve"],
            "review_rubric": ["acceptance_criteria_evidenced"],
            "expected_outputs": ["code_changes", "trace_summary"],
        }

        path = self.write_payload(payload)
        data = validate_wbs_artifact.load_json(path)
        validate_wbs_artifact.validate_against_schema("handoff-packet", data)
        validate_wbs_artifact.validate_semantics("handoff-packet", data)

    def test_handoff_packet_rejects_same_sender_and_receiver(self) -> None:
        payload = {
            "packet_id": "H-2026-03-06-001",
            "run_id": "RUN-2026-03-06-A",
            "seq": 1,
            "slice_id": "MVP-TS-INSERT",
            "parent_wbs": "mvp-wbs/v1",
            "owner_role": "impl",
            "handoff_from": "impl",
            "handoff_to": "impl",
            "goal": "타임스탬프 삽입 구현",
            "inputs": ["docs/product/mvp-spec.md:61"],
            "contracts": ["docs/product/contracts/domain.ts"],
            "acceptance_criteria": ["버튼 클릭 시 링크가 삽입된다"],
            "owned_paths": ["apps/web/src/features/timestamp/**"],
            "required_tests": ["unit"],
            "validator_rules": ["inputs_resolve"],
            "review_rubric": ["acceptance_criteria_evidenced"],
            "expected_outputs": ["code_changes", "trace_summary"],
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("handoff-packet", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)

    def test_trace_summary_rejects_success_with_failure_type(self) -> None:
        payload = {
            "trace_id": "T-2026-03-06-001",
            "run_id": "RUN-2026-03-06-A",
            "seq": 2,
            "packet_id": "H-2026-03-06-001",
            "slice_id": "MVP-TS-INSERT",
            "agent_role": "impl",
            "attempt_index": 1,
            "execution_state": "done",
            "result": "success",
            "failure_type": "contract",
            "started_at": "2026-03-06T10:00:00+09:00",
            "ended_at": "2026-03-06T10:24:00+09:00",
            "summary": "요약",
            "artifacts_used": ["docs/product/mvp-spec.md:61"],
            "changes": ["apps/web/src/example.ts"],
            "tests_run": [{"command": "pnpm test -- example", "result": "passed"}],
            "requested_decision": "accept",
            "next_action": "integration 검토",
            "decision_rationale": "왜 accept 인지",
            "context_notes": ["상세 맥락"],
            "confidence": "high",
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("trace-summary", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)

    def test_operator_decision_requires_next_packet_for_rework(self) -> None:
        payload = {
            "decision_id": "D-2026-03-06-001",
            "run_id": "RUN-2026-03-06-A",
            "seq": 3,
            "slice_id": "MVP-TS-INSERT",
            "packet_id": "H-2026-03-06-001",
            "reviewed_trace_ids": ["T-2026-03-06-001"],
            "made_at": "2026-03-06T10:30:00+09:00",
            "operator_actor": "operator",
            "decision": "rework",
            "review_summary": "재작업 필요",
            "reason_code": "bad_handoff",
            "reason_detail": "입력 부족",
            "slice_state_before": "active",
            "slice_state_after": "active",
            "packet_disposition_before": "active",
            "packet_disposition_after": "superseded",
            "updated_current_ledger_ref": "context/wbs/runs/RUN-2026-03-06-A/current.run-ledger.json",
            "snapshot_ref": "context/wbs/runs/RUN-2026-03-06-A/snapshots/0003.rework.run-ledger.json",
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("operator-decision", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)

    def test_run_ledger_rejects_snapshot_without_source_decision(self) -> None:
        payload = {
            "run_id": "RUN-2026-03-06-A",
            "ledger_kind": "snapshot",
            "projection_seq": 3,
            "parent_wbs": "mvp-wbs/v1",
            "updated_at": "2026-03-06T12:30:00+09:00",
            "slice_entries": [
                {
                    "slice_id": "MVP-TS-INSERT",
                    "slice_state": "active",
                    "current_owner": "operator",
                    "active_packet_id": "H-2026-03-06-001",
                    "active_packet_disposition": "superseded",
                    "latest_trace_id": "T-2026-03-06-001",
                    "latest_execution_state": "review_required",
                    "latest_result": "partial",
                    "recent_failure_type": "orchestration",
                    "latest_decision_id": "D-2026-03-06-001",
                    "latest_decision": "rework",
                    "latest_decision_at": "2026-03-06T12:20:00+09:00",
                    "next_operator_decision": "dispatch",
                    "open_feedback": [],
                    "packet_history": [
                        {
                            "packet_id": "H-2026-03-06-001",
                            "disposition": "superseded",
                            "trace_count": 1,
                            "latest_trace_id": "T-2026-03-06-001",
                            "latest_result": "partial"
                        }
                    ],
                    "updated_at": "2026-03-06T12:30:00+09:00"
                }
            ]
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("run-ledger", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)

    def test_run_ledger_rejects_recent_trace_refs_longer_than_trace_count(self) -> None:
        payload = {
            "run_id": "RUN-2026-03-06-A",
            "ledger_kind": "current",
            "projection_seq": 6,
            "parent_wbs": "mvp-wbs/v1",
            "updated_at": "2026-03-06T12:30:00+09:00",
            "slice_entries": [
                {
                    "slice_id": "MVP-TS-INSERT",
                    "slice_state": "active",
                    "current_owner": "operator",
                    "active_packet_id": "H-2026-03-06-002",
                    "active_packet_disposition": "active",
                    "latest_trace_id": "T-2026-03-06-002",
                    "latest_execution_state": "review_required",
                    "latest_result": "success",
                    "recent_failure_type": "none",
                    "latest_decision_id": "D-2026-03-06-002",
                    "latest_decision": "accept",
                    "latest_decision_at": "2026-03-06T12:30:00+09:00",
                    "next_operator_decision": "dispatch",
                    "open_feedback": [],
                    "packet_history": [
                        {
                            "packet_id": "H-2026-03-06-002",
                            "disposition": "active",
                            "trace_count": 1,
                            "latest_trace_id": "T-2026-03-06-002",
                            "latest_result": "success",
                            "recent_trace_refs": ["T-2026-03-06-001", "T-2026-03-06-002"]
                        }
                    ],
                    "updated_at": "2026-03-06T12:30:00+09:00"
                }
            ]
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("run-ledger", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)


if __name__ == "__main__":
    unittest.main()
