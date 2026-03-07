# WBS Slice Definition

이 문서는 이 저장소에서 `WBS slice`가 무엇을 정의하고,
무엇을 정의하지 않는지의 경계를 고정한다.

현재 운영 모델에서 WBS는 runtime artifact가 아니라
planning-layer SoT다.

사람이 작성하는 표현 규칙은 `wbs-writing-conventions.md`를 따른다.

현재 권장 저장 단위는 `slice 1개 = task YAML 파일 1개`다.
사람이 backlog 전체를 빠르게 보는 용도로는
별도 `index.md` projection을 함께 둔다.

## 목적

- slice를 사용자 가치 기준의 독립 단위로 정의한다.
- `planned flow`, `packet`, `trace`와 역할을 분리한다.
- WBS가 너무 이른 concrete path/test 계획으로 무거워지는 것을 막는다.
- 병렬 작업 전 필요한 안정적 제약만 남긴다.

## 기본 원칙

### 1. WBS는 slice 정의 문서다

- WBS는 "무엇을 왜 끝내야 하는가"를 정의한다.
- WBS는 slice 경계, 계약 경계, 완료 기준, 선후관계의 SoT다.
- WBS는 planning 상태와 작업 공간 바인딩은 가질 수 있지만,
  runtime 상태를 소유하지 않는다.

### 2. WBS는 abstract boundary를 가진다

- WBS는 파일 경로 목록을 직접 고정하지 않는다.
- WBS는 테스트 명령 목록을 직접 고정하지 않는다.
- 대신 `owned_scope`와 `verification_requirements` 같은 추상 경계를 가진다.

핵심은 "지금 정확히 어떤 파일을 고칠까"보다
"어느 경계 안에서 움직여야 하는가"를 먼저 고정하는 것이다.

### 3. Concrete detail은 runtime에 가까운 레이어로 내린다

- `planned flow`는 어떤 node/transition과 packet blueprint가 허용되는지 정의한다.
- `packet`은 현재 node 기준 concrete `owned_paths`, `required_tests`, `inputs`를 정의한다.
- `trace`는 실제 변경 파일과 실제 실행 테스트를 기록한다.

즉, WBS는 stable constraint를 잡고,
runtime에 가까워질수록 detail을 늦게 바인딩한다.

## WBS가 가져야 할 것

각 slice는 최소한 아래 필드를 가져야 한다.

- `slice_id`: slice 식별자
- `parent_wbs`: 어떤 WBS 계열에 속하는지 나타내는 식별자
- `planning_status`: backlog/planning 관점의 준비 상태
- `goal`: 이 slice가 끝내는 사용자 가치
- `why`: 왜 이 slice가 필요한가
- `contracts`: 참조해야 하는 contract SoT
- `acceptance_criteria`: 완료 판정 기준
- `owned_scope`: 수정 책임이 미칠 기능/모듈/경계 수준
- `verification_requirements`: 어떤 수준의 검증 증거가 필요한가
- `dependencies`: 선행 slice, 선행 결정, 외부 의존성
- `non_goals`: 이번 slice에서 하지 않을 것

필요하면 아래를 추가할 수 있다.

- `risks`: 시작 시점에 이미 알려진 위험
- `assumptions`: 현재 slice가 기대는 가정
- `open_questions`: planned flow 작성 전에 닫아야 하는 쟁점
- `workspace_bindings`: branch, worktree, 용도를 담는 planning-layer 작업 공간 바인딩 목록
- `refs`: planned flow, run, 관련 문서 참조
- `notes`: 운영 메모

## WBS가 직접 가지지 않을 것

아래 항목은 WBS가 직접 정본으로 가지지 않는 것을 기본값으로 둔다.

- 정확한 수정 파일 경로 목록
- 정확한 테스트 명령 목록
- actor별 세부 실행 순서
- node별 handoff route
- runtime 진행 상태
- 실제 변경 결과

이 정보는 아래처럼 다른 레이어에서 다룬다.

- concrete path/test: `packet`
- route/node/loop: `planned flow`
- actual changes/tests: `trace`
- current status: `run ledger`

여기서 `planning_status`는 예외다.
이는 runtime 상태가 아니라 backlog/planning 준비 상태이므로
WBS가 직접 가진다.

## 핵심 필드 해석

### `owned_scope`

`owned_scope`는 파일 glob이 아니라 ownership boundary다.

예:

- `note editor insertion boundary`
- `player time integration boundary`
- `timestamp rendering and parsing boundary`

좋은 `owned_scope`는 아래 조건을 만족한다.

- 사람이 읽고 어떤 모듈 경계를 뜻하는지 이해할 수 있다
- packet 단계에서 concrete `owned_paths`로 내릴 수 있다
- ownership 충돌 여부를 계획 단계에서 판단하는 데 도움이 된다

나쁜 예시는 아래와 같다.

- `apps/web/src/features/note-editor/insert.ts`
- `src/**`

첫 번째는 너무 구체적이고, 두 번째는 너무 넓다.

### `verification_requirements`

`verification_requirements`는 테스트 명령이 아니라
검증 의무 수준을 뜻한다.

예:

- `unit evidence required`
- `integration evidence required`
- `manual UX verification required`
- `contract compatibility evidence required`

좋은 `verification_requirements`는 아래 질문에 답해야 한다.

- 이 slice를 완료로 보기 위해 어떤 종류의 증거가 필요한가
- 그 증거를 어떤 node에서 확보해야 하는가
- packet 단계에서 어떤 concrete test로 내려갈 수 있는가

### `planning_status`

`planning_status`는 runtime execution state가 아니라
slice 준비 단계를 나타낸다.

예:

- `draft`
- `planned`
- `planning_blocked`
- `ready_for_flow`
- `ready_for_dispatch`

좋은 `planning_status`는 아래 조건을 만족한다.

- 사람이 "이 slice가 planning 상 어디까지 왔는가"를 즉시 이해할 수 있다
- `active`, `blocked`, `done` 같은 runtime 상태와 섞이지 않는다
- operator가 다음 planning action을 정하는 데 도움이 된다

### `workspace_bindings`

`workspace_bindings`는 한 slice를 실제 어디서 다룰지에 대한
planning-layer 작업 공간 바인딩 목록이다.

한 slice는 구현, 버그 수정, 실험 같은 이유로
여러 branch/worktree를 가질 수 있다.

예:

- `purpose: 구현`
- `branch: feat/mvp-ts-insert`
- `worktree: /worktrees/q1-mvp-ts-insert`
- `purpose: 버그 수정`
- `branch: fix/mvp-ts-insert-follow-up`
- `worktree: /worktrees/q1-mvp-ts-insert-fix`

이 정보는 route 문서인 `planned flow`에 두지 않는다.
같은 flow를 여러 branch/worktree/run에서 재사용할 수 있어야 하기 때문이다.

다만 이 정보 역시 runtime 상태는 아니다.
현재 누가 실제로 packet을 들고 있는지는 `run ledger`가 소유한다.

### `refs`

`refs`는 slice와 연결된 planning/runtime artifact를 가리키는 참조 묶음이다.

예:

- `planned_flow`
- `run_id`
- `related_docs`

`refs`는 연결 포인터를 담고,
`workspace_bindings`는 실제 작업 위치 계획을 담는다.

## 레이어 간 매핑

### WBS -> Planned Flow

WBS는 slice의 목표와 경계를 준다.
planned flow는 그 slice를 어떤 route로 완료시킬지 설계한다.

- `goal`, `acceptance_criteria`는 node 목적과 exit evidence의 기반이 된다
- `owned_scope`는 node별 packet blueprint를 나누는 기준이 된다
- `verification_requirements`는 어떤 node에서 어떤 증거가 필요한지 정하는 기준이 된다
- `planning_status`는 flow를 만들 수 있는 준비 정도를 보여준다
- `workspace_bindings`는 flow와 별개로 어떤 branch/worktree 묶음을 준비해 둘지 알려준다

### Planned Flow -> Packet

planned flow는 blueprint를 주고,
packet은 현재 node에서 필요한 concrete detail을 채운다.

- `owned_scope` -> `owned_paths`
- `verification_requirements` -> `required_tests`
- `contracts` -> `inputs` / `contracts`
- node purpose -> packet `goal` / `why`

### Packet -> Trace

packet은 기대 경계를 주고,
trace는 실제 실행 결과를 남긴다.

- `owned_paths` -> 실제 `changes`
- `required_tests` -> `tests_run` / `tests_skipped`
- packet goal -> `result`, `requested_decision`, `next_action`

## Orchestration-ready 판단 기준

slice는 최소한 아래가 준비됐을 때 orchestration-ready로 본다.

- `slice_id`가 고정됐다
- `planning_status`가 `ready_for_flow` 또는 그에 준하는 상태다
- `goal`과 `acceptance_criteria`가 판정 가능하다
- `contracts`가 식별 가능하다
- `owned_scope`가 너무 넓거나 모호하지 않다
- `verification_requirements`가 필요한 증거 수준을 말해 준다
- `dependencies`와 `non_goals`가 명시돼 있다

이후 runtime에 들어가기 전에는 같은 slice의 `planned flow`가 먼저 준비돼야 한다.

## 예시

```yaml
slice_id: NOTE-TIMESTAMP-INSERT
parent_wbs: mvp-wbs/v1
planning_status: ready_for_flow
goal: 사용자가 현재 재생 시점을 노트에 삽입할 수 있다.
why: 학습 중 중요한 구간을 노트와 연결하는 핵심 UX다.
contracts:
  - docs/product/contracts/player-time.md
  - docs/product/contracts/editor-insert.md
acceptance_criteria:
  - 현재 시점이 노트 에디터에 삽입된다.
  - 삽입 후 편집 흐름이 깨지지 않는다.
owned_scope:
  - note editor insertion boundary
  - player time integration boundary
verification_requirements:
  - unit evidence required
  - integration evidence required
dependencies:
  - player time contract confirmed
non_goals:
  - timestamp click-to-seek
  - keyboard shortcut
workspace_bindings:
  - purpose: 구현
    branch: feat/note-timestamp-insert
    worktree: /worktrees/q1-note-timestamp-insert
refs:
  planned_flow: context/wbs/flows/NOTE-TIMESTAMP-INSERT.flow.v1.md
  run_id: null
  related_docs: []
```

위 slice에서 실제 `owned_paths`와 `required_tests`는
packet 단계에서 node 목적에 맞게 구체화한다.
