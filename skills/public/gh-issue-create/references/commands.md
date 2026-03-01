# GH Issue Create Commands

## Required
- `./scripts/repo/issue_create.sh --type <feature|bug|chore> --task-id <T-000N> --title "<title>" --body-file <path>`

## Preflight checks
- `origin` remote configured
- `gh auth` valid
- issue body quality guard pass (`body_quality_guard.py`)

## Body writing rule (important)
- `.github/ISSUE_TEMPLATE/<type>.md`의 모든 섹션을 구체 문장으로 채운다.
- placeholder/빈 bullet 금지 (`T-000N`, `- `, 빈 체크박스).

## Expected output
- Issue URL
- Issue number
