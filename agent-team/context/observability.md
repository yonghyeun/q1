# Observability

## Decision
- agent-team 관측성은 `trace`, `operator decision`, `current run ledger`, `snapshot ledger`, `failure pattern log` 5축으로 정의한다.
- runtime 이력과 판정 근거는 분리해서 기록한다.
- backlog 상태와 runtime 상태는 같은 ledger에 섞지 않는다.

## Why
- `누가 무엇을 했는지`와 `왜 그렇게 판정했는지`를 한 문서에 섞으면 audit이 약해진다.
- 반복 실패를 잡으려면 개별 trace뿐 아니라 패턴 축적 레이어가 따로 필요하다.
- 현재 저장소의 WBS runtime 모델과 맞춰야 이후 schema 재사용이 쉽다.

## Core Questions
- 누가 어떤 packet을 언제 처리했는가
- 어떤 근거로 accept, rework, block이 결정됐는가
- 현재 run의 최신 상태는 무엇인가
- 어떤 실패가 반복되고 있는가

## Artifact Model
### Trace
- 목적:
  - `누가 무엇을 했는지` 기록
- 성격:
  - append-only execution record
- 최소 포함 항목:
  - `trace_id`
  - `run_id`
  - `packet_id`
  - `actor_role`
  - `action_summary`
  - `changed_artifacts`
  - `executed_checks`
  - `blockers`
  - `timestamp`

### Operator Decision
- 목적:
  - `왜 그렇게 판정했는지` 기록
- 성격:
  - trace와 분리된 review/decision event
- 최소 포함 항목:
  - `decision_id`
  - `run_id`
  - `reviewed_trace_ids`
  - `decision`
  - `reason_summary`
  - `reason_detail`
  - `reviewer_role`
  - `timestamp`

### Current Run Ledger
- 목적:
  - 현재 run의 최신 상태 projection
- 성격:
  - current state SoT
- 최소 포함 항목:
  - `run_id`
  - `current_packet_id`
  - `latest_trace_id`
  - `latest_decision_id`
  - `current_stage`
  - `current_status`
  - `open_feedback`

### Snapshot Ledger
- 목적:
  - 주요 decision 시점의 frozen projection 보존
- 성격:
  - append-only checkpoint
- 사용 시점:
  - `accept`
  - `rework`
  - `block`
  - `cancel`
  - `close`

### Failure Pattern Log
- 목적:
  - 실패 패턴 축적
  - 동일 병목 재발률 계산 기반
- 최소 포함 항목:
  - `pattern_id`
  - `related_run_ids`
  - `related_trace_ids`
  - `stage`
  - `failure_type`
  - `root_cause_hypothesis`
  - `recurrence_count`
  - `remediation_status`

## Logging Rules
### Who Did What
- 실행 행위는 `trace`에 남긴다.
- 역할 이름은 `Router`, `Planner`, `Worker`, `Reviewer`, `Human` 중 하나로 고정한다.
- 변경 파일, 실행 커맨드, 검증 결과 요약을 함께 남긴다.

### Why The Decision Happened
- 판정 근거는 `operator decision`에 남긴다.
- `accept`, `rework`, `block`, `cancel`, `dispatch`, `close`는 decision enum으로 관리한다.
- `trace`에 verdict를 섞지 않는다.

### Current State
- 현재 상태 판단은 packet 원문이 아니라 `current run ledger`를 우선 본다.
- packet과 trace는 원본 이력이다.
- ledger는 최신 상태 projection이다.

### Failure Accumulation
- 단발 실패는 trace와 decision에 남긴다.
- 반복 실패는 `failure pattern log`로 승격한다.
- 같은 `stage + failure_type + root_cause_hypothesis` 조합이 반복되면 패턴으로 본다.

## Practical Minimal Rule
- 초기 도입에서는 아래 4개만 반드시 남긴다.
  - trace
  - operator decision
  - current run ledger
  - failure pattern log
- snapshot ledger는 주요 decision checkpoint부터 점진 도입 가능.

## Boundary
- backlog input 상태는 issue가 소유한다.
- runtime 상태는 run ledger가 소유한다.
- trace는 실행 이력이다.
- decision은 판정 이력이다.
- failure pattern log는 개선 이력이다.

## Initial Failure Types
- `input_missing`
- `normalization_failure`
- `planning_conflict`
- `runtime_block`
- `verification_failure`
- `policy_violation`
- `repeated_rework`

## Open Point
- failure pattern log를 독립 artifact로 둘지, current ledger의 `open_feedback` projection에서 먼저 시작할지는 파일럿 단계에서 다시 닫는다.
