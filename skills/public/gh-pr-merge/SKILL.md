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
3. Use `--dry-run` when user wants command preview.

## Behavior
- Validate gh preflight and branch policy.
- Merge PR with selected method.
- Delete remote head branch.
- Run local cleanup (`post_merge_cleanup.sh`).

## Guardrails
- Do not run from `main`.
- Stop on any failed preflight/check.

## References
- Detailed commands: `references/commands.md`
