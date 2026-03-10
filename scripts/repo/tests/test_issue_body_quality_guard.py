from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import issue_body_quality_guard as guard  # noqa: E402


CHORE_ISSUE_BODY_VALID = """## Summary
- 운영 정책 구조를 정리한다.

## Context
- stale governance 잔재를 제거한 이후 현재 규칙 구조를 다시 정리할 필요가 있다.

## Objective
- issue/PR 생성 규칙을 최신 템플릿 기준으로 통일한다.

## In Scope
- issue 생성 경로 점검

## Out of Scope
- CI gate 재생성

## Related Issues
- Related: #12

## Decision Candidates
- Candidate:
  - Options: separate guards / unified guard
  - Notes: 책임 분리 관점에서 separate guard 선호

## Operational Impact
- 운영 입력과 검증 경로가 일관된다.

## Acceptance Criteria
- [ ] issue 생성 경로가 최신 템플릿을 통과한다.

## Risks
- 스크립트 참조 경로 누락 위험 존재.
"""


class IssueBodyQualityGuardTests(unittest.TestCase):
    def test_validate_issue_body_success(self) -> None:
        guard.validate_issue_body(CHORE_ISSUE_BODY_VALID, "chore")

    def test_validate_issue_body_rejects_related_issue_placeholder(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_issue_body(CHORE_ISSUE_BODY_VALID.replace("- Related: #12", "- Related: #"), "chore")

    def test_validate_issue_body_requires_context(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_issue_body(CHORE_ISSUE_BODY_VALID.replace("- stale governance 잔재를 제거한 이후 현재 규칙 구조를 다시 정리할 필요가 있다.", "- "), "chore")


if __name__ == "__main__":
    unittest.main()
