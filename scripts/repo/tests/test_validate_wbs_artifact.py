from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_wbs_artifact  # noqa: E402


class ValidateWbsArtifactTests(unittest.TestCase):
    def test_valid_handoff_packet_passes(self) -> None:
        payload = {
            "packet_id": "H-2026-03-06-001",
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

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "artifact.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            data = validate_wbs_artifact.load_json(path)
            validate_wbs_artifact.validate_against_schema("handoff-packet", data)
            validate_wbs_artifact.validate_semantics("handoff-packet", data)

    def test_handoff_packet_rejects_same_sender_and_receiver(self) -> None:
        payload = {
            "packet_id": "H-2026-03-06-001",
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
            "packet_id": "H-2026-03-06-001",
            "agent_role": "impl",
            "execution_state": "done",
            "result": "success",
            "failure_type": "contract",
            "started_at": "2026-03-06T10:00:00+09:00",
            "ended_at": "2026-03-06T10:24:00+09:00",
            "changes": ["apps/web/src/example.ts"],
            "tests_run": ["pnpm test -- example"],
            "requested_decision": "accept",
            "next_action": "integration 검토",
            "confidence": "high",
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("trace-summary", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)

    def test_run_ledger_rejects_duplicate_slice_ids(self) -> None:
        payload = {
            "run_id": "RUN-2026-03-06-A",
            "parent_wbs": "mvp-wbs/v1",
            "updated_at": "2026-03-06T12:30:00+09:00",
            "slice_entries": [
                {
                    "slice_id": "MVP-TS-INSERT",
                    "slice_state": "active",
                    "current_owner": "impl",
                    "active_packet_id": "H-2026-03-06-001",
                    "active_packet_disposition": "active",
                    "latest_trace_id": "T-2026-03-06-001",
                    "latest_execution_state": "review_required",
                    "latest_result": "partial",
                    "recent_failure_type": "orchestration",
                    "next_operator_decision": "rework",
                    "open_feedback": [],
                    "packet_history": [{"packet_id": "H-2026-03-06-001", "disposition": "active"}],
                    "updated_at": "2026-03-06T12:30:00+09:00",
                },
                {
                    "slice_id": "MVP-TS-INSERT",
                    "slice_state": "active",
                    "current_owner": "impl",
                    "active_packet_id": "H-2026-03-06-002",
                    "active_packet_disposition": "active",
                    "latest_trace_id": "T-2026-03-06-002",
                    "latest_execution_state": "review_required",
                    "latest_result": "partial",
                    "recent_failure_type": "orchestration",
                    "next_operator_decision": "rework",
                    "open_feedback": [],
                    "packet_history": [{"packet_id": "H-2026-03-06-002", "disposition": "active"}],
                    "updated_at": "2026-03-06T12:30:00+09:00",
                },
            ],
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("run-ledger", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)

    def test_run_ledger_rejects_done_slice_without_close_decision(self) -> None:
        payload = {
            "run_id": "RUN-2026-03-06-A",
            "parent_wbs": "mvp-wbs/v1",
            "updated_at": "2026-03-06T12:30:00+09:00",
            "slice_entries": [
                {
                    "slice_id": "MVP-TS-INSERT",
                    "slice_state": "done",
                    "current_owner": "operator",
                    "active_packet_id": "H-2026-03-06-001",
                    "active_packet_disposition": "closed",
                    "latest_trace_id": "T-2026-03-06-001",
                    "latest_execution_state": "done",
                    "latest_result": "success",
                    "recent_failure_type": "none",
                    "next_operator_decision": "accept",
                    "open_feedback": [],
                    "packet_history": [{"packet_id": "H-2026-03-06-001", "disposition": "closed"}],
                    "updated_at": "2026-03-06T12:30:00+09:00",
                }
            ],
        }

        with self.assertRaises(validate_wbs_artifact.WbsArtifactError) as ctx:
            validate_wbs_artifact.validate_semantics("run-ledger", payload)
        self.assertEqual(ctx.exception.exit_code, validate_wbs_artifact.EXIT_SEMANTIC_VIOLATION)


if __name__ == "__main__":
    unittest.main()
