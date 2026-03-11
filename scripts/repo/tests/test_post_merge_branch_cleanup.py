from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "post_merge_branch_cleanup.sh",
    "dirty_worktree_guard.py",
]


class PostMergeBranchCleanupTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path, str]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        workspace = Path(temp_dir.name)
        root = workspace / "repo"
        root.mkdir(parents=True)
        scripts_dir = root / "scripts/repo"
        scripts_dir.mkdir(parents=True)

        for script_name in SCRIPT_NAMES:
            source = ROOT_DIR / "scripts/repo" / script_name
            target = scripts_dir / script_name
            shutil.copy2(source, target)
            target.chmod(0o755)

        origin = workspace / "origin.git"
        subprocess.run(["git", "init", "--bare", str(origin)], check=True, capture_output=True)

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(origin)], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=root, check=True, capture_output=True)

        branch = "feature/cleanup-flow"
        subprocess.run(["git", "switch", "-c", branch], cwd=root, check=True, capture_output=True)
        return root, scripts_dir / "post_merge_branch_cleanup.sh", branch

    def run_script(self, root: Path, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", f"./scripts/repo/{script.name}", *args],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_prints_cleanup_plan(self) -> None:
        root, script, branch = self.make_repo()
        result = self.run_script(root, script, "--branch", branch, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("switch to main", result.stdout)
        self.assertIn(f"git branch -d {branch}", result.stdout)

    def test_actual_cleanup_switches_to_main_and_deletes_branch(self) -> None:
        root, script, branch = self.make_repo()
        result = self.run_script(root, script, "--branch", branch)
        self.assertEqual(result.returncode, 0, result.stderr)

        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(current_branch, "main")

        branches = subprocess.run(
            ["git", "branch", "--list", branch],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(branches, "")

    def test_dry_run_reports_linked_worktree_cleanup_precondition(self) -> None:
        root, script, branch = self.make_repo()
        subprocess.run(["git", "switch", "main"], cwd=root, check=True, capture_output=True)
        linked = root.parent / "cleanup-linked--impl"
        subprocess.run(["git", "worktree", "add", str(linked), branch], cwd=root, check=True, capture_output=True)
        self.addCleanup(lambda: shutil.rmtree(linked, ignore_errors=True))

        result = self.run_script(root, script, "--branch", branch, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("remove linked worktree first", result.stdout)
        self.assertIn(str(linked), result.stdout)

    def test_actual_cleanup_fails_when_branch_is_still_in_linked_worktree(self) -> None:
        root, script, branch = self.make_repo()
        subprocess.run(["git", "switch", "main"], cwd=root, check=True, capture_output=True)
        linked = root.parent / "cleanup-linked--impl"
        subprocess.run(["git", "worktree", "add", str(linked), branch], cwd=root, check=True, capture_output=True)
        self.addCleanup(lambda: shutil.rmtree(linked, ignore_errors=True))

        result = self.run_script(root, script, "--branch", branch)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("linked worktree", result.stderr)
        self.assertIn("worktree cleanup을 먼저", result.stderr)


if __name__ == "__main__":
    unittest.main()
