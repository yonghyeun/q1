# Task Model

## Decision
- agent-team이 받는 입력 task는 WBS에 한정하지 않는다.
- WBS는 주요 입력원 중 하나로 취급한다.
- 따라서 agent-team은 여러 입력원을 받을 수 있는 공통 task ingress shape를 가져야 한다.
- 또한 task를 받아 원자 단위로 분해하는 레이어와, 분해된 작업을 계획/실행하는 레이어를 분리한다.

## Why
- 실제 작업은 WBS 외의 문서, 대화, 메모, 운영 요청에서도 생성될 수 있다.
- 입력원이 다르더라도 같은 실행 루프로 보내려면 공통 shape가 필요하다.
- 그렇지 않으면 입력원마다 다른 방식으로 분해와 실행이 이루어져 trace 비교가 어려워진다.
- 분해와 실행 계획을 한 레이어에 섞으면 상위 목표 정리와 하위 실행 최적화가 서로 오염된다.

## Layers
### 1. Task Ingress Layer
- 역할: 여러 입력원을 agent-team이 받을 수 있는 공통 task 형태로 정규화한다.
- 입력 예시:
  - WBS slice
  - 사용자의 자연어 작업 요청
  - backlog 메모
  - 운영성 개선 요청
- 출력:
  - 공통 task spec
- 책임:
  - task의 목표를 한 문장으로 정리
  - 입력원의 근거를 링크로 남김
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
- raw request
  -> task ingress spec
  -> atomic task decomposition
  -> execution planning
  -> runtime execution
  -> verification
  -> feedback into next run

## Boundary
- WBS는 planning-layer SoT다.
- WBS가 없는 요청도 먼저 ingress spec으로 정규화한 뒤 같은 분해 루프에 넣는다.
- decomposition layer는 "무엇을 어떤 단위로 나눌 것인가"에 집중한다.
- execution planning layer는 "그 단위를 어떤 node와 packet으로 실행할 것인가"에 집중한다.

## Initial Shape Proposal
### Common Task Spec
- `task_id`
- `source_type`
- `source_ref`
- `objective`
- `why`
- `constraints`
- `acceptance_criteria`
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
- ingress spec과 WBS slice의 정확한 매핑 규칙
- atomic task와 handoff packet의 차이
- source type 분류 체계
