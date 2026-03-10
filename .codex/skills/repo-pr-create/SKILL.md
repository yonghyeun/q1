---
name: repo-pr-create
description: >-
  Create, draft, or fix a GitHub pull request in this repository. Use when the
  user wants to open a PR, draft a PR, write or rewrite a PR body, prepare a
  pull request from the current branch, dry-run PR creation, or fix PR
  title/body/branch/issue-link gate failures through the local PR wrapper. 한국어
  요청 예: PR 생성, PR 초안 작성, PR 본문 작성, PR 열기, 현재 브랜치로 PR 만들기, PR
  게이트 실패 수정.
---

# Repo PR Create

Use this skill for PR creation in this repository.

Trigger when the user asks to open, draft, write, revise, or fix a GitHub pull request for this repository. 한국어 요청 예: PR 생성, PR 초안 작성, PR 본문 수정, PR 열기, 풀리퀘 생성, PR 게이트 오류 수정.

## Workflow
1. Read `.github/pull_request_template.md`.
2. If needed, read `policies/branch-pr-convention.md` and the PR gate docs under `policies/gates/`.
3. Before drafting, identify the operating problem, why this work is needed now, and what behavior or workflow should improve after merge.
4. Draft the PR title and PR body in a local temp file.
5. Write `Changes` as expected effects, operating model shifts, or newly enabled workflow. Do not default to a file-by-file changelog.
6. Write `Decisions Made` with the context that forced the decision, the chosen direction, and why the rejected alternative was not kept.
7. Run `./.codex/skills/repo-pr-create/scripts/run.sh` instead of raw `gh pr create`.
8. If the PR already exists and only title/body must be revised, keep the same local draft flow and use `gh pr edit` only for the final remote update.
9. If a gate fails, follow the error message's `다음 행동:` and retry the same wrapper path.

## Guardrails
- Raw `gh pr create` 직접 호출 지양.
- `Primary Issue`에는 close keyword 필요.
- `Related Issues`, `Decisions Made`, `Validation Notes`까지 빠짐없이 채우기.
- `Changes`는 파일 목록보다 기대 효과와 운영 변화가 먼저 드러나야 함.
- `Decisions Made`는 결론만 적지 말고, 그 결정을 하게 된 맥락과 버린 대안을 함께 남겨야 함.
- 장기 SoT가 필요한 결정은 `context/decisions/`로 분리하고 PR에는 요약과 링크만 남기기.

## References
- Command options and examples: `references/commands.md`
