# Issue Convention

## 목적
- issue 제목과 본문에 포함되어야 할 최소 정보를 정의.
- issue를 작업 입력 문서로 일관되게 유지.

## 제목 규칙
- 권장 형식: `[type] 요약`
- 허용 type: `feature|bug|chore`
- 예:
  - `[feature] PR remote review ledger 구조 정리`
  - `[bug] PR body guard가 최신 템플릿을 통과하지 못함`
  - `[chore] issue/pr 생성 스크립트 정합성 정리`

## 본문 규칙
- issue type별 GitHub 템플릿을 따른다.
- 관련 이슈는 `Related Issues` 섹션에 기록.
- 작업 전 쟁점은 `Decision Candidates` 섹션에 기록.
- 범위 경계는 `In Scope`, `Out of Scope`에서 명시.

## 템플릿
- feature: `.github/ISSUE_TEMPLATE/feature.md`
- bug: `.github/ISSUE_TEMPLATE/bug.md`
- chore: `.github/ISSUE_TEMPLATE/chore.md`

## Gate
- 제목 가드: `scripts/repo/issue_title_guard.sh`
- 본문 가드: `scripts/repo/issue_body_quality_guard.py`

## 예외 정책
- 예외 운영이 발생하면 `Context` 또는 `Notes`에서 이유를 명시.
