# GH Issue Create Commands

## Required
- `./scripts/repo/issue_create.sh --type <feature|bug|chore> --task-id <T-000N> --title "<title>" --body-file <path>`

## Preflight checks
- `origin` remote configured
- `gh auth` valid
- issue body quality guard pass (`body_quality_guard.py`)

## Body writing rule (important)
- 본문 작성 전에 작업 근거를 먼저 확인한다.
  - `context/tasks/<task-id>/context.md` (있으면 참조)
  - `context/tasks/<task-id>/result.md` (있으면 반영)
- `.github/ISSUE_TEMPLATE/<type>.md`의 모든 섹션을 구체 문장으로 채운다.
- placeholder/빈 bullet 금지 (`T-000N`, `- `, 빈 체크박스).

## Recommended self-check
1. `python3 scripts/repo/body_quality_guard.py --kind issue --issue-type <feature|bug|chore> --body-file <path>`
2. 본문의 `Task ID`와 `--task-id` 값이 동일한지 확인
3. 생성 후 출력된 issue URL/번호를 기록

## Expected output
- Issue URL
- Issue number
