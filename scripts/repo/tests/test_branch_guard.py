from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import branch_guard  # noqa: E402


class BranchGuardTests(unittest.TestCase):
    def test_validate_branch_name_success(self) -> None:
        meta = branch_guard.validate_branch_name("config/wbs-governance-reset")
        self.assertEqual(meta.scope, "config")

    def test_validate_branch_name_rejects_reserved(self) -> None:
        with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
            branch_guard.validate_branch_name("main")
        self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)

    def test_validate_branch_name_rejects_invalid_format(self) -> None:
        with self.assertRaises(branch_guard.BranchPolicyError) as ctx:
            branch_guard.validate_branch_name("task/i1-T-0001-old")
        self.assertEqual(ctx.exception.exit_code, branch_guard.EXIT_INVALID_NAME)


if __name__ == "__main__":
    unittest.main()
