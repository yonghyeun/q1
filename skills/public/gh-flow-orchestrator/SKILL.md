---
name: gh-flow-orchestrator
description: Orchestrate end-to-end GitHub workflow using atomic skills (issue create, task branch start, PR create, PR merge, branch cleanup). Use when the user asks for one-command flow management across multiple steps rather than running each step manually.
---

# GH Flow Orchestrator

Use this skill as a thin orchestrator over atomic scripts.  
Keep policy enforcement in repository scripts, not in the skill text.

## Modes
1. `start`: start task branch from known issue number
2. `open-pr`: create PR from current branch
3. `merge`: merge PR and cleanup
4. `full`: create issue + start branch + create PR

## Execute
- Run:
  - `./skills/public/gh-flow-orchestrator/scripts/run_flow.sh --mode <start|open-pr|merge|full> ...`
- `open-pr/full` 모드에서는 `--pr-body-file`을 반드시 제공한다.
- `full` 모드에서 새 issue 생성 시 `--issue-body-file`을 반드시 제공한다.
- Prefer `--dry-run` first for high-risk or unfamiliar tasks.
- `open-pr/full`에서 PR 본문은 `gh-pr-create` 스킬 규칙(근거 수집 + 템플릿 충실 작성)을 따른다.
- merge 시 issue 자동 종료를 의도하므로 PR 본문에는 `Closes #<branch-issue>`를 유지한다.

## Guardrails
- Do not bypass atomic checks.
- Stop immediately when any sub-step fails.
- Surface exact failed command and next recovery action.
- 본문 파일은 템플릿 섹션을 모두 채운 상태여야 하며 placeholder가 없어야 한다.
- 실행하지 않은 테스트를 본문에 적지 않는다.

## References
- Workflow and examples: `references/workflow.md`
