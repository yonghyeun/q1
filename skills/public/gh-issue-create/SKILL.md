---
name: gh-issue-create
description: Create a GitHub issue from local terminal with task linkage and standard templates. Use when the user asks to open a new issue, start a task from an issue, or standardize issue metadata (feature/bug/chore + T-000N).
---

# GH Issue Create

Create issue first, then derive branch workflow from the issue number.

## Input Evidence (write body after reading these)
Issue 본문 작성 전에 아래 근거를 먼저 확인한다.
1. `agent-team/runs/<task-id>/task-brief.json` (있으면 우선 참조)
2. `agent-team/runs/<task-id>/trace.md`, `run-log.md`, `run-report.json` (있으면 반영)
3. 관련 정책/아키텍처 문서 (`policies/*`, `docs/architecture/*`) 중 작업과 직접 연관된 파일

근거 확인 없이 추상 문장만으로 issue 본문을 작성하지 않는다.

## Execute
1. `.github/ISSUE_TEMPLATE/<type>.md` 구조를 기준으로 본문 파일을 먼저 작성한다.
   - 모든 섹션에 구체 내용을 채운다(빈 bullet/placeholder 금지).
   - `Scope`/`Acceptance Criteria`는 실제 실행 가능한 항목으로 작성한다.
   - 실행하지 않은 결과(테스트 통과, 운영 반영 완료 등)를 사실처럼 적지 않는다.
   - 확인되지 않은 메타데이터(assignee 확정, 외부 승인 완료 등)는 단정적으로 기재하지 않는다.
   - 샘플 톤이 필요하면 `references/sample-feature-issue.md`를 기준으로 맞춘다.
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
- 사실과 다른 상태를 작성하지 않는다(예: 미실행 검증을 완료로 기재).
- 생성 직후 issue URL/번호를 반드시 사용자에게 명시한다.

## References
- Command details: `references/commands.md`
- Body sample: `references/sample-feature-issue.md`
