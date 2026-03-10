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
2. 필요 시 `policies/branch-pr-convention.md` 확인.
3. `./.codex/skills/repo-pr-create/scripts/run.sh --dry-run ...` 으로 preflight 확인.
4. 실패 시 gate 메시지의 `다음 행동:`을 반영.
5. 동일 명령 경로로 재시도.

## Gates reached through the wrapper
- `pr-title`
- `pr-body`
- `pr-primary-issue-link`
- branch naming validation
- `detached-head-write`
- `protected-branch-write`
- `dirty-worktree-write`
