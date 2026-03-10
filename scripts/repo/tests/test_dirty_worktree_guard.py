from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dirty_worktree_guard  # noqa: E402


class DirtyWorktreeGuardTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        root = Path(temp_dir.name)
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)

        tracked = root / "tracked.txt"
        tracked.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
        subprocess.run(
            ["git", "commit", "-m", "base commit"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        return root

    def test_summarize_counts_each_dirty_class(self) -> None:
        delta = dirty_worktree_guard.summarize(["M  staged.txt", " M unstaged.txt", "?? untracked.txt"])
        self.assertEqual(delta.staged, 1)
        self.assertEqual(delta.unstaged, 1)
        self.assertEqual(delta.untracked, 1)

    def test_validate_clean_worktree_passes_on_clean_repo(self) -> None:
        root = self.make_repo()
        previous = Path.cwd()
        try:
            subprocess.run(["git", "status", "--porcelain"], cwd=root, check=True, capture_output=True)
            os_chdir(root)
            delta = dirty_worktree_guard.validate_clean_worktree()
        finally:
            os_chdir(previous)
        self.assertEqual(delta.total, 0)

    def test_validate_clean_worktree_rejects_untracked_file(self) -> None:
        root = self.make_repo()
        (root / "extra.txt").write_text("new\n", encoding="utf-8")

        previous = Path.cwd()
        try:
            os_chdir(root)
            with self.assertRaises(dirty_worktree_guard.DirtyWorktreeError) as ctx:
                dirty_worktree_guard.validate_clean_worktree()
        finally:
            os_chdir(previous)

        self.assertIn("untracked=1", str(ctx.exception))

    def test_validate_clean_worktree_rejects_unstaged_change(self) -> None:
        root = self.make_repo()
        (root / "tracked.txt").write_text("changed\n", encoding="utf-8")

        previous = Path.cwd()
        try:
            os_chdir(root)
            with self.assertRaises(dirty_worktree_guard.DirtyWorktreeError) as ctx:
                dirty_worktree_guard.validate_clean_worktree()
        finally:
            os_chdir(previous)

        self.assertIn("unstaged=1", str(ctx.exception))

    def test_validate_clean_worktree_rejects_staged_change(self) -> None:
        root = self.make_repo()
        (root / "tracked.txt").write_text("changed\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)

        previous = Path.cwd()
        try:
            os_chdir(root)
            with self.assertRaises(dirty_worktree_guard.DirtyWorktreeError) as ctx:
                dirty_worktree_guard.validate_clean_worktree()
        finally:
            os_chdir(previous)

        self.assertIn("staged=1", str(ctx.exception))


def os_chdir(path: Path) -> None:
    import os

    os.chdir(path)


if __name__ == "__main__":
    unittest.main()
