# GH Issue Create Commands

## Required
- `./scripts/repo/issue_create.sh --type <feature|bug|chore> --task-id <T-000N> --title "<title>" --body-file <path>`

## Preflight checks
- `origin` remote configured
- `gh auth` valid
- issue body quality guard pass (`body_quality_guard.py`)

## Body writing rule (important)
- 본문 작성 전에 작업 근거를 먼저 확인한다.
  - `agent-team/runs/<task-id>/task-brief.json` (있으면 필수 참조)
  - `agent-team/runs/<task-id>/trace.md`, `run-log.md`, `run-report.json` (있으면 반영)
- `.github/ISSUE_TEMPLATE/<type>.md`의 모든 섹션을 구체 문장으로 채운다.
- 톤/밀도 기준이 필요하면 `references/sample-feature-issue.md`를 참조한다.
- placeholder/빈 bullet 금지 (`T-000N`, `- `, 빈 체크박스).
- 실행하지 않은 테스트/검증 결과를 완료로 기재하지 않는다.
- 확인되지 않은 assignee/외부 승인/운영 반영 상태를 단정적으로 쓰지 않는다.

## Recommended self-check
1. `python3 scripts/repo/body_quality_guard.py --kind issue --issue-type <feature|bug|chore> --body-file <path>`
2. 본문의 `Task ID`와 `--task-id` 값이 동일한지 확인
3. 생성 후 출력된 issue URL/번호를 기록

## Expected output
- Issue URL
- Issue number
