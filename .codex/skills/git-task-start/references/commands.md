# Git Task Start Commands

## Default
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug>`

## Apply
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug> --apply --yes`
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug> --codex none --apply --yes`

## Common options
- `--branch <type/slug>`
- `--purpose impl|review|fix|verify|docs|ops`
- `--base <ref>`
- `--path-root <dir>`
- `--codex resume|fork|none`

## Recommended flow
1. 기본 dry-run 실행.
2. 계획된 branch, base, purpose, target path 확인.
3. 기존 branch 재사용인지, 새 branch 생성인지 확인.
4. apply 이후 현재 session 유지인지, 새 terminal + 새 session 재시작인지 결정.
5. `--codex` 기본값은 `resume`.
6. `CODEX_THREAD_ID`가 있으면 wrapper가 `codex resume -C <worktree> <thread>` 또는 `codex fork -C <worktree> <thread>` 명령을 출력하는지 확인.
7. apply에서 `--codex resume|fork` 이면 wrapper가 마지막에 해당 Codex 명령을 직접 실행한다.
8. 새 session 재시작이면 `references/session-handoff.md` 기준으로 handoff 요약 제공.
9. gate 실패 시 `다음 행동:`에 따라 수정.
10. 사용자 승인 후 동일 경로에 `--apply --yes` 추가.

## Typical examples
- 기본 task start 계획 확인:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow`
- Codex follow-up 비활성화:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow --codex none`
- purpose를 fix로 지정:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch fix/token-refresh-race --purpose fix`
- 승인 후 실제 실행:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow --apply --yes`

## Notes
- core wrapper는 기본적으로 dry-run만 수행.
- interactive prompt는 `task_start_interactive.sh` 같은 인간용 경로에서만 처리.
- skill은 interactive wrapper가 아니라 core wrapper를 사용.
- 병렬 작업이면 새 terminal에서 target worktree로 이동 후 새 session 시작 권장.
- `codex resume` 는 같은 대화를 새 worktree에서 이어받는 경로.
- `codex fork` 는 기존 대화를 보존하고 병렬 세션을 새 worktree에서 여는 경로.
- 자동 follow-up을 원하지 않으면 `--codex none` 사용.
