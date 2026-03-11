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

## Operational Problem
- issue 입력 문서와 실행 artifact의 경계가 흐리다.

## Goal
- issue 생성 규칙을 backlog 입력 문서 기준으로 통일한다.

## Affected Surface
- repo
- github

## Constraints
- 기존 issue type 3개는 유지한다.

## Decision Candidates
- Candidate:
  - Options: input-only / input+execution
  - Notes: 입력과 실행을 분리하는 편이 backlog 관리에 유리하다.

## Done Signal
- issue 템플릿이 공통 운영 원칙과 일치한다.

## Out of Scope
- CI gate 재생성

## Related Links
- Issue: #12
"""


class IssueBodyQualityGuardTests(unittest.TestCase):
    def test_validate_issue_body_success(self) -> None:
        guard.validate_issue_body(CHORE_ISSUE_BODY_VALID, "chore")

    def test_validate_issue_body_rejects_related_links_placeholder(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_issue_body(CHORE_ISSUE_BODY_VALID.replace("- Issue: #12", "- Related: #"), "chore")

    def test_validate_issue_body_requires_context(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_issue_body(CHORE_ISSUE_BODY_VALID.replace("- stale governance 잔재를 제거한 이후 현재 규칙 구조를 다시 정리할 필요가 있다.", "- "), "chore")


if __name__ == "__main__":
    unittest.main()
