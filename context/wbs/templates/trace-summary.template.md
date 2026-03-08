# Trace Summary Template

이 템플릿은 사람이 trace를 남기거나 리뷰할 때 사용한다.
자동 생성이 필요하면 `context/wbs/schemas/trace-summary.schema.json`과
`scripts/repo/codex_wbs_emit.sh`를 우선 사용한다.

```yaml
trace_id: T-YYYY-MM-DD-001
run_id: RUN-YYYY-MM-DD-A
seq: 2
packet_id: H-YYYY-MM-DD-001
slice_id: SLICE-ID
agent_role: impl
attempt_index: 1
execution_state: review_required
result: partial
failure_type: orchestration
started_at: 2026-03-06T10:00:00+09:00
ended_at: 2026-03-06T10:24:00+09:00
summary: 이번 실행의 핵심 상태 요약
artifacts_used:
  - docs/product/mvp-spec.md:61
changes:
  - apps/web/src/example.ts
tests_run:
  - command: pnpm test -- example
    result: passed
tests_skipped:
  - command: pnpm test -- example-integration
    reason_code: missing_input
    reason_detail: 왜 실행하지 못했는가
decisions_made:
  - 새 결정
new_facts:
  - 이번 실행으로 새로 드러난 사실
blockers: []
risks:
  - code: example_risk
    detail: 남아 있는 위험
feedback:
  - target: packet
    severity: must_fix
    note: inputs 명세가 부족함
requested_decision: rework
next_action: 다음 actor가 해야 할 액션
decision_rationale: 왜 이 requested_decision 을 권장하는가
context_notes:
  - 다음 actor/operator가 알아야 할 구체 맥락
confidence: medium
```

## Notes

- trace는 append-only 이력으로 남긴다.
- 테스트/스킵/리스크/블로커는 구조화된 객체 필드로 남긴다.
- 실패는 actor 비난보다 수정 대상 레이어 분류를 우선한다.
