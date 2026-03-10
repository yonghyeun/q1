from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pr_body_quality_guard as guard  # noqa: E402


PR_BODY_VALID = """## Summary
- 이 PR의 목적과 결과를 요약한다.

## Primary Issue
- Primary issue 링크는 전용 gate에서 검증한다.

## Related Issues
- Related: #2

## Context
- stale gate 제거 이후 fresh policy 기준으로 PR 흐름을 재정렬한다.

## Changes
- PR 템플릿 갱신
- PR 생성 경로 정합성 점검

## Decisions Made
- Decision:
  - Rationale: PR 본문을 remote review ledger로 사용한다.
  - Reference: context/decisions/2026-03-09_agent-document-taxonomy.md

## Deferred / Not Included
- CI gate 재생성은 이번 PR에 포함하지 않는다.

## Validation Notes
- dry-run 기준 생성 명령과 본문 검증 흐름 확인.

## Risks
- Impact: PR 생성 경로
- Residual risk: 후속 gate 재설계 전까지 원격 검증은 제한적이다.
- Rollback note: 템플릿과 스크립트 참조를 이전 버전으로 되돌리면 된다.

## Reviewer Focus
- Primary Issue와 Decisions Made 섹션 구조가 적절한지 확인.
"""


class PrBodyQualityGuardTests(unittest.TestCase):
    def test_validate_pr_body_success(self) -> None:
        guard.validate_pr_body(PR_BODY_VALID)

    def test_validate_pr_body_rejects_primary_issue_placeholder(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_pr_body(
                PR_BODY_VALID.replace(
                    "- Primary issue 링크는 전용 gate에서 검증한다.",
                    "Closes #<issue-number>",
                )
            )

    def test_validate_pr_body_requires_primary_issue_content(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_pr_body(
                PR_BODY_VALID.replace("- Primary issue 링크는 전용 gate에서 검증한다.", "- ")
            )

    def test_validate_pr_body_requires_related_issues_content(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_pr_body(PR_BODY_VALID.replace("- Related: #2", "- "))


if __name__ == "__main__":
    unittest.main()
