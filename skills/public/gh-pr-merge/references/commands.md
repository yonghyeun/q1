# GH PR Merge Commands

## Required
- `./scripts/repo/pr_merge.sh --method <squash|merge|rebase>`

## Optional
- `--pr <number-or-url>`
- `--subject "[scope] 머지 제목"`
- `--dry-run`

## Recommended flow
1. `./scripts/repo/pr_merge.sh --method squash --dry-run`
2. `./scripts/repo/pr_merge.sh --method squash`
