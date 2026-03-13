# Artifact Placement

## Decision
- agent-team 작업 context artifact는 `artifact type 기준 분리 + issue/task 인덱스 projection` 구조로 저장한다.
- backlog input SoT는 계속 GitHub issue가 소유한다.
- agent-team 전용 장기 문서는 `agent-team/context/`에 둔다.
- 승인된 task 정본과 task-level 분해 산출물은 `agent-team/tasks/<task-id>/`에 둔다.
- 임시 협업 메모는 issue 단위와 task 단위로 나눠 `agent-team/working-memory/issues/<issue-number>/`, `agent-team/working-memory/tasks/<task-id>/`에 둔다.
- runtime execution artifact는 `agent-team/runtime/`에 둔다.
- `run` 경로나 이름에 issue 번호나 task 식별자가 직접 드러나지 않아도 허용한다.
- 다만 모든 run root에는 issue/task 연결 metadata가 반드시 있어야 한다.
- task와 run의 연결은 각 run metadata를 읽어 생성한 `agent-team/tasks/<task-id>/run-index.yaml` projection과 run metadata의 양방향 참조로 관리한다.
- 장기 결정 기록은 계속 `context/decisions/`에 둔다.

## Why
- issue, 임시 메모, runtime trace, 영구 decision log를 한 경로에 섞으면 SoT와 보존 주기가 흐려진다.
- artifact type 기준 분리는 validator, retention rule, audit path를 단순하게 만든다.
- 반면 사람은 issue/task 기준으로 탐색하고 싶어하므로, 탐색 문제는 별도 projection으로 해결하는 편이 구조 drift가 적다.
- issue 수준 임시 메모와 task 수준 임시 메모를 분리하면 큰 작업의 공통 맥락과 세부 실행 메모를 분리할 수 있다.
- `run` 이름에 issue 번호를 강제하지 않으면 naming 충돌과 rename 비용을 줄일 수 있다.
- 대신 metadata와 인덱스를 강제하면 "어떤 run이 어떤 issue/task에 연결되는가"는 안정적으로 복원할 수 있다.

## Placement Rule
### 1. Backlog Input
- GitHub issue가 backlog input SoT다.
- issue 원문을 저장소 안에 mirror하지 않는다.
- 로컬 문서에는 issue 해석본, 계획 메모, runtime 결과만 저장한다.

### 2. Team-specific Long-lived Context
- `agent-team/context/`
- 목적:
  - agent-team이 장기적으로 공유해야 하는 운영 모델, 규칙, 인터페이스, 관측성 정의
- 예:
  - task model
  - role boundary
  - artifact placement

### 3. Temporary Working Memory
- `agent-team/working-memory/issues/<issue-number>/`
- `agent-team/working-memory/tasks/<task-id>/`
- 목적:
  - 현재 작업 중에만 필요한 임시 협업 메모 저장
- 예:
  - `plan.md`
  - `open-points.md`
  - `handoff-notes.md`
- 규칙:
  - scratchpad 성격 유지
  - 장기 SoT로 인용하지 않음
  - task 종료 후 삭제 가능
  - issue 단위 working memory는 큰 목표, 공통 쟁점, task 간 공유 메모를 담는다
  - task 단위 working memory는 특정 task의 세부 실행 메모를 담는다
  - 같은 내용을 issue/task working memory에 중복 복제하지 않는다
  - task working memory는 반드시 `issue_ref`, `task_ref`를 명시해 상위 issue와 연결되게 한다

### 4. Task Artifact
- `agent-team/tasks/<task-id>/`
- 목적:
  - 승인된 task 정본과 task-level 계획 산출물 저장
- 예:
  - `accepted-task.yaml`
  - `atomic-tasks.yaml`
  - `run-index.yaml`
- 규칙:
  - task 정의의 정본은 task 폴더가 소유한다
  - 하나의 task에서 여러 run이 파생될 수 있다
  - run artifact를 task 폴더에 복제하지 않는다

### 5. Runtime Artifact
- `agent-team/runtime/runs/<run-id>/`
- 목적:
  - 실제 실행 packet, trace, decision, ledger 저장
- 예:
  - `run.meta.yaml`
  - `planning/execution-plan.yaml`
  - `packets/`
  - `traces/`
  - `decisions/`
  - `ledgers/current.yaml`
  - `ledgers/snapshots/`

### 6. Repository-wide Long-lived Decision Log
- `context/decisions/`
- 목적:
  - 특정 작업의 임시 판단이 아니라 저장소 차원의 장기 결정 기록
- 규칙:
  - task-local memo나 runtime trace를 직접 보관하는 곳으로 쓰지 않음

## Recommended Layout
```text
agent-team/
  context/
    artifact-placement.md
  tasks/
    task-52-a/
      accepted-task.yaml
      atomic-tasks.yaml
      run-index.yaml
  working-memory/
    issues/
      52/
        plan.md
        open-points.md
        handoff-notes.md
    tasks/
      task-52-a/
        notes.md
        open-points.md
  runtime/
    runs/
      run-20260313-001/
        run.meta.yaml
        planning/
          execution-plan.yaml
        packets/
          packet-001-plan-worker.yaml
          packet-002-verify-reviewer.yaml
        traces/
          trace-001-worker-execution.yaml
          trace-002-worker-commit.yaml
        decisions/
          decision-001-accept.yaml
        ledgers/
          current.yaml
          snapshots/
            snapshot-001-accept.yaml

context/
  decisions/
    2026-03-13_agent-runtime-prompt-layering.md
```

## Run Identity Rule
- `run_id`는 runtime 실행 단위를 식별하는 중립 ID로 둔다.
- 파일명이나 디렉터리명만 보고 issue 번호를 즉시 추론할 수 없어도 괜찮다.
- 대신 아래 조건은 필수다.
  - 각 run root에 metadata file 존재
  - metadata에서 `issue_ref` 또는 동등한 source ref 확인 가능
  - metadata에서 `task_ref` 또는 accepted task ref 확인 가능
  - 사람용 인덱스에서 issue/task 기준 역추적 가능

## Run Metadata Minimum Shape
### Required Fields
- `run_id`
- `source_type`
- `issue_ref`
- `issue_url`
- `task_ref`
- `accepted_task_path`
- `task_run_index_path`
- `current_status`
- `created_at`
- `updated_at`

### Optional Fields
- `branch`
- `worktree`
- `owner_role`
- `latest_commit_sha`
- `latest_packet_id`
- `latest_trace_id`
- `latest_decision_id`

### Example
```yaml
run_id: run-20260313-001
source_type: github_issue
issue_ref: 52
issue_url: https://github.com/yonghyeun/q1/issues/52
task_ref: task-52-a
accepted_task_path: agent-team/tasks/task-52-a/accepted-task.yaml
task_run_index_path: agent-team/tasks/task-52-a/run-index.yaml
current_status: in_progress
created_at: 2026-03-13T09:10:00Z
updated_at: 2026-03-13T09:24:00Z
branch: chore/agent-team-context-artifact-path-rules
worktree: /abs/path/agent-team-context-artifact-path-rules--docs
latest_commit_sha: abc1234
latest_packet_id: packet-003
latest_trace_id: trace-004
latest_decision_id: decision-002
```

## Task-to-Run Linkage Rule
- `task`는 작업 정의와 task-level 계획의 정본을 소유한다.
- `run`은 실제 실행 이력을 소유한다.
- 따라서 task와 run은 아래처럼 연결한다.
  - `agent-team/tasks/<task-id>/run-index.yaml`
  - `agent-team/runtime/runs/<run-id>/run.meta.yaml`
- `run-index.yaml`은 task 관점의 run 목록 projection이다.
- `run.meta.yaml`은 run 관점의 task 참조 metadata다.
- 두 위치에 같은 packet, trace, ledger를 중복 저장하지 않는다.
- `run-index.yaml`은 수동 정본이 아니라 run metadata를 읽어 생성하는 projection이다.

## Single-team Run Example
- 아래 예시는 하나의 agent team이 issue 하나를 받아 `원자 작업 분해 -> 실행 -> 검증 -> 커밋`까지 진행한 경우다.
- commit은 별도 최상위 artifact 타입으로 분리하지 않는다.
- 대신 commit 결과는 `trace`와 `run.meta.yaml`의 `latest_commit_sha`로 남긴다.

```text
agent-team/
  tasks/
    task-52-a/
      accepted-task.yaml
      atomic-tasks.yaml
      run-index.yaml

  working-memory/
    issues/
      52/
        plan.md
        open-points.md
    tasks/
      task-52-a/
        notes.md
        open-points.md

  runtime/
    runs/
      run-20260313-001/
        run.meta.yaml
        planning/
          execution-plan.yaml
        packets/
          packet-001-plan-worker.yaml
          packet-002-verify-reviewer.yaml
        traces/
          trace-001-worker-execution.yaml
          trace-002-worker-commit.yaml
        decisions/
          decision-001-accept.yaml
        ledgers/
          current.yaml
          snapshots/
            snapshot-001-accept.yaml

agent-team/
  context/
    artifact-placement.md
```

### Stage Mapping
- 원자 작업 단계:
  - `tasks/task-52-a/atomic-tasks.yaml`
  - `runtime/runs/run-20260313-001/planning/execution-plan.yaml`
- 실행 단계:
  - `packets/packet-001-plan-worker.yaml`
  - `traces/trace-001-worker-execution.yaml`
- 검증 단계:
  - `packets/packet-002-verify-reviewer.yaml`
  - `decisions/decision-001-accept.yaml`
  - `ledgers/snapshots/snapshot-001-accept.yaml`
- 커밋 단계:
  - `traces/trace-002-worker-commit.yaml`
  - `run.meta.yaml`의 `latest_commit_sha`

### Example Meaning
- `accepted-task.yaml`
  - issue에서 승인된 작업 정의
- `tasks/task-52-a/atomic-tasks.yaml`
  - accepted task를 원자 단위로 쪼갠 목록
- `planning/execution-plan.yaml`
  - 특정 run에서 각 atomic task를 어떤 packet 순서로 처리할지 정한 계획
- `tasks/task-52-a/run-index.yaml`
  - run metadata를 읽어 생성한 이 task의 run 목록과 최신 run 상태 요약
- `working-memory/issues/52/`
  - issue 전체에서 공유되는 임시 메모
- `working-memory/tasks/task-52-a/`
  - 특정 task 실행 중에만 필요한 임시 메모
- `trace-001-worker-execution.yaml`
  - 실제 수정 파일, 실행 커맨드, check 결과 요약
- `trace-002-worker-commit.yaml`
  - commit SHA, commit message, 관련 changed files 요약
- `decision-001-accept.yaml`
  - reviewer의 accept/rework/block 판정

## Index Projection Rule
- 사람 탐색성은 metadata를 읽는 projection으로 해결한다.
- issue/task와 run을 직접 같은 디렉터리에 섞지 않는다.
- 권장 projection 경로:
  - `agent-team/index/issues/<issue-number>.md`
  - `agent-team/index/tasks/<task-id>.md`
- task별 `run-index.yaml`도 metadata를 읽어 생성하는 projection으로 본다.

### Issue Index Minimum Content
- `issue_ref`
- `title`
- `linked_working_memory`
- `linked_runs`
- `latest_run`
- `latest_status`

## Ownership By Artifact
- issue 해석본:
  - `agent-team/working-memory/issues/<issue-number>/`
- task 임시 메모:
  - `agent-team/working-memory/tasks/<task-id>/`
- accepted task:
  - `agent-team/tasks/<task-id>/accepted-task.yaml`
- atomic task list:
  - `agent-team/tasks/<task-id>/atomic-tasks.yaml`
- task별 run index:
  - `agent-team/tasks/<task-id>/run-index.yaml`
- execution plan:
  - `agent-team/runtime/runs/<run-id>/planning/execution-plan.yaml`
- packet:
  - `agent-team/runtime/runs/<run-id>/packets/`
- trace:
  - `agent-team/runtime/runs/<run-id>/traces/`
- operator decision:
  - `agent-team/runtime/runs/<run-id>/decisions/`
- current ledger:
  - `agent-team/runtime/runs/<run-id>/ledgers/current.yaml`
- snapshot ledger:
  - `agent-team/runtime/runs/<run-id>/ledgers/snapshots/`
- 장기 정책/모델 변경 결정:
  - `context/decisions/`

## Retention Rule
### Working Memory
- task 종료 후 삭제 가능
- 단, 장기 규칙으로 승격된 내용은 먼저 다른 SoT로 이동한다.

### Runtime Artifact
- audit과 replay를 위해 기본적으로 유지한다.
- `current ledger`는 projection이므로 갱신 가능하다.
- 그 외 trace, decision, snapshot은 append-only 원칙을 우선한다.

### Decision Log
- `context/decisions/` 문서는 삭제 대신 후속 decision으로 supersede한다.

## Boundary
- issue는 `what`, `why`, 제약, done signal을 담는 backlog input이다.
- working memory는 임시 협업 메모다.
- issue working memory는 `issue number`를 키로 쓴다.
- task working memory는 `task id`를 키로 쓴다.
- task는 승인된 작업 정의와 task-level 분해 산출물의 정본을 소유한다.
- runtime artifact는 실행 이력과 현재 상태 projection이다.
- run은 task의 복제본이 아니라 task를 참조하는 실행 단위다.
- decision log는 장기 정책 판단 기록이다.
- 같은 내용을 여러 계층에 중복 복제하지 않는다.

## Related Artifact
- backlog input과 task ingress 경계는 [task-model.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/task-model.md)에 둔다.
- runtime observability와 ledger 경계는 [observability.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/observability.md)에 둔다.
