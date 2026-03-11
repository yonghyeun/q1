# Task Model

## Decision
- agent-team이 실제로 받는 backlog 입력의 기본 SoT는 GitHub issue다.
- WBS, 사람 요청, runtime 관찰은 issue 생성의 upstream source로 취급한다.
- 따라서 agent-team은 issue를 읽어 공통 task ingress shape로 정규화한다.
- 또한 task를 받아 원자 단위로 분해하는 레이어와, 분해된 작업을 계획/실행하는 레이어를 분리한다.

## Why
- 실제 작업의 최종 backlog 저장소를 issue로 고정해야 조회, triage, PR 연결이 쉬워진다.
- WBS 외의 문서, 대화, 메모, 운영 요청도 issue로 수렴시키면 같은 intake 흐름을 유지할 수 있다.
- issue를 공통 intake로 삼아야 입력원별 drift 없이 trace 비교가 가능하다.
- 분해와 실행 계획을 한 레이어에 섞으면 상위 목표 정리와 하위 실행 최적화가 서로 오염된다.

## Layers
### 1. Task Ingress Layer
- 역할: GitHub issue를 agent-team이 처리할 수 있는 공통 task 형태로 정규화한다.
- 입력:
  - GitHub issue backlog input
- 출력:
  - 공통 task spec
- 책임:
  - issue 제목, 본문, label을 읽는다
  - task의 목표를 한 문장으로 정리
  - issue와 upstream source의 근거를 링크로 남김
  - 제약, 비목표, 완료 기준 초안을 수집
  - 아직 불분명한 점을 open point로 표기

### 2. Decomposition Layer
- 역할: 공통 task spec을 실행 가능한 원자 단위 작업으로 분해한다.
- 출력:
  - slice 또는 atomic task 목록
- 책임:
  - 큰 목표를 반복 가능한 단위로 자름
  - 선후관계와 의존성을 드러냄
  - 사람 판단이 꼭 필요한 지점을 표시
  - 아직 runtime path/test 수준으로 과도하게 concretize하지 않음

### 3. Execution Planning Layer
- 역할: 분해된 작업을 실제 trace node에 맞춰 계획한다.
- 기본 node:
  - 분해
  - 계획
  - 실행
  - 검증
  - 개선
- 출력:
  - node별 계획
  - handoff-ready task packet
- 책임:
  - 어떤 node를 거칠지 결정
  - node별 입력/출력/evidence를 정함
  - 로깅 의무와 검증 기준을 붙임

### 4. Runtime Execution Layer
- 역할: 계획된 packet을 실제로 실행하고 trace를 남긴다.
- 출력:
  - 산출물
  - trace
  - 검증 결과
  - 병목 피드백

## Recommended Flow
- raw request or WBS or runtime observation
  -> GitHub issue backlog input
  -> task ingress spec
  -> atomic task decomposition
  -> execution planning
  -> runtime execution
  -> verification
  -> feedback into next run

## Operating-Order Breakdown
- `Issue Intake`
- `Ingress Normalization`
- `Accepted Task Approval`
- `Atomic Decomposition`
- `Execution Planning`
- `Runtime Execution`
- `Verification`
- `Feedback And Improvement`

## Boundary
- GitHub issue는 backlog input SoT다.
- WBS는 planning-layer source이며 직접 runtime intake SoT가 아니다.
- WBS가 없는 요청도 issue로 수렴한 뒤 같은 분해 루프에 넣는다.
- decomposition layer는 "무엇을 어떤 단위로 나눌 것인가"에 집중한다.
- execution planning layer는 "그 단위를 어떤 node와 packet으로 실행할 것인가"에 집중한다.

## Initial Shape Proposal
### Common Task Spec
- `task_id`
- `source_type`
- `source_ref`
- `objective`
- `why`
- `acceptance_criteria`
- `constraints`
- `non_goals`
- `dependencies`
- `open_points`

### Atomic Task
- `atomic_task_id`
- `parent_task_id`
- `goal`
- `why`
- `inputs`
- `done_condition`
- `dependencies`
- `human_decision_required`

## Open Point
- issue를 `ready`로 승격하는 승인 조건

## Common Task Spec Options
### Minimal
- `task_id`
- `objective`
- `acceptance_criteria`
- `constraints`
- 특징: 가장 단순하지만 입력원, 비목표, 미해결 쟁점이 빠진다.

### Standard
- `task_id`
- `source_ref`
- `objective`
- `scope`
- `acceptance_criteria`
- `constraints`
- `dependencies`
- `owner`
- `priority`
- 특징: 일반적인 티켓 관리에는 익숙하지만, agent-team ingress 관점에서는 관리 성격이 강하다.

### Compromise
- `task_id`
- `source_ref`
- `objective`
- `why`
- `acceptance_criteria`
- `constraints`
- `dependencies`
- `open_points`
- 특징: 가볍지만 `non_goals`, `source_type` 부재로 범위와 입력원 구분이 약하다.

### Selected
- `task_id`
- `source_type`
- `source_ref`
- `objective`
- `why`
- `acceptance_criteria`
- `constraints`
- `non_goals`
- `dependencies`
- `open_points`
- 특징: 입력원 다양성, 작업 이유, 범위 통제, 미해결 쟁점을 함께 담을 수 있다.

## Final Decision
- 공통 task ingress spec은 `Selected` 안을 채택한다.
- `why`, `non_goals`, `open_points`는 초기에 익숙하지 않아도 유지한다.
- 이유:
  - `why`가 있어야 분해 방향이 흔들리지 않는다.
  - `non_goals`가 있어야 범위 팽창을 막을 수 있다.
  - `open_points`가 있어야 모르는 것을 감춘 채 진행하지 않는다.

## Normalization Policy
- issue 본문과 label을 1:1 필드 매핑으로만 고정하지 않는다.
- 입력원은 issue 안에 수렴한 뒤, `semantic normalization`을 통해 공통 task ingress spec 초안으로 변환한다.
- 변환 레이어의 에이전트는 입력 의미를 읽고 필드를 추론할 수 있다.
- 다만 근거가 약한 추정은 확정값으로 채우지 않고 `open_points`로 남긴다.
- 생성된 ingress draft는 사람 승인 전까지 확정본이 아니다.
- 승인 전후 모두 구조 유효성은 타입체크 또는 검증 스크립트로 확인한다.

## Normalization Flow
### 1. Source Read
- GitHub issue 제목, 본문, label을 읽고 `source_type`, `source_ref`, 핵심 근거를 수집한다.
- issue label은 최소한 아래 값을 가져야 한다.
  - `type:*`
  - `status:*`
  - `priority:*`
  - `area:*`
  - `source_type:*`

### 2. Ingress Draft
- 에이전트가 공통 task spec 초안을 작성한다.
- 이때 필드는 입력원의 의미를 기준으로 재구성할 수 있다.
- 예:
  - issue `Summary`와 `Goal`은 `objective` 초안으로 해석할 수 있다.
  - issue `Constraints`와 upstream WBS의 `owned_scope`, `verification_requirements`는 `constraints` 초안에 반영할 수 있다.
- 억지 추론은 금지한다.

### 3. Validation
- draft 구조를 타입체크 또는 검증 스크립트로 확인한다.
- 확인 대상:
  - 필수 필드 존재 여부
  - 필드 타입
  - 참조 경로 해석 가능 여부
  - enum 또는 형식 규칙 위반 여부

### 4. Human Approval
- 사람이 draft를 검토한다.
- 승인 가능한 행동:
  - 승인
  - 수정
  - 반려
- 승인 전에는 decomposition layer로 넘기지 않는다.
- 승인 후 issue status는 `ready` 또는 그에 준하는 상태로 올린다.

### 5. Accepted Task
- 승인된 ingress task만 분해 레이어의 입력이 된다.
- 이후 atomic task 분해와 execution planning은 이 승인본을 기준으로 진행한다.

## Issue Intake Rule
- 작업 시작은 GitHub issue에서 출발한다.
- issue는 `what`, `why`, 제약, 쟁점, label taxonomy를 담는 backlog input이다.
- issue가 곧 atomic task는 아니다.
- agent-team은 issue를 읽고 accepted task를 만든 뒤, 그 다음에 atomic task로 분해한다.

## Source Type Enum
- `source_type:human-request`
  - 사람의 직접 요청에서 온 issue
- `source_type:agent-team`
  - agent-team 운영 개선에서 나온 issue
- `source_type:runtime-observation`
  - trace, 실패, 병목, 회고에서 파생된 issue
- `source_type:wbs-planned`
  - WBS planning source에서 발행된 issue

## Issue Status For Intake
- `status:inbox`
  - 아직 정리되지 않은 backlog input
- `status:ready`
  - intake와 승인까지 끝나 작업 시작 가능
- `status:active`
  - 현재 작업 중인 issue
- `status:blocked`
  - 외부 입력 부족으로 진행 불가
- `status:cancelled`
  - 더 이상 진행하지 않기로 결정
- 완료는 `status:done`이 아니라 issue close로 처리한다.

## Atomic Task vs Handoff Packet
### Core Difference
- `atomic task`는 분해 레이어의 산출물이다.
- `handoff packet`은 실행 계획 레이어와 런타임 handoff의 산출물이다.
- 즉 atomic task는 "무엇을 끝내야 하는가"에 가깝고, packet은 "누가 지금 무엇을 실행해야 하는가"에 가깝다.

### Atomic Task
- 목적: 큰 목표를 더 작은 실행 단위로 자른다.
- 레이어: decomposition layer
- 시점: 실행 계획 이전
- 성격: 비교적 추상적
- 포함:
  - 목표
  - 완료 조건
  - 의존성
  - 사람 판단 필요 여부
- 아직 가지지 않는 것:
  - `run_id`
  - `owner_role`
  - `handoff_from`
  - `handoff_to`
  - `owned_paths`
  - `required_tests`
  - `validator_rules`
- 질문 형태:
  - 이 큰 목표를 어떤 작업 단위로 나눌 것인가
  - 이 작업 단위가 끝났다고 보려면 무엇이 필요한가

### Handoff Packet
- 목적: 특정 node와 역할에게 실행 지시를 내린다.
- 레이어: execution planning layer -> runtime execution layer
- 시점: atomic task가 계획된 뒤
- 성격: 더 구체적이고 handoff-ready
- 포함:
  - `run_id`
  - `owner_role`
  - `handoff_from`
  - `handoff_to`
  - `inputs`
  - `contracts`
  - `owned_paths`
  - `required_tests`
  - `validator_rules`
  - `expected_outputs`
- 질문 형태:
  - 지금 이 역할은 무엇을 실행해야 하는가
  - 어떤 입력과 검증 기준이 있어야 하는가

### Relation
- accepted task는 여러 atomic task로 분해될 수 있다.
- 하나의 atomic task는 하나 이상의 packet으로 전개될 수 있다.
- 이유:
  - atomic task 하나가 여러 node를 거칠 수 있기 때문이다.
  - 같은 atomic task도 재작업, 역할 전환, 검증 단계에서 packet이 다시 발행될 수 있다.

### Example
- accepted task:
  - `agent-team 문서 구조를 정의한다`
- atomic task:
  - `agent-team 루트 경계 문서를 작성한다`
  - `로드맵 문서를 작성한다`
  - `공통 task ingress spec을 확정한다`
- packet:
  - `문서 작성 역할`에게 `agent-team/README.md` 작성을 맡기는 packet
  - `검토 역할`에게 `경계 문구가 기존 taxonomy와 충돌하지 않는지` 검토를 맡기는 packet

### Why This Split Matters
- atomic task와 packet을 섞으면 분해 품질과 실행 품질을 따로 측정하기 어렵다.
- atomic task는 decomposition 품질 지표와 연결된다.
- packet은 node별 성공률과 trace 성공률 지표와 연결된다.
- 따라서 두 artifact를 분리해야 병목 위치를 정확히 볼 수 있다.

## Final Decision On This Boundary
- atomic task와 handoff packet은 별도 artifact로 유지한다.
- atomic task는 decomposition layer의 planning artifact다.
- handoff packet은 execution planning과 runtime handoff artifact다.
- packet은 atomic task를 concrete execution unit으로 투영한 결과로 본다.

## Why Not Fixed Mapping
- WBS와 ingress task의 형태는 시간이 지나며 바뀔 수 있다.
- 1:1 매핑을 고정하면 schema 변경 때마다 매핑 규칙을 계속 손봐야 한다.
- 반면 normalization 방식은 입력 형식 변화에 더 강하다.
- 또한 WBS 외 입력원도 같은 ingress shape로 수용할 수 있다.

## Human Role
- 사람은 변환 결과의 의미 적합성을 최종 확인한다.
- 에이전트가 잘 추론했더라도 범위 과장, 누락, 잘못된 비목표 설정은 사람이 교정한다.
- 구조 검증은 스크립트가 맡고, 의미 검증은 사람이 맡는다.

## Reading Aid
- `source_type`: task가 어디서 왔는지
- `source_ref`: 원문 근거가 어디 있는지
- `objective`: 이번 작업의 한 문장 목표
- `why`: 왜 필요한지
- `acceptance_criteria`: 무엇이 되면 완료인지
- `constraints`: 반드시 지켜야 할 제한
- `non_goals`: 이번에 하지 않을 것
- `dependencies`: 먼저 확인하거나 해결해야 할 것
- `open_points`: 아직 모르는 것

## Reading Aid For This Policy
- `normalization`: 원문 입력을 공통 task spec으로 의미 기반 재구성하는 과정
- `ingress draft`: 아직 승인되지 않은 task spec 초안
- `validation`: 구조와 형식을 기계적으로 확인하는 단계
- `approval`: 의미와 범위를 사람이 최종 확인하는 단계
