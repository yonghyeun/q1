---
name: git-branch-cleanup
description: Clean merged local branches and sync local main safely after remote merge. Use when the user asks to remove merged branch leftovers, prune stale refs, or standardize post-merge local cleanup.
---

# Git Branch Cleanup

Run post-merge cleanup as a deterministic sequence.

## Execute
1. Run:
   - `./skills/public/git-branch-cleanup/scripts/run.sh <merged-branch>`
2. Confirm final branch is `main`.

## Sequence
1. `fetch --prune`
2. `pull --ff-only origin main`
3. `branch -d <merged-branch>`

## Guardrails
- Require `origin` remote.
- Keep safe delete mode (`-d`), never force delete by default.

## References
- Command details: `references/commands.md`
