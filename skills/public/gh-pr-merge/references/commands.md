# GH PR Merge Commands

## Required
- `./scripts/repo/pr_merge.sh --method <squash|merge|rebase>`

## Optional
- `--pr <number-or-url>`
- `--subject "<merge-subject>"` (squash/merge 전용)
- `--dry-run`

## Behavior
1. Validate gh preflight
2. Validate current branch policy
3. Merge PR with selected method and remote branch deletion
4. `squash|merge`에서 subject 미지정 시 PR 제목을 자동 subject로 사용
5. Run local cleanup (`post_merge_cleanup.sh`) with `pull --rebase`

## Examples
- `./scripts/repo/pr_merge.sh --method squash`
- `./scripts/repo/pr_merge.sh --method squash --subject "[T-0001] 브랜치 거버넌스 v1"`
- `./scripts/repo/pr_merge.sh --method rebase --dry-run`
