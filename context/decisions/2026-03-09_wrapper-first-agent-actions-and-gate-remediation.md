# DEC: Use wrapper-first action paths and gate remediation for Agent-executed issue, PR, merge, and worktree actions

- Date: 2026-03-09
- Context: 이 저장소의 gate와 피드백 루프는 이미 정리되었지만, Agent가 규칙을 실제로 잘 지키게 하려면 단순히 `AGENTS.md`에서 gate 존재를 알려주는 것만으로는 부족했다. 이슈 생성, PR 생성, PR merge, worktree 생성은 raw 명령으로도 수행할 수 있어 gate 우회 가능성이 남아 있었고, gate 실패 시에도 단순 실패 메시지만으로는 Agent가 어떤 수정 경로를 따라야 하는지 일관되게 행동하기 어려웠다.
- Decision: Agent가 gate를 지켜야 하는 액션은 wrapper-first 경로와 remediation-first 실패 처리 규칙을 따른다.
  - issue 생성은 `scripts/repo/issue_create.sh`를 우선 사용한다.
  - PR 생성은 `scripts/repo/pr_create.sh`를 우선 사용한다.
  - PR merge는 `scripts/repo/pr_merge.sh`를 우선 사용한다.
  - worktree 생성은 `scripts/repo/worktree_add.sh`를 우선 사용한다.
  - wrapper가 존재하는 액션에서는 같은 기능의 raw `gh`나 raw `git worktree` 명령보다 wrapper 경로를 우선한다.
  - gate 실패 시 Agent는 우회하지 않고, 실패 메시지의 `다음 행동:`을 따라 입력이나 상태를 수정한 뒤 동일 경로로 재시도한다.
  - 이 운영 규칙의 상세 SoT는 `policies/agent-action-policy.md`에 둔다.
- Alternatives: gate 존재만 `AGENTS.md`에 기록하고 행동 경로는 자유롭게 둔다. raw 명령 사용을 허용하고 Agent의 주의력에만 의존한다. gate 실패 시 단순 에러만 출력하고 후속 행동은 Agent가 임의로 판단하게 둔다.
- Tradeoffs: wrapper-first 구조는 우회 여지를 줄이고 gate 준수율을 높이지만, 직접 명령 사용보다 유연성은 줄어든다. remediation-first 구조는 self-heal 루프를 만들 수 있지만, gate 메시지 품질이 낮으면 오히려 재시도 품질이 떨어질 수 있다. 반대로 자유 경로를 허용하면 초기 사용은 단순해 보이지만, 실제 운영에서는 규칙 준수가 불안정해진다.
- Revisit if: wrapper 경로보다 raw 명령 경로가 지속적으로 더 안정적이거나, gate를 wrapper 내부가 아니라 다른 실행 계층에서 일관되게 강제하는 구조로 전환할 때.
