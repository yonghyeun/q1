# Agent Interface

## Decision
- 에이전트 간 공통 인터페이스는 `handoff packet` 하나로 통일한다.
- packet은 `template + schema + validator` 하이브리드로 운영한다.
- 사람이 읽는 기준 포맷과 기계가 검증하는 기준 포맷을 분리하되, 논리적 필드 집합은 동일하게 유지한다.

## Why
- handoff가 자유 서술형이면 역할 경계가 다시 흐려진다.
- config/profile만으로는 packet shape를 hard enforcement할 수 없다.
- packet은 control-plane artifact이므로 drift를 허용하면 안 된다.

## Interface Options
### Minimal
- 필수 필드:
  - `task_id`
  - `objective`
  - `status`
- 장점:
  - 가장 단순
- 단점:
  - 근거, 제약, 기대 산출물이 빠져 재작업이 잦아진다

### Standard
- 필수 필드:
  - `task_id`
  - `owner_role`
  - `objective`
  - `constraints`
  - `expected_output`
  - `status`
  - `evidence`
- 장점:
  - 일반적인 task handoff에는 충분
- 단점:
  - trace/run 연결성과 path ownership이 약하다

### Compromise
- 필수 필드:
  - `packet_id`
  - `task_id`
  - `atomic_task_id`
  - `from_role`
  - `to_role`
  - `objective`
  - `constraints`
  - `expected_outputs`
  - `status`
  - `evidence`
- 장점:
  - 역할 간 전달에는 충분
  - 너무 무겁지 않음
- 단점:
  - runtime 검증과 path control이 약하다

### Selected
- 필수 필드:
  - `packet_id`
  - `run_id`
  - `trace_id`
  - `task_id`
  - `atomic_task_id`
  - `from_role`
  - `to_role`
  - `stage`
  - `objective`
  - `constraints`
  - `inputs`
  - `expected_outputs`
  - `owned_paths`
  - `required_checks`
  - `status`
  - `evidence`
  - `open_points`
  - `human_approval`
- 선택 이유:
  - traceability, path boundary, 검증 가능성을 같이 확보할 수 있다
  - 역할 경계와 approval boundary를 packet 수준에서 바로 검증할 수 있다

## Final Packet Shape
### Identity
- `packet_id`
- `run_id`
- `trace_id`
- `task_id`
- `atomic_task_id`

### Routing
- `from_role`
- `to_role`
- `stage`

### Intent
- `objective`
- `constraints`
- `inputs`
- `expected_outputs`
- `open_points`

### Execution Control
- `owned_paths`
- `required_checks`
- `human_approval`

### Runtime State
- `status`
- `evidence`

## Required Fields In Roadmap Terms
- `task id`
  - packet에서는 `task_id`
- `objective`
  - 현재 packet이 달성해야 할 목표
- `constraints`
  - 지켜야 할 제한과 금지 범위
- `expected output`
  - 산출물 형태와 완료 기준
- `status`
  - packet 진행 상태
- `evidence`
  - 현재 상태를 뒷받침하는 근거

## Field Meaning
### `inputs`
- 실행에 필요한 선행 artifact와 참조 목록

### `expected_outputs`
- 만들어야 할 산출물 목록
- 예:
  - file path
  - review note
  - trace update

### `owned_paths`
- `Worker`가 수정 가능한 경로 범위
- `Planner`가 추론한 범위를 packet에 concrete하게 내린 값

### `required_checks`
- 실행 후 반드시 확인해야 하는 검증 항목
- 예:
  - test command
  - lint
  - schema validator
  - manual review point

### `human_approval`
- 추가 승인 필요 여부와 이유
- 예:
  - `required: true`
  - `reason: scope_expansion`

### `status`
- 초기 enum:
  - `draft`
  - `ready`
  - `in_progress`
  - `blocked`
  - `completed`
  - `rejected`

### `evidence`
- status를 뒷받침하는 근거
- 예:
  - changed files
  - command result summary
  - review note link
  - validation result

## Machine And Narrative Split
- machine field:
  - id
  - role
  - stage
  - enum
  - paths
  - checks
- narrative field:
  - objective
  - constraint notes
  - output explanation
  - open point detail
  - evidence summary

## Handoff Failure Conditions
- 필수 필드 누락
- `from_role`, `to_role`, `stage`, `status` enum 위반
- `task_id` 또는 `atomic_task_id` 추적 불가
- `owned_paths` 없이 file write를 요구
- `required_checks` 없이 completion을 요구
- `human_approval.required=true`인데 승인 기록 없음
- `expected_outputs`와 `status=completed`가 불일치
- `evidence`가 비어 있는데 `blocked`, `completed`, `rejected` 같은 terminal 성격 상태를 주장
- role boundary와 충돌하는 write 요청 포함

## Validation Rule
- 1차:
  - schema validation
- 2차:
  - semantic validation
  - 예:
    - role/stage 조합 타당성
    - owned path와 write action 일치 여부
    - approval requirement 충족 여부

## Practical Handoff Rule
- `Router -> Planner`
  - packet보다는 accepted task 또는 planning packet 사용
- `Planner -> Worker`
  - full handoff packet 필요
- `Worker -> Reviewer`
  - execution result packet 필요
- `Reviewer -> Router`
  - feedback packet 또는 follow-up backlog suggestion 필요

## Open Point
- packet artifact를 JSON 우선으로 둘지, Markdown template 우선으로 둘지는 구현 단계에서 다시 닫는다.

## Related Artifact
- 시스템 레벨 우선순위, 충돌 처리, fallback, 승인 규칙은 [operating-rules.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/operating-rules.md)에 둔다.
