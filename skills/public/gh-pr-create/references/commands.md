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
- 본문 작성 전에 아래 근거를 먼저 수집한다.
  - `git diff --name-status main...HEAD`
  - `git log --oneline $(git merge-base main HEAD)..HEAD`
  - `agent-team/runs/<task-id>/` 핵심 산출물 4종
- `.github/pull_request_template.md` 필수 섹션을 모두 채운다.
- `Closes/Fixes/Resolves #N` 키워드와 실제 issue 번호를 정확히 맞춘다.
- 기본 링크는 `Closes #N`을 사용한다(merge 시 issue 자동 종료 목적).
- placeholder/빈 bullet/빈 체크박스 금지.
- 추상 문장 금지: `변경 요약`에는 실제 파일/모듈 단위 근거를 포함한다.
- 테스트 자동화가 아직 workflow에 편입되지 않았다면, 실행하지 않은 테스트 결과를 기재하지 않는다.

## Recommended self-check
1. `python3 scripts/repo/body_quality_guard.py --kind pr --body-file <path>`
2. `python3 scripts/repo/pr_issue_guard.py --branch <current-branch> --pr-body-file <path>`
3. `./skills/public/gh-pr-create/scripts/run.sh --title "<PR title>" --body-file <path> --dry-run`
