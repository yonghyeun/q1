# Git Task Start Commands

## Default
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug>`

## Apply
- `./.codex/skills/git-task-start/scripts/run.sh --branch <type/slug> --apply --yes`

## Common options
- `--branch <type/slug>`
- `--issue <number>`
- `--purpose impl|review|fix|verify|docs|ops`
- `--base <ref>`
- `--path-root <dir>`

## Recommended flow
1. dry-run 전에 네트워크 의존성을 먼저 판단.
2. `git fetch origin --prune` 또는 `gh issue view` 가 예상되면 첫 실행부터 권한 승격 요청.
3. 기본 dry-run 실행.
4. 계획된 branch, base, purpose, target path 확인.
5. 기존 branch 재사용인지, 새 branch 생성인지 확인.
6. gate 실패 시 `다음 행동:`에 따라 수정.
7. 사용자 승인 후 동일 경로에 `--apply --yes` 추가.

## Typical examples
- 기본 task start 계획 확인:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow`
- issue와 함께 task start 계획 확인:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch chore/task-start-issue-transition --issue 15`
- purpose를 fix로 지정:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch fix/token-refresh-race --purpose fix`
- 승인 후 실제 실행:
  - `./.codex/skills/git-task-start/scripts/run.sh --branch feature/signup-flow --apply --yes`
  - `./.codex/skills/git-task-start/scripts/run.sh --branch chore/task-start-issue-transition --issue 15 --apply --yes`

## Notes
- core wrapper는 기본적으로 dry-run만 수행.
- dry-run 시작 시 `git fetch origin --prune` 를 수행한다.
- `--issue` 지정 시 dry-run/apply 모두 GitHub issue 조회를 수행.
- 네트워크 의존이 보이면 sandbox 실패를 기다리지 말고 첫 실행부터 승격 경로를 우선한다.
- apply 성공 후 issue status는 `status:active` 로 맞춘다.
- interactive prompt는 `task_start_interactive.sh` 같은 인간용 경로에서만 처리.
- skill은 interactive wrapper가 아니라 core wrapper를 사용.
