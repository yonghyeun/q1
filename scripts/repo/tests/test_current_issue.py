from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "worktree_config_bootstrap.sh",
    "worktree_issue_metadata.sh",
    "current_issue.sh",
]


class CurrentIssueTests(unittest.TestCase):
    def make_repo(self) -> Path:
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

        worktree = workspace / "feature-test--impl"
        subprocess.run(["git", "worktree", "add", str(worktree), "-b", "feature/test", "main"], cwd=root, check=True, capture_output=True)

        return worktree

    def run_script(self, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/current_issue.sh"],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_prints_empty_message_when_metadata_missing(self) -> None:
        worktree = self.make_repo()
        result = self.run_script(worktree)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("연결된 issue 없음", result.stdout)

    def test_prints_current_issue_from_metadata(self) -> None:
        worktree = self.make_repo()
        write_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_issue_metadata.sh",
                "write",
                "--number",
                "19",
                "--url",
                "https://example.test/issues/19",
                "--title",
                "issue title",
                "--status-at-record",
                "status:active",
                "--branch",
                "config/local-issue-linkage",
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(write_result.returncode, 0, write_result.stderr)

        result = self.run_script(worktree)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("- 번호: #19", result.stdout)
        self.assertIn("- 제목: issue title", result.stdout)
        self.assertIn("- 기록 상태: status:active", result.stdout)


if __name__ == "__main__":
    unittest.main()
