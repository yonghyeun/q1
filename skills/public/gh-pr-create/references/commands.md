# GH PR Create Commands

## Required
- `./scripts/repo/pr_create.sh --title "<PR title>" --body-file <path>`

## Title convention helper
- 생성:
  - `./scripts/repo/pr_title_guard.sh generate --scope <scope> --summary "<요약>"`
- 검증:
  - `./scripts/repo/pr_title_guard.sh validate --title "[scope] <요약>" --branch <current-branch>`

## Optional
- `--base main`
- `--draft`
- `--dry-run`

## Validations included
1. branch naming policy
2. PR body quality guard pass (`body_quality_guard.py`)
3. PR body close-link validation (`pr_issue_guard.py`)
