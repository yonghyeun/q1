# GH PR Create Commands

## Required
- `./scripts/repo/pr_create.sh --title "<PR title>" --body-file <path>`

## Optional
- `--base main`
- `--draft`
- `--dry-run`

## Validations included
1. branch naming policy
2. task context existence
3. required run artifacts
4. PR body close-link match with branch issue number
5. PR body quality guard pass (`body_quality_guard.py`)

## Body writing rule (important)
- `.github/pull_request_template.md` 필수 섹션을 모두 채운다.
- `Closes/Fixes/Resolves #N` 키워드와 실제 issue 번호를 정확히 맞춘다.
- placeholder/빈 bullet/빈 체크박스 금지.
