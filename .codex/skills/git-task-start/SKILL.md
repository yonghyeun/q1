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
3. Check whether the wrapper will need network access on the first run. `git-task-start` dry-run performs `git fetch origin --prune`, and `--issue` also calls `gh issue view`.
4. If that network dependency is expected, request escalated network permission on the first wrapper execution instead of waiting for a sandbox failure/retry loop. Approval is still explicit and user-driven.
5. Run `./.codex/skills/git-task-start/scripts/run.sh` first. This path performs dry-run only.
6. Summarize the plan for the user. Highlight branch, base, purpose, target path, and whether branch creation is needed.
7. Ask for explicit approval in chat before any side effect.
8. After approval, run the same wrapper path with `--apply --yes`.
9. If `--issue` was used, fetch the issue body after apply with `gh issue view <number> --json number,title,body,labels,url` and summarize it through `scripts/issue_summary.py`.
10. Present the summary in chat with four bullets: `목적`, `완료 조건`, `제약/주의`, `첫 작업 후보`. If the body is sparse, allow title/labels/checklist fallback.
11. If the current session will continue the implementation, pin all further work to the new worktree path explicitly.
12. If a gate fails, follow the error message's `다음 행동:` and retry the same wrapper path.

## Guardrails
- skill은 `task_start_interactive.sh` 를 호출하지 않음.
- raw `git worktree add` 직접 호출 지양.
- dry-run 이더라도 네트워크 의존성이 예상되면 sandbox 실패 후 재시도보다 선승격 요청을 우선한다.
- 실제 실행은 사용자 승인 후 `--apply --yes` 경로로만 진행.
- issue 요약 생성 책임은 skill 레이어에 둔다. core wrapper에 summary 출력을 추가하지 않는다.
- branch가 이미 다른 worktree에서 checkout 중이면 기존 worktree 재사용 또는 새 branch 사용으로 유도.
- 기존 worktree 생성 전용 흐름보다 task 시작 오케스트레이션을 우선한다.

## References
- Command options and examples: `references/commands.md`
