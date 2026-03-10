# Git Task Start Commands

## Default
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug>`

## Apply
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug> --apply --yes`

## Common options
- `--branch <type/slug>`
- `--purpose impl|review|fix|verify|docs|ops`
- `--base <ref>`
- `--path-root <dir>`

## Recommended flow
1. 기본 dry-run 실행.
2. 계획된 branch, base, purpose, target path 확인.
3. 기존 branch 재사용인지, 새 branch 생성인지 확인.
4. gate 실패 시 `다음 행동:`에 따라 수정.
5. 사용자 승인 후 동일 경로에 `--apply --yes` 추가.

## Typical examples
- 기본 task start 계획 확인:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow`
- purpose를 fix로 지정:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch fix/token-refresh-race --purpose fix`
- 승인 후 실제 실행:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow --apply --yes`

## Notes
- core wrapper는 기본적으로 dry-run만 수행.
- interactive prompt는 `task_start_interactive.sh` 같은 인간용 경로에서만 처리.
- skill은 interactive wrapper가 아니라 core wrapper를 사용.
