# DEC: git approval rules order by decision priority

- Date: 2026-03-11
- Context: `git-approval.rules`를 `match`/`not_match` 예시 중심으로 읽으면 위험도보다 예시 위치가 먼저 보였다. 검토와 수정 시 `forbidden`, `prompt`, `allow` 우선순위가 한눈에 드러나지 않았다.
- Decision: 규칙 배치를 `decision` 우선순위인 `forbidden -> prompt -> allow` 순서로 재정렬한다. 예시는 각 규칙의 보조 검증 수단으로만 유지한다.
- Alternatives: 기존처럼 명령 종류별로 섞어서 유지. 또는 `match`/`not_match` 예시를 더 늘려 문맥을 보강.
- Tradeoffs: 같은 계열 명령이 여러 섹션으로 흩어질 수 있다. 대신 위험도 기준 검토와 정책 감사는 더 빨라진다.
- Revisit if: 규칙 엔진이 명시적 priority 메타데이터를 지원하거나, decision 순서보다 명령군 단위 탐색이 더 중요해지는 운영 요구가 생기면 재검토.
