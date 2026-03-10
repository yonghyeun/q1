# Git Task End Commands

## Default
- `./.codex/skills/git-task-end/scripts/run.sh`

## Apply
- `./.codex/skills/git-task-end/scripts/run.sh --apply --yes`
- `./.codex/skills/git-task-end/scripts/run.sh --codex none --apply --yes`

## Common options
- `--pr <number-or-url>`
- `--branch <branch>`
- `--worktree <path>`
- `--method squash|merge|rebase`
- `--subject "<merge-subject>"`
- `--codex resume|fork|none`
- `--codex-target-worktree <path>`
- `--no-worktree-remove`
- `--no-branch-cleanup`

## Recommended flow
1. 기본 dry-run 실행.
2. 계획된 PR, branch, worktree, merge subject 확인.
3. `--codex` 기본값은 `resume`.
4. 기본 Codex target worktree는 primary worktree인지 확인.
5. `CODEX_THREAD_ID`가 있으면 wrapper가 `codex resume -C <worktree> <thread>` 또는 `codex fork -C <worktree> <thread>` 명령을 출력하는지 확인.
6. apply에서 `--codex resume|fork` 이면 wrapper가 마지막에 해당 Codex 명령을 직접 실행한다.
7. gate 실패 시 `다음 행동:`에 따라 수정.
8. 사용자 승인 후 동일 경로에 `--apply --yes` 추가.

## Typical examples
- 기본 추론 + 계획 확인:
  - `./.codex/skills/git-task-end/scripts/run.sh`
- 승인 후 실제 실행:
  - `./.codex/skills/git-task-end/scripts/run.sh --apply --yes`
- worktree cleanup 없이 종료:
  - `./.codex/skills/git-task-end/scripts/run.sh --apply --yes --no-worktree-remove`
- Codex follow-up 비활성화:
  - `./.codex/skills/git-task-end/scripts/run.sh --codex none --apply --yes`

## Notes
- core wrapper는 기본적으로 dry-run만 수행.
- interactive prompt는 `task_end_interactive.sh` 같은 인간용 경로에서만 처리.
- skill은 interactive wrapper가 아니라 core wrapper를 사용.
- `codex resume` 는 task 종료 후 다음 worktree에서 같은 대화를 이어받는 경로.
- `codex fork` 는 task 종료 후 다음 worktree에서 병렬 분기를 여는 경로.
