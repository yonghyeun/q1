---
name: gh-issue-create
description: Create a GitHub issue from local terminal with task linkage and standard templates. Use when the user asks to open a new issue, start a task from an issue, or standardize issue metadata (feature/bug/chore + T-000N).
---

# GH Issue Create

Create issue first, then derive branch workflow from the issue number.

## Input Evidence (write body after reading these)
Issue 본문 작성 전에 아래 근거를 먼저 확인한다.
1. `context/tasks/<task-id>/context.md` (있으면 우선 참조)
2. `context/tasks/<task-id>/result.md` (있으면 반영)
3. 관련 정책/아키텍처 문서 (`policies/*`, `docs/architecture/*`) 중 작업과 직접 연관된 파일

근거 확인 없이 추상 문장만으로 issue 본문을 작성하지 않는다.

## Execute
1. `.github/ISSUE_TEMPLATE/<type>.md` 구조를 기준으로 본문 파일을 먼저 작성한다.
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

## References
- Command details: `references/commands.md`
- Body sample: `references/sample-feature-issue.md`
