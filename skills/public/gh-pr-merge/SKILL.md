---
name: gh-pr-merge
description: Merge an approved pull request and trigger post-merge cleanup safely. Use when the user requests PR merge from terminal, with explicit merge method (squash/merge/rebase) and remote branch deletion.
---

# GH PR Merge

Merge PR and clean local state in one flow.

## Execute
1. Run:
   - `./skills/public/gh-pr-merge/scripts/run.sh --method <squash|merge|rebase>`
2. Use `--pr <number-or-url>` when merging a PR not mapped to current branch.
3. squash/merge에서 merge commit 제목을 직접 지정하려면:
   - `--subject "[T-000N] 머지 제목"`
4. Use `--dry-run` when user wants command preview.

## Behavior
- Validate gh preflight and branch policy.
- Merge PR with selected method.
- `--method squash|merge`에서 `--subject`가 없으면 PR 제목을 merge subject로 자동 사용한다.
- `--method rebase`에서는 `--subject`를 사용하지 않는다.
- Delete remote head branch.
- Run local cleanup (`post_merge_cleanup.sh`) with `pull --rebase`.

## Guardrails
- Do not run from `main`.
- Stop on any failed preflight/check.
- `pull --rebase` 충돌 시 자동 복구하지 않고 즉시 실패한다(수동 해결 후 재실행).

## References
- Detailed commands: `references/commands.md`
