from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SUMMARY_SCRIPT = ROOT_DIR / ".codex/skills/git-task-end/scripts/pr_summary.py"


class GitTaskEndPrSummaryTests(unittest.TestCase):
    def make_env(self, *, body: str, state: str = "MERGED", merged_at: str = "2026-03-13T10:00:00Z") -> dict[str, str]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        workspace = Path(temp_dir.name)
        bin_dir = workspace / "bin"
        bin_dir.mkdir()
        gh_script = bin_dir / "gh"
        gh_script.write_text(
            """#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys

args = sys.argv[1:]
if args[:2] != ["pr", "view"]:
    print(f"unexpected gh args: {' '.join(args)}", file=sys.stderr)
    raise SystemExit(1)

payload = {
    "number": 42,
    "title": os.environ["FAKE_PR_TITLE"],
    "body": os.environ["FAKE_PR_BODY"],
    "url": "https://example.test/pull/42",
    "state": os.environ["FAKE_PR_STATE"],
    "mergedAt": os.environ["FAKE_PR_MERGED_AT"],
    "baseRefName": "main",
    "headRefName": "chore/task-end-pr-summary-flow",
}
print(json.dumps(payload))
""",
            encoding="utf-8",
        )
        gh_script.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        env["FAKE_PR_TITLE"] = "[chore] task end 후 PR 요약 출력 흐름 정리"
        env["FAKE_PR_BODY"] = body
        env["FAKE_PR_STATE"] = state
        env["FAKE_PR_MERGED_AT"] = merged_at
        return env

    def run_script(self, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SUMMARY_SCRIPT), *args],
            cwd=ROOT_DIR,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_renders_structured_summary_from_pr_body(self) -> None:
        env = self.make_env(
            body="""## Summary
- task end 종료 직후 merged PR 요약을 바로 출력한다.
- 종료 맥락 복기를 빠르게 만든다.

## Primary Issue
Closes #49

## Related Issues
- Related: #48

## Context
- core wrapper는 merge/cleanup에 집중한다.

## Changes
- skill apply 이후 gh pr view 로 merged PR 최신 상태를 다시 읽는다.
- PR 본문에서 요약 섹션을 추출해 handoff용 텍스트를 만든다.

## Decisions Made
- Decision:
  - Chosen: skill 레이어에 summary 책임을 둔다.

## Deferred / Not Included
- core wrapper 책임 확장은 제외한다.

## Validation Notes
- task end apply 후 즉시 summary helper를 호출한다.

## Risks
- Impact: 종료 직후 사용자 handoff 품질에 영향을 준다.
- Residual risk: PR body가 약하면 fallback 품질이 제한된다.

## Reviewer Focus
- 변경 목적, 핵심 변경점, 후속 확인 포인트가 모두 드러나는지 확인.
""",
        )
        result = self.run_script(env, "--pr", "42", "--linked-issue-number", "49", "--linked-issue-title", "task end 후 PR 요약 출력 흐름 정리")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[git-task-end] Merged PR summary", result.stdout)
        self.assertIn("변경 목적: task end 종료 직후 merged PR 요약을 바로 출력한다.", result.stdout)
        self.assertIn("핵심 변경점:", result.stdout)
        self.assertIn("skill apply 이후 gh pr view 로 merged PR 최신 상태를 다시 읽는다.", result.stdout)
        self.assertIn("영향 범위:", result.stdout)
        self.assertIn("Impact: 종료 직후 사용자 handoff 품질에 영향을 준다.", result.stdout)
        self.assertIn("후속 확인 포인트:", result.stdout)
        self.assertIn("변경 목적, 핵심 변경점, 후속 확인 포인트가 모두 드러나는지 확인.", result.stdout)

    def test_falls_back_when_pr_body_is_sparse(self) -> None:
        env = self.make_env(body="")
        result = self.run_script(env, "--pr", "42", "--linked-issue-number", "49", "--linked-issue-title", "task end 후 PR 요약 출력 흐름 정리")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("변경 목적: task end 후 PR 요약 출력 흐름 정리 해결 흐름 정리 (issue #49)", result.stdout)
        self.assertIn("PR 제목 기준 fallback: task end 후 PR 요약 출력 흐름 정리", result.stdout)
        self.assertIn("chore/task-end-pr-summary-flow 변경이 main 에 반영됨", result.stdout)
        self.assertIn("linked issue #49 종료 상태와 후속 커뮤니케이션 확인", result.stdout)


if __name__ == "__main__":
    unittest.main()
