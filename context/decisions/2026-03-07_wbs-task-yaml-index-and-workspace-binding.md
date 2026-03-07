# DEC: WBS task YAML, index projection, and workspace binding

- Date: 2026-03-07
- Context: WBS를 실제 운영 artifact로 쓰기 시작하면서 slice 정본을 어떤 단위로 저장할지, 사람이 backlog 전체를 어떻게 훑을지, 그리고 branch/worktree 같은 병렬 개발 바인딩 정보를 어디에 둘지가 필요해졌다. 특히 branch/worktree를 `planned flow`에 둘지, `refs`에 둘지, WBS task 자체에 둘지 명확하지 않았다. 동시에 runtime 상태는 이미 `run ledger`가 소유하도록 합의되어 있어, planning-layer 정보와 runtime 상태가 다시 섞이지 않게 해야 했다.
- Decision: WBS는 `slice 1개 = task YAML 파일 1개`를 기본 저장 단위로 사용하고, backlog overview는 별도 `index.md` projection으로 제공한다. branch/worktree/agent assignment 같은 작업 바인딩 정보는 `refs`나 `planned flow`가 아니라 WBS task YAML의 `workspace_binding` 필드에 둔다.
  - WBS task 정본 경로는 `context/wbs/tasks/<slice_id>.yaml`를 기본값으로 둔다.
  - 사람이 빠르게 읽는 backlog overview는 `context/wbs/tasks/index.md`에서 관리한다.
  - `index.md`는 요약 projection이며 SoT는 개별 task YAML이다.
  - WBS는 runtime 상태 대신 `planning_status`를 가진다.
  - `planning_status`는 `draft`, `planned`, `planning_blocked`, `ready_for_flow`, `ready_for_dispatch`, `archived`, `cancelled` 같은 planning 상태만 표현한다.
  - `workspace_binding`은 `branch`, `worktree`, `assigned_agent`, `assigned_profile` 같은 planning-layer 실행 바인딩을 담는다.
  - `refs`는 `planned_flow`, `run_id`, `related_docs` 같은 artifact 연결 포인터만 담는다.
  - `planned flow`는 route/node/transition 문서이므로 branch/worktree를 직접 소유하지 않는다.
  - runtime의 실제 진행 상태(`active`, `blocked`, `done` 등)는 계속 `run ledger`가 소유한다.
- Alternatives: WBS를 계속 Markdown + YAML block 문서로 유지한다. branch/worktree를 `refs`나 `planned flow`에 넣는다. backlog overview를 별도 index 없이 디렉터리 listing이나 run ledger 확장으로 해결한다.
- Tradeoffs: task YAML + index 구조는 파일 수가 늘고, index projection을 함께 유지해야 한다. 대신 slice별 diff/review가 쉬워지고, 에이전트가 task YAML만 읽고도 "무엇을 할지"와 "어디서 할지"를 함께 파악할 수 있다. 또한 `planned flow`는 route 문서, `workspace_binding`은 작업 위치 바인딩, `run ledger`는 runtime 상태라는 경계가 분명해진다.
- Revisit if: backlog 규모가 너무 커져 `index.md` 수동 유지 비용이 커지거나, branch/worktree가 slice 단위보다 packet/run 단위에서 더 정확하게 관리돼야 한다고 확인되거나, WBS task YAML을 자동 생성/동기화하는 도구가 도입되어 다른 projection 방식이 더 적합해질 때.
