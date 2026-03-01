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
- Prefer `--dry-run` first for high-risk or unfamiliar tasks.

## Guardrails
- Do not bypass atomic checks.
- Stop immediately when any sub-step fails.
- Surface exact failed command and next recovery action.

## References
- Workflow and examples: `references/workflow.md`
