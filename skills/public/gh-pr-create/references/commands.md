# GH PR Create Commands

## Required
- `./scripts/repo/pr_create.sh --title "<PR title>" --body-file <path>`

## Title convention helper
- 생성:
  - `./scripts/repo/pr_title_guard.sh generate --task-id <T-000N> --summary "<요약>"`
- 검증:
  - `./scripts/repo/pr_title_guard.sh validate --title "[T-000N] <요약>" --branch <current-branch>`

## Optional
- `--base main`
- `--draft`
- `--dry-run`

## Validations included
1. branch naming policy
2. task context existence
3. required task artifacts
4. PR body close-link match with branch issue number
5. PR body quality guard pass (`body_quality_guard.py`)

## Body writing rule (important)
- 본문 작성 전에 아래 근거를 먼저 수집한다.
  - `git diff --name-status main...HEAD`
  - `git log --oneline $(git merge-base main HEAD)..HEAD`
  - `context/tasks/<task-id>/context.md`, `result.md`
- `.github/pull_request_template.md` 필수 섹션을 모두 채운다.
- `Closes/Fixes/Resolves #N` 키워드와 실제 issue 번호를 정확히 맞춘다.
