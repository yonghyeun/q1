# GH Flow Orchestrator Workflow

## Modes
1. `start`: issue number 기반 브랜치 시작
2. `open-pr`: 현재 브랜치 PR 생성
3. `merge`: PR merge + local cleanup
4. `full`: issue 생성 + 브랜치 시작 + PR 생성

## Commands
- `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode <...> ...`

## Examples
- full:
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode full --task-id T-0002 --type feature --title "결제 플로우 정리" --issue-body-file /tmp/issue.md --slug billing-flow --pr-title "[T-0002] 결제 플로우 정리" --pr-body-file /tmp/pr.md`
- open-pr:
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode open-pr --pr-title "[T-0002] 결제 플로우 정리" --pr-body-file /tmp/pr.md`
- merge:
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode merge --merge-method squash`

## Body quality rule
- Issue/PR 본문 파일은 템플릿 필수 섹션을 모두 채워야 한다.
- placeholder(`T-000N`, `<issue-number>`)나 빈 bullet은 허용되지 않는다.
- PR 본문은 작성 전에 `git diff`/`git log`/`runs 산출물` 근거를 먼저 확인한다.
- PR 이슈 링크는 기본적으로 `Closes #<branch-issue-number>`를 사용한다.
- 실행하지 않은 테스트 결과를 기재하지 않는다(테스트 workflow 도입 전에는 추정 표현 금지).

## Existing PR update command
- 제목/본문 수정은 `gh pr edit` 대신 API PATCH를 사용한다.
  - `gh api --method PATCH repos/<owner>/<repo>/pulls/<number> -f title='<new-title>'`
  - `BODY=\"$(cat /tmp/pr.md)\" && gh api --method PATCH repos/<owner>/<repo>/pulls/<number> -f body=\"$BODY\"`
