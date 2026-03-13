# Artifact Placement

## Decision
- agent-team 작업 context artifact는 `artifact type 기준 분리 + issue/task 인덱스 projection` 구조로 저장한다.
- backlog input SoT는 계속 GitHub issue가 소유한다.
- agent-team 전용 장기 문서는 `agent-team/context/`에 둔다.
- 승인된 task 정본과 task-level 분해 산출물은 `agent-team/tasks/<task-id>/`에 둔다.
- 임시 협업 메모는 `agent-team/working-memory/tasks/<task-id>/`에 둔다.
- task id 형식은 `task-<issue-number>-<seq>`로 고정한다.
- runtime execution artifact는 `agent-team/runtime/`에 둔다.
- `run` 경로나 이름에 issue 번호나 task 식별자가 직접 드러나지 않아도 허용한다.
- 다만 모든 run root에는 task 연결 metadata가 반드시 있어야 한다.
- task와 run의 연결은 각 run metadata를 읽어 생성한 `agent-team/tasks/<task-id>/run-index.yaml` projection과 run metadata의 양방향 참조로 관리한다.
- 장기 결정 기록은 계속 `context/decisions/`에 둔다.

## Why
- issue, 임시 메모, runtime trace, 영구 decision log를 한 경로에 섞으면 SoT와 보존 주기가 흐려진다.
- artifact type 기준 분리는 validator, retention rule, audit path를 단순하게 만든다.
- 반면 사람은 issue/task 기준으로 탐색하고 싶어하므로, 탐색 문제는 별도 projection으로 해결하는 편이 구조 drift가 적다.
- issue가 항상 task 단위로 생성된다면, 로컬 실행 계층은 task 중심으로만 유지하는 편이 중복 참조와 sync 비용이 적다.
- `run` 이름에 issue 번호를 강제하지 않으면 naming 충돌과 rename 비용을 줄일 수 있다.
- 대신 metadata와 인덱스를 강제하면 "어떤 run이 어떤 task에 연결되는가"는 안정적으로 복원할 수 있고, issue는 task 정본을 따라 역추적할 수 있다.

## Placement Rule
### 1. Backlog Input
- GitHub issue가 backlog input SoT다.
- issue 원문을 저장소 안에 mirror하지 않는다.
- issue 정보는 task 정본에서 참조한다.
- 로컬 문서에는 task 정본, 계획 메모, runtime 결과만 저장한다.

### 2. Team-specific Long-lived Context
- `agent-team/context/`
- 목적:
  - agent-team이 장기적으로 공유해야 하는 운영 모델, 규칙, 인터페이스, 관측성 정의
- 예:
  - task model
  - role boundary
  - artifact placement

### 3. Temporary Working Memory
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
  - task 단위 working memory는 특정 task의 세부 실행 메모를 담는다
  - issue 정보는 task 정본을 따라 참조한다
  - task working memory는 반드시 `task_ref`를 명시한다

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

## Task ID Rule
- task id는 로컬 실행 계층의 기본 식별자다.
- task id 형식은 아래로 고정한다.
  - `task-<issue-number>-<seq>`
- 예:
  - `task-52-a`
  - `task-52-b`
  - `task-103-a`

### Rule
- prefix는 항상 `task-`
- `<issue-number>`는 연결된 GitHub issue 번호를 그대로 사용
- `<seq>`는 같은 issue에서 여러 task가 생길 때 소문자 알파벳을 순서대로 사용
- issue당 첫 task는 항상 `a`부터 시작
- 문자 집합은 소문자, 숫자, 하이픈만 허용
- 의미 slug는 task id에 넣지 않는다

### Why This Form
- issue와의 연결이 즉시 보인다
- 같은 issue에서 task가 분기돼도 naming 충돌을 피할 수 있다
- path 길이가 과도하게 길어지지 않는다
- task 이름 변경 없이 objective 수정이나 문서 보강을 수용하기 쉽다
- working-memory, runtime metadata, index projection이 같은 key를 재사용하기 쉽다

### Example Mapping
- issue `#52`에서 첫 task 생성:
  - `task-52-a`
- issue `#52`에서 두 번째 task 추가 생성:
  - `task-52-b`
- issue `#103`에서 첫 task 생성:
  - `task-103-a`

## Accepted Task Shape
- `accepted-task.yaml`은 task 정본이다.
- issue 연결 정보와 작업 정의는 이 파일이 소유한다.

### Required Fields
- `task_id`
- `source_type`
- `source_ref`
- `issue_ref`
- `issue_url`
- `objective`
- `why`
- `acceptance_criteria`
- `constraints`
- `non_goals`
- `dependencies`
- `open_points`
- `status`
- `created_at`
- `updated_at`

### Optional Fields
- `labels`
- `related_docs`
- `approved_by`
- `approved_at`

### Status Rule
- 초기 허용 상태:
  - `draft`
  - `accepted`
  - `blocked`
  - `done`
- runtime 진행 상태는 `accepted-task.yaml`이 아니라 `run.meta.yaml`과 ledger가 소유한다.

### Why This Shape
- run이 issue를 직접 추적하지 않으므로 task 정본이 issue 연결 정보를 반드시 가져야 한다.
- planning, review, rerun이 모두 같은 task 정본에서 출발할 수 있어야 한다.
- acceptance criteria, constraints, open points를 같이 두어야 task scope drift를 줄일 수 있다.

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
    tasks/
      task-52-a/
        notes.md
        open-points.md
        handoff-notes.md
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
  - metadata에서 `task_ref` 또는 accepted task ref 확인 가능
  - 사람용 인덱스에서 task 기준 역추적 가능
  - issue는 task 정본을 따라 역추적 가능

## Run Metadata Minimum Shape
### Required Fields
- `run_id`
- `source_type`
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

## Run Metadata Lifecycle
- `run.meta.yaml`은 run의 최신 포인터 metadata다.
- run 정본은 packet, trace, decision, ledger 원본이지만, 최신 참조 포인터는 `run.meta.yaml`이 담당한다.

### Create Timing
- 아래 시점에 생성한다.
  - 첫 runtime run이 시작될 때
  - 첫 packet이 발행되기 직전 또는 직후

### Update Timing
- 아래 이벤트 직후 갱신한다.
  - 새 packet 발행
  - 새 trace 기록
  - 새 decision 기록
  - 새 commit 생성
  - current ledger 상태 전이

### Update Rule
- `updated_at`은 매 갱신 시점에 갱신한다.
- `latest_packet_id`, `latest_trace_id`, `latest_decision_id`, `latest_commit_sha`는 최신 포인터만 유지한다.
- 과거 이력은 `run.meta.yaml`에 누적하지 않는다.
- 과거 이력의 정본은 packet, trace, decision, snapshot artifact가 소유한다.

### Projection Sync Rule
- `run.meta.yaml`이 갱신되면 해당 task의 `run-index.yaml` projection도 같은 흐름에서 재생성한다.
- `run-index.yaml`은 task 관점 projection이고, `run.meta.yaml`은 run 관점 projection이다.
- 둘 중 어느 것도 packet/trace/decision 원본을 대체하지 않는다.

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
- issue 연결 정보는 `run.meta.yaml`이 아니라 `accepted-task.yaml` 정본을 따른다.

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
    tasks/
      task-52-a/
        notes.md
        open-points.md
        handoff-notes.md

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
  - `agent-team/index/tasks/<task-id>.md`
- task별 `run-index.yaml`도 metadata를 읽어 생성하는 projection으로 본다.

## Ownership By Artifact
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

## Open Point
- 이 문서 범위에서 남은 open point 없음.

## Boundary
- issue는 `what`, `why`, 제약, done signal을 담는 backlog input이다.
- working memory는 임시 협업 메모다.
- task working memory는 `task id`를 키로 쓴다.
- issue 연결 정보는 task 정본이 소유한다.
- task는 승인된 작업 정의와 task-level 분해 산출물의 정본을 소유한다.
- runtime artifact는 실행 이력과 현재 상태 projection이다.
- run은 task의 복제본이 아니라 task를 참조하는 실행 단위다.
- decision log는 장기 정책 판단 기록이다.
- 같은 내용을 여러 계층에 중복 복제하지 않는다.

## Related Artifact
- backlog input과 task ingress 경계는 [task-model.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/task-model.md)에 둔다.
- runtime observability와 ledger 경계는 [observability.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/observability.md)에 둔다.
