# GH PR Create Commands

## Required
- `./scripts/repo/pr_create.sh --title "<PR title>"`

## Optional
- `--base main`
- `--draft`
- `--body-file <path>`
- `--dry-run`

## Validations included
1. branch naming policy
2. task context existence
3. required run artifacts
4. PR body close-link match with branch issue number
