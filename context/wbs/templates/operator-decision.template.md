# Operator Decision Template

이 템플릿은 사람이 operator decision event를 작성하거나 검토할 때 사용한다.
자동 생성이 필요하면 `context/wbs/schemas/operator-decision.schema.json`과
`scripts/repo/codex_wbs_emit.sh`를 우선 사용한다.

```yaml
decision_id: D-YYYY-MM-DD-001
run_id: RUN-YYYY-MM-DD-A
seq: 3
slice_id: SLICE-ID
packet_id: H-YYYY-MM-DD-001
reviewed_trace_ids:
  - T-YYYY-MM-DD-001
made_at: 2026-03-06T12:30:00+09:00
operator_actor: operator
decision: rework
review_summary: operator가 trace를 검토한 결과 요약
reason_code: bad_handoff
reason_detail: 왜 이 판정을 내렸는가
slice_state_before: active
slice_state_after: active
packet_disposition_before: active
packet_disposition_after: superseded
next_packet_id: H-YYYY-MM-DD-002
updated_current_ledger_ref: context/wbs/runs/RUN-YYYY-MM-DD-A/current.run-ledger.json
snapshot_ref: context/wbs/runs/RUN-YYYY-MM-DD-A/snapshots/0003.rework.run-ledger.json
feedback_applied:
  - target: packet
    action: 실제 반영한 변경
feedback_opened:
  - target: wbs
    severity: should_fix
    note: 남겨 두는 후속 피드백
context_notes:
  - 다음 판정자나 자동화가 알아야 할 맥락
```

## Notes

- decision은 operator의 상태 전이 기록이다.
- trace를 대체하지 않고, trace 검토 후 별도 artifact로 남긴다.
