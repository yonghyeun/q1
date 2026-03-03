---
name: gh-issue-create
description: Create a GitHub issue from local terminal with standard templates.
---

# GH Issue Create

Create issue from template-complete body.

## Execute
1. `.github/ISSUE_TEMPLATE/<type>.md` 구조를 기준으로 본문 파일을 작성한다.
2. Run:
   - `./skills/public/gh-issue-create/scripts/run.sh --type <feature|bug|chore> --title "<title>" --body-file /tmp/issue.md`
3. 출력된 issue URL/번호를 사용자에게 전달한다.

## Guardrails
- `origin` remote 및 `gh auth`가 유효하지 않으면 중단한다.
- placeholder/빈 bullet이 남은 본문은 사용하지 않는다.

## References
- Command details: `references/commands.md`
