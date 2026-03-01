# GH PR Merge Commands

## Required
- `./scripts/repo/pr_merge.sh --method <squash|merge|rebase>`

## Optional
- `--pr <number-or-url>`
- `--dry-run`

## Behavior
1. Validate gh preflight
2. Validate current branch policy
3. Merge PR with selected method and remote branch deletion
4. Run local cleanup (`post_merge_cleanup.sh`)
