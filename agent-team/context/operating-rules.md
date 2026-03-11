# Operating Rules

## Decision
- 운영 규칙은 `우선순위`, `충돌 해결`, `fallback`, `인간 승인` 4축으로 정의한다.
- 기본 원칙은 `속도보다 안전`, `추정보다 근거`, `자동 진행보다 명시적 승인`이다.

## Why
- 역할과 인터페이스만 있어도, 충돌 시 무엇이 우선인지 없으면 운영 drift가 생긴다.
- 실패 시 fallback이 없으면 blocked와 재작업이 임의 처리된다.
- 승인 조건이 시스템 규칙으로 고정되지 않으면 역할별로 다르게 해석된다.

## Priority Rules
### Rule 1
- 사람 승인과 명시적 사용자 지시가 최우선.

### Rule 2
- 저장소 정책과 gate는 역할 편의보다 우선.

### Rule 3
- accepted task와 acceptance criteria는 실행 편의보다 우선.

### Rule 4
- handoff packet은 runtime에서 직접 따르는 작업 단위다.
- 단, packet이 accepted task나 정책과 충돌하면 상위 artifact를 따른다.

### Rule 5
- 속도 최적화는 품질과 안정성을 침해하지 않는 범위에서만 허용한다.

## Conflict Resolution Order
- 충돌 해결 순서는 아래와 같이 고정한다.
  1. Human approval or explicit user instruction
  2. Repository policy and gate
  3. Accepted task
  4. Role boundary
  5. Handoff packet
  6. Local optimization or convenience

## Conflict Handling Rule
- 상위 규칙과 하위 규칙이 충돌하면 하위 규칙을 폐기한다.
- 충돌 사실은 숨기지 않고 `open_points` 또는 review note로 남긴다.
- `Worker`는 충돌을 자체 해석으로 덮지 않는다.
- `Reviewer`는 충돌이 해소되지 않았으면 pass를 주지 않는다.

## Fallback Paths
### Case 1. Input Missing
- 증상:
  - source ref 부족
  - acceptance criteria 불명확
  - owner path 미정
- fallback:
  - `Router`가 `open_points`로 승격
  - issue status를 `blocked` 또는 intake 보류로 유지
  - 사람 승인 전 다음 단계 진행 금지

### Case 2. Normalization Failed
- 증상:
  - schema 불일치
  - 필수 필드 누락
  - 의미 추론 근거 부족
- fallback:
  - ingress draft 반려
  - source reread
  - 필요 시 사용자 clarification 요청

### Case 3. Planning Conflict
- 증상:
  - atomic task가 과대함
  - packet scope가 accepted task보다 큼
  - 사람 판단 필요 task가 자동화 흐름에 섞임
- fallback:
  - `Planner`가 더 작은 atomic task로 재분해
  - 사람 판단 필요 task를 별도 packet으로 분리
  - scope expansion이면 승인 요청

### Case 4. Runtime Block
- 증상:
  - packet 밖 파일 수정 필요
  - required check 실행 불가
  - 정책 surface 수정 필요
- fallback:
  - `Worker`가 구현을 멈추고 block note 기록
  - `Reviewer` 또는 사람에게 escalation
  - 승인 전 우회 금지

### Case 5. Verification Failed
- 증상:
  - acceptance criteria 미충족
  - evidence 부족
  - check 실패
- fallback:
  - `Reviewer`가 `rework required`로 판정
  - `Planner` 또는 `Worker`로 반환
  - 동일 병목이면 feedback item 생성

### Case 6. Repeated Failure
- 증상:
  - 동일 병목 반복
  - 같은 stage에서 trace failure 재발
- fallback:
  - 자동 재시도보다 root cause 분리 우선
  - follow-up backlog input 생성
  - 필요 시 정책, prompt, handoff 포맷 수정 후보로 승격

## Human Approval Conditions
- 아래는 공통 승인 필요.
  - objective 변경
  - acceptance criteria 변경 또는 축소
  - scope expansion
  - packet 밖 경로 수정
  - destructive action
  - branch switch, rebase, reset, force push
  - hook, CI, deploy path 수정
  - migration 또는 irreversible transform
  - label taxonomy, issue status taxonomy 변경
  - blocker를 무시하고 pass 처리
  - policy 예외 처리

## Approval Timing Rule
- 승인 필요 항목은 `사후 보고`가 아니라 `사전 승인` 대상으로 둔다.
- 승인 전 상태는 `blocked` 또는 `awaiting_approval` 의미로 기록한다.
- 승인 없이 진행한 변경은 정상 완료로 간주하지 않는다.

## Runtime Decision Rules
- `Router`
  - ambiguity를 줄이되, 의미를 날조하지 않는다.
- `Planner`
  - 큰 task를 쪼개는 쪽으로 보수적으로 판단한다.
- `Worker`
  - packet 밖 확장보다 stop-and-escalate를 우선한다.
- `Reviewer`
  - evidence 없는 pass보다 rework를 우선한다.

## Success Bias To Avoid
- 빨리 끝내기 위해 acceptance criteria를 묵시적으로 낮추는 행동
- evidence 없이 completed로 넘기는 행동
- policy/gate를 로컬 판단으로 무시하는 행동
- blocked 상태를 숨기고 partial completion을 정상 완료처럼 보고하는 행동

## Open Point
- approval 대기 상태를 packet `status` enum에 별도 추가할지는 추후 packet schema 구현 단계에서 다시 닫는다.

## Related Artifact
- 완료 정의와 gate 통과 기준은 [quality-gates.md](/home/yonghyeun/Desktop/git_repositories/agent-team-setup--ops/agent-team/context/quality-gates.md)에 둔다.
