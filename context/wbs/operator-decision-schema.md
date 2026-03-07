# Operator Decision Schema

이 문서는 operator가 trace를 검토한 뒤 상태 전이를 기록하는 `operator decision event` 표준을 정의한다.

## 왜 별도 decision artifact가 필요한가

`trace`는 actor의 실행 결과다.
반면 `accept`, `rework`, `block`, `cancel`, `remediate`, `close`는 operator의 통제 판단이다.

둘을 하나로 섞으면 아래 문제가 생긴다.

- 실행 결과와 통제 판단의 책임이 섞인다
- operator의 상태 변화 사유를 audit하기 어렵다
- run ledger가 어떤 decision을 근거로 갱신됐는지 연결이 약해진다

따라서 operator 판정은 별도 artifact로 남기는 것을 권장한다.

## 권장 스키마

```yaml
decision_id: D-2026-03-06-001
run_id: RUN-2026-03-06-A
seq: 3
slice_id: MVP-TS-INSERT
packet_id: H-2026-03-06-001
reviewed_trace_ids:
  - T-2026-03-06-014
made_at: 2026-03-06T12:30:00+09:00
operator_actor: operator
decision: rework
review_summary: 구현 방향은 맞지만 packet 입력이 부족해 다음 actor가 판단 가능한 수준에 도달하지 못했다.
reason_code: bad_handoff
reason_detail: editor command surface 입력이 빠져 integration 판단이 불가능했다.
slice_state_before: active
slice_state_after: active
packet_disposition_before: active
packet_disposition_after: superseded
next_packet_id: H-2026-03-06-002
updated_current_ledger_ref: context/wbs/runs/RUN-2026-03-06-A/current.run-ledger.json
snapshot_ref: context/wbs/runs/RUN-2026-03-06-A/snapshots/0003.rework.run-ledger.json
feedback_applied:
  - target: packet
    action: packet inputs에 editor command surface 명세를 추가했다.
feedback_opened:
  - target: wbs
    severity: should_fix
    note: impl handoff와 integration handoff를 분리 검토한다.
context_notes:
  - 구현자 실패보다 handoff 품질 부족으로 분류했다.
```

## 필드 설명

- `decision_id`: operator decision 식별자
- `run_id`: 소속 orchestration run
- `seq`: run 내부 총순서
- `slice_id`: 대상 WBS slice
- `packet_id`: 검토 대상 packet
- `reviewed_trace_ids`: 판정 근거가 된 trace 목록
- `made_at`: decision 시각
- `operator_actor`: 판정을 내린 actor
- `decision`: 상태 전이 종류
- `review_summary`: operator가 본 핵심 판정 요약
- `reason_code`: 기계적 분류용 사유 코드
- `reason_detail`: 사람이 읽는 판단 근거
- `slice_state_before/after`: slice 상태 전이
- `packet_disposition_before/after`: packet disposition 전이
- `next_packet_id`: 후속 packet이 있으면 참조
- `updated_current_ledger_ref`: 갱신된 current ledger 경로
- `snapshot_ref`: snapshot checkpoint를 남긴 decision이면 그 snapshot ledger 경로
- `feedback_applied`: 이번 decision에서 실제 반영한 피드백
- `feedback_opened`: 남겨 둔 후속 피드백
- `context_notes`: 후속 operator/automation이 알아야 할 맥락

## 권장 reason code

- `goal_met`
- `insufficient_evidence`
- `missing_input`
- `bad_handoff`
- `contract_violation`
- `harness_issue`
- `slice_redesign_needed`
- `corrective_action_needed`

## 운영 규칙

- operator decision은 `trace`를 대체하지 않는다. trace를 검토한 후 별도로 생성한다.
- `rework`, `block`, `cancel`, `remediate`, `accept`, `close` decision은 `snapshot ledger`를 남기고 `snapshot_ref`를 연결한다.
- `dispatch`는 기본적으로 current ledger만 갱신하고 `snapshot_ref`는 생략한다. 다만 운영상 checkpoint가 필요하면 예외적으로 남길 수 있다.
- `current ledger` 갱신은 decision event 이후에만 일어나는 것을 기본값으로 둔다.
