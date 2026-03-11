# Repo Issue Create Commands

## Required
- `./.codex/skills/repo-issue-create/scripts/run.sh --type <feature|bug|chore> --status <inbox|ready|active|blocked|cancelled> --priority <p0|p1|p2|p3> --source-type <human-request|agent-team|runtime-observation|wbs-planned> --area <product|repo|docs|agent-team> [--area <product|repo|docs|agent-team> ...] --title "<title>" --body-file <path>`

## Type selection
- `feature`: 제품/사용자 관점의 기능 추가, 기능 개선, 가치 변화.
- `bug`: 재현 가능한 오류, 회귀, 잘못된 동작.
- `chore`: 운영, 정책, 자동화, 설정, 문서 정리.
- branch/worktree/task wrapper, hook, metadata, taxonomy, template 정비는 기본적으로 `chore`.
- "추가", "지원", "연결", "추적" 같은 표현만으로 `feature`로 분류하지 않음.

## Suggested authoring flow
1. 해당 type의 `.github/ISSUE_TEMPLATE/<type>.md` 읽기.
2. `status`, `priority`, `area`, `source_type` 값을 선택.
3. 제목을 `[type] 요약` 형식으로 작성.
4. body 초안 작성.
5. wrapper 실행.
6. 실패 시 gate 메시지의 `다음 행동:` 반영 후 재시도.

## Self-check helpers
- 제목 검증:
  - `./scripts/repo/issue_title_guard.sh validate --type <type> --title "[type] 요약"`
- 본문 검증:
  - `python3 ./scripts/repo/issue_body_quality_guard.py --issue-type <type> --body-file <path>`
- label 검증:
  - `python3 ./scripts/repo/issue_label_guard.py --type <type> --status <status> --priority <priority> --source-type <source-type> --area <area>`

## Gates reached through the wrapper
- `issue-title`
- `issue-body`
- `issue-label`
