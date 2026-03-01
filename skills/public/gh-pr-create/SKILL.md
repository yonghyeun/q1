---
name: gh-pr-create
description: Create a pull request with enforced issue close linkage and branch policy checks. Use when the user asks to open a PR, prepare merge readiness, or generate PR body that must include Closes #issue matching branch issue token.
---

# GH PR Create

Open PR only after policy and artifact checks pass.

## Execute
1. `.github/pull_request_template.md` 구조를 기준으로 PR 본문 파일을 먼저 작성한다.
   - 모든 필수 섹션(`Issue Link`, `Why`, `What`, `범위`, `리스크`, `리뷰 포인트`, `참고 링크`)을 구체적으로 채운다.
2. Run:
   - `./skills/public/gh-pr-create/scripts/run.sh --title "<PR title>" --body-file /tmp/pr.md`
3. Use `--draft` when the user wants review-before-ready mode.
4. Use `--dry-run` when user asks for preview only.

## What this already validates
- branch naming policy
- task context path existence
- required run artifacts
- PR close keyword (`Closes/Fixes/Resolves #N`) matching branch issue number

## Guardrails
- Do not skip validations manually.
- Do not open PR if command returns non-zero exit.
- `Closes/Fixes/Resolves #N`는 브랜치 issue 번호와 반드시 일치해야 한다.
- placeholder/빈 bullet/빈 체크박스가 남아 있으면 본문을 수정한 뒤 재시도한다.

## References
- Command matrix: `references/commands.md`
