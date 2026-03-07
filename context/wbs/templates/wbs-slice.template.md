# WBS Slice Template

이 템플릿은 slice별 WBS 초안을 작성하거나 검토할 때 사용한다.

현재 WBS는 concrete runtime detail을 직접 고정하지 않고,
`owned_scope`, `verification_requirements` 같은 planning-layer boundary를 정의한다.

```yaml
slice_id: SLICE-ID
parent_wbs: mvp-wbs/v1
status: planned
goal: 이 slice가 끝내는 사용자 가치
why: 왜 이 slice가 필요한가
contracts:
  - docs/product/contracts/example.md
acceptance_criteria:
  - 측정 가능한 완료 조건 1
owned_scope:
  - 기능/모듈/경계 수준의 ownership boundary
verification_requirements:
  - unit evidence required
dependencies:
  - 선행 slice 또는 선행 결정
non_goals:
  - 이번 slice에서 하지 않을 것
risks:
  - 시작 시점에 알려진 위험
assumptions:
  - 현재 기대하는 가정
open_questions:
  - planned flow 작성 전에 닫아야 하는 쟁점
notes:
  - 특이사항
```

## Notes

- `owned_scope`는 concrete file path가 아니라 ownership boundary를 적는다.
- `verification_requirements`는 concrete test command가 아니라 검증 의무 수준을 적는다.
- 실제 `owned_paths`, `required_tests`는 packet 단계에서 node 목적에 맞게 구체화한다.
- actor route, node, transition, exception loop는 WBS가 아니라 planned flow에서 정의한다.
- runtime 상태는 WBS가 아니라 run ledger가 가진다.
