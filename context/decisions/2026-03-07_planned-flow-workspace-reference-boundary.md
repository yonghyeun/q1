# DEC: Planned flow does not own exact workspace references

- Date: 2026-03-07
- Context: WBS task YAML에 `workspace_bindings`를 도입하면서 한 slice가 여러 branch/worktree를 가질 수 있게 됐다. 이 다음 질문은 `planned flow`가 이 workspace를 어떻게 참조해야 하는가였다. 하지만 `planned flow`는 route와 packet blueprint의 SoT이고, 같은 flow가 구현용 branch, 후속 버그 수정 branch, 실험용 branch 등 여러 작업 공간에서 재사용될 수 있다. exact branch/worktree를 flow에 넣으면 route 문서가 execution allocation 문서로 변질되고 쉽게 stale해진다.
- Decision: `planned flow`는 exact `branch`나 `worktree`를 직접 소유하거나 참조하지 않는다.
  - branch/worktree의 정본은 계속 WBS task YAML의 `workspace_bindings`에 둔다.
  - 실제 어떤 workspace를 이번 handoff에 사용할지는 packet 발행 또는 dispatch 시점에 선택한다.
  - 현재 사용 중인 workspace는 runtime projection 또는 ledger 계층이 소유한다.
  - `planned flow`에 workspace 정보가 꼭 필요하면 exact path 대신 `workspace_purpose_hints` 같은 약한 힌트만 둘 수 있다.
  - `workspace_purpose_hints`는 `구현`, `버그 수정`, `실험`, `안정화` 같은 purpose 수준으로만 쓴다.
- Alternatives: `planned flow`가 node별 exact branch/worktree를 직접 가진다. 또는 `planned flow`가 workspace를 전혀 언급하지 못하게 완전히 금지한다.
- Tradeoffs: flow에서 exact workspace를 제거하면 dispatch 시점에 한 단계 선택이 더 필요하다. 대신 flow를 여러 workspace/run에서 재사용하기 쉬워지고, route 설계와 execution allocation을 분리할 수 있다. 또한 branch/worktree 변경만으로 flow 버전을 새로 발행해야 하는 상황을 줄일 수 있다.
- Revisit if: 실제 운영에서 node와 workspace가 거의 1:1로 강하게 고정돼 exact binding이 없으면 dispatch 오류가 반복되거나, 반대로 workspace purpose hint조차 불필요해 flow가 workspace를 완전히 몰라도 된다고 확인될 때.
