# DEC: Planned flow before runtime packet routing

- Date: 2026-03-07
- Context: WBS 기반 orchestration 문서에는 `packet`, `trace`, `operator decision`, `run ledger`의 runtime 모델이 정의돼 있었지만, packet이 어떤 node와 transition을 따라 움직여야 하는지에 대한 planning-layer artifact는 분리되어 있지 않았다. 이 때문에 `trace`가 개별 packet 실행 기록인지, packet이 이동한 전체 경로인지 해석이 흔들릴 수 있었고, operator가 packet 생성 시점마다 routing을 즉흥적으로 다시 정할 여지도 남아 있었다. 이런 상태에서는 실패가 actor 구현 문제인지, edge/routing 문제인지, WBS slice 설계 문제인지 분리하기 어렵고, 반복 루프 평가와 자동 dispatch 기준도 불안정해진다.
- Decision: runtime packet을 발행하기 전에 slice별 `planned flow`를 먼저 고정한다.
  - `planned flow`는 WBS와 packet 사이의 planning-layer artifact다.
  - `planned flow`는 허용 node, transition, exception loop, escalation 기준의 SoT다.
  - `trace`는 계속해서 개별 packet의 실행 기록을 뜻하며, packet route 자체를 의미하지 않는다.
  - operator는 runtime에서 경로를 새로 발명하지 않고, `planned flow`가 허용한 transition 중 하나를 선택한다.
  - packet은 `planned flow`의 특정 node를 런타임 handoff로 투영한 artifact로 본다.
  - 허용되지 않은 transition 선택은 기본적으로 `orchestration failure`로 분류한다.
  - 동일 loop 반복이 threshold를 넘으면 packet 재작업으로만 덮지 않고 `planned flow` 또는 WBS 재검토로 승격한다.
- Alternatives: WBS와 packet만으로 운영하며 routing은 operator 판단에 맡긴다. 또는 packet lineage와 run ledger만으로 사후적으로 경로를 복원하고 별도 planning-layer route artifact는 두지 않는다.
- Tradeoffs: 문서 레이어가 하나 늘어나고, slice 준비 시 operator가 미리 node/transition을 설계해야 하므로 초기 진입 비용이 조금 커진다. 반대로 node 실패, routing 실패, WBS 실패를 분리해 평가하기 쉬워지고, rework/block/remediate 루프의 경계가 선명해진다. 또한 packet 생성과 auto-dispatch를 policy-bounded하게 만들 수 있어 전체 복잡성과 운영 편차를 낮출 수 있다.
- Revisit if: 실제 운영에서 대부분의 slice가 단일 packet으로 끝나 별도 flow 문서 유지 비용이 과하다고 확인되거나, runtime schema가 `planned_flow_id`, `node_id`, `allowed_transitions`를 직접 가지게 되어 현재의 문서형 planned flow를 다른 형태의 정형 artifact로 대체하는 편이 더 적절해질 때.
