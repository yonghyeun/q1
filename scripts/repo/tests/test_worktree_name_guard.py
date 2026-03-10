from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import worktree_name_guard  # noqa: E402


class WorktreeNameGuardTests(unittest.TestCase):
    def test_validate_worktree_name_success(self) -> None:
        meta = worktree_name_guard.validate_worktree_name(
            "signup-flow--impl",
            "feature/signup-flow",
        )
        self.assertEqual(meta.purpose, "impl")
        self.assertEqual(meta.slug, "signup-flow")

    def test_validate_worktree_name_rejects_invalid_format(self) -> None:
        with self.assertRaises(worktree_name_guard.WorktreeNameError):
            worktree_name_guard.validate_worktree_name(
                "signup-flow_impl",
                "feature/signup-flow",
            )

    def test_validate_worktree_name_rejects_unknown_purpose(self) -> None:
        with self.assertRaises(worktree_name_guard.WorktreeNameError):
            worktree_name_guard.validate_worktree_name(
                "signup-flow--qa",
                "feature/signup-flow",
            )

    def test_validate_worktree_name_rejects_branch_slug_mismatch(self) -> None:
        with self.assertRaises(worktree_name_guard.WorktreeNameError):
            worktree_name_guard.validate_worktree_name(
                "signup-flow--impl",
                "feature/login-flow",
            )

    def test_branch_slug_requires_scoped_branch(self) -> None:
        with self.assertRaises(worktree_name_guard.WorktreeNameError):
            worktree_name_guard.branch_slug("main")


if __name__ == "__main__":
    unittest.main()
