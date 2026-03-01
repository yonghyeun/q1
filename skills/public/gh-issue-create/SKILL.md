---
name: gh-issue-create
description: Create a GitHub issue from local terminal with task linkage and standard templates. Use when the user asks to open a new issue, start a task from an issue, or standardize issue metadata (feature/bug/chore + T-000N).
---

# GH Issue Create

Create issue first, then derive branch workflow from the issue number.

## Execute
1. Confirm repository root and run:
   - `./skills/public/gh-issue-create/scripts/run.sh --type <feature|bug|chore> --task-id <T-000N> --title "<title>"`
2. Capture output values:
   - issue URL
   - issue number
3. Return both values explicitly to the user.

## Guardrails
- Stop immediately when `origin` remote is missing.
- Stop immediately when `gh auth` is invalid.
- Do not fabricate issue numbers; always use the command output.

## References
- Command details: `references/commands.md`
