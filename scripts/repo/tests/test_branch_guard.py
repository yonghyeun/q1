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
    "policy_version": "v3.0.0",
    "default_branch": "main",
    "branch_regex": r"^(feature|fix|docs|config|chore|refactor|hotfix)/[a-z0-9]+(?:-[a-z0-9]+)*$",
    "reserved_branches": ["main"],
    "required_context_for_push": [],
    "required_artifacts_for_pr": [],
}


class BranchGuardTests(unittest.TestCase):
    def test_validate_branch_name_success(self) -> None:
        meta = branch_guard.validate_branch_name(
            "config/wbs-governance-reset",
            RULES,
        )
        self.assertEqual(meta.scope, "config")

    def test_validate_branch_name_rejects_reserved(self) -> None:
        with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
            branch_guard.validate_branch_name("main", RULES)
        self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)

    def test_validate_branch_name_rejects_invalid_format(self) -> None:
        with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
            branch_guard.validate_branch_name("task/i1-T-0001-old", RULES)
        self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)

    def test_validate_context_success_empty(self) -> None:
        branch_guard.validate_context(RULES)

    def test_validate_context_missing_path(self) -> None:
        rules = dict(RULES)
        rules["required_context_for_push"] = ["context/wbs"]
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with patch("branch_guard.repo_root", return_value=root):
                with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
                    branch_guard.validate_context(rules)
            self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_CONTEXT_MISSING)

    def test_validate_pr_artifacts_success(self) -> None:
        branch_guard.validate_pr_artifacts(RULES)

    def test_validate_pr_artifacts_missing(self) -> None:
        rules = dict(RULES)
        rules["required_artifacts_for_pr"] = ["README.required.md"]
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with patch("branch_guard.repo_root", return_value=root):
                with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
                    branch_guard.validate_pr_artifacts(rules)

            self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_ARTIFACT_MISSING)
            self.assertIn("README.required.md", str(ctx.exception))

    def test_load_rules_missing_required_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_path = Path(temp_dir) / "rules.json"
            broken = dict(RULES)
            del broken["branch_regex"]
            rules_path.write_text(json.dumps(broken), encoding="utf-8")

            with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
                branch_guard.load_rules(rules_path)
            self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)


if __name__ == "__main__":
    unittest.main()
