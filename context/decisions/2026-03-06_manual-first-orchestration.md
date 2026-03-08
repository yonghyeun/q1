# DEC: Manual-first orchestration before automated agent routing

- Date: 2026-03-06
- Context: 이 프로젝트는 vertical slice 기반으로 작업을 쪼개고, 필요 시 전문화된 여러 에이전트를 수동 오케스트레이션하는 개발 방식을 검토하고 있다. 이전 자동 오케스트레이션 시도에서는 operator agent가 기대한 방식으로 작동하지 않았고, 특히 어떤 작업 trace를 다음 에이전트에게 넘겨야 하는지와 handoff packet을 어떻게 표준화해야 하는지가 불명확했다. 이 상황에서 에이전트 수를 늘리는 것만으로는 처리량이 늘지 않고, 오히려 통합 실패와 재작업이 커질 위험이 있다.
- Decision: 자동 오케스트레이션을 바로 기본값으로 두지 않고, 우선은 사람이 control plane을 맡는 manual-first orchestration으로 시작한다.
  - 병렬 효율의 1차 결정요인은 에이전트 수가 아니라 **handoff schema와 work trace protocol의 품질**로 본다.
  - 전문화된 에이전트는 최소 집합만 운용하고, 각 작업은 `goal`, `inputs`, `contracts`, `acceptance criteria`, `owned files`, `non-goals`, `output format`, `open risks`를 포함한 handoff packet으로 넘긴다.
  - 사람 오퍼레이터는 초기 단계에서 task routing, trace 요약, merge 타이밍, 실패 시 escalation을 직접 판단한다.
  - 자동화는 manual-first 운영에서 반복적으로 검증된 패턴만 단계적으로 승격한다.
- Alternatives: 범용 단일 에이전트로만 순차 개발한다. 처음부터 operator agent 기반 자동 오케스트레이션을 기본값으로 둔다.
- Tradeoffs: 수동 오케스트레이션은 초기 throughput이 낮고 사람이 병목이 되기 쉽다. 대신 실패 원인을 관찰하기 쉽고, 어떤 trace/handoff가 실제로 필요한지 학습할 수 있다. 반대로 자동 오케스트레이션은 잠재 throughput은 높지만, routing 기준·trace schema·retry policy가 안정화되기 전에는 실패 원인 추적이 더 어려워지고 잘못된 자동화를 굳힐 수 있다.
- Revisit if: handoff packet 형식이 여러 slice에서 안정적으로 재사용되고, operator의 trace 요약 규칙이 문서화되며, handoff failure/rework rate가 낮아지고, 반복적인 routing 패턴을 자동화해도 품질 저하가 없다고 판단될 때. 이 조건을 만족하면 low-risk slice부터 semi-automatic 또는 automatic orchestration으로 승격한다.
