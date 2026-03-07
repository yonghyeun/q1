# Orchestration Flow

수동 오케스트레이션 기반 멀티 에이전트 개발에서,
handoff packet과 trace가 어떻게 생성·이동·축적되고
오퍼레이터가 어떤 기준으로 판단하는지의 전체 흐름을 정의한다.

이 문서는 `agent-handoff-schema.md`의 상위 운영 플로우 문서다.
`trace`는 이 문서에서도 개별 packet 실행 기록을 뜻하며,
packet route 자체는 `planned-flow.md`가 정의하는 node / transition 모델로 다룬다.

## 목적

- WBS, handoff packet, trace, operator decision, run ledger의 역할을 구분한다.
- packet 생성 전에 고정해야 하는 planned flow를 명시한다.
- "누가 지금 무엇을 들고 있는가"를 한 번에 이해할 수 있게 한다.
- 완료, 재작업, blocked, remediation(되돌림/수정) 흐름을 표준화한다.
- 실패 조건, 평가 기준, 피드백 루프를 명시한다.
- 추후 자동 오케스트레이션으로 승격 가능한 control-plane을 설계한다.

## 기본 운영 모델

- 기본 운영자는 사람(operator)이다.
- 전문화된 에이전트는 필요 시에만 투입한다.
- handoff는 "한 actor가 다른 actor에게 ownership을 넘기는 행위"다.
- actor는 사람(operator) 또는 에이전트(`spec`, `impl`, `test`, `integration`)일 수 있다.

핵심은 "에이전트가 몇 개인가"보다 아래 4개가 안정적인가다.

1. WBS가 안정적인가
2. planned flow가 안정적인가
3. handoff packet이 명확한가
4. trace가 판정 가능하게 누적되는가

## 핵심 아티팩트

### 1. WBS

- 계획의 SoT
- slice 정의, 선후관계, 기본 AC, abstract ownership / verification 경계를 가진다

### 2. Planned Flow

- routing / transition 계획의 SoT
- 어떤 node가 있고 어떤 경로가 허용되는지, 어떤 loop에서 상위 재설계로 승격할지를 가진다
- 현재 단계에서는 node별 상세 실행 계획이 아니라 packet blueprint까지를 고정하는 문서다

### 3. Handoff Packet

- immutable runtime work order
- 이번 ownership transfer에서 무엇을 맡길지 정의한다

### 4. Trace

- append-only 실행 기록
- 실제 변경, 테스트, 결정, blocker, risk와 실행 상태를 남긴다

### 5. Run Ledger

- orchestration control-plane
- 현재 어떤 slice가 누구 손에 있고, 다음 판단이 무엇인지 보여준다

### 6. Operator Decision

- operator의 상태 전이 기록
- 어떤 trace를 보고 어떤 판정을 내렸는지와, ledger 갱신의 근거를 남긴다

## 아티팩트 간 관계

권장 관계는 아래와 같다.

- `1 WBS slice -> 1 planned flow`
- `1 planned flow -> N packets`
- `1 packet -> N trace entries`
- `1 run ledger(current) -> N slices / packets / decisions`
- `1 run ledger(snapshot) -> 1 decision checkpoint`

즉, WBS는 오래 살고, planned flow는 slice의 허용 경로를 고정하며,
packet은 handoff마다 생기고, trace는 packet 실행 중 누적된다.

## 상태 소유권

현재 상태는 아래처럼 나누는 것을 권장한다.

- `planned flow`: 허용된 node / transition / exception loop
- `packet`: handoff 명세를 담는 불변 문서
- `trace.execution_state`: 개별 실행의 상태
- `operator decision`: 상태 전이와 판정 사유
- `run ledger.slice_state`: slice의 현재 상태
- `run ledger.current_packet_id`: slice 기준 최신 packet이 무엇인지

이 분리를 하지 않으면 packet이 계획과 상태를 동시에 들고 다니게 되어 drift가 커진다.

## 전체 흐름

### 0. Slice 준비

operator가 WBS에서 다음 slice를 고른다.

이 단계에서 최소한 아래가 준비되어 있어야 한다.

- `slice_id`
- `goal`
- `contracts`
- `acceptance criteria`
- `owned_scope`
- `verification_requirements`

이 기준이 충족되지 않으면 아직 orchestration-ready가 아니다.

여기서 중요한 점은,
WBS는 concrete file path나 concrete test command를 직접 고정하지 않는다는 것이다.

- `owned_scope`는 기능/모듈 수준 ownership boundary다
- `verification_requirements`는 필요한 검증 증거 수준이다

실제 `owned_paths`와 `required_tests`는
planned flow의 packet blueprint를 거쳐 packet 단계에서 구체화한다.

### 0.5. Planned flow 고정

operator는 packet을 만들기 전에 slice의 planned flow를 먼저 고정한다.

최소한 아래가 정의돼 있어야 한다.

- 시작 node
- terminal node
- 허용된 node와 transition
- node별 기본 owner / 목적
- `rework`, `block`, `remediate`, `cancel` 같은 예외 경로
- 반복 실패 시 WBS 또는 flow 재검토로 승격하는 기준

이 단계가 없으면 packet은 만들어져도
"원래 어떤 경로 위에서 움직여야 하는가"를 판정할 수 없다.

기본 작성 책임은 operator에게 둔다.

- 권장 저장 위치는 `context/wbs/flows/<slice_id>.flow.vN.md`다.
- 사람이 초안을 만들 때는 `templates/planned-flow.template.md`를 사용한다.
- 경로 규칙이 실질적으로 바뀌면 기존 문서를 덮어쓰기보다 새 버전을 발행한다.
- 현재 기본값은 `compiled flow`가 아니라 `blueprint flow`다.

### 1. Packet 생성

operator는 WBS slice와 planned flow의 현재 node에서 handoff packet을 만든다.

이 packet은 아래를 담는다.

- 어떤 actor가 맡을지
- 어떤 planned node의 실행인지
- 이번 handoff에서 필요한 입력만 무엇인지
- 이번 handoff의 비목표는 무엇인지
- 어떤 결과 형식으로 되돌아와야 하는지

즉, packet은 WBS 전체를 복제하는 것이 아니라,
WBS와 planned flow의 일부를 실행 가능한 요청으로 얇게 투영(projection)한 것이다.
packet 자체는 발행 후 가능한 한 불변으로 유지하고,
현재 실행 상태는 trace, operator decision, run ledger에서 관리한다.

현재 schema에는 `planned_flow_id`나 `node_id`가 없으므로,
packet `inputs`에 planned flow 문서 경로를 넣고
`goal/why`에서 현재 node 목적을 드러내는 것을 기본 연결 방식으로 사용한다.

operator는 이때 planned flow의 `packet blueprint`를 바탕으로
이번 transition에 필요한 concrete packet을 만든다.

즉, operator는 packet을 만들 때 아래를 수행한다.

- WBS의 `owned_scope`를 현재 node 목적에 맞는 `owned_paths`로 내린다
- WBS의 `verification_requirements`를 현재 node에서 요구할 `required_tests`로 내린다

### 2. Packet 할당

packet은 특정 actor에게 전달된다.

- operator -> impl
- operator -> test
- operator -> integration
- agent -> operator
- agent -> agent

다만 사람이 control-plane을 유지하는 현재 단계에서는
`operator -> agent -> operator` 패턴을 기본값으로 권장한다.

에이전트끼리 직접 handoff하는 흐름은 추후 자동화 단계에서 점진적으로 허용한다.

### 3. 실행과 Trace 누적

packet을 받은 actor는 작업을 수행하며 trace를 남긴다.
세부 구현 순서와 작업 분해는 actor가 packet을 받은 뒤 local plan으로 세운다.

trace는 최소한 아래를 포함한다.

- 실제 변경 파일
- 실행한 테스트
- 실행하지 못한 테스트와 이유
- 새로 생긴 결정
- blocker / risk
- `execution_state`
- 다음 권장 액션

핵심은 "무엇을 했는가"보다 "왜 지금 다음 판단이 가능한가"가 trace에 드러나야 한다는 점이다.

### 3.5. 자기 평가와 피드백 방출

actor는 작업 종료 시 단순히 결과만 반환하지 않고,
이번 handoff를 어떻게 평가하는지까지 함께 반환해야 한다.

최소한 아래 질문에 답해야 한다.

- handoff goal에 비춰 `success`, `partial`, `failed` 중 무엇인가
- 실패했다면 주요 원인이 `implementation`, `contract`, `missing_input`, `harness`, `orchestration`, `wbs` 중 무엇인가
- 다음 액션은 `accept`, `rework`, `block`, `cancel`, `remediate` 중 무엇을 권장하는가
- 이 피드백은 `packet`, `wbs`, `contracts`, `harness`, `orchestration` 중 어디로 되돌아가야 하는가

이 단계가 없으면 operator는 "실행 결과"는 보지만 "시스템 학습"은 하지 못한다.

### 4. Operator 판정

operator는 trace, 결과물, 테스트 결과를 보고 아래 중 하나를 결정한다.
이 판정은 `operator decision event`로 별도 기록한다.
이때 operator는 자유 형식으로 다음 packet을 발행하는 것이 아니라,
planned flow가 허용한 transition 중 하나를 선택해야 한다.

operator는 최소한 아래 평가 기준을 체크해야 한다.

1. handoff goal이 실제로 전진했는가
2. acceptance criteria 충족 증거가 있는가
3. required tests가 충족됐는가
4. contracts / owned paths 위반이 없는가
5. trace가 다음 판단에 충분한가
6. 선택하려는 다음 transition이 planned flow에 존재하는가

아래 중 하나라도 해당하면 `done`으로 넘기지 않는다.

- required tests가 빠졌는데 설명이 없다
- contract violation이 열려 있다
- owned paths 밖 변경이 정당화되지 않았다
- acceptance criteria 충족 여부를 trace만으로 판단할 수 없다
- planned flow에 없는 경로로만 다음 packet을 설명할 수 있다
- 실패 원인이 WBS/harness/orchestration인데 packet rework로만 덮으려 한다

#### A. Accept

- 현 handoff 목적을 충족했고
- 현재 packet을 닫아도 될 때
- operator는 `accept` decision을 남기고 현재 handoff 종료를 승인한다
- decision 직후 snapshot ledger를 남긴다
- 다음 actor handoff가 필요하면 ledger에는 `next_operator_decision: dispatch`를 남긴다

예:
- impl handoff 완료 -> current packet을 `accept`
- integration handoff 완료 -> current packet을 `accept`

#### B. Dispatch

- 다음 actor packet이 준비됐을 때
- operator는 새 packet을 만들고 별도 `dispatch` decision/event를 남긴다
- operator UX에서 한 번에 처리하더라도 artifact는 `accept` 다음 `dispatch` 순서로 기록한다
- `dispatch`는 기본적으로 current ledger만 갱신하고 snapshot은 생략한다
- dispatch 대상은 planned flow가 허용한 다음 node여야 한다
- operator는 review summary 또는 rationale에서 어떤 transition을 택했는지 설명하는 편이 좋다

예:
- impl handoff `accept` 직후 -> integration packet `dispatch`
- integration handoff `accept` 직후 -> test/harness packet `dispatch`

#### C. Rework

- 방향은 맞지만 미완성/불충분할 때
- 기존 packet/trace는 유지하고 새 packet으로 재지시한다
- `supersedes_packet_id`와 decision event로 lineage를 연결한다
- 일반적으로 같은 planned node 안에서 새 packet을 다시 발행한다

핵심은 "과거 기록 삭제"가 아니라 "새 시도 생성"이다.

권장 사용 사례:

- 구현은 맞지만 required tests가 부족함
- packet 설명이 불충분해서 같은 slice 내 재시도가 필요함

#### D. Block

- 외부 결정, 누락된 계약, 미준비 의존성 때문에 더 진행할 수 없을 때
- `trace.execution_state`와 `run ledger.slice_state`를 `blocked`로 반영한다
- blocked decision 직후 snapshot ledger를 남긴다
- blocked에서 빠져나오는 경로도 planned flow에 정의돼 있어야 한다

권장 사용 사례:

- 의존 계약이 아직 결정되지 않음
- 상위 slice 완료 없이는 판정 불가
- operator 또는 사람 승인 없이는 더 진행하면 위험함

#### E. Cancel

- 이 handoff 자체가 잘못 정의됐거나, slice 경계를 다시 쪼개야 할 때
- run ledger에서 해당 packet을 `cancelled` disposition으로 기록하고 WBS를 수정하거나 재분할한다
- cancel decision 자체도 별도 decision event로 남긴다
- cancel이 반복된다면 packet 문제가 아니라 flow 또는 WBS 경계 문제가 먼저 의심된다

권장 사용 사례:

- slice가 너무 크거나 여러 ownership이 얽힘
- AC 자체가 모순되거나 handoff 대상이 잘못 지정됨

#### F. Remediate / Revert

- 잘못된 변경이 이미 반영됐고, 되돌림 또는 수정이 필요할 때
- trace를 지우지 않고 remediation packet을 새로 만든다
- remediation packet 발행 전 decision event를 먼저 남긴다
- remediation도 즉흥 분기가 아니라 별도 예외 node/transition으로 계획돼 있는 편이 좋다

리버트는 기록 삭제가 아니라 "새로운 corrective action"으로 남기는 것이 원칙이다.

### 5. 완료 처리

최종적으로 아래가 충족되면 slice를 완료로 본다.

- acceptance criteria 충족
- required tests 충족
- contract violation 없음
- 다음 actor가 더 이상 필요하지 않음

완료 시 operator는:

- decision event를 남기고
- run ledger에서 current packet을 `closed` 또는 `superseded`로 기록하고
- current ledger를 갱신하며
- 해당 decision 시점 snapshot ledger를 남기고
- WBS slice를 완료 처리한다

## 정렬과 checkpoint

- runtime artifact는 모두 `run-local seq`를 가진다.
- 시간값은 참고 정보이고, ordering 정본은 `seq`다.
- `current ledger`는 각 run당 1개만 유지한다.
- `snapshot ledger`는 decision 직후 append-only로 저장한다.

## 실패 분류와 대응 규칙

같은 `failed`라도 대응은 다를 수 있다.

### 1. Implementation failure

- 증상: 구현 미완성, 로직 버그, 테스트 실패
- 기본 대응: 같은 slice 내 rework packet 생성

### 2. Contract failure

- 증상: 타입/응답/스토리지/이벤트 계약 불일치
- 기본 대응: contract owner review 또는 contract update 판단
- 주의: 단순 재작업으로 덮으면 병렬 슬라이스 전체에 재작업이 전파될 수 있다

### 3. Missing input failure

- 증상: 선행 정보, 의존 slice, 승인, fixture 부족
- 기본 대응: `blocked`

### 4. Harness failure

- 증상: fake adapter 불안정, fixture 오류, validator 문제, flaky test
- 기본 대응: harness remediation packet 생성
- 주의: 구현 에이전트 실패로 오인하지 않는다

### 5. Orchestration failure

- 증상: handoff packet 부족, ownership 불명확, routing 실수, planned flow 밖 transition 선택
- 기본 대응: packet schema 또는 operator 절차 피드백 반영
- 주의: node 자체 수행이 맞았더라도 edge 선택이 틀리면 orchestration failure다

### 6. WBS failure

- 증상: slice 경계가 잘못됐거나 AC 자체가 판정 불가능
- 기본 대응: slice 재분할 또는 WBS 수정
- planned flow를 계속 늘려도 설명이 안 되면 planning layer를 먼저 고친다
- 주의: 이 경우 packet 수를 더 늘리기 전에 planning layer를 고친다

## 상태 모델

상태는 slice 수준, trace 수준, ledger 수준을 분리해서 보는 것이 좋다.

### Slice 상태

- `planned`
- `ready`
- `active`
- `blocked`
- `integration_review`
- `done`
- `cancelled`

### Trace 실행 상태

- `in_progress`
- `blocked`
- `review_required`
- `done`

### Run Ledger packet disposition

- `issued`
- `active`
- `closed`
- `superseded`
- `cancelled`

slice 상태와 trace 상태, packet disposition을 하나로 섞으면 operator가 전체 진행률과 현재 handoff 상태를 혼동하게 된다.

## Run Ledger에 꼭 있어야 할 것

run ledger는 다음 질문에 즉시 답할 수 있어야 한다.

- 지금 활성화된 slice는 무엇인가
- 각 slice의 최신 packet은 무엇인가
- 현재 owner는 누구인가
- 마지막 trace 시각은 언제인가
- 다음 operator decision은 무엇인가
- blocked 이유는 무엇인가
- 최근 실패 유형은 무엇인가
- 아직 반영되지 않은 feedback item은 무엇인가
- current packet의 disposition은 무엇인가

즉, run ledger는 "현재 상황판"이며,
operator 또는 향후 operator agent가 가장 먼저 보는 entry point다.

## 피드백 루프

오케스트레이션은 "작업 전달"뿐 아니라 "시스템 수정"의 루프를 가져야 한다.

권장 루프는 아래와 같다.

1. actor가 trace에 결과와 실패 유형을 남긴다
2. operator가 즉시 packet 판정을 내린다
3. operator가 필요하면 상위 대상에 feedback item을 기록한다
4. feedback item은 아래 중 하나로 흘러간다
   - packet 수정
   - WBS 수정
   - contracts 수정
   - harness 수정
   - orchestration 규칙 수정
5. 동일 실패가 반복되면 run ledger에 escalation 표시를 남긴다

중요한 점은, feedback이 "다음 packet 지시"에만 머무르면 안 된다는 것이다.
반복 실패가 관찰되면 상위 문서와 운영 규칙까지 되돌아가야 한다.

## 표준 흐름 예시

`S1: timestamp-insert` slice가 있다고 가정한다.

1. operator가 WBS에서 `S1`을 선택한다
2. `F1(impl -> integration -> test -> done, rework/block loop 포함)` planned flow를 고정한다
3. `P1(operator -> impl)` 생성
4. impl이 코드 작성 후 `T1` trace 기록
5. operator가 `F1`의 허용 transition과 비교해 검토한다
6. impl handoff를 `accept` decision으로 닫는다
7. `P2(operator -> integration)`를 만들고 `dispatch` decision으로 발행한다
8. integration이 wiring 확인 후 `T2` 기록
9. operator가 다시 `F1` 기준으로 다음 edge를 선택한다
10. integration handoff를 `accept` decision으로 닫는다
11. `P3(operator -> test)`를 만들고 `dispatch` decision으로 발행한다
12. test/harness가 검증 후 `T3` 기록
13. operator가 slice `S1`을 `done`으로 마감

방향이 잘못됐으면:

- `P1`이나 `P2`의 기록은 남기고
- `P4(operator -> impl, rework)` 또는 remediation packet을 새로 만든다

harness가 불안정했다면:

- `T3`에는 `failure_type: harness`와 feedback target이 기록되고
- operator는 `P4(operator -> harness-remediation)`를 먼저 만든 뒤
- 검증 환경이 안정화된 후 다시 `test` handoff를 재개한다

## 자동화 경계

초기에는 사람이 아래를 직접 한다.

- slice 선택
- packet 생성
- trace 해석
- accept/rework/block/cancel 판정

자동화는 아래 순서로 점진 도입한다.

1. packet completeness validator
2. trace summarizer
3. run ledger updater
4. low-risk routing suggestion
5. low-risk auto-dispatch
6. policy-bounded operator automation

중요한 원칙은,
"지금 operator가 하는 판단을 설명할 수 있을 때만 자동화한다"는 점이다.
이 설명 가능성은 trace뿐 아니라 planned flow가 먼저 안정돼 있어야 확보된다.

## 실패 패턴

아래 징후가 보이면 orchestration 설계가 흔들리고 있다는 신호다.

- packet이 사실상 WBS 전체 복사본이 된다
- trace가 결과 자랑만 있고 판정 근거가 없다
- run ledger 없이 채팅 로그만 뒤져야 현재 상태를 알 수 있다
- blocked와 rework를 구분하지 못한다
- remediation이 기존 기록 삭제로 처리된다

## 이 저장소 기준 권장안

- `agent-handoff-schema.md`는 packet/trace 구조를 정의한다
- `planned-flow.md`는 packet이 따라야 할 node / transition 모델을 정의한다
- `templates/planned-flow.template.md`는 planned flow 산출물 형태를 고정한다
- 이 문서는 end-to-end flow와 decision loop를 정의한다
- 실제 운영 시에는 WBS, planned flow, packet, trace, run ledger를 5층으로 분리한다
- node별 상세 pre-plan을 모두 연결한 `compiled flow`는 현재 기본 운영이 아니라 미래 옵션이다
- 자동 오케스트레이션은 planned flow, run ledger, trace schema가 충분히 안정화된 뒤에만 시도한다
