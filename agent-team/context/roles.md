# Roles

## Decision
- 역할 설계는 `config.toml` profile 설계보다 먼저 수행한다.
- 이유는 profile은 runtime adapter이고, 역할 설계는 operating model이기 때문이다.
- 초기 운영 모델은 `Router`, `Planner`, `Worker`, `Reviewer` 4역할을 기본으로 둔다.
- `Reporter`는 1차 도입에서 독립 역할로 두지 않고, 산출물 책임으로 흡수한다.

## Why
- 역할 경계가 먼저 닫혀야 이후 profile, handoff, tool mapping이 흔들리지 않는다.
- 초도 도입에서 역할 수가 많으면 handoff와 책임 중복이 먼저 늘어난다.
- reporting은 독립 실행보다 `verification result`, `feedback item`, `issue update` 같은 artifact 책임으로 다루는 편이 단순하다.

## Role Options
### Minimal
- 역할:
  - `Router`
  - `Worker`
  - `Reviewer`
- 장점:
  - 시작이 가장 빠름
  - handoff 수가 적음
- 단점:
  - intake와 planning이 섞임
  - decomposition 품질이 사람 역량에 크게 의존

### Standard
- 역할:
  - `Router`
  - `Planner`
  - `Worker`
  - `Reviewer`
  - `Reporter`
- 장점:
  - 책임 설명이 쉬움
  - 대시보드/보고 흐름이 눈에 잘 보임
- 단점:
  - 초도 도입에는 role count가 많음
  - `Reviewer`와 `Reporter` 중복 위험

### Compromise
- 역할:
  - `Router`
  - `Planner`
  - `Worker`
  - `Reviewer`
- 장점:
  - planning 분리 가능
  - verification 독립 유지
  - role count가 과도하지 않음
- 단점:
  - reporting을 별도 role로 기대하면 아쉬움

### Selected
- 역할:
  - `Router`
  - `Planner`
  - `Worker`
  - `Reviewer`
- 선택 이유:
  - 운영 순서 기준 8단계를 무리 없이 덮음
  - planning/runtime/quality gate를 분리할 수 있음
  - `Reporter`를 독립 role로 두지 않아 중복을 줄일 수 있음

## Stage Mapping
### 1. Issue Intake
- primary: `Router`
- responsibility:
  - issue 제목, 본문, label, source ref 읽기
  - intake 가능 여부 판단

### 2. Ingress Normalization
- primary: `Router`
- responsibility:
  - issue를 공통 task spec 초안으로 정규화
  - 불명확한 내용은 `open_points`로 승격

### 3. Accepted Task Approval
- primary: `Human`
- support: `Reviewer`
- responsibility:
  - ingress draft 완결성 점검
  - 승인, 수정, 반려 판단

### 4. Atomic Decomposition
- primary: `Planner`
- responsibility:
  - accepted task를 atomic task로 분해
  - 의존성과 사람 판단 지점 표시

### 5. Execution Planning
- primary: `Planner`
- responsibility:
  - atomic task를 trace node 흐름으로 계획
  - handoff packet 설계

### 6. Runtime Execution
- primary: `Worker`
- responsibility:
  - packet 실행
  - 산출물, trace, 실행 evidence 기록

### 7. Verification
- primary: `Reviewer`
- responsibility:
  - acceptance criteria 충족 여부 판정
  - 재작업, 통과, 차단 여부 결정

### 8. Feedback And Improvement
- primary: `Reviewer`
- support: `Router`
- responsibility:
  - 병목과 실패 원인 정리
  - follow-up backlog input 필요 시 issue로 환류

## Role Summary
### Router
- 소유 단계:
  - `Issue Intake`
  - `Ingress Normalization`
- 핵심 질문:
  - 이 backlog input은 무엇을 요구하는가
  - 아직 무엇이 비어 있는가
- 주요 산출물:
  - ingress draft
  - source summary

### Planner
- 소유 단계:
  - `Atomic Decomposition`
  - `Execution Planning`
- 핵심 질문:
  - 이 목표를 어떤 원자 작업으로 자를 것인가
  - 어떤 node와 packet으로 실행할 것인가
- 주요 산출물:
  - atomic task list
  - execution plan
  - handoff packet

### Worker
- 소유 단계:
  - `Runtime Execution`
- 핵심 질문:
  - 현재 packet을 어떻게 안전하게 실행할 것인가
- 주요 산출물:
  - code or docs artifact
  - trace
  - execution evidence

### Reviewer
- 소유 단계:
  - `Accepted Task Approval` 지원
  - `Verification`
  - `Feedback And Improvement`
- 핵심 질문:
  - 이 결과가 완료 조건을 충족하는가
  - 어떤 병목이 재발했고 무엇을 수정해야 하는가
- 주요 산출물:
  - review result
  - bottleneck note
  - improvement recommendation

## Reporter Handling
- `Reporter`는 독립 agent로 두지 않는다.
- 대신 reporting 책임은 아래 artifact로 분산한다.
  - `Router`: issue update와 source summary
  - `Worker`: trace와 execution evidence
  - `Reviewer`: verification result와 feedback item
- 이유:
  - 보고는 실행 이후 붙는 산출물 책임이지, 초도 도입에서 별도 판단 역할이 아니기 때문이다.

## Boundary
- `Router`는 task를 실행하지 않는다.
- `Planner`는 runtime 결과를 직접 검증하지 않는다.
- `Worker`는 완료 판정을 소유하지 않는다.
- `Reviewer`는 새로운 구현을 직접 수행하지 않는다.
- 사람 승인은 계속 별도 control point로 유지한다.

## Related Artifact
- 상세 권한 경계는 [role-boundaries.md](/home/yonghyeun/Desktop/git_repositories/agent-team-setup--ops/agent-team/context/role-boundaries.md)에 둔다.
- 상세 도구 맵핑은 [tool-mapping.md](/home/yonghyeun/Desktop/git_repositories/agent-team-setup--ops/agent-team/context/tool-mapping.md)에 둔다.

## Open Point
- 추후 profile 설계 시 role 이름을 그대로 쓸지, `worker`를 `executor`로 내릴지는 별도 결정한다.
