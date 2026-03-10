# Git Task Start Session Handoff

## Why
- worktree 생성만으로 terminal/session 분리가 자동으로 생기지 않음.
- 같은 worktree를 여러 terminal이 공유하면 branch, index, working tree 상태가 공유됨.
- 병렬 작업이면 `작업 1개 = worktree 1개 = terminal 1개 = Codex 1개` 운영이 더 안전함.
- task start wrapper는 shell cwd나 Codex session을 자동으로 옮기지 않음.

## Modes

### Continue in current session
- 현재 Codex 세션이 후속 작업까지 계속 맡는 경우.
- 이후 모든 명령의 작업 경로를 새 worktree로 고정.
- 사용자의 shell cwd는 바뀌지 않았다고 명시.

### Restart in a new session
- 사용자가 새 terminal에서 새 worktree로 `cd` 후 Codex를 다시 시작하는 경우.
- chat history만으로 부족한 문맥은 task start를 호출한 현재 세션이 restart handoff로 요약해 전달.

## Minimum restart handoff
- branch
- worktree path
- task goal or purpose
- change transfer status
- key modified areas or files
- open risks
- immediate next action

## Example handoff

```text
Task start handoff
- Branch: config/agent-common-instructions-gates
- Worktree: /abs/path/agent-common-instructions-gates--ops
- Purpose: ops
- Transfer status: main의 변경을 stash로 보관 후 새 worktree에 적용 완료
- Goal: agent 공통 지침과 gate 구조 정비 이어서 진행
- Key areas: AGENTS.md, policies/, scripts/repo/, .codex/skills/
- Open risks: 이전 세션 대화는 새 세션에 자동 승계되지 않음
- Next action: 새 terminal에서 해당 worktree로 이동 후 Codex 시작, 위 요약을 첫 prompt에 포함
```
