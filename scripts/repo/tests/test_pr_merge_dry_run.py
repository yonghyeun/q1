from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "pr_merge.sh",
    "post_merge_cleanup.sh",
    "branch_guard.py",
    "detached_head_guard.py",
    "protected_branch_write_guard.py",
    "dirty_worktree_guard.py",
]


class PrMergeDryRunTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path, str]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        root = Path(temp_dir.name)
        scripts_dir = root / "scripts/repo"
        scripts_dir.mkdir(parents=True)

        for script_name in SCRIPT_NAMES:
            source = ROOT_DIR / "scripts/repo" / script_name
            target = scripts_dir / script_name
            shutil.copy2(source, target)
            target.chmod(0o755)

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)

        branch = "config/merge-dry-run"
        subprocess.run(["git", "switch", "-c", branch], cwd=root, check=True, capture_output=True)
        return root, scripts_dir / "pr_merge.sh", branch

    def run_script(self, root: Path, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(script), *args],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_squash_uses_placeholder_subject_when_not_set(self) -> None:
        root, script, _branch = self.make_repo()
        result = self.run_script(root, script, "--method", "squash", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--squash", result.stdout)
        self.assertIn("--subject", result.stdout)
        self.assertIn("PR_TITLE_FROM_GH", result.stdout)
        self.assertNotIn("--delete-branch", result.stdout)
        self.assertNotIn("post_merge_cleanup", result.stdout)

    def test_dry_run_squash_uses_manual_subject(self) -> None:
        root, script, _branch = self.make_repo()
        subject = "[config] squash merge 제목"
        result = self.run_script(
            root,
            script,
            "--method",
            "squash",
            "--subject",
            subject,
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--squash", result.stdout)
        self.assertIn("--subject", result.stdout)
        self.assertIn("config", result.stdout)
        self.assertIn("squash\\ merge\\ 제목", result.stdout)
        self.assertNotIn("--delete-branch", result.stdout)

    def test_dry_run_rebase_ignores_subject(self) -> None:
        root, script, _branch = self.make_repo()
        result = self.run_script(
            root,
            script,
            "--method",
            "rebase",
            "--subject",
            "ignored-subject",
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--rebase", result.stdout)
        self.assertNotIn("--subject", result.stdout)
        self.assertNotIn("--delete-branch", result.stdout)
        self.assertIn("무시", result.stderr)

    def test_rejects_invalid_method(self) -> None:
        root, script, _branch = self.make_repo()
        result = self.run_script(root, script, "--method", "invalid", "--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("squash|merge|rebase", result.stderr)


if __name__ == "__main__":
    unittest.main()
