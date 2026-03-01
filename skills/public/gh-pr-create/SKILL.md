---
name: gh-pr-create
description: Create a pull request with enforced issue close linkage and branch policy checks. Use when the user asks to open a PR, prepare merge readiness, or generate PR body that must include Closes #issue matching branch issue token.
---

# GH PR Create

Open PR only after policy and artifact checks pass.

## Execute
1. Run:
   - `./skills/public/gh-pr-create/scripts/run.sh --title "<PR title>"`
2. Use `--draft` when the user wants review-before-ready mode.
3. Use `--dry-run` when user asks for preview only.

## What this already validates
- branch naming policy
- task context path existence
- required run artifacts
- PR close keyword (`Closes/Fixes/Resolves #N`) matching branch issue number

## Guardrails
- Do not skip validations manually.
- Do not open PR if command returns non-zero exit.

## References
- Command matrix: `references/commands.md`
