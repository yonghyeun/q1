# GH Flow Orchestrator Workflow

## 예시
- full 흐름
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode full --branch config/wbs-governance-reset --type chore --title "거버넌스 정리" --issue-body-file /tmp/issue.md --pr-title "[config] 거버넌스 정리" --pr-body-file /tmp/pr.md`
- PR만 생성
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode open-pr --pr-title "[config] 거버넌스 정리" --pr-body-file /tmp/pr.md`
- merge만 실행
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode merge --merge-method squash --merge-subject "[config] 거버넌스 정리"`

## 유의사항
- placeholder나 빈 bullet이 남은 issue/PR 본문은 허용되지 않는다.
- 브랜치 정책을 먼저 통과해야 후속 단계가 진행된다.
