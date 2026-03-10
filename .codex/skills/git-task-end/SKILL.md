---
name: git-task-end
description: >-
  Finalize a Git task in this repository through the task-end wrapper. Use when
  the user wants to end the current task, finish the current branch/PR work,
  close out the active worktree, review a task-end dry-run, or apply task-end
  after approval. 한국어 요청 예: task 종료, 작업 마무리, 현재 브랜치 작업 끝내기,
  현재 PR/task 종료, task end dry-run 확인, 승인 후 task end 실행.
---

# Git Task End

Use this skill for task finalization in this repository.

Trigger when the user asks to finish the current task, end a PR-backed task, finalize the current branch/worktree context, or review and apply task-end after approval. 한국어 요청 예: task 종료, 작업 마무리, 현재 PR 종료, 브랜치와 워크트리까지 정리, dry-run 보고 승인 후 실행.

## Workflow
1. Treat the request as task finalization, not raw PR merge.
2. Run `./.codex/skills/git-task-end/scripts/run.sh` first. This path performs dry-run only.
3. Summarize the plan for the user. Highlight PR, branch, worktree, merge method, and planned cleanup.
4. Ask for explicit approval in chat before any side effect.
5. After approval, run the same wrapper path with `--apply --yes`.
6. If a gate fails, follow the error message's `다음 행동:` and retry the same wrapper path.

## Guardrails
- Raw `gh pr merge` 직접 호출 지양.
- raw branch cleanup / raw worktree cleanup 조합으로 우회하지 않음.
- 기본 merge method는 `squash`.
- merge subject는 기본적으로 PR title 사용.
- skill은 interactive shell wrapper를 호출하지 않음. 항상 core wrapper만 사용.
- 실제 실행은 사용자 승인 후 `--apply --yes` 경로로만 진행.

## References
- Command options and examples: `references/commands.md`
