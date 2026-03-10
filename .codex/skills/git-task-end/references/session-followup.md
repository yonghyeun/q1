# Git Task End Session Follow-Up

## Why
- task end는 현재 branch/worktree를 정리한 뒤 다음 작업 위치로 이동하는 경계다.
- 현재 worktree를 제거하면 같은 경로에서 작업을 이어갈 수 없다.
- 종료 후에도 Codex를 계속 쓸 거면 다음 target worktree를 명시해야 한다.

## Default
- `--codex` 기본값은 `resume`.
- `--codex-target-worktree` 기본값은 primary worktree다.

## Modes
- `resume`
  - 같은 대화를 target worktree에서 재개.
- `fork`
  - 현재 대화를 보존하고 target worktree에서 새 병렬 세션 시작.
- `none`
  - 자동 Codex follow-up 비활성화.

## Notes
- 제거될 worktree를 `--codex-target-worktree` 로 지정하면 실패해야 한다.
- chat history만으로 부족한 문맥은 task end를 호출한 현재 세션이 handoff 요약으로 남긴다.
