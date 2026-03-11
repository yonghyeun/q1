from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "worktree_config_bootstrap.sh",
    "worktree_pr_metadata.sh",
]


class WorktreePrMetadataTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path]:
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

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)

        worktree = workspace / "config-pr-number-metadata--impl"
        subprocess.run(
            ["git", "worktree", "add", str(worktree), "-b", "config/pr-number-metadata", "main"],
            cwd=root,
            check=True,
            capture_output=True,
        )

        return root, worktree

    def run_script(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/worktree_pr_metadata.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_write_persists_pr_metadata(self) -> None:
        _root, worktree = self.make_repo()
        result = self.run_script(
            worktree,
            "write",
            "--number",
            "42",
            "--url",
            "https://example.test/pull/42",
            "--title",
            "pr title",
            "--state",
            "OPEN",
            "--base-branch",
            "main",
            "--head-branch",
            "config/pr-number-metadata",
            "--worktree",
            str(worktree),
            "--recorded-at",
            "2026-03-11T15:00:00+09:00",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("기록 완료", result.stdout)

        read_result = self.run_script(worktree, "read")
        self.assertEqual(read_result.returncode, 0, read_result.stderr)
        self.assertIn("q1.pr.number=42", read_result.stdout)
        self.assertIn("q1.pr.title=pr title", read_result.stdout)
        self.assertIn("q1.pr.recordedBy=pr_create", read_result.stdout)

    def test_write_bootstraps_worktree_config(self) -> None:
        root, worktree = self.make_repo()
        result = self.run_script(
            worktree,
            "write",
            "--number",
            "42",
            "--url",
            "https://example.test/pull/42",
            "--head-branch",
            "config/pr-number-metadata",
            "--worktree",
            str(worktree),
            "--recorded-at",
            "2026-03-11T15:00:00+09:00",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        bootstrap_value = subprocess.run(
            ["git", "config", "--get", "--bool", "extensions.worktreeConfig"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(bootstrap_value, "true")

    def test_read_is_empty_before_write(self) -> None:
        _root, worktree = self.make_repo()
        result = self.run_script(worktree, "read")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_clear_removes_pr_metadata(self) -> None:
        _root, worktree = self.make_repo()
        write_result = self.run_script(
            worktree,
            "write",
            "--number",
            "42",
            "--url",
            "https://example.test/pull/42",
            "--head-branch",
            "config/pr-number-metadata",
            "--worktree",
            str(worktree),
            "--recorded-at",
            "2026-03-11T15:00:00+09:00",
        )
        self.assertEqual(write_result.returncode, 0, write_result.stderr)

        clear_result = self.run_script(worktree, "clear")
        self.assertEqual(clear_result.returncode, 0, clear_result.stderr)
        self.assertIn("정리 완료", clear_result.stdout)

        read_result = self.run_script(worktree, "read")
        self.assertEqual(read_result.returncode, 0, read_result.stderr)
        self.assertEqual(read_result.stdout.strip(), "")

    def test_clear_is_noop_when_backend_not_bootstrapped(self) -> None:
        _root, worktree = self.make_repo()
        result = self.run_script(worktree, "clear")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no-op", result.stdout)


if __name__ == "__main__":
    unittest.main()
