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
2. Check whether the wrapper will need network access on the first run. `git-task-end` may call `gh pr view` during dry-run, and may also call `gh issue view`, `gh issue edit`, remote branch lookup, or push/PR creation helpers during apply.
3. If that network dependency is expected, request escalated network permission on the first wrapper execution instead of waiting for a sandbox failure/retry loop. Approval is still explicit and user-driven.
4. Run `./.codex/skills/git-task-end/scripts/run.sh` first. This path performs dry-run only.
5. Summarize the plan for the user. Highlight PR, branch, worktree, merge method, and planned cleanup.
6. Ask for explicit approval in chat before any side effect.
7. After approval, run the same wrapper path with `--apply --yes`.
8. If apply succeeds, read the merged PR again and print a short handoff summary with change purpose, key changes, impact scope, and follow-up checks. Prefer `./.codex/skills/git-task-end/scripts/pr_summary.py --pr <number> ...` and pass linked issue context when already known.
9. If a gate fails, follow the error message's `다음 행동:` and retry the same wrapper path.

## Guardrails
- Raw `gh pr merge` 직접 호출 지양.
- raw branch cleanup / raw worktree cleanup 조합으로 우회하지 않음.
- dry-run 또는 apply 에서 네트워크 의존성이 예상되면 sandbox 실패 후 재시도보다 선승격 요청을 우선한다.
- 기본 merge method는 `squash`.
- merge subject는 기본적으로 PR title 사용.
- skill은 interactive shell wrapper를 호출하지 않음. 항상 core wrapper만 사용.
- 실제 실행은 사용자 승인 후 `--apply --yes` 경로로만 진행.
- post-apply PR summary는 skill 레이어 책임. core wrapper에 merge 후 요약 출력 책임을 추가하지 않는다.
- PR body가 빈약하면 title, linked issue, merge 결과를 이용해 fallback 요약을 구성한다.

## References
- Command options and examples: `references/commands.md`
