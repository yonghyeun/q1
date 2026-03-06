# Trace Summary Template

이 템플릿은 사람이 trace를 남기거나 리뷰할 때 사용한다.
자동 생성이 필요하면 `context/wbs/schemas/trace-summary.schema.json`과
`scripts/repo/codex_wbs_emit.sh`를 우선 사용한다.

```yaml
trace_id: T-YYYY-MM-DD-001
packet_id: H-YYYY-MM-DD-001
agent_role: impl
execution_state: review_required
result: partial
failure_type: orchestration
started_at: 2026-03-06T10:00:00+09:00
ended_at: 2026-03-06T10:24:00+09:00
changes:
  - apps/web/src/example.ts
tests_run:
  - pnpm test -- example
tests_not_run:
  - e2e not available yet
decisions_made:
  - 새 결정
blockers:
  - 없음
risks:
  - 남아 있는 위험
feedback:
  - target: packet
    severity: must_fix
    note: inputs 명세가 부족함
requested_decision: rework
next_action: 다음 actor가 해야 할 액션
confidence: medium
```

## Notes

- trace는 append-only 이력으로 남긴다.
- 실패는 actor 비난보다 수정 대상 레이어 분류를 우선한다.
