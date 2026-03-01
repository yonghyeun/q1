---
name: gh-pr-create
description: Create a pull request with enforced issue close linkage and branch policy checks. Use when the user asks to open a PR, prepare merge readiness, or generate PR body that must include Closes #issue matching branch issue token.
---

# GH PR Create

Open PR only after policy and artifact checks pass.

## Input Evidence (write body after reading these)
PR 본문을 쓰기 전에 아래 근거를 먼저 확인한다.
1. `git diff --name-status main...HEAD`
2. `git log --oneline $(git merge-base main HEAD)..HEAD`
3. `agent-team/runs/<task-id>/` 산출물 (`task-brief.json`, `trace.md`, `run-log.md`, `run-report.json`)
4. 정책 문서 (`policies/branch-pr-convention.md`, `.github/pull_request_template.md`)

근거를 읽지 않고 추상 문장만으로 본문을 작성하지 않는다.

## Execute
1. `.github/pull_request_template.md` 구조를 기준으로 PR 본문 파일을 먼저 작성한다.
   - 모든 필수 섹션(`Issue Link`, `Why`, `What`, `범위`, `리스크`, `리뷰 포인트`, `참고 링크`)을 구체적으로 채운다.
   - `변경 요약(What)`에는 실제 변경 파일/모듈 단위를 포함한다(예: `scripts/repo/pr_create.sh`, `.github/workflows/branch-governance.yml`).
   - `범위`는 In/Out을 명확히 분리하고, 추후 과제를 Out-of-Scope에 분명히 적는다.
   - `수동 검증(선택)`은 실제 실행한 명령만 적는다. 실행하지 않은 테스트 결과를 추정/기재하지 않는다.
2. PR 제목을 컨벤션으로 생성/검증한다.
   - 생성: `./scripts/repo/pr_title_guard.sh generate --task-id <T-000N> --summary "<요약>"`
   - 검증: `./scripts/repo/pr_title_guard.sh validate --title "[T-000N] <요약>" --branch <current-branch>`
3. Run:
   - `./skills/public/gh-pr-create/scripts/run.sh --title "<PR title>" --body-file /tmp/pr.md`
4. Use `--draft` when the user wants review-before-ready mode.
5. Use `--dry-run` when user asks for preview only.

## Existing PR Update Rule
- 이미 같은 head branch의 PR이 열려 있으면, PR 수정은 `gh pr edit` 대신 `gh api --method PATCH`를 사용한다.
- 권장 명령:
  - 제목 수정:
    - `gh api --method PATCH repos/<owner>/<repo>/pulls/<number> -f title='<new-title>'`
  - 본문 수정:
    - `BODY=\"$(cat /tmp/pr.md)\"`
    - `gh api --method PATCH repos/<owner>/<repo>/pulls/<number> -f body=\"$BODY\"`
- 수정 후 `gh pr view <number> --json title,body,url`로 반영 여부를 반드시 확인한다.

## Issue Closing Policy
- 기본 정책은 `Closes #<issue-number>` 유지다(merge 시 해당 issue 자동 종료 목적).
- `Closes/Fixes/Resolves #N`의 `N`은 현재 브랜치 issue 번호와 반드시 동일해야 한다.
- close 링크는 1개 기준으로 명확히 작성하고, 다른 참조 이슈는 별도 텍스트로 분리한다.

## What this already validates
- branch naming policy
- task context path existence
- required run artifacts
- PR close keyword (`Closes/Fixes/Resolves #N`) matching branch issue number

## Guardrails
- Do not skip validations manually.
- Do not open PR if command returns non-zero exit.
- PR 본문에 사실과 다른 내용을 쓰지 않는다(특히 테스트 실행/운영 반영 여부).
- `Closes/Fixes/Resolves #N`는 브랜치 issue 번호와 반드시 일치해야 한다.
- placeholder/빈 bullet/빈 체크박스가 남아 있으면 본문을 수정한 뒤 재시도한다.
- 아래 자기검증을 통과하지 못하면 PR을 생성하지 않는다:
  1. `python3 scripts/repo/body_quality_guard.py --kind pr --body-file <path>`
  2. `python3 scripts/repo/pr_issue_guard.py --branch <current-branch> --pr-body-file <path>`
  3. `./skills/public/gh-pr-create/scripts/run.sh --title "<...>" --body-file <path> --dry-run`

## References
- Command matrix: `references/commands.md`
