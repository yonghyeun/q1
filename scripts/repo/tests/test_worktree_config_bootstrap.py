from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]


class WorktreeConfigBootstrapTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        workspace = Path(temp_dir.name)
        root = workspace / "repo"
        root.mkdir(parents=True)
        scripts_dir = root / "scripts/repo"
        scripts_dir.mkdir(parents=True)

        source = ROOT_DIR / "scripts/repo/worktree_config_bootstrap.sh"
        target = scripts_dir / "worktree_config_bootstrap.sh"
        shutil.copy2(source, target)
        target.chmod(0o755)

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)

        worktree = workspace / "feature-test--impl"
        subprocess.run(["git", "worktree", "add", str(worktree), "-b", "feature/test", "main"], cwd=root, check=True, capture_output=True)

        return root, worktree

    def run_script(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/worktree_config_bootstrap.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_validate_fails_when_not_bootstrapped(self) -> None:
        _root, worktree = self.make_repo()
        result = self.run_script(worktree, "validate")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("extensions.worktreeConfig", result.stderr)
        self.assertIn("ensure", result.stderr)

    def test_ensure_sets_common_repo_config(self) -> None:
        root, worktree = self.make_repo()
        result = self.run_script(worktree, "ensure")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("bootstrap 완료", result.stdout)

        stored = subprocess.run(
            ["git", "config", "--get", "--bool", "extensions.worktreeConfig"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(stored, "true")

    def test_validate_passes_after_ensure(self) -> None:
        _root, worktree = self.make_repo()
        ensure_result = self.run_script(worktree, "ensure")
        self.assertEqual(ensure_result.returncode, 0, ensure_result.stderr)

        validate_result = self.run_script(worktree, "validate")
        self.assertEqual(validate_result.returncode, 0, validate_result.stderr)
        self.assertIn("bootstrap 통과", validate_result.stdout)

    def test_ensure_is_idempotent(self) -> None:
        _root, worktree = self.make_repo()
        first = self.run_script(worktree, "ensure")
        self.assertEqual(first.returncode, 0, first.stderr)

        second = self.run_script(worktree, "ensure")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("이미 활성화", second.stdout)


if __name__ == "__main__":
    unittest.main()
