---
name: gh-pr-create
description: Create a pull request with enforced issue close linkage and branch policy checks. Use when the user asks to open a PR, prepare merge readiness, or generate PR body that must include Closes #issue matching branch issue token.
---

# GH PR Create

Open PR only after policy and artifact checks pass.

## Input Evidence (write body after reading these)
PR 본문을 쓰기 전에 아래 근거를 먼저 확인한다.
1. `git diff --name-status main...HEAD`
2. `git log --oneline $(git merge-base main HEAD)..HEAD`
3. `context/tasks/<task-id>/context.md`, `context/tasks/<task-id>/result.md`
4. 정책 문서 (`policies/branch-pr-convention.md`, `.github/pull_request_template.md`)

## Execute
1. `.github/pull_request_template.md` 구조를 기준으로 PR 본문 파일을 먼저 작성한다.
2. PR 제목을 컨벤션으로 생성/검증한다.
3. Run:
   - `./skills/public/gh-pr-create/scripts/run.sh --title "<PR title>" --body-file /tmp/pr.md`
4. Use `--draft` when the user wants review-before-ready mode.
5. Use `--dry-run` when user asks for preview only.

## Issue Closing Policy
- 기본 정책은 `Closes #<issue-number>` 유지다.
- `Closes/Fixes/Resolves #N`의 `N`은 현재 브랜치 issue 번호와 반드시 동일해야 한다.

## What this already validates
- branch naming policy
- task context path existence
- required task artifacts
- PR close keyword matching branch issue number

## References
- Command matrix: `references/commands.md`
