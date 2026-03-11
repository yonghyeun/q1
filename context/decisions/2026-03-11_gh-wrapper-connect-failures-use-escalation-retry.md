# DEC: gh wrapper connect failures use escalation retry hint

- Date: 2026-03-11
- Context: Codex sandbox에서는 `gh auth status`가 통과해도 `api.github.com` 연결이 차단될 수 있다. 이때 issue/PR/task wrapper는 로컬 validation까지는 통과하지만 실제 GitHub API 호출 단계에서 흐름이 끊겼다.
- Decision: 저장소의 GitHub wrapper는 `api.github.com` 연결 실패를 일반 입력 오류로 취급하지 않고, `같은 wrapper 명령을 권한 상승으로 재실행`해야 하는 운영 힌트로 출력한다.
- Alternatives: connect failure를 기존 generic gh 실패 메시지로 유지. 또는 sandbox 제약을 숨기고 수동 웹 확인만 안내.
- Tradeoffs: 운영자는 다음 행동을 더 빨리 알 수 있다. 반면 sandbox 정책 자체가 해결된 것은 아니므로 권한 상승 재실행이 계속 필요하다.
- Revisit if: Codex sandbox에서 GitHub API outbound가 기본 허용되거나, read-only/approved wrapper 범위가 확장되어 재실행 비용이 사라지면 재검토.
