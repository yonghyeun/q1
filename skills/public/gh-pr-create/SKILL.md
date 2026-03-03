---
name: gh-pr-create
description: Create a pull request with close-link and branch policy checks.
---

# GH PR Create

Open PR only after policy and body checks pass.

## Execute
1. `.github/pull_request_template.md` 구조를 기준으로 PR 본문 파일을 작성한다.
2. PR 제목을 컨벤션으로 생성/검증한다.
   - 생성: `./scripts/repo/pr_title_guard.sh generate --scope <scope> --summary "<요약>"`
   - 검증: `./scripts/repo/pr_title_guard.sh validate --title "[scope] <요약>" --branch <current-branch>`
3. Run:
   - `./skills/public/gh-pr-create/scripts/run.sh --title "<PR title>" --body-file /tmp/pr.md`

## What this validates
- branch naming policy
- PR body quality
- close keyword presence (`Closes/Fixes/Resolves #N`)

## References
- Command matrix: `references/commands.md`
