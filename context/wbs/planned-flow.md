# Planned Flow

이 문서는 WBS slice가 runtime에 들어가기 전에
어떤 node와 transition을 허용할지 미리 고정하는 `planned flow` 레이어를 정의한다.
현재 단계에서 `planned flow`는 **compiled execution plan**이 아니라
`route + packet blueprint`를 담는 planning artifact로 본다.

목표는 3가지다.

1. packet 생성 전에 허용된 경로를 명시한다.
2. 문제를 node 실패, transition/routing 실패, WBS 실패로 분리해 판정 가능하게 만든다.
3. operator의 런타임 재량을 줄여 재작업 루프와 복잡성을 관리한다.

## 왜 필요한가

기존 문서에서 `trace`는 개별 packet 실행 기록을 뜻한다.
하지만 실제 운영에서는 "packet이 어디로 흘러가야 하는가"도 따로 정해져 있어야 한다.

이 경로가 미리 고정되지 않으면 아래 문제가 생긴다.

- packet 생성 시점마다 routing을 즉흥적으로 다시 판단하게 된다.
- 실패 원인이 actor 구현 문제인지, handoff edge 문제인지, WBS slice 설계 문제인지 분리하기 어렵다.
- 동일한 slice에서 매번 다른 경로를 타며 operator 판단 편차가 커진다.
- 자동화 전제인 low-risk dispatch rule을 만들기 어렵다.

따라서 권장 레이어는 아래와 같다.

- `WBS`: 목표, AC, ownership, 선후관계의 SoT
- `planned flow`: 허용 node/transition과 packet blueprint의 SoT
- `packet`: planned flow의 특정 node를 런타임 handoff로 투영한 work order
- `trace`: 개별 packet 실행 기록
- `operator decision`: 어떤 transition을 실제로 선택했는지 남기는 event
- `run ledger`: 현재 위치와 미반영 feedback을 보여주는 projection

## 용어 정리

- 이 저장소에서 `trace`는 packet route가 아니라 **per-packet execution record**다.
- packet route는 `planned flow`와 runtime의 `packet lineage + decision history`로 해석한다.
- `node`는 orchestration 상의 단계다. 보통 `impl`, `integration`, `test`, `blocked`, `done` 같은 상태/역할 단위를 뜻한다.
- `transition`은 한 node에서 다른 node로 넘어가는 허용 경로다.
- `packet blueprint`는 각 node packet이 최소한 어떤 입력/출력/경계 조건을 가져야 하는지 정의하는 얇은 명세다.

## 현재 채택하는 방식

현재는 `blueprint-first` 방식을 기본값으로 둔다.

- planned flow는 node별 상세 실행 계획을 미리 완성하지 않는다.
- planned flow는 node 목적, transition, packet blueprint, escalation rule까지만 고정한다.
- concrete packet은 transition 시점에 최신 trace와 입력을 반영해 만든다.
- packet을 받은 actor는 그 packet 범위 안에서 **local execution plan**을 세운다.

즉 지금 문서에서 planned flow의 역할은
"각 node가 무엇을 하게 될지의 세부 계획"이 아니라
"어떤 경로와 어떤 packet shape가 허용되는가"를 고정하는 것이다.

## 지금 compiled flow를 기본값으로 두지 않는 이유

downstream operator들이 구현 전에 자기 node plan을 모두 먼저 작성하는
`compiled flow` 방식은 미래 옵션으로 열어둘 수 있다.
하지만 현재 기본값으로는 채택하지 않는다.

이유는 아래와 같다.

- upstream 결과가 아직 없는데 downstream 계획을 자세히 쓰면 쉽게 stale해진다.
- 작은 slice까지 planning pass를 강제하면 운영 비용이 과해진다.
- 현재 schema와 artifact 체계는 per-node 계획 문서를 정형적으로 연결할 준비가 아직 덜 됐다.

따라서 현재 단계에서는:

- `planned flow`: blueprint
- `packet`: concrete handoff
- `actor plan`: packet 수신 후 로컬 계획

으로 역할을 나누는 편이 더 적절하다.

## 누가 만들고 누가 바꾸나

기본 작성 책임은 `operator`에게 둔다.

- WBS slice가 orchestration-ready가 되는 시점에 operator가 first version을 만든다.
- node 경계가 contract나 ownership 경계와 강하게 연결되면 관련 owner가 review에 참여할 수 있다.
- runtime actor는 planned flow를 직접 고치는 것이 기본 역할이 아니다.
- actor는 trace에서 route 문제를 드러내고, operator가 이를 보고 flow를 수정하거나 새 버전으로 교체한다.

현재 schema에는 `feedback.target: planned_flow`가 없으므로,
flow 수정 필요 피드백은 우선 `orchestration` target으로 기록하고
operator가 planned flow 문서에 반영하는 것을 기본 규칙으로 둔다.

## 산출물 형태와 저장 위치

planned flow는 **planning artifact**이며 runtime run artifact가 아니다.

- 권장 포맷: Markdown 문서 + 고정된 YAML block
- 권장 저장 위치: `context/wbs/flows/<slice_id>.flow.vN.md`
- 사람이 초안 작성할 때는 `context/wbs/templates/planned-flow.template.md`를 사용한다

권장 메타데이터는 아래와 같다.

- `flow_id`: flow 식별자
- `flow_version`: route 규칙 버전
- `slice_id`: 연결된 WBS slice
- `entry_node_id`: 시작 node
- `terminal_node_ids`: 종료 가능 node
- `nodes`: node 정의와 packet 기대 산출물
- `nodes[].packet_blueprint`: packet에 미리 고정할 최소 입력/출력/비목표
- `transitions`: 허용 edge와 진입 조건
- `exception_loops`: blocked/remediate 같은 예외 경로
- `revisit_rules`: 반복 실패 시 상위 재설계로 승격하는 기준

runtime이 시작된 뒤 경로 규칙이 실질적으로 바뀌면
기존 flow 문서를 덮어쓰기보다 `v2`, `v3`처럼 새 버전을 만드는 편이 좋다.
그래야 과거 packet이 어떤 route 기준으로 발행됐는지 audit 가능하다.

## 언제 만들어야 하나

원칙적으로 runtime packet을 발행하는 slice는 planned flow를 먼저 가져야 한다.

- 단일 handoff로 끝나는 아주 단순한 slice도 최소한 `entry -> accept/close` 형태의 축약 flow는 있어야 한다.
- actor가 둘 이상 개입하거나 `rework`, `block`, `remediate` 가능성이 있으면 별도 문서로 유지하는 편이 좋다.

## 최소 포함 내용

planned flow는 최소한 아래 질문에 답해야 한다.

1. 시작 node는 무엇인가
2. terminal node는 무엇인가
3. 허용된 node는 무엇인가
4. 각 node에서 어떤 decision이 허용되는가
5. 어떤 증거가 있어야 다음 transition이 가능한가
6. 어떤 반복 패턴이 나오면 node 문제가 아니라 WBS/flow 재설계로 승격해야 하는가

## 권장 구조

아래는 사람이 작성하고 검토하기 위한 최소 권장 구조다.

```yaml
flow_id: FLOW-2026-03-07-001
parent_wbs: mvp-wbs/v1
slice_id: MVP-TS-INSERT
goal: 현재 재생 시점을 노트에 삽입하는 기능을 handoff 가능한 수준까지 완성한다.
entry_node_id: impl
terminal_node_ids:
  - done
  - cancelled
nodes:
  - node_id: impl
    owner_role: impl
    purpose: 기능 구현과 unit 수준 검증을 완료한다.
    planning_mode: local_after_packet
    packet_expectations:
      required_inputs:
        - contracts
        - acceptance_criteria
        - owned_paths
      required_outputs:
        - code_changes
        - tests
        - trace_summary
    packet_blueprint:
      goal_hint: timestamp 기능 구현과 unit evidence 확보
      non_goals:
        - integration wiring closure
      autonomy_boundary:
        - implementation steps are agent-local
        - contract/route changes require operator feedback
    allowed_decisions:
      - accept
      - rework
      - block
    exit_evidence:
      - unit tests passed
      - next actor can decide from trace
  - node_id: integration
    owner_role: integration
    purpose: wiring, adapter, cross-module 경계를 닫는다.
    allowed_decisions:
      - accept
      - rework
      - block
  - node_id: test
    owner_role: test
    purpose: required integration/e2e 검증을 완료한다.
    allowed_decisions:
      - accept
      - rework
      - block
  - node_id: done
    owner_role: operator
    purpose: slice 종료
transitions:
  - transition_id: impl_accept_to_integration
    from: impl
    decision: accept
    to: integration
    conditions:
      - impl AC evidence exists
      - integration actor can decide from trace
  - transition_id: impl_rework_to_impl
    from: impl
    decision: rework
    to: impl
    conditions:
      - direction is correct
      - packet or inputs need revision
  - transition_id: integration_accept_to_test
    from: integration
    decision: accept
    to: test
  - transition_id: test_accept_to_done
    from: test
    decision: accept
    to: done
exception_loops:
  - loop_id: blocked_wait_contract
    enter_via:
      - impl -> block
      - integration -> block
    exit_rule: missing contract or approval is resolved
revisit_rules:
  - if same node rework repeats twice without new input, escalate to WBS/flow review
  - if node accept 이후 다음 node가 판단 불가능하면 routing/orchestration failure로 본다
```

## 운영 규칙

### 1. Packet은 flow를 따라 생성한다

- packet은 자유롭게 만들어지는 요청이 아니라, planned flow의 특정 node를 구체화한 런타임 인스턴스다.
- operator는 packet 생성 전에 "이 packet이 어떤 node의 실행인가"를 먼저 명시적으로 판단해야 한다.
- 동일 actor가 여러 node를 맡을 수 있으면 actor 이름만으로 충분하지 않으므로 node 목적을 packet goal/why에 분명히 써야 한다.
- operator는 packet을 만들 때 node의 `packet_blueprint`를 concrete packet으로 구체화한다.
- 현재 schema에는 `node_id` 필드가 없으므로, packet `inputs`에 planned flow 문서 경로를 넣고 `goal/why`에서 현재 node 목적을 드러내는 것을 기본 연결 방식으로 둔다.

### 2. Actor는 packet 안에서 local plan을 세운다

- planned flow가 actor별 상세 구현 절차를 선생성해 두지는 않는다.
- actor는 packet을 받은 뒤, packet 범위 안에서 실행 순서와 세부 작업을 계획한다.
- 이 local plan은 trace에 반영될 수는 있어도 planned flow 자체를 대체하지 않는다.
- actor가 route 자체를 바꾸고 싶으면 구현 대신 trace feedback으로 escalation한다.

### 3. Decision은 허용 transition만 선택한다

- `accept`, `dispatch`, `rework`, `block`, `cancel`, `remediate`는 모두 flow 상 허용 transition과 연결돼야 한다.
- 허용되지 않은 transition을 탔다면 기본적으로 `orchestration failure`다.
- 허용 transition이 아예 현실과 맞지 않다면 `planned flow` 또는 WBS를 수정해야 한다.
- operator는 decision을 남길 때 어떤 transition을 택했는지 review summary나 rationale에서 설명하는 것이 좋다.

### 4. Route drift는 별도 실패로 본다

아래 경우는 구현 실패와 분리해서 본다.

- node 자체는 성공했는데 다음 packet 경로가 일관되지 않다
- 같은 조건에서 operator가 다른 node로 계속 dispatch한다
- trace는 충분한데 operator decision이 flow 밖 경로를 선택한다

이 경우 기본 원인은 actor가 아니라 routing/modeling layer다.

### 5. 반복 루프는 상위 레이어로 승격한다

- 같은 node rework가 반복되면 packet 품질 문제일 수 있다.
- 같은 transition ambiguity가 반복되면 planned flow 문제다.
- 같은 slice에서 node를 계속 새로 늘려야만 진행되면 WBS 문제일 가능성이 높다.

## 평가 질문

operator 또는 향후 validator는 최소한 아래를 점검하는 것이 좋다.

1. 현재 packet이 어떤 planned node를 실행하는지 설명 가능한가
2. 이번 decision이 허용 transition 중 하나인가
3. transition 조건을 만족하는 증거가 trace에 남았는가
4. 같은 loop가 반복될 때 escalation 규칙이 발동했는가
5. node 실패와 route 실패를 구분해 기록했는가

## 현재 저장소에 적용하는 방식

이 저장소의 현재 schema는 아직 `planned_flow_id`나 `node_id`를 runtime artifact 필수 필드로 요구하지 않는다.
따라서 당장은 아래 원칙으로 운영한다.

1. operator가 slice 준비 단계에서 `context/wbs/flows/<slice_id>.flow.vN.md`를 만든다.
2. 첫 packet부터 `inputs`에 해당 flow 문서 경로를 포함한다.
3. packet `goal/why`는 현재 node 목적을 반영해 "이 packet이 flow 어디에 있는가"를 드러낸다.
4. operator decision은 해당 flow의 허용 transition과 비교해 `accept`, `dispatch`, `rework`, `block` 등을 선택한다.
5. 경로 규칙을 바꿔야 하면 새 flow 버전을 만들고 이후 packet이 그 버전을 참조하게 한다.
6. schema 확장은 planned flow 운영이 안정화된 뒤 별도 단계에서 진행한다.
