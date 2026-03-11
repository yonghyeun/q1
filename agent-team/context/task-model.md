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
- atomic task와 handoff packet의 차이
- source type 분류 체계

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
- WBS와 ingress spec 사이를 1:1 필드 매핑으로 고정하지 않는다.
- 입력원은 `semantic normalization`을 통해 공통 task ingress spec 초안으로 변환한다.
- 변환 레이어의 에이전트는 입력 의미를 읽고 필드를 추론할 수 있다.
- 다만 근거가 약한 추정은 확정값으로 채우지 않고 `open_points`로 남긴다.
- 생성된 ingress draft는 사람 승인 전까지 확정본이 아니다.
- 승인 전후 모두 구조 유효성은 타입체크 또는 검증 스크립트로 확인한다.

## Normalization Flow
### 1. Source Read
- 입력원을 읽고 `source_type`, `source_ref`, 핵심 근거를 수집한다.
- 입력원 예시:
  - WBS slice
  - 자연어 요청
  - backlog 메모
  - 운영 개선 요청

### 2. Ingress Draft
- 에이전트가 공통 task spec 초안을 작성한다.
- 이때 필드는 입력원의 의미를 기준으로 재구성할 수 있다.
- 예:
  - WBS의 `goal`은 `objective` 초안으로 해석할 수 있다.
  - `owned_scope`와 `verification_requirements`는 `constraints` 초안에 반영할 수 있다.
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

### 5. Accepted Task
- 승인된 ingress task만 분해 레이어의 입력이 된다.
- 이후 atomic task 분해와 execution planning은 이 승인본을 기준으로 진행한다.

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
