# Run Ledger Template

이 템플릿은 사람이 현재 orchestration 상태를 정리할 때 사용한다.
자동 갱신이 필요하면 `context/wbs/schemas/run-ledger.schema.json`과
validator/harness 경로를 우선 사용한다.

```yaml
run_id: RUN-YYYY-MM-DD-A
ledger_kind: current
projection_seq: 6
parent_wbs: mvp-wbs/v1
updated_at: 2026-03-06T12:30:00+09:00
slice_entries:
  - slice_id: SLICE-ID
    slice_state: active
    current_owner: impl
    active_packet_id: H-YYYY-MM-DD-001
    active_packet_disposition: active
    latest_trace_id: T-YYYY-MM-DD-001
    latest_execution_state: review_required
    latest_result: partial
    recent_failure_type: orchestration
    latest_decision_id: D-YYYY-MM-DD-001
    latest_decision: rework
    latest_decision_at: 2026-03-06T12:20:00+09:00
    next_operator_decision: rework
    open_feedback:
      - target: packet
        severity: must_fix
        note: inputs 명세 보강 필요
    packet_history:
      - packet_id: H-YYYY-MM-DD-001
        disposition: superseded
        trace_count: 1
        latest_trace_id: T-YYYY-MM-DD-001
        latest_result: partial
        superseded_by_packet_id: H-YYYY-MM-DD-002
        recent_trace_refs:
          - T-YYYY-MM-DD-001
    updated_at: 2026-03-06T12:30:00+09:00
```

## Notes

- ledger는 current state SoT다.
- snapshot ledger는 같은 스키마를 쓰되 `ledger_kind: snapshot`, `source_decision_id`, `source_seq`를 포함한다.
- packet/trace 원문을 덮어쓰지 않고, 현재 상태만 요약한다.
