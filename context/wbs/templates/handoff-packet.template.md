# Handoff Packet Template

이 템플릿은 사람이 handoff packet을 초안 작성하거나 검토할 때 사용한다.
자동 생성이 필요하면 `context/wbs/schemas/handoff-packet.schema.json`과
`scripts/repo/codex_wbs_emit.sh`를 우선 사용한다.

```yaml
packet_id: H-YYYY-MM-DD-001
run_id: RUN-YYYY-MM-DD-A
seq: 1
slice_id: SLICE-ID
parent_wbs: mvp-wbs/v1
owner_role: impl
handoff_from: operator
handoff_to: impl
supersedes_packet_id: H-YYYY-MM-DD-000
goal: 한 문장 목표
why: 왜 이 handoff가 필요한가
inputs:
  - path/to/input.md:1
contracts:
  - docs/product/contracts/domain.ts
acceptance_criteria:
  - 측정 가능한 완료 조건 1
owned_paths:
  - apps/web/src/features/example/**
non_goals:
  - 이번 handoff에서 하지 않을 것
dependencies:
  - 선행 의존성
required_tests:
  - unit
validator_rules:
  - inputs_resolve
review_rubric:
  - acceptance_criteria_evidenced
escalation_policy:
  on_block: operator_review
expected_outputs:
  - code_changes
  - tests
  - trace_summary
open_risks:
  - 알려진 위험
```

## Notes

- `packet`은 불변 명세에 가깝게 유지한다.
- 재작업은 기존 packet 수정이 아니라 새 packet 발행 + `supersedes_packet_id` 연결로 표현한다.
- 실행 상태는 `trace`와 `run ledger`가 책임진다.
- 경로는 가능하면 링크 가능한 repo-relative path를 사용한다.
