# Git Task End Commands

## Default
- `./.codex/skills/git-task-end/scripts/run.sh`

## Apply
- `./.codex/skills/git-task-end/scripts/run.sh --apply --yes`
- `python3 ./.codex/skills/git-task-end/scripts/pr_summary.py --pr <number> [--linked-issue-number <n>] [--linked-issue-title "<title>"]`

## Common options
- `--pr <number-or-url>`
- `--branch <branch>`
- `--worktree <path>`
- `--method squash|merge|rebase`
- `--subject "<merge-subject>"`
- `--no-worktree-remove`
- `--no-branch-cleanup`

## Recommended flow
1. dry-run 전에 네트워크 의존성을 먼저 판단.
2. `gh pr view` 또는 linked issue 조회가 예상되면 첫 실행부터 권한 승격 요청.
3. 기본 dry-run 실행.
4. 계획된 PR, branch, worktree, merge subject 확인.
5. branch cleanup과 worktree cleanup 계획을 확인.
6. gate 실패 시 `다음 행동:`에 따라 수정.
7. 사용자 승인 후 동일 경로에 `--apply --yes` 추가.
8. apply 성공 후 merged PR 번호를 기준으로 `pr_summary.py` 를 호출해 handoff 요약을 출력.

## Typical examples
- 기본 추론 + 계획 확인:
  - `./.codex/skills/git-task-end/scripts/run.sh`
- 승인 후 실제 실행:
  - `./.codex/skills/git-task-end/scripts/run.sh --apply --yes`
- worktree cleanup 없이 종료:
  - `./.codex/skills/git-task-end/scripts/run.sh --apply --yes --no-worktree-remove`
- apply 후 PR 요약 출력:
  - `python3 ./.codex/skills/git-task-end/scripts/pr_summary.py --pr 42 --linked-issue-number 49 --linked-issue-title "[chore] task end 후 PR 요약 출력 흐름 정리"`

## Notes
- core wrapper는 기본적으로 dry-run만 수행.
- dry-run 또는 apply 에서 `gh pr view`, `gh issue view`, `gh issue edit` 같은 네트워크 호출이 발생할 수 있다.
- remote branch 확인/생성 helper 때문에 apply 단계에서도 네트워크가 필요할 수 있다.
- post-apply summary helper도 `gh pr view` 로 merged PR 최신 상태를 다시 읽는다.
- 네트워크 의존이 보이면 sandbox 실패를 기다리지 말고 첫 실행부터 승격 경로를 우선한다.
- interactive prompt는 `task_end_interactive.sh` 같은 인간용 경로에서만 처리.
- skill은 interactive wrapper가 아니라 core wrapper를 사용.
