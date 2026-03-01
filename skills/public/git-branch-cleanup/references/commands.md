# Git Branch Cleanup Commands

## Required
- `./scripts/repo/post_merge_cleanup.sh <merged-branch>`

## Cleanup sequence
1. `git fetch origin --prune`
2. `git pull --ff-only origin main`
3. `git branch -d <merged-branch>`

## Guardrails
- Requires `origin` remote
- Fails safely if branch is not merged
