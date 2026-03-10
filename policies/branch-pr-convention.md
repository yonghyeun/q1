# PR Convention

## 목적
- PR 생성과 merge 흐름을 일관되게 유지.
- PR 제목과 본문에 포함되어야 할 최소 정보를 정의.

## 표준 흐름
1. 변경 구현 및 검증.
2. PR 제목 작성.
3. PR 본문 작성.
4. PR 생성.
5. Merge 후 head branch 정리.

## 대상 브랜치
- 기본 대상 브랜치: `main`.
- 다른 대상 브랜치가 필요하면 PR 본문에 이유를 명시.

## PR 제목 규칙
- 제목은 작업 범위와 목적이 드러나야 함.
- 권장 형식: `[scope] 요약`
- 예: `[config] codex routing cleanup`

## PR 본문 규칙
- close keyword 포함 필요.
- 허용 형식: `Closes #1234`, `Fixes #1234`, `Resolves #1234`
- 현재 PR이 직접 닫는 primary issue를 명시.
- 현재 작업과 연관된 related issue도 별도 섹션에서 링크.
- 작업 목적 명시 필요.
- 변경 범위만이 아니라 merge 후 기대되는 운영 효과와 workflow 변화가 드러나야 함.
- `Changes` 섹션은 파일 목록보다 기대 효과, 동작 변화, 새로 가능해진 경로를 우선 설명.
- 작업 중 확정한 결정 사항 요약 필요.
- `Decisions Made`에는 결론뿐 아니라 그 결정을 하게 된 배경, 버린 대안, 선택 근거를 함께 남김.
- 검증 방법 명시 필요.

## 권장 본문 구조
- Summary
- Primary Issue
- Related Issues
- Context
- Changes
- Decisions Made
- Deferred / Not Included
- Validation Notes
- Risks

## 섹션 작성 원칙
- `Summary`: 리뷰어가 이 PR의 존재 이유를 30초 안에 이해할 수 있어야 함.
- `Context`: 기존 운영 흐름의 문제, 제약, 이번 정리의 필요 조건을 설명.
- `Changes`: 구현 목록보다 기대 효과와 운영 모델 변화를 먼저 설명.
- `Decisions Made`: decision 자체보다 decision을 유발한 맥락과 대안 비교를 먼저 설명.

## PR 템플릿
- 기본 PR 템플릿은 `.github/pull_request_template.md`를 따른다.
- PR 본문은 remote review ledger 역할을 수행한다.
- 장기 SoT가 필요한 결정은 `context/decisions/` 문서로 분리하고 PR에서는 요약과 링크만 유지.
- 별도 reference 섹션은 강제하지 않고, 필요한 링크는 해당 섹션 안에 inline으로 둔다.

## 예외 정책
- 예외 운영이 발생하면 PR 본문에 이유와 후속 조치를 기록.

## 관련 문서
- 브랜치 이름 규칙: `policies/branch-naming.md`
- 커밋 규칙: `policies/commit-convention.md`
