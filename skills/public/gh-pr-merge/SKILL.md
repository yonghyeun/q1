---
name: gh-pr-merge
description: Merge an approved pull request and trigger post-merge cleanup safely.
---

# GH PR Merge

Merge PR after approvals and run local cleanup.

## Execute
1. Dry-run first.
   - `./skills/public/gh-pr-merge/scripts/run.sh --method squash --dry-run`
2. 실제 실행.
   - `./skills/public/gh-pr-merge/scripts/run.sh --method squash`
3. 필요 시 subject 지정.
   - `--subject "[config] 머지 제목"`
