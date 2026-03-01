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
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode full --task-id T-0002 --type feature --title "결제 플로우 정리" --slug billing-flow --pr-title "[T-0002] 결제 플로우 정리"`
- merge:
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode merge --merge-method squash`
