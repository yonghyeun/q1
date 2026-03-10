from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import protected_branch_write_guard  # noqa: E402


class ProtectedBranchWriteGuardTests(unittest.TestCase):
    def test_validate_write_allows_feature_branch(self) -> None:
        protected_branch_write_guard.validate_protected_branch_write("feature/add-guard")

    def test_validate_write_rejects_main(self) -> None:
        with self.assertRaises(protected_branch_write_guard.ProtectedBranchWriteError) as ctx:
            protected_branch_write_guard.validate_protected_branch_write("main")
        self.assertEqual(
            ctx.exception.exit_code,
            protected_branch_write_guard.EXIT_PROTECTED_BRANCH,
        )


if __name__ == "__main__":
    unittest.main()
