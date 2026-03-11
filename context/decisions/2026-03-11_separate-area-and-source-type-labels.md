# DEC: area와 source_type label을 분리

- Date: 2026-03-11
- Context: 초기 label taxonomy에서는 `area`가 문제의 적용 대상과 작업의 발생 출처를 함께 설명하려 해 경계가 흐려졌다. 특히 `wbs`는 독립 문제 영역보다 planning 출처에 가깝고, agent-team 운영 중 생긴 작업도 별도 출처 축이 필요했다.
- Decision: `area`는 변경/영향 대상만 나타내고, 작업 발생 출처는 `source_type` 축으로 분리한다. `area` 허용값은 `product`, `repo`, `docs`, `agent-team`으로 두고, `source_type` 허용값은 `human-request`, `agent-team`, `runtime-observation`, `wbs-planned`로 둔다.
- Alternatives: `area` 하나에 출처 의미까지 계속 혼합. `wbs`를 area로 유지. source_type 없이 free-form 메모로 출처 기록.
- Tradeoffs: label 축이 하나 늘어난다. 대신 backlog triage 시 "무엇의 문제인가"와 "어디서 생긴 작업인가"를 분리해 필터링할 수 있다.
- Revisit if: source_type 축이 거의 쓰이지 않거나 area/source_type 경계가 운영 중 다시 자주 흔들릴 때.
