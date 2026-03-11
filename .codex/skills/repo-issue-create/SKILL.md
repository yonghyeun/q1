---
name: repo-issue-create
description: >-
  Create, draft, or fix a GitHub issue in this repository. Use when the user
  wants to open an issue, file a bug, write a feature request, create a chore
  issue, choose an issue type, fill the local issue template, or fix issue
  title/body gate failures through the local issue wrapper. 한국어 요청 예: 이슈 생성,
  버그 이슈 작성, 기능 요청 이슈 작성, chore 이슈 만들기, 이슈 템플릿 채우기, 이슈
  게이트 실패 수정.
---

# Repo Issue Create

Use this skill for issue creation in this repository.

Trigger when the user asks to open, draft, write, revise, or fix a GitHub issue for this repository. 한국어 요청 예: 이슈 생성, 이슈 초안 작성, 이슈 본문 작성, 버그 이슈 등록, 기능 요청 이슈 작성, 이슈 게이트 오류 수정.

## Workflow
1. Choose the issue type: `feature`, `bug`, or `chore`.
   - 제품/사용자 관점의 동작이나 가치 전달이 바뀌면 `feature`를 우선 검토.
   - branch/worktree/wrapper/policy/template/metadata 같은 repo 운영 작업이면 `chore` 가설에서 시작.
2. Choose labels for all required axes: `status`, `priority`, `area`, `source_type`.
3. Read the matching template under `.github/ISSUE_TEMPLATE/`.
4. If needed, read `policies/issue-convention.md` and the issue gate docs under `policies/gates/`.
5. Draft the title and issue body in a local temp file.
6. Run `./.codex/skills/repo-issue-create/scripts/run.sh` instead of raw `gh issue create`.
7. If a gate fails, follow the error message's `다음 행동:` and retry the same wrapper path.

## Guardrails
- Raw `gh issue create` 직접 호출 지양.
- 제목은 `[type] 요약` 형식 유지.
- "추가", "지원", "연결" 같은 표현만으로 `feature`로 분류하지 않기.
- `Decision Candidates`, `Done Signal`, `Related Links`를 비우지 않기.
- `status`, `priority`, `source_type`는 각각 1개씩 지정.
- `area`는 1개 이상 지정.
- 필요한 링크는 각 섹션 안에 inline으로 두기.

## References
- Command options and type selection: `references/commands.md`
