# GH Issue Create Commands

## Required
- `./scripts/repo/issue_create.sh --type <feature|bug|chore> --title "<title>" --body-file <path>`

## Preflight checks
- `origin` remote configured
- `gh auth` valid
- issue body quality guard pass (`body_quality_guard.py`)

## Body writing rule
- `.github/ISSUE_TEMPLATE/<type>.md`의 모든 섹션을 구체 문장으로 채운다.
- placeholder/빈 bullet 금지.

## Recommended self-check
1. `python3 scripts/repo/body_quality_guard.py --kind issue --issue-type <feature|bug|chore> --body-file <path>`
2. 생성 후 출력된 issue URL/번호를 기록
