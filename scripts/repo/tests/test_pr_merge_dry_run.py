from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "pr_merge.sh"
BRANCH_REGEX = re.compile(r"^(feature|fix|docs|config|chore|refactor|hotfix)/[a-z0-9]+(?:-[a-z0-9]+)*$")


class PrMergeDryRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
        ).strip()
        if not branch or branch == "main" or not BRANCH_REGEX.fullmatch(branch):
            raise unittest.SkipTest(
                "pr_merge.sh dry-run 테스트는 정책 브랜치에서만 실행합니다."
            )
        cls.branch = branch

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_squash_uses_placeholder_subject_when_not_set(self) -> None:
        result = self.run_script("--method", "squash", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--squash", result.stdout)
        self.assertIn("--subject", result.stdout)
        self.assertIn("PR_TITLE_FROM_GH", result.stdout)

    def test_dry_run_squash_uses_manual_subject(self) -> None:
        subject = "[config] squash merge 제목"
        result = self.run_script(
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

    def test_dry_run_rebase_ignores_subject(self) -> None:
        result = self.run_script(
            "--method",
            "rebase",
            "--subject",
            "ignored-subject",
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--rebase", result.stdout)
        self.assertNotIn("--subject", result.stdout)
        self.assertIn("무시", result.stderr)

    def test_rejects_invalid_method(self) -> None:
        result = self.run_script("--method", "invalid", "--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("squash|merge|rebase", result.stderr)


if __name__ == "__main__":
    unittest.main()
