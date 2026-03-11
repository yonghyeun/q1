# DEC: plan allow rule for gh issue list

- Date: 2026-03-11
- Context: PR 생성 준비 중 `gh issue list`로 연결 가능한 이슈를 조회해야 했다. 현재는 권한 상승 승인 후에만 실행할 수 있어 issue 확인 흐름이 불필요하게 끊긴다.
- Decision: `gh issue list`는 추후 approval rule의 allow 대상으로 추가하는 방향으로 기록한다. 이번 턴에서는 규칙 자체는 변경하지 않고 decision만 남긴다.
- Alternatives: 계속 매번 승인 요청 후 실행. 또는 issue 조회를 수동 웹 확인으로 대체.
- Tradeoffs: allow 추가 시 issue 조회 흐름은 빨라지지만, GitHub 메타데이터 조회 권한 범위가 넓어진다. 반대로 지금처럼 유지하면 운영 마찰이 계속 남는다.
- Revisit if: 실제 approval rule 정리 작업을 수행할 때, `gh issue list` 외에 함께 묶어야 할 read-only GitHub 명령 범위가 더 명확해지면 재검토.
