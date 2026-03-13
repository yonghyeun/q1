# Agent Team Roadmap

이 문서는 멀티에이전트 도입 순서를 고정하는 로드맵이다.
완전 무지 상태에서 시작하는 것을 전제로 하며, 순서를 바꾸지 않는다.

## Working Rules
- 한 번에 한 단계씩 진행한다.
- 다음 단계로 넘어가기 전 현재 단계의 컨텍스트를 합의한다.
- 규칙보다 컨텍스트를 먼저 고정한다.
- 산출물 생성 시 가능한 한 원자적 작업 단위로 커밋한다.

## Recording Pattern
- 체크박스는 대화를 통해 합의가 끝난 항목만 체크한다.
- 상세 내용은 로드맵에 장문으로 누적하지 않고, 단계별 문서로 분리한다.
- 로드맵에는 각 단계의 `결정`, `보류`, `산출물`만 짧게 남긴다.
- 각 단계 산출물은 다음 단계의 입력으로 재사용 가능해야 한다.

## Current Phase
- 현재 단계: `작은 파일럿 실행`

## Steps
- [x] 목표 정의
  - [x] 무엇을 자동화할지 명확화
  - [x] 성공 기준 설정
  - [x] 예시 지표 정의
    - [x] 전체 trace 성공률
    - [x] node별 성공률
    - [x] 동일 병목 재발률
- [x] 업무 분해
  - [x] 큰 목표를 반복 가능한 단위 작업으로 분해
  - [x] 입력, 처리, 출력 기준 정리
  - [x] 사람 판단이 필요한 구간 표시
- [x] 역할 설계
  - [x] 에이전트별 책임 분리
  - [x] 역할 초안 정의
    - [x] Router: 요청 분류
    - [x] Planner: 작업 계획
    - [x] Worker: 실행
    - [x] Reviewer: 검토
    - [x] Reporter: 결과 정리
  - [x] 역할 중복 최소화
- [x] 역할 별 경계 정의
  - [x] 각 에이전트의 권한 범위 설정
  - [x] 읽기 가능 자원 정의
  - [x] 쓰기 가능 자원 정의
  - [x] 금지 행위 정의
  - [x] destructive action 승인 조건 명시
- [x] 에이전트 간 인터페이스 정의
  - [x] 전달 포맷 통일
  - [x] 필수 항목 정의
    - [x] task id
    - [x] objective
    - [x] constraints
    - [x] expected output
    - [x] status
    - [x] evidence
  - [x] handoff 실패 조건 정의
- [x] 운영 규칙 정의
  - [x] 우선순위 규칙 정의
  - [x] 충돌 시 결정 방식 정의
  - [x] 실패 시 fallback 경로 정의
  - [x] 인간 승인 필요 조건 정의
- [x] Tool 맵핑
  - [x] 역할마다 사용할 도구 연결
  - [x] 예시 매핑 검토
    - [x] 검색 전용
    - [x] 코드 수정 전용
    - [x] 테스트 실행 전용
    - [x] 배포 금지
  - [x] 최소 권한 원칙 적용
- [x] 품질 게이트 설정
  - [x] 완료 정의 필요
  - [x] 예시 게이트 정의
    - [x] 테스트 통과
    - [x] 포맷 통과
    - [x] 리뷰 승인
    - [x] 근거 링크 포함
  - [x] 게이트 우회 금지 규칙 정의
- [x] 관측성 확보
  - [x] 누가 무엇을 했는지 로그화
  - [x] 의사결정 이유 기록
  - [x] 실패 패턴 축적
- [ ] 작은 파일럿 실행
  - [ ] 저위험 업무 1개부터 시작
  - [ ] 예시 후보 검토
    - [ ] 이슈 triage
    - [ ] 문서 초안
    - [ ] 테스트 보강
  - [ ] 처음부터 전 영역 자동화 금지
- [ ] 회고 및 재설계
  - [ ] 병목 역할 확인
  - [ ] 책임 겹침 제거
  - [ ] 프롬프트 수정
  - [ ] 정책 수정
  - [ ] handoff 포맷 수정
- [ ] 점진적 확장
  - [ ] 성공한 흐름만 범위 확대
  - [ ] 권한 확대는 마지막 단계
  - [ ] 신규 에이전트 추가 전 기존 역할 재사용 검토
- [ ] 실무 기준 최소 팀 구조
  - [ ] Router
  - [ ] Executor
  - [ ] Reviewer
- [ ] 조금 더 안정적인 구조
  - [ ] Router
  - [ ] Planner
  - [ ] Executor
  - [ ] Reviewer
  - [ ] Coordinator
- [ ] 처음 만들 때 가장 중요한 3가지
  - [ ] 역할보다 책임 경계
  - [ ] 성능보다 실패 처리
  - [ ] 자동화보다 승인 규칙

## Notes
### 목표 정의
- 결정: GitHub issue backlog input을 받아 원자 분해 -> 계획 -> 작업 -> 로깅 -> 검증 -> 병목 탐지/수정의 피드백 루프를 자동화한다.
- 결정: 이 시스템은 이슈/PR 준비 자동화보다 하네스 엔지니어링이 포함된 에이전트 개발 시스템을 목표로 한다.
- 결정: 속도보다 품질, 안정성, 안정적 운영 방안을 우선한다.
- 결정: 초기 핵심 지표는 전체 trace 성공률, node별 성공률, 동일 병목 재발률로 둔다.
- 결정: 리드타임은 핵심 KPI가 아니라 보조 관측 지표로 둔다.
- 보류: 성공 지표의 수치 목표와 계산 주기는 아직 미정이다.
- 산출물: [agent-team/context/goal.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/goal.md)
- 산출물: [agent-team/context/metrics.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/metrics.md)

### 업무 분해
- 결정: agent-team의 backlog 입력 SoT는 GitHub issue로 둔다.
- 결정: WBS, 사람 요청, runtime 관찰은 issue 생성의 upstream source로 취급한다.
- 결정: agent-team 구축 작업은 시스템 레이어가 아니라 실제 운영 순서 기준으로 분해한다.
- 결정: 상위 운영 순서는 `Issue Intake -> Ingress Normalization -> Accepted Task Approval -> Atomic Decomposition -> Execution Planning -> Runtime Execution -> Verification -> Feedback And Improvement`로 둔다.
- 결정: task를 원자 단위로 자르는 decomposition layer와, 분해된 작업을 trace node로 계획하는 execution planning layer를 분리한다.
- 결정: 초기 trace node는 분해 -> 계획 -> 실행 -> 검증 -> 개선으로 둔다.
- 결정: 공통 task ingress spec은 `task_id`, `source_type`, `source_ref`, `objective`, `why`, `acceptance_criteria`, `constraints`, `non_goals`, `dependencies`, `open_points`를 기본 필드로 둔다.
- 결정: issue 본문과 label은 1:1 필드 매핑 대신 `추론 + 승인 + 검증` 기반 normalization flow로 ingress draft를 만든다.
- 결정: 의미 추론은 에이전트가 수행하고, 구조 검증은 스크립트가 수행하며, 최종 의미 승인과 범위 교정은 사람이 수행한다.
- 결정: atomic task는 decomposition artifact로, handoff packet은 execution planning/runtime artifact로 분리한다.
- 결정: `source_type`은 `human-request`, `agent-team`, `runtime-observation`, `wbs-planned`로 고정한다.
- 결정: issue status는 `inbox`, `ready`, `active`, `blocked`, `cancelled`로 해석하고 완료는 issue close로 처리한다.
- 보류: issue를 `ready`로 승격하는 승인 조건과 validation 구체 규칙은 아직 확정 전이다.
- 산출물: [agent-team/context/task-model.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/task-model.md)
- 산출물: [agent-team/context/work-breakdown.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/work-breakdown.md)

### 역할 설계
- 결정: `config.toml` profile 설계보다 역할 설계를 먼저 확정한다.
- 결정: 초기 운영 모델은 `Router`, `Planner`, `Worker`, `Reviewer` 4역할로 둔다.
- 결정: `Reporter`는 독립 role이 아니라 산출물 책임으로 흡수한다.
- 결정: 운영 8단계의 주 소유자는 `Router -> Router -> Human/Reviewer -> Planner -> Planner -> Worker -> Reviewer -> Reviewer/Router` 순서로 둔다.
- 결정: 사람 승인은 계속 별도 control point로 유지한다.
- 보류: runtime profile 이름에서 `Worker`를 `Executor`로 바꿀지는 아직 미정이다.
- 산출물: [agent-team/context/roles.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/roles.md)

### 역할 별 경계 정의
- 결정: 역할 경계는 `권한 범위`, `읽기 가능 자원`, `쓰기 가능 자원`, `금지 행위`, `승인 조건` 5축으로 정의한다.
- 결정: `Router`, `Planner`, `Worker`, `Reviewer`, `Human Control Point` 기준으로 경계를 고정한다.
- 결정: destructive action과 scope expansion은 역할 자율 판단이 아니라 사람 승인 대상으로 둔다.
- 결정: `Router`는 intake artifact까지만 쓰고, `Planner`는 planning artifact까지만 쓰며, `Worker`는 runtime output만 쓰고, `Reviewer`는 verdict와 feedback만 쓴다.
- 결정: branch switch, rebase, reset, force push, 삭제, 대량 rename, CI/hook/deploy 수정은 공통 승인 대상으로 둔다.
- 보류: remote issue update를 어느 역할의 기본 write로 둘지는 아직 미정이다.
- 산출물: [agent-team/context/role-boundaries.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/role-boundaries.md)

### 에이전트 간 인터페이스 정의
- 결정: 에이전트 간 공통 인터페이스는 `handoff packet` 하나로 통일한다.
- 결정: packet은 `template + schema + validator` 하이브리드로 운영한다.
- 결정: 필수 필드는 `packet_id`, `run_id`, `trace_id`, `task_id`, `atomic_task_id`, `from_role`, `to_role`, `stage`, `objective`, `constraints`, `inputs`, `expected_outputs`, `owned_paths`, `required_checks`, `status`, `evidence`, `open_points`, `human_approval`로 둔다.
- 결정: roadmap 필수 항목인 `task id`, `objective`, `constraints`, `expected output`, `status`, `evidence`는 packet 공통 필드로 강제한다.
- 결정: 필수 필드 누락, enum 위반, owned path 없는 write 요청, approval 누락, evidence 없는 terminal status는 handoff 실패로 본다.
- 보류: packet artifact를 JSON 우선으로 둘지 Markdown template 우선으로 둘지는 아직 미정이다.
- 산출물: [agent-team/context/interface.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/interface.md)

### 운영 규칙 정의
- 결정: 운영 규칙은 `우선순위`, `충돌 해결`, `fallback`, `인간 승인` 4축으로 정의한다.
- 결정: 시스템 기본 원칙은 `속도보다 안전`, `추정보다 근거`, `자동 진행보다 명시적 승인`으로 둔다.
- 결정: 충돌 해결 우선순위는 `Human approval -> Repository policy and gate -> Accepted task -> Role boundary -> Handoff packet -> Local optimization`으로 고정한다.
- 결정: input missing, normalization failure, planning conflict, runtime block, verification failure, repeated failure에 대한 fallback 경로를 명시한다.
- 결정: objective 변경, acceptance criteria 변경/축소, scope expansion, packet 밖 경로 수정, destructive action, branch 전환 계열, policy surface 수정, taxonomy 수정, policy 예외 처리는 공통 승인 대상으로 둔다.
- 보류: approval 대기 상태를 packet status enum에 별도로 둘지는 아직 미정이다.
- 산출물: [agent-team/context/operating-rules.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/operating-rules.md)

### Tool 맵핑
- 결정: 역할별 도구 맵핑은 `허용 도구`, `우선 도구`, `금지 도구`, `검증 도구` 기준으로 정의한다.
- 결정: wrapper가 있는 액션은 raw 명령보다 wrapper-first를 기본으로 둔다.
- 결정: `Router`는 read-heavy 도구, `Planner`는 planning artifact 도구, `Worker`는 수정/테스트 도구, `Reviewer`는 diff/validator 재검증 도구를 기본으로 둔다.
- 결정: 예시 매핑은 `검색 전용`, `코드 수정 전용`, `테스트 실행 전용`, `배포 금지` 4분류로 정리한다.
- 결정: 초기 범위에서 deploy, merge 자동화, infra mutation은 공통 금지 도구로 둔다.
- 보류: profile 단계에서 tool permission을 config로 얼마나 강하게 분리할지는 아직 미정이다.
- 산출물: [agent-team/context/tool-mapping.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/tool-mapping.md)

### 품질 게이트 설정
- 결정: agent-team 품질 게이트는 `완료 정의`, `검증 게이트`, `우회 금지` 3축으로 정의한다.
- 결정: 저장소 공통 gate는 재사용하고, agent-team 문서는 task/packet/trace 관점 완료 조건을 추가한다.
- 결정: 완료 정의는 `acceptance criteria 충족`, `required checks 통과`, `reviewer verdict 확보`, `evidence 기록 완료`, `follow-up 필요 시 feedback 기록`으로 둔다.
- 결정: 초기 최소 게이트는 `relevant test pass`, `relevant format/schema pass`, `reviewer approval`, `evidence link` 4개로 둔다.
- 결정: gate 실패 시 `completed`로 올리지 않으며 `rework`, `blocked`, `rejected` 중 하나로 분기한다.
- 결정: gate 실패 후 raw command 우회, evidence 없는 completed, reviewer 없는 self-pass, required checks 생략 완료 처리는 금지한다.
- 보류: `warning-only` 게이트와 `blocking` 게이트의 분리 시점은 아직 미정이다.
- 산출물: [agent-team/context/quality-gates.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/quality-gates.md)

### 관측성 확보
- 결정: agent-team 관측성은 `trace`, `operator decision`, `current run ledger`, `snapshot ledger`, `failure pattern log` 5축으로 정의한다.
- 결정: `누가 무엇을 했는지`는 trace에, `왜 그렇게 판정했는지`는 operator decision에 분리 기록한다.
- 결정: 현재 상태 판단은 packet 원문보다 `current run ledger`를 우선한다.
- 결정: backlog 상태와 runtime 상태는 같은 ledger에 섞지 않는다.
- 결정: 반복 실패는 `failure pattern log`로 승격해 `동일 병목 재발률` 계산 기반으로 사용한다.
- 보류: failure pattern log를 독립 artifact로 둘지 ledger projection에서 먼저 시작할지는 아직 미정이다.
- 산출물: [agent-team/context/observability.md](/home/yonghyeun/Desktop/git_repositories/agent-team-context-artifact-path-rules--docs/agent-team/context/observability.md)
