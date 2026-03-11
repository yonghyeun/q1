# Issue Convention

## 목적
- issue 제목과 본문에 포함되어야 할 최소 정보를 정의.
- issue를 remote backlog 입력 문서로 일관되게 유지.

## 저장 위치 원칙
- 해결해야 할 backlog 항목의 기본 저장소는 GitHub issue.
- `context/decisions/`는 장기 rationale이 필요한 구조적 판단만 기록.
- branch, PR, WBS는 issue에서 파생된 실행 artifact.

## 제목 규칙
- 권장 형식: `[type] 요약`
- 허용 type: `feature|bug|chore`
- 예:
  - `[feature] PR remote review ledger 구조 정리`
  - `[bug] PR body guard가 최신 템플릿을 통과하지 못함`
  - `[chore] issue/pr 생성 스크립트 정합성 정리`

## Type 정의
- `feature`: 기능 요청, 기능 개선, 제품 가치 변화
- `bug`: 기대 동작과 실제 동작의 불일치
- `chore`: 운영, 정책, 자동화, 저장소 정비

## 본문 규칙
- issue type별 GitHub 템플릿을 따른다.
- issue는 `what`, `why`, 제약, 쟁점을 기록하고 실행 `how`는 별도 artifact로 분리.
- 작업 전 쟁점은 `Decision Candidates` 섹션에 기록.
- 종료 조건은 `Done Signal`에 얇게 기록.
- 관련 링크는 `Related Links` 섹션에 기록.
- 범위 경계가 필요한 type은 `Out of Scope`에서 명시.

## Label 분류
- `type:*`
  - `type:feature`
  - `type:bug`
  - `type:chore`
- `status:*`
  - `status:inbox`
  - `status:ready`
  - `status:active`
  - `status:blocked`
  - `status:cancelled`
- `priority:*`
  - `priority:p0`
  - `priority:p1`
  - `priority:p2`
  - `priority:p3`
- `area:*`
  - `area:product`
  - `area:repo`
  - `area:docs`
  - `area:agent-team`
- `source_type:*`
  - `source_type:human-request`
  - `source_type:agent-team`
  - `source_type:runtime-observation`
  - `source_type:wbs-planned`

## Label 운영 규칙
- issue 생성 시 아래 다섯 축을 모두 명시.
  - `type:*` 1개
  - `status:*` 1개
  - `priority:*` 1개
  - `source_type:*` 1개
  - `area:*` 1개 이상
- status 해석
  - `status:inbox`: 들어왔지만 아직 정리되지 않은 backlog 입력
  - `status:ready`: 실행 가능한 상태로 정리 완료
  - `status:active`: 현재 작업 중
  - `status:blocked`: 외부 입력/의존성 부족으로 진행 불가
  - `status:cancelled`: 더 이상 진행하지 않기로 결정
- 완료는 `status:done` 대신 issue close로 처리.
- label은 template frontmatter에서 자동 부여하지 않는다.
- issue 생성 wrapper에서 taxonomy를 검증한 뒤 `gh issue create --label ...`로 전달한다.
- GitHub UI로 직접 생성할 때도 같은 taxonomy를 수동으로 적용.

## Template 구조
- feature
  - `Summary`
  - `Context`
  - `Problem / Opportunity`
  - `Goal`
  - `Expected Impact`
  - `Constraints`
  - `Decision Candidates`
  - `Done Signal`
  - `Out of Scope`
  - `Related Links`
- bug
  - `Summary`
  - `Context`
  - `Observed Behavior`
  - `Expected Behavior`
  - `Impact`
  - `Reproduction Clues`
  - `Suspected Area`
  - `Constraints`
  - `Decision Candidates`
  - `Done Signal`
  - `Related Links`
- chore
  - `Summary`
  - `Context`
  - `Operational Problem`
  - `Goal`
  - `Affected Surface`
  - `Constraints`
  - `Decision Candidates`
  - `Done Signal`
  - `Out of Scope`
  - `Related Links`

## 템플릿
- feature: `.github/ISSUE_TEMPLATE/feature.md`
- bug: `.github/ISSUE_TEMPLATE/bug.md`
- chore: `.github/ISSUE_TEMPLATE/chore.md`

## Gate
- 제목 가드: `scripts/repo/issue_title_guard.sh`
- 본문 가드: `scripts/repo/issue_body_quality_guard.py`
- label 가드: `scripts/repo/issue_label_guard.py`

## 예외 정책
- 예외 운영이 발생하면 `Context` 또는 `Notes`에서 이유를 명시.
