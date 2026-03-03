---
name: gh-flow-orchestrator
description: Orchestrate GitHub issue/branch/PR/merge workflow with one command.
---

# GH Flow Orchestrator

`run_flow.sh`로 issue 생성, 브랜치 시작, PR 생성, merge 단계를 한 번에 실행한다.

## Modes
- `start`: 브랜치 시작
- `open-pr`: PR 생성
- `merge`: PR 머지
- `full`: issue 생성 + 브랜치 시작 + PR 생성

## 핵심 인자
- `--branch <scope/slug>`
- `--type <feature|bug|chore>`
- `--title "..."`
- `--issue-body-file /tmp/issue.md`
- `--pr-title "[scope] ..."`
- `--pr-body-file /tmp/pr.md`

## 실행
- `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode full ...`
