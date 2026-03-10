# Repo PR Create Commands

## Required
- `./.codex/skills/repo-pr-create/scripts/run.sh --title "<PR title>" --body-file <path>`

## Optional
- `--base main`
- `--draft`
- `--dry-run`

## Title helper
- 생성:
  - `./scripts/repo/pr_title_guard.sh generate --scope <scope> --summary "<요약>"`
- 검증:
  - `./scripts/repo/pr_title_guard.sh validate --title "[scope] <요약>" --branch <current-branch>`

## Suggested authoring flow
1. `.github/pull_request_template.md`를 기준으로 body 초안 작성.
2. 먼저 `왜 이 PR이 필요한지`, `merge 후 무엇이 쉬워지거나 안전해지는지`를 한 문장씩 정리.
3. `Changes`는 변경 파일 나열보다 기대 효과와 운영 변화 중심으로 작성.
4. `Decisions Made`는 결정 배경, 선택한 방향, 버린 대안을 함께 기록.
5. 필요 시 `policies/branch-pr-convention.md` 확인.
6. `./.codex/skills/repo-pr-create/scripts/run.sh --dry-run ...` 으로 preflight 확인.
7. 실패 시 gate 메시지의 `다음 행동:`을 반영.
8. 동일 명령 경로로 재시도.

## Existing PR revision
- 이미 열린 PR의 title/body만 수정할 때:
  - 로컬에서 body 초안을 다시 작성하고 gate를 통과시킨 뒤 `gh pr edit <number> --title "<title>" --body-file <path>` 사용
- 이유:
  - 현재 local wrapper는 PR 생성 경로를 담당.
  - remote PR 본문 수정은 `gh pr edit`가 직접 담당.

## Gates reached through the wrapper
- `pr-title`
- `pr-body`
- `pr-primary-issue-link`
- branch naming validation
- `detached-head-write`
- `protected-branch-write`
- `dirty-worktree-write`
