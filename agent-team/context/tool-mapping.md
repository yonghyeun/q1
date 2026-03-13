# Tool Mapping

## Decision
- 역할별 도구 맵핑은 `허용 도구`, `우선 도구`, `금지 도구`, `검증 도구` 기준으로 정의한다.
- wrapper가 있는 액션은 raw 명령보다 wrapper-first를 기본으로 둔다.
- 최소 권한 원칙에 따라 각 역할은 자신의 stage에 필요한 도구만 사용한다.

## Why
- 같은 역할이라도 사용할 수 있는 도구가 무제한이면 boundary가 다시 무너진다.
- wrapper-first를 명시해야 gate 우회 가능성을 줄일 수 있다.
- tool mapping은 profile 설계 전 단계에서 runtime capability boundary 역할을 한다.

## Global Principles
- 검색은 읽기 전용 경로를 우선한다.
- 생성/수정/상태 전이는 wrapper 또는 gate가 있는 경로를 우선한다.
- 검증 가능한 변경은 validator, test, guard를 먼저 실행한다.
- 배포와 merge는 초기 agent-team 범위에서 제외한다.

## Tool Classes
- `Read/Search`
  - `rg`
  - `sed`
  - `git status`
  - `git diff`
  - `git show`
  - `current_issue.sh`
  - `current_pr.sh`
- `Planning/Artifact`
  - `codex_wbs_emit.sh`
  - `validate_wbs_artifact.py`
  - template/schema 문서
- `Repo Wrapper`
  - `task_start.sh`
  - `task_end.sh`
  - `issue_create.sh`
  - `pr_create.sh`
  - `worktree_add.sh`
- `Guards/Validation`
  - `branch_guard.py`
  - `detached_head_guard.py`
  - `protected_branch_write_guard.py`
  - `dirty_worktree_guard.py`
  - `issue_title_guard.sh`
  - `issue_body_quality_guard.py`
  - `issue_label_guard.py`
  - `pr_title_guard.sh`
  - `pr_body_quality_guard.py`
  - `pr_issue_guard.py`
- `Execution/Test`
  - repo/unit test commands
  - formatter/linter
  - schema validator
- `Forbidden In Initial Scope`
  - `pr_merge.sh`
  - raw deploy command
  - infra mutation command

## Role Mapping
### Router
- primary use:
  - `rg`
  - `sed`
  - `current_issue.sh`
  - `git status`
  - `git diff`
- optional support:
  - `issue_label_guard.py`
  - `issue_body_quality_guard.py`
- does not use:
  - code formatter
  - app test runner
  - deploy/merge command
- reason:
  - intake와 normalization은 read-heavy이기 때문

### Planner
- primary use:
  - `rg`
  - `sed`
  - `codex_wbs_emit.sh`
  - `validate_wbs_artifact.py`
  - schema/template 문서
- optional support:
  - `git diff`
  - `git show`
- does not use:
  - production deploy
  - merge command
  - broad write command outside planning artifact
- reason:
  - decomposition과 packet 설계는 artifact generation/validation 중심이기 때문

### Worker
- primary use:
  - file edit path
  - repo-local test command
  - formatter/linter
  - `git diff`
  - `git status`
- wrapper-first actions:
  - issue/PR/worktree 관련 액션 필요 시 전용 wrapper 우선
- required validation:
  - owned path 관련 테스트
  - schema/format guard
  - relevant repo gate
- does not use:
  - deploy command
  - merge command
  - raw `git worktree` create
- reason:
  - runtime execution은 수정 + 검증 범위에 한정하기 때문

### Reviewer
- primary use:
  - `git diff`
  - `git show`
  - test rerun
  - validator rerun
  - guard rerun
- optional support:
  - `current_issue.sh`
  - `current_pr.sh`
- does not use:
  - implementation write command as 기본 수단
  - deploy/merge command
- reason:
  - review는 evidence 확인과 재검증이 중심이기 때문

## Example Mapping In Roadmap Terms
### 검색 전용
- 주 역할:
  - `Router`
  - `Planner`
  - `Reviewer`
- 도구:
  - `rg`
  - `sed`
  - `git show`
  - `git diff`

### 코드 수정 전용
- 주 역할:
  - `Worker`
- 도구:
  - file edit path
  - formatter
  - repo-local test command
- 조건:
  - `owned_paths` 안에서만 허용

### 테스트 실행 전용
- 주 역할:
  - `Worker`
  - `Reviewer`
- 도구:
  - unit test
  - integration test
  - `validate_wbs_artifact.py`
  - quality guards

### 배포 금지
- 적용 역할:
  - `Router`
  - `Planner`
  - `Worker`
  - `Reviewer`
- 금지 도구:
  - deploy command
  - infra mutation command
  - merge 자동화 command

## Wrapper First Rules
- issue 생성:
  - `issue_create.sh`
- PR 생성:
  - `pr_create.sh`
- task 시작:
  - `task_start.sh`
- task 종료:
  - `task_end.sh`
- worktree 생성:
  - `worktree_add.sh`
- 금지:
  - wrapper가 있는 액션에서 raw `gh` 또는 raw `git worktree`를 우선 사용하는 것

## Least Privilege Rules
- `Router`
  - read-only 기본
  - intake artifact 외 write 금지
- `Planner`
  - planning artifact write만 허용
  - runtime output write 금지
- `Worker`
  - owned path write만 허용
  - policy surface write 금지
- `Reviewer`
  - review artifact write만 허용
  - implementation write를 기본 경로로 쓰지 않음

## Open Point
- profile 단계에서 tool permission을 config로 얼마나 강하게 분리할지는 추후 결정한다.
