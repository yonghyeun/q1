# DEC: GitHub issue를 remote backlog로 사용

- Date: 2026-03-11
- Context: 해결해야 할 문제와 요청이 여러 workspace의 로컬 `decision` 영역에 흩어지면 backlog 저장소 역할과 장기 rationale 저장소 역할이 섞인다.
- Decision: 해결해야 할 backlog 항목의 기본 저장소는 GitHub issue로 둔다.
- Alternatives: 로컬 `context/decisions/`에 backlog를 계속 적재. 별도 로컬 backlog 문서 디렉토리 신설.
- Tradeoffs: 원격 의존이 생긴다. 대신 backlog 조회, 검색, 필터, PR 연결이 쉬워진다.
- Revisit if: GitHub issue가 backlog 조회와 triage 흐름에 반복적으로 맞지 않거나 별도 tracker가 필요해질 때.
