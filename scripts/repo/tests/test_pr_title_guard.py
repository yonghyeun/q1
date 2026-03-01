from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "pr_title_guard.sh"


class PrTitleGuardTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_generate_success(self) -> None:
        result = self.run_script(
            "generate",
            "--task-id",
            "T-0001",
            "--summary",
            "브랜치 거버넌스 정비",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[T-0001] 브랜치 거버넌스 정비")

    def test_generate_rejects_invalid_task_id(self) -> None:
        result = self.run_script(
            "generate",
            "--task-id",
            "T-1",
            "--summary",
            "요약",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("task-id 형식", result.stderr)

    def test_validate_success_with_branch(self) -> None:
        result = self.run_script(
            "validate",
            "--title",
            "[T-0007] PR 제목 예시",
            "--branch",
            "task/i22-T-0007-title-check",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("컨벤션 통과", result.stdout)

    def test_validate_rejects_invalid_title_format(self) -> None:
        result = self.run_script(
            "validate",
            "--title",
            "T-0007 PR 제목 예시",
            "--branch",
            "task/i22-T-0007-title-check",
        )
        self.assertEqual(result.returncode, 10)
        self.assertIn("허용 형식", result.stderr)

    def test_validate_rejects_task_id_mismatch(self) -> None:
        result = self.run_script(
            "validate",
            "--title",
            "[T-0008] PR 제목 예시",
            "--branch",
            "task/i22-T-0007-title-check",
        )
        self.assertEqual(result.returncode, 12)
        self.assertIn("다릅니다", result.stderr)


if __name__ == "__main__":
    unittest.main()
