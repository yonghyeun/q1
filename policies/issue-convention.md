# Issue Convention

## 목적
- issue 제목과 본문에 포함되어야 할 최소 정보를 정의.
- issue를 remote backlog 입력 문서로 일관되게 유지.

## 저장 위치 원칙
- 해결해야 할 backlog 항목의 기본 저장소는 GitHub issue.
- `context/decisions/`는 장기 rationale이 필요한 구조적 판단만 기록.
- branch, PR, WBS는 issue에서 파생된 실행 artifact.
- 현재 worktree의 실행 issue linkage snapshot은 worktree metadata에 둘 수 있다.
- local metadata는 조회 편의를 위한 실행 snapshot이며 backlog SoT를 대체하지 않는다.

## 제목 규칙
- 권장 형식: `[type] 요약`
- 허용 type: `feature|bug|chore`
- 예:
  - `[feature] PR remote review ledger 구조 정리`
  - `[bug] PR body guard가 최신 템플릿을 통과하지 못함`
  - `[chore] issue/pr 생성 스크립트 정합성 정리`

## Type 정의
- `feature`: 기능 요청, 기능 개선, 제품 가치 변화
  - 사용자나 제품 관점의 동작, 경험, 제공 capability가 바뀌는가를 기준으로 본다.
  - 저장소 내부 workflow나 운영 자동화에 "추가"가 있어도 제품 동작이 바뀌지 않으면 기본적으로 `feature`로 보지 않는다.
- `bug`: 기대 동작과 실제 동작의 불일치
- `chore`: 운영, 정책, 자동화, 저장소 정비
  - branch/worktree/task wrapper, hook, metadata, template, repo 정책, agent workflow 정비는 기본적으로 `chore` 가설에서 시작한다.
  - 실행면 정비가 이후 작업을 쉽게 만들어도 곧바로 제품 기능 추가로 해석하지 않는다.

## Type 판단 질문
- 먼저 묻는 질문: "이 변경이 제품/사용자 관점의 동작이나 가치 전달을 바꾸는가?"
  - 그렇다면 `feature` 가능성이 높다.
- 다음 질문: "이 변경이 저장소 운영 기준, 실행 workflow, 자동화, 정책 정합성을 다루는가?"
  - 그렇다면 `chore` 가능성이 높다.
- "추가", "지원", "연결", "추적" 같은 표현만으로 `feature`로 기울이지 않는다.
- repo 내부 운영 작업은 결과물이 새 스크립트나 metadata여도 우선 `chore`에서 검토한다.
- 분류가 애매하면 `Context`에 제품 변화인지 repo 운영 변화인지 한 줄 근거를 남긴다.

## Repo 운영 작업 분류 예시
- `chore`
  - branch naming, worktree naming, task start/end wrapper 정비
  - issue/PR template, label taxonomy, gate, hook, CI 운영 규칙 정리
  - worktree issue metadata, local ledger, agent workflow 보조 도구 추가
  - repo 문서 구조, 운영 policy, automation helper 개선
- `feature`
  - 실제 제품 동작, 사용자-facing workflow, 제공 기능 자체의 추가/확장
  - 저장소 변경이 포함되더라도 최종 변화의 중심이 제품 capability라면 `feature`

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
- open issue는 `status:*` label 1개를 유지한다.
- closed issue의 status 해석
  - 완료로 닫힌 issue는 `status:*` label을 남기지 않는다.
  - 완료가 아닌 종료는 close 전에 종료 사유를 `status:blocked` 또는 `status:cancelled` 로 명시한 뒤 닫는다.
  - `status:ready` 또는 `status:active` 가 남은 채 닫힌 issue는 정리되지 않은 상태로 본다.
- `task end` 성공 종료는 완료 close로 간주한다.
  - PR merge로 linked issue가 닫힌 뒤 남아 있는 `status:*` label을 제거한다.
  - linked issue가 닫히지 않았다면 status를 제거하지 않고, close linkage 또는 수동 close를 먼저 정리한다.
- 완료가 아닌 종료는 `task end` 자동화 대상이 아니다.
  - `status:blocked` 또는 `status:cancelled` 로 먼저 전환한다.
  - 그 뒤 GitHub에서 수동 close 하거나 별도 운영 절차로 종료한다.
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
