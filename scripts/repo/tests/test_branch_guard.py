from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import branch_guard  # noqa: E402


RULES = {
    "policy_version": "v1.0.0",
    "default_branch": "main",
    "branch_regex": r"^task/T-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$",
    "task_id_regex": r"^T-[0-9]{4}$",
    "reserved_branches": ["main"],
    "required_context_for_push": ["agent-team/runs/{task_id}"],
    "required_artifacts_for_pr": [
        "task-brief.json",
        "trace.md",
        "run-log.md",
        "run-report.json",
    ],
}


class BranchGuardTests(unittest.TestCase):
    def test_validate_branch_name_success(self) -> None:
        task_id = branch_guard.validate_branch_name(
            "task/T-0001-branch-governance",
            RULES,
        )
        self.assertEqual(task_id, "T-0001")

    def test_validate_branch_name_rejects_reserved(self) -> None:
        with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
            branch_guard.validate_branch_name("main", RULES)
        self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)

    def test_validate_branch_name_rejects_invalid_format(self) -> None:
        with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
            branch_guard.validate_branch_name("feature/T-0001-something", RULES)
        self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)

    def test_validate_context_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "agent-team/runs/T-0001").mkdir(parents=True)
            with patch("branch_guard.repo_root", return_value=root):
                branch_guard.validate_context("T-0001", RULES)

    def test_validate_context_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with patch("branch_guard.repo_root", return_value=root):
                with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
                    branch_guard.validate_context("T-0001", RULES)
            self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_CONTEXT_MISSING)

    def test_validate_pr_artifacts_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "agent-team/runs/T-0001"
            run_dir.mkdir(parents=True)
            for artifact in RULES["required_artifacts_for_pr"]:
                (run_dir / artifact).write_text("ok", encoding="utf-8")

            with patch("branch_guard.repo_root", return_value=root):
                branch_guard.validate_pr_artifacts("T-0001", RULES)

    def test_validate_pr_artifacts_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "agent-team/runs/T-0001"
            run_dir.mkdir(parents=True)
            (run_dir / "task-brief.json").write_text("ok", encoding="utf-8")

            with patch("branch_guard.repo_root", return_value=root):
                with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
                    branch_guard.validate_pr_artifacts("T-0001", RULES)

            self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_ARTIFACT_MISSING)
            self.assertIn("run-report.json", str(ctx.exception))

    def test_load_rules_missing_required_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_path = Path(temp_dir) / "rules.json"
            broken = dict(RULES)
            del broken["task_id_regex"]
            rules_path.write_text(json.dumps(broken), encoding="utf-8")

            with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
                branch_guard.load_rules(rules_path)
            self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)


if __name__ == "__main__":
    unittest.main()
