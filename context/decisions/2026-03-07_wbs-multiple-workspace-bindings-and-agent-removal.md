# DEC: Multiple workspace bindings per WBS task and no agent assignment in WBS

- Date: 2026-03-07
- Context: WBS task를 실제 planning artifact로 보면서 `workspace_binding`을 단일 객체로 두었는데, 병렬 개발에서는 같은 slice에 구현용 branch/worktree와 후속 버그 수정용 branch/worktree가 함께 계획될 수 있다. 또한 `assigned_agent`, `assigned_profile`은 planning 단계보다는 dispatch/runtime 직전에 결정될 가능성이 높아 WBS에 넣으면 planning-layer와 runtime allocation이 다시 섞인다.
- Decision: WBS task YAML의 작업 공간 필드는 단일 `workspace_binding` 객체가 아니라 `workspace_bindings` 목록으로 관리한다. 각 항목은 `purpose`, `branch`, `worktree`를 가진다. `assigned_agent`, `assigned_profile`은 WBS에서 제거한다.
  - 한 slice는 `구현`, `버그 수정`, `실험`, `안정화`처럼 여러 planning-layer workspace를 가질 수 있다.
  - branch/worktree 정보는 계속 `planned flow`나 `refs`가 아니라 WBS task YAML에 둔다.
  - `index.md`는 exact path를 모두 복제하지 않고 workspace 요약만 보여주는 projection으로 유지한다.
  - 실제 어떤 actor가 어느 packet을 들고 있는지는 계속 `run ledger`와 dispatch/runtime artifact가 소유한다.
- Alternatives: `workspace_binding` 단일 객체를 유지하고 필요 시 덮어쓴다. branch/worktree 정보를 `planned flow` 또는 `refs`에 이동한다. agent/profile 필드를 남기고 null 허용으로 운영한다.
- Tradeoffs: `workspace_bindings` 목록은 단일 객체보다 YAML이 약간 길어진다. 대신 slice 하나에 여러 개발 트랙을 자연스럽게 담을 수 있고, implementation/fix/experiment 브랜치를 덮어쓰지 않아도 된다. 또한 WBS는 "어디서 작업할 준비가 되어 있는가"까지만 표현하고, "누가 지금 맡고 있는가"는 runtime 레이어로 남겨 planning/runtime 경계를 더 분명히 한다.
- Revisit if: branch/worktree가 slice 단위가 아니라 packet/run 단위에서만 유의미하다고 확인되거나, workspace 계획도 별도 artifact로 분리하는 편이 더 낫다고 판단될 때.
