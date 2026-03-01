---
name: gh-issue-create
description: Create a GitHub issue from local terminal with task linkage and standard templates. Use when the user asks to open a new issue, start a task from an issue, or standardize issue metadata (feature/bug/chore + T-000N).
---

# GH Issue Create

Create issue first, then derive branch workflow from the issue number.

## Execute
1. `.github/ISSUE_TEMPLATE/<type>.md` 구조를 기준으로 본문 파일을 먼저 작성한다.
   - 모든 섹션에 구체 내용을 채운다(빈 bullet/placeholder 금지).
2. Confirm repository root and run:
   - `./skills/public/gh-issue-create/scripts/run.sh --type <feature|bug|chore> --task-id <T-000N> --title "<title>" --body-file /tmp/issue.md`
3. Capture output values:
   - issue URL
   - issue number
4. Return both values explicitly to the user.

## Guardrails
- Stop immediately when `origin` remote is missing.
- Stop immediately when `gh auth` is invalid.
- Do not fabricate issue numbers; always use the command output.
- 본문 파일에 `T-000N`, 빈 `- `, 빈 체크박스 같은 미완성 텍스트를 남기지 않는다.

## References
- Command details: `references/commands.md`
