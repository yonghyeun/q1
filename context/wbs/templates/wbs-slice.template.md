# WBS Slice Template Reference

실제 WBS task 파일은 `context/wbs/templates/wbs-task.template.yaml`을 사용한다.
이 문서는 사람이 빠르게 필드 의미를 훑는 참고용 요약본이다.
작성 규칙은 `context/wbs/wbs-writing-conventions.md`를 따른다.

현재 WBS는 concrete runtime detail을 직접 고정하지 않고,
`owned_scope`, `verification_requirements` 같은 planning-layer boundary를 정의한다.

```yaml
slice_id: SLICE-ID
parent_wbs: mvp-wbs/v1
planning_status: draft
goal: 이 slice가 끝내는 사용자 가치
why: 왜 이 slice가 필요한가
contracts:
  - docs/product/contracts/example.md
acceptance_criteria:
  - 측정 가능한 완료 조건 1
owned_scope:
  - 기능/모듈/경계 수준의 소유 경계
verification_requirements:
  - 단위 검증 증거 필요
dependencies:
  - 선행 slice 또는 선행 결정
non_goals:
  - 이번 slice에서 하지 않을 것
risks:
  - 시작 시점에 알려진 위험
assumptions:
  - 현재 기대하는 가정
open_questions:
  - "[blocking] planned flow 작성 전에 닫아야 하는 쟁점"
workspace_binding:
  branch: null
  worktree: null
  assigned_agent: null
  assigned_profile: null
refs:
  planned_flow: null
  run_id: null
  related_docs: []
notes:
  - 특이사항
```

## Notes

- 사람이 읽는 설명은 기본적으로 한국어로 작성한다.
- 실제 정본은 Markdown block 문서가 아니라 task YAML 파일이다.
- `owned_scope`는 concrete file path가 아니라 소유 경계를 적는다.
- `verification_requirements`는 concrete test command가 아니라 검증 의무 수준을 적는다.
- 실제 `owned_paths`, `required_tests`는 packet 단계에서 node 목적에 맞게 구체화한다.
- actor route, node, transition, exception loop는 WBS가 아니라 planned flow에서 정의한다.
- runtime 상태는 WBS가 아니라 run ledger가 가진다.
