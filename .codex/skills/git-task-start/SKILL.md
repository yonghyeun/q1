---
name: git-task-start
description: >-
  Start a new task in this repository through the task-start wrapper. Use when
  the user wants to start a new task, prepare a fresh branch/worktree pair,
  review a task-start dry-run, or apply task-start after approval. 한국어 요청 예:
  새 작업 시작, 브랜치와 워크트리 준비, task start dry-run 확인, 승인 후 task start
  실행.
---

# Git Task Start

Use this skill for task start in this repository.

Trigger when the user asks to start a new task, prepare a fresh branch/worktree pair, review a task-start dry-run, or apply task-start after approval. 한국어 요청 예: 새 작업 시작, 새 브랜치와 워크트리 만들기, 작업 시작 준비, task start dry-run 보고 승인 후 실행.

## Workflow
1. Decide the target branch and worktree purpose.
2. If naming is unclear, read `policies/branch-naming.md` and `policies/worktree-naming.md`.
3. Run `./.codex/skills/git-task-start/scripts/run.sh` first. This path performs dry-run only.
4. Summarize the plan for the user. Highlight branch, base, purpose, target path, and whether branch creation is needed.
5. Ask for explicit approval in chat before any side effect.
6. After approval, run the same wrapper path with `--apply --yes`.
7. After apply, state that the user's shell cwd is unchanged.
8. If the current session will continue the implementation, pin all further work to the new worktree path explicitly.
9. If the user will restart from the new worktree, emit a concise restart handoff that includes branch, worktree path, task goal, current diff status, open risks, and next recommended action.
10. If a gate fails, follow the error message's `다음 행동:` and retry the same wrapper path.

## Guardrails
- skill은 `task_start_interactive.sh` 를 호출하지 않음.
- raw `git worktree add` 직접 호출 지양.
- 실제 실행은 사용자 승인 후 `--apply --yes` 경로로만 진행.
- branch가 이미 다른 worktree에서 checkout 중이면 기존 worktree 재사용 또는 새 branch 사용으로 유도.
- 기존 worktree 생성 전용 흐름보다 task 시작 오케스트레이션을 우선한다.
- 병렬 작업이나 명시적 재시작 흐름에서는 새 세션이 이전 대화를 자동 상속한다고 가정하지 않는다.
- 새 세션 재실행을 권장할 때는 현재 세션이 handoff 요약을 남겨야 한다.

## References
- Command options and examples: `references/commands.md`
- Session split and restart handoff: `references/session-handoff.md`
