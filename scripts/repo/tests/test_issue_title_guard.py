from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "issue_title_guard.sh"


class IssueTitleGuardTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_generate_success(self) -> None:
        result = self.run_script("generate", "--type", "feature", "--summary", "이슈 생성 경로 정리")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[feature] 이슈 생성 경로 정리", result.stdout)

    def test_validate_success(self) -> None:
        result = self.run_script("validate", "--type", "chore", "--title", "[chore] 정책 문서 정리")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validate_rejects_type_mismatch(self) -> None:
        result = self.run_script("validate", "--type", "bug", "--title", "[feature] 정책 문서 정리")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("type과 issue type이 다릅니다", result.stderr)


if __name__ == "__main__":
    unittest.main()
