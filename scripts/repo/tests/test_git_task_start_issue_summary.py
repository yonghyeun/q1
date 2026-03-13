from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT_DIR / ".codex/skills/git-task-start/scripts/issue_summary.py"


class GitTaskStartIssueSummaryTests(unittest.TestCase):
    def run_script(self, payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(payload, handle, ensure_ascii=False)
            handle.flush()
            path = handle.name

        self.addCleanup(lambda: Path(path).unlink(missing_ok=True))
        return subprocess.run(
            ["python3", str(SCRIPT_PATH), "--json-file", path],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_renders_section_based_summary(self) -> None:
        payload = {
            "number": 48,
            "title": "[chore] task start 후 issue 요약 출력 흐름 정리",
            "labels": [
                {"name": "status:active"},
                {"name": "priority:p2"},
                {"name": "area:repo"},
            ],
            "body": """## Summary
`git-task-start`로 issue 기반 task start를 수행한 직후, 새 worktree로 이동한 뒤 읽은 issue 내용을 간단히 요약해 출력하는 흐름을 정리한다.

## Goal
- `git-task-start` skill에 apply 후 후속 단계로 issue 읽기 및 요약 출력을 추가한다.
- 요약 출력은 최소한 목적, 완료 조건, 제약/주의사항, 첫 작업 후보를 포함한다.

## Affected Surface
- `.codex/skills/git-task-start/SKILL.md`
- repo wrapper orchestration around task start output expectations

## Constraints
- core wrapper의 책임 범위를 불필요하게 확장하지 않는다.
- issue body가 비어 있거나 정보가 부족한 경우 title/labels/checklist 기반 fallback이 필요하다.

## Done Signal
- issue 기반 `task start` apply 이후 새 worktree path를 기준으로 issue 요약이 바로 출력된다.
- 출력에 목적, 완료 조건, 제약/주의사항, 첫 작업 후보가 포함된다.
""",
        }

        result = self.run_script(payload)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Issue Summary", result.stdout)
        self.assertIn("- 이슈: #48 [chore] task start 후 issue 요약 출력 흐름 정리", result.stdout)
        self.assertIn("- 목적: git-task-start skill에 apply 후 후속 단계로 issue 읽기 및 요약 출력을 추가한다.", result.stdout)
        self.assertIn("issue 기반 task start apply 이후 새 worktree path를 기준으로 issue 요약이 바로 출력된다.", result.stdout)
        self.assertIn("core wrapper의 책임 범위를 불필요하게 확장하지 않는다.", result.stdout)
        self.assertIn("fallback 정의: issue body 부족 시 title/labels/checklist 기반 요약", result.stdout)

    def test_falls_back_to_title_and_labels_when_body_is_sparse(self) -> None:
        payload = {
            "number": 7,
            "title": "[fix] token refresh race",
            "labels": [
                {"name": "status:ready"},
                {"name": "priority:p1"},
                {"name": "area:repo"},
            ],
            "body": "",
        }

        result = self.run_script(payload)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("- 목적: token refresh race", result.stdout)
        self.assertIn("- 완료 조건: token refresh race 기준으로 완료 조건 재확인 필요.", result.stdout)
        self.assertIn("라벨: status:ready, priority:p1, area:repo", result.stdout)
        self.assertIn("- 첫 작업 후보: 이슈 재확인: token refresh race", result.stdout)


if __name__ == "__main__":
    unittest.main()
