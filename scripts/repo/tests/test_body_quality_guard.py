from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import body_quality_guard as guard  # noqa: E402


PR_BODY_VALID = """## Issue Link (Required)
Closes #1

## 목적 (Why)
- 이 변경이 필요한 이유를 구체적으로 설명한다.

## 변경 요약 (What)
- 핵심 변경 사항 1
- 핵심 변경 사항 2

## 범위
### In Scope
- 정책 검증 스크립트 반영

### Out of Scope
- 릴리즈 자동화 변경

## 영향도 / 리스크
- 영향 범위: repo 스크립트 및 운영 문서
- 잠재 리스크:
  - 템플릿 변경에 따른 불일치
- 완화 방안:
  - 가드 검증 및 테스트 실행

## 리뷰 포인트 (Reviewer Focus)
- issue 번호와 close-link 존재 여부

## 참고 링크
- 정책 문서: policies/branch-pr-convention.md
"""


ISSUE_BODY_VALID = """## WBS Link (Optional)
- WBS-01

## Objective
- 정책 기반 workflow의 실제 적용 범위를 명확히 한다.

## Scope
- issue/pr 생성 자동화 경로를 점검한다.

## Operational Impact
- 운영 일관성과 추적성이 개선된다.

## Acceptance Criteria
- [ ] 주요 검증 명령이 통과한다.

## Risks
- 템플릿 변경 시 본문 규칙이 어긋날 수 있다.
"""


class BodyQualityGuardTests(unittest.TestCase):
    def _write_temp(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "body.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_validate_pr_body_success(self) -> None:
        guard.validate_pr_body(PR_BODY_VALID)

    def test_validate_pr_body_rejects_placeholder(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_pr_body(PR_BODY_VALID.replace("Closes #1", "Closes #<issue-number>"))

    def test_validate_issue_body_success(self) -> None:
        guard.validate_issue_body(ISSUE_BODY_VALID, "chore")

    def test_validate_issue_body_rejects_placeholder(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.validate_issue_body(ISSUE_BODY_VALID.replace("WBS-01", "<wbs-id>"), "chore")

    def test_read_text_missing_file(self) -> None:
        with self.assertRaises(guard.BodyQualityError):
            guard.read_text(Path("/tmp/not-found-body-quality-guard.md"))


if __name__ == "__main__":
    unittest.main()
