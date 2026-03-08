# WBS Writing Conventions

이 문서는 WBS slice 초안과 정식 문서를 사람이 일관되게 작성하기 위한
최소 작성 규칙을 정의한다.

목표는 3가지다.

1. slice 간 비교가 가능하도록 필드 표현을 정렬한다.
2. planned flow / packet으로 내려갈 때 해석 흔들림을 줄인다.
3. 사람과 에이전트가 같은 문서를 읽을 때 의미 차이가 줄어들게 한다.

이 문서는 schema가 아니라 작성 컨벤션이다.
필수/선택 필드 자체는 `wbs-slice-definition.md`를 따른다.

## 기본 원칙

### 1. 사람을 위한 설명은 한국어로 쓴다

- `goal`, `why`, `acceptance_criteria`, `owned_scope`, `verification_requirements`,
  `dependencies`, `non_goals`, `risks`, `assumptions`, `open_questions`, `notes`
  같은 사람이 읽는 설명 필드는 기본적으로 한국어로 작성한다.
- 아래 항목은 원문을 유지할 수 있다.
  - 파일 경로
  - 코드 식별자
  - schema field name
  - 외부 서비스/제품 이름
- 한국어로 자연스럽게 쓸 수 있는 표현을 굳이 영어로 두지 않는다.

예:

- 좋은 예: `노트 편집 삽입 경계`
- 피해야 할 예: `note editor insertion boundary`

### 2. WBS는 planning-layer 문서로 유지한다

- concrete `owned_paths`를 직접 적지 않는다.
- concrete `required_tests`를 직접 적지 않는다.
- actor route, node, transition을 직접 적지 않는다.
- runtime 상태를 적지 않는다.

### 3. 문장보다 판정 가능한 표현을 우선한다

- `goal`과 `acceptance_criteria`는 완료 여부를 판단할 수 있어야 한다.
- 구현 방식보다 사용자 가치와 관찰 가능한 결과를 우선한다.
- 같은 의미의 표현을 slice마다 다르게 쓰지 않는다.

## 파일 형태

- WBS task의 정본은 `context/wbs/tasks/<slice_id>.yaml` 형태의 YAML 파일을 기본값으로 둔다.
- backlog 전체를 보는 요약 projection은 `context/wbs/tasks/index.md`에 둔다.
- task YAML이 SoT이고 `index.md`는 사람이 빠르게 읽기 위한 요약본이다.
- 필드 순서는 템플릿 순서를 유지한다.
- 초안은 파일명에 `draft`를 포함할 수 있다.
- 예시 권장 패턴:
  - `<slice_id>.yaml`
  - `<slice_id>.draft.yaml`

## 필드별 작성 규칙

### `slice_id`

- 대문자 토큰을 `-`로 연결한 안정적 식별자를 권장한다.
- 제품 범위 + 사용자 행동이 보이면 좋다.

예:

- `MVP-TS-INSERT`
- `MVP-VIDEO-OPEN-BY-URL`

### `parent_wbs`

- 어떤 WBS 버전 계열에 속하는지 드러내는 안정적 식별자를 쓴다.
- 런타임 상태처럼 자주 바꾸지 않는다.

예:

- `mvp-wbs/v1`

### `planning_status`

- WBS는 runtime state를 소유하지 않으므로 `active`, `blocked`, `done` 같은 값은 적지 않는다.
- `planning_status`는 backlog/planning 기준 준비 상태를 나타낸다.
- 현재 단계에서는 아래 최소값을 권장한다.
  - `draft`
  - `planned`
  - `planning_blocked`
  - `ready_for_flow`
  - `ready_for_dispatch`
  - `archived`
  - `cancelled`

### `goal`

- 한 문장으로 쓴다.
- 가능하면 `사용자가 ... 할 수 있다` 형태를 권장한다.
- UI 조각이 아니라 사용자 가치 기준으로 적는다.

좋은 예:

- `사용자가 현재 재생 시점을 노트에 삽입할 수 있다.`

피해야 할 예:

- `타임스탬프 버튼을 추가한다.`

### `why`

- 왜 이 slice가 제품적으로 필요한지 1~2문장으로 적는다.
- 구현 편의보다 사용자 가치, 실험 가치, 통합 가치가 드러나야 한다.

### `contracts`

- 현재 단계에서는 contract SoT 문서 경로를 우선 적는다.
- 필요하면 같은 항목에 어떤 contract를 보는지 짧게 덧붙인다.
- 문서 전체를 요약해 붙여 넣지 않는다.
- 나중에 context cost가 문제가 되면 contract registry나 excerpt reference로 세분화한다.

예:

```yaml
contracts:
  - docs/product/contracts/storage.ts
  - docs/product/contracts/analytics.ts
```

### `acceptance_criteria`

- 관찰 가능한 완료 조건만 적는다.
- 구현 방법이나 내부 구조를 적지 않는다.
- 각 항목은 서로 다른 판정 포인트를 나타내야 한다.

좋은 예:

- `삽입된 타임스탬프는 현재 열린 video_id와 연결된다.`

피해야 할 예:

- `React hook으로 player state를 구독한다.`

### `owned_scope`

- concrete file path 대신 ownership boundary를 적는다.
- 가능한 한 `... 경계` 형태를 권장한다.
- 너무 넓은 표현과 너무 구체적인 표현을 둘 다 피한다.

좋은 예:

- `플레이어 현재 시점 노출 경계`
- `노트 편집 삽입 경계`

피해야 할 예:

- `apps/web/src/features/player/**`
- `앱 전체`

### `verification_requirements`

- 테스트 명령이 아니라 필요한 검증 증거 수준을 적는다.
- 가능한 한 아래 표현을 재사용한다.
  - `단위 검증 증거 필요`
  - `통합 검증 증거 필요`
  - `수동 UX 검증 필요`
  - `계약 호환성 검증 필요`

필요하면 도메인 맥락을 덧붙인다.

예:

- `통합 검증 증거 필요`
- `계약 호환성 검증 필요`

### `dependencies`

- 선행 slice, 선행 결정, 외부 조건만 적는다.
- 막연한 희망사항은 적지 않는다.
- 없으면 `[]`를 권장한다.

### `non_goals`

- 이번 slice에서 하지 않을 것을 적는다.
- 인접 기능과의 경계를 분명히 하는 데 사용한다.
- "언젠가 할 수도 있음" 정도의 잡담은 적지 않는다.

### `risks`

- 작성 시점에 이미 알려진 위험만 적는다.
- 막연한 불안이나 일반론은 적지 않는다.
- risk가 있다고 해서 WBS가 잘못된 것은 아니다.
- 다만 `goal`, `acceptance_criteria`, `owned_scope`를 무너뜨리는 risk라면
  먼저 WBS를 다시 써야 한다.

### `assumptions`

- 현재 slice가 기대고 있는 가정을 적는다.
- 이 가정이 깨지면 planned flow나 packet에서 재판단이 필요해야 한다.

### `open_questions`

- 아직 닫히지 않은 쟁점을 적는다.
- 각 항목 앞에 아래 prefix를 붙이는 것을 권장한다.
  - `[blocking]`: planned flow 전에 닫아야 하는 쟁점
  - `[later]`: packet 구체화 단계나 runtime 직전까지 미룰 수 있는 쟁점

예:

- `[blocking] player current time read contract를 별도 SoT로 만들 것인가?`
- `[later] 버튼과 단축키를 같은 slice로 둘 것인가?`

### `workspace_bindings`

- branch, worktree, 용도처럼 slice의 작업 공간 계획 묶음을 적는다.
- 이 필드는 planning-layer binding이며 runtime status가 아니다.
- 한 task에 여러 workspace binding을 둘 수 있다.
- 값이 아직 없으면 `[]`를 사용한다.
- 현재 권장 하위 필드는 아래와 같다.
  - `purpose`
  - `branch`
  - `worktree`

예:

```yaml
workspace_bindings:
  - purpose: 구현
    branch: feat/mvp-ts-insert
    worktree: /home/yonghyeun/worktrees/q1-mvp-ts-insert
  - purpose: 버그 수정
    branch: fix/mvp-ts-insert-follow-up
    worktree: /home/yonghyeun/worktrees/q1-mvp-ts-insert-fix
```

- `purpose`는 가능한 한 짧은 한국어 명사로 쓴다.
- 권장 예:
  - `구현`
  - `버그 수정`
  - `실험`
  - `안정화`

### `refs`

- slice와 연결된 planning/runtime artifact 참조를 적는다.
- branch/worktree는 `refs`가 아니라 `workspace_bindings`에 둔다.
- 현재 권장 하위 필드는 아래와 같다.
  - `planned_flow`
  - `run_id`
  - `related_docs`

예:

```yaml
refs:
  planned_flow: context/wbs/flows/MVP-TS-INSERT.flow.v1.md
  run_id: null
  related_docs: []
```

### `notes`

- 나머지 필드에 넣기 어려운 운영 메모만 적는다.
- 규칙을 우회하는 예외 처리 문구를 남발하지 않는다.

## 필드 간 구분 규칙

### `acceptance_criteria`와 `verification_requirements`를 섞지 않는다

- `acceptance_criteria`: 무엇이 완료인가
- `verification_requirements`: 어떤 종류의 증거가 필요한가

예:

- AC: `타임스탬프 삽입 결과가 노트에 남는다.`
- Verification: `통합 검증 증거 필요`

### `owned_scope`와 `contracts`를 섞지 않는다

- `owned_scope`: 어디까지 수정 책임이 미치는가
- `contracts`: 어떤 SoT를 기준으로 맞춰야 하는가

### `risks`와 `open_questions`를 섞지 않는다

- `risks`: 이미 드러난 불확실성 또는 충돌 가능성
- `open_questions`: 아직 결정되지 않은 질문

### `planning_status`와 runtime 상태를 섞지 않는다

- `planning_status`: backlog/planning 상태
- runtime 상태: `run ledger.slice_state`

예:

- WBS: `ready_for_flow`
- Run ledger: `active`

### `workspace_bindings`와 `refs`를 섞지 않는다

- `workspace_bindings`: branch/worktree/용도 정보
- `refs`: planned flow, run, 문서 참조

## 현재 단계의 실무 규칙

- context limit 최적화는 지금 WBS 작성의 1순위가 아니다.
- 우선은 사람이 읽고 판단하기 쉬운 WBS를 만든다.
- contract 참조가 과도하게 무거워진다고 확인되면 그때 contract registry,
  excerpt reference, packet input compaction을 추가로 도입한다.

## 체크리스트

WBS를 저장하기 전에 아래를 확인한다.

- 설명 필드가 한국어로 작성됐는가
- `planning_status`가 runtime 상태와 섞이지 않았는가
- `goal`이 사용자 가치 한 문장으로 닫히는가
- `acceptance_criteria`가 구현 디테일 없이 판정 가능한가
- `owned_scope`가 경계 수준으로 표현됐는가
- `verification_requirements`가 검증 의무 수준으로 표현됐는가
- `non_goals`가 scope 경계를 분명히 하는가
- `risks`와 `open_questions`가 구분됐는가
- `workspace_bindings`와 `refs`가 역할에 맞게 분리됐는가
- concrete path/test/route가 WBS에 섞이지 않았는가
