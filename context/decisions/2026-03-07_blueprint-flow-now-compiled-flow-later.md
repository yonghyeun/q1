# DEC: Blueprint flow now, compiled flow later if needed

- Date: 2026-03-07
- Context: `planned flow`를 도입한 뒤, node별 actor가 downstream 계획까지 미리 연결한 `compiled flow`를 기본 운영으로 삼을지 검토했다. 이 방식은 구현 전에 여러 operator가 flow를 따라 계획만 먼저 세우고, 사람이 그 전체 계획을 검토한 뒤 실제 실행에 들어가게 하는 모델이다. 장점은 구현 비용이 큰 slice에서 downstream invalidation을 더 이르게 발견할 수 있다는 점이다. 하지만 현재 문서 체계와 schema는 per-node planning artifact를 정형적으로 연결하지 않고 있고, upstream 산출물이 실제로 나오기 전 downstream plan이 쉽게 stale해질 수 있다.
- Decision: 현재 기본 운영은 `planned flow = route + packet blueprint`로 두고, `compiled flow`는 미래 옵션으로만 남긴다.
  - `planned flow`는 허용 node, transition, exception loop, packet blueprint를 고정한다.
  - concrete packet은 transition 시점에 최신 trace와 입력을 반영해 생성한다.
  - actor는 packet을 받은 뒤 그 범위 안에서 local execution plan을 세운다.
  - downstream operator가 구현 전에 자기 node 상세 계획까지 미리 쓰는 `compiled flow`는 현재 기본값으로 채택하지 않는다.
  - `compiled flow`는 high-cost, multi-node, high-coupling slice에서만 미래에 선택적으로 검토할 수 있다.
- Alternatives: `compiled flow`를 기본 운영으로 채택해 모든 주요 slice에서 planning-only pass를 먼저 수행한다. 반대로 planned flow조차 두지 않고 packet 생성 시점마다 operator가 routing과 packet shape를 함께 결정한다.
- Tradeoffs: blueprint 방식은 runtime 유연성과 운영 경량성을 유지하지만, 구현 전에 downstream 계획을 모두 잠가두는 수준의 조기 검증은 제공하지 않는다. 반대로 compiled flow를 지금 기본값으로 두지 않으면서 planning cost와 stale-plan 위험을 줄일 수 있고, 현재 schema/decision/trace 모델과도 더 자연스럽게 맞는다.
- Revisit if: 구현 비용이 큰 slice에서 downstream invalidation이 반복적으로 큰 손실을 만든다거나, node-plan artifact와 human gate를 정형적으로 연결할 schema가 추가되어 compiled flow를 안정적으로 운영할 수 있게 될 때.
