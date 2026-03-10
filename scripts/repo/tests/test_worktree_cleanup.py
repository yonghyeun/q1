from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]


class WorktreeCleanupTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path, Path, str]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        workspace = Path(temp_dir.name)
        root = workspace / "repo"
        root.mkdir(parents=True)
        scripts_dir = root / "scripts/repo"
        scripts_dir.mkdir(parents=True)

        source = ROOT_DIR / "scripts/repo" / "worktree_cleanup.sh"
        target = scripts_dir / "worktree_cleanup.sh"
        shutil.copy2(source, target)
        target.chmod(0o755)

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)

        branch = "feature/worktree-cleanup"
        subprocess.run(["git", "branch", branch], cwd=root, check=True, capture_output=True)

        worktree = workspace / "feature-worktree-cleanup--impl"
        subprocess.run(["git", "worktree", "add", str(worktree), branch], cwd=root, check=True, capture_output=True)
        return root, target, worktree, branch

    def run_script(self, cwd: Path, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", f"./scripts/repo/{script.name}", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_reports_remove_plan(self) -> None:
        root, script, worktree, branch = self.make_repo()
        result = self.run_script(
            root,
            script,
            "--worktree",
            str(worktree),
            "--expected-branch",
            branch,
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("git worktree remove", result.stdout)
        self.assertIn(branch, result.stdout)

    def test_rejects_current_active_worktree(self) -> None:
        _root, script, worktree, branch = self.make_repo()
        result = self.run_script(
            worktree,
            script,
            "--worktree",
            str(worktree),
            "--expected-branch",
            branch,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("현재 활성 worktree", result.stderr)

    def test_actual_cleanup_removes_linked_worktree(self) -> None:
        root, script, worktree, branch = self.make_repo()
        result = self.run_script(
            root,
            script,
            "--worktree",
            str(worktree),
            "--expected-branch",
            branch,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(worktree.exists())


if __name__ == "__main__":
    unittest.main()
