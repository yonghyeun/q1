# Git Task End Commands

## Default
- `./.codex/skills/git-task-end/scripts/run.sh`

## Apply
- `./.codex/skills/git-task-end/scripts/run.sh --apply --yes`

## Common options
- `--pr <number-or-url>`
- `--branch <branch>`
- `--worktree <path>`
- `--method squash|merge|rebase`
- `--subject "<merge-subject>"`
- `--no-worktree-remove`
- `--no-branch-cleanup`

## Recommended flow
1. 기본 dry-run 실행.
2. 계획된 PR, branch, worktree, merge subject 확인.
3. branch cleanup과 worktree cleanup 계획을 확인.
4. gate 실패 시 `다음 행동:`에 따라 수정.
5. 사용자 승인 후 동일 경로에 `--apply --yes` 추가.

## Typical examples
- 기본 추론 + 계획 확인:
  - `./.codex/skills/git-task-end/scripts/run.sh`
- 승인 후 실제 실행:
  - `./.codex/skills/git-task-end/scripts/run.sh --apply --yes`
- worktree cleanup 없이 종료:
  - `./.codex/skills/git-task-end/scripts/run.sh --apply --yes --no-worktree-remove`

## Notes
- core wrapper는 기본적으로 dry-run만 수행.
- interactive prompt는 `task_end_interactive.sh` 같은 인간용 경로에서만 처리.
- skill은 interactive wrapper가 아니라 core wrapper를 사용.
