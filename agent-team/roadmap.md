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
- 현재 단계: `업무 분해`

## Steps
- [x] 목표 정의
  - [x] 무엇을 자동화할지 명확화
  - [x] 성공 기준 설정
  - [x] 예시 지표 정의
    - [x] 전체 trace 성공률
    - [x] node별 성공률
    - [x] 동일 병목 재발률
- [ ] 업무 분해
  - [ ] 큰 목표를 반복 가능한 단위 작업으로 분해
  - [ ] 입력, 처리, 출력 기준 정리
  - [ ] 사람 판단이 필요한 구간 표시
- [ ] 역할 설계
  - [ ] 에이전트별 책임 분리
  - [ ] 역할 초안 정의
    - [ ] Router: 요청 분류
    - [ ] Planner: 작업 계획
    - [ ] Worker: 실행
    - [ ] Reviewer: 검토
    - [ ] Reporter: 결과 정리
  - [ ] 역할 중복 최소화
- [ ] 역할 별 경계 정의
  - [ ] 각 에이전트의 권한 범위 설정
  - [ ] 읽기 가능 자원 정의
  - [ ] 쓰기 가능 자원 정의
  - [ ] 금지 행위 정의
  - [ ] destructive action 승인 조건 명시
- [ ] 에이전트 간 인터페이스 정의
  - [ ] 전달 포맷 통일
  - [ ] 필수 항목 정의
    - [ ] task id
    - [ ] objective
    - [ ] constraints
    - [ ] expected output
    - [ ] status
    - [ ] evidence
  - [ ] handoff 실패 조건 정의
- [ ] 운영 규칙 정의
  - [ ] 우선순위 규칙 정의
  - [ ] 충돌 시 결정 방식 정의
  - [ ] 실패 시 fallback 경로 정의
  - [ ] 인간 승인 필요 조건 정의
- [ ] Tool 맵핑
  - [ ] 역할마다 사용할 도구 연결
  - [ ] 예시 매핑 검토
    - [ ] 검색 전용
    - [ ] 코드 수정 전용
    - [ ] 테스트 실행 전용
    - [ ] 배포 금지
  - [ ] 최소 권한 원칙 적용
- [ ] 품질 게이트 설정
  - [ ] 완료 정의 필요
  - [ ] 예시 게이트 정의
    - [ ] 테스트 통과
    - [ ] 포맷 통과
    - [ ] 리뷰 승인
    - [ ] 근거 링크 포함
  - [ ] 게이트 우회 금지 규칙 정의
- [ ] 관측성 확보
  - [ ] 누가 무엇을 했는지 로그화
  - [ ] 의사결정 이유 기록
  - [ ] 실패 패턴 축적
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
- 결정: WBS 또는 해야 할 작업을 입력으로 받아 원자 분해 -> 계획 -> 작업 -> 로깅 -> 검증 -> 병목 탐지/수정의 피드백 루프를 자동화한다.
- 결정: 이 시스템은 이슈/PR 준비 자동화보다 하네스 엔지니어링이 포함된 에이전트 개발 시스템을 목표로 한다.
- 결정: 속도보다 품질, 안정성, 안정적 운영 방안을 우선한다.
- 결정: 초기 핵심 지표는 전체 trace 성공률, node별 성공률, 동일 병목 재발률로 둔다.
- 결정: 리드타임은 핵심 KPI가 아니라 보조 관측 지표로 둔다.
- 보류: 성공 지표의 수치 목표와 계산 주기는 아직 미정이다.
- 산출물: [agent-team/context/goal.md](/home/yonghyeun/Desktop/git_repositories/agent-team-setup--ops/agent-team/context/goal.md)
- 산출물: [agent-team/context/metrics.md](/home/yonghyeun/Desktop/git_repositories/agent-team-setup--ops/agent-team/context/metrics.md)

### 업무 분해
- 결정: agent-team 입력 task는 WBS에 한정하지 않고, 공통 task ingress shape로 정규화한다.
- 결정: task를 원자 단위로 자르는 decomposition layer와, 분해된 작업을 trace node로 계획하는 execution planning layer를 분리한다.
- 결정: 초기 trace node는 분해 -> 계획 -> 실행 -> 검증 -> 개선으로 둔다.
- 결정: 공통 task ingress spec은 `task_id`, `source_type`, `source_ref`, `objective`, `why`, `acceptance_criteria`, `constraints`, `non_goals`, `dependencies`, `open_points`를 기본 필드로 둔다.
- 보류: WBS와 ingress spec의 정확한 매핑 규칙은 아직 확정 전이다.
- 산출물: [agent-team/context/task-model.md](/home/yonghyeun/Desktop/git_repositories/agent-team-setup--ops/agent-team/context/task-model.md)
