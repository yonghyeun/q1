# Run Ledger Schema

run ledger는 수동 오케스트레이션의 상태 projection이다.

이 문서는 `agent-handoff-schema.md`가 정의한 `packet`/`trace`를
실행 시점의 상태와 연결해 주는 control-plane 스키마를 정의한다.

## 목적

- 지금 어떤 slice가 활성 상태인지 한 번에 보여준다.
- current packet, 최신 trace, 다음 operator decision을 연결한다.
- 실패 유형과 미반영 feedback을 누적해 재작업과 구조 개선을 구분한다.
- 추후 자동 오케스트레이션이 읽을 상태 정본을 마련한다.
- current 상태와 snapshot checkpoint를 분리한다.

## 왜 별도 ledger가 필요한가

`packet`은 handoff 명세다.
`trace`는 실행 기록이다.

둘만으로는 아래 질문에 즉시 답하기 어렵다.

- 지금 기준 packet은 무엇인가
- 어떤 slice가 blocked 상태인가
- 어떤 feedback이 아직 반영되지 않았는가
- 다음 operator 판단이 무엇인가

그래서 run ledger는 "현재 상태"만 모아 둔 별도 문서로 관리한다.

## 표준적 역할 분리

- `WBS`: 계획의 SoT
- `packet`: handoff 명세
- `trace`: 실행 이력
- `operator decision`: 상태 전이 기록
- `run ledger`: 현재 상태 projection 또는 snapshot projection

중요한 원칙은, packet에 runtime 상태를 넣지 않고 ledger가 현재 상태를 소유하게 하는 것이다.

현재 schema는 runtime artifact가 이미 발행된 slice를 주 대상으로 본다.
packet 발행 전 `planned`/`ready` slice까지 ledger에 넣을지는 `open-questions.md`에서 별도 합의한다.

## 권장 스키마

```yaml
run_id: RUN-2026-03-06-A
ledger_kind: current
projection_seq: 6
parent_wbs: mvp-wbs/v1
updated_at: 2026-03-06T12:30:00+09:00
slice_entries:
  - slice_id: MVP-TS-INSERT
    slice_state: active
    current_owner: impl
    current_packet_id: H-2026-03-06-001
    current_packet_disposition: active
    latest_trace_id: T-2026-03-06-014
    latest_execution_state: review_required
    latest_result: partial
    recent_failure_type: orchestration
    latest_decision_id: D-2026-03-06-001
    latest_decision: rework
    next_operator_decision: rework
    open_feedback:
      - target: packet
        severity: must_fix
        note: editor command surface 입력 명세를 보강해야 함
    packet_history:
      - packet_id: H-2026-03-06-001
        disposition: superseded
        trace_count: 1
        latest_trace_id: T-2026-03-06-014
        latest_result: partial
        superseded_by_packet_id: H-2026-03-06-002
        recent_trace_refs:
          - T-2026-03-06-014
    updated_at: 2026-03-06T12:30:00+09:00
```

## 필드 설명

- `run_id`: 현재 orchestration run 식별자
- `ledger_kind`: `current | snapshot`
- `projection_seq`: 이 ledger projection이 반영한 마지막 event seq
- `parent_wbs`: 어떤 WBS 버전을 기준으로 ledger를 해석해야 하는지
- `updated_at`: ledger 전체 갱신 시각
- `slice_entries`: slice별 현재 상태 엔트리 목록

각 `slice_entry`는 최소한 아래를 포함하는 것을 권장한다.

- `slice_id`: WBS slice 식별자
- `slice_state`: slice 전체 상태
- `current_owner`: 현재 owner role 또는 actor
- `current_packet_id`: 현재 projection 기준 packet
- `current_packet_disposition`: current packet의 disposition
- `latest_trace_id`: 가장 최근 trace
- `latest_execution_state`: 가장 최근 trace의 실행 상태
- `latest_result`: 최신 자기 평가 결과
- `recent_failure_type`: 최근 실패 유형
- `latest_decision_id`: 최신 operator decision
- `latest_decision`: 최신 operator decision 종류
- `next_operator_decision`: operator가 다음에 내려야 할 판단
- `open_feedback`: 아직 반영되지 않은 feedback item
- `packet_history`: packet lineage와 trace 요약을 함께 가진 참조 목록
- `updated_at`: slice 엔트리 마지막 갱신 시각

여기서 `current_packet`은 반드시 `active` 상태 packet만 뜻하지 않는다.
가장 최근 operator 판단 기준이 된 packet을 가리키며, 따라서 `closed`나 `superseded`일 수도 있다.

## 상태 권장안

### Slice 상태

- `planned`
- `ready`
- `active`
- `blocked`
- `integration_review`
- `done`
- `cancelled`

### Packet disposition

- `issued`
- `active`
- `closed`
- `superseded`
- `cancelled`

### Operator decision

- `dispatch`
- `accept`
- `rework`
- `block`
- `cancel`
- `remediate`
- `close`

## 표준 운영 규칙

### 1. Current ledger가 최신 상태의 정본이다

- 현재 누가 무엇을 들고 있는지 판단할 때는 packet이나 trace가 아니라 ledger를 먼저 본다.
- packet과 trace는 ledger가 가리키는 참조 대상이다.

### 2. Packet은 불변, ledger는 갱신

- packet은 발행 후 가능한 한 수정하지 않는다.
- 상태 변경은 ledger entry 갱신으로 표현한다.

### 3. Trace/decision은 이력, ledger는 projection

- trace는 append-only로 남긴다.
- decision도 append-only로 남긴다.
- current ledger는 최신 정보만 요약해 보여준다.
- snapshot ledger는 특정 decision 시점의 frozen projection을 남긴다.

### 4. Feedback은 ledger에서 추적

- `feedback`이 trace에만 있으면 현재 미반영 항목을 놓치기 쉽다.
- 미반영 feedback은 ledger의 `open_feedback`으로 끌어올려 추적한다.

## 최소 검증 규칙

run ledger validator가 있다면 최소한 아래를 검사하는 것이 좋다.

- `slice_id`가 WBS에 존재하는가
- `current_packet_id`가 실제 packet 문서와 연결되는가
- `latest_trace_id`가 실제 trace 문서와 연결되는가
- `latest_decision_id`가 실제 decision 문서와 연결되는가
- `latest_execution_state`와 `current_packet_disposition`이 모순되지 않는가
- `slice_state: done`인데 `next_operator_decision`이 남아 있지 않은가

## 표준적 trade-off

### 장점

- 현재 상태 확인이 빨라진다
- operator와 자동화 모두 동일한 상태 정본을 읽을 수 있다
- 실패와 feedback 누적을 구조적으로 추적할 수 있다

### 단점

- packet, trace, decision, ledger의 4중 구조를 관리해야 한다
- current ledger와 snapshot ledger 갱신 discipline이 없으면 금방 stale해질 수 있다

## 이 저장소 기준 권장안

- current ledger와 snapshot ledger를 구분한다
- packet/trace/decision 문서와 분리해 현재 상태 projection만 담는다
- active slice 수가 적더라도 early stage부터 ledger를 두는 편이 낫다
- 자동 오케스트레이션은 ledger가 stale하지 않게 유지될 때만 시도한다
