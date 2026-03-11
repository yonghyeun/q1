# Role Boundaries

## Decision
- 역할 경계는 `권한 범위`, `읽기 가능 자원`, `쓰기 가능 자원`, `금지 행위`, `승인 조건` 5축으로 정의한다.
- 초기 역할 경계는 `Router`, `Planner`, `Worker`, `Reviewer`, `Human Control Point` 기준으로 둔다.
- destructive action과 scope expansion은 역할 자율 결정이 아니라 사람 승인 대상으로 둔다.

## Why
- 역할 이름만 있고 권한 경계가 없으면 handoff와 책임 회피가 동시에 늘어난다.
- planning layer와 runtime layer를 분리했으므로, 읽기/쓰기 경계도 같은 기준으로 분리해야 한다.
- 승인 조건이 문서화되지 않으면 속도 때문에 위험한 우회가 먼저 발생한다.

## Shared Boundary
- 모든 역할은 현재 accepted task와 handoff packet 범위를 넘는 임의 확장을 하지 않는다.
- 모든 역할은 근거가 약한 추정을 확정 사실로 쓰지 않는다.
- 모든 역할은 사람 승인 없이 destructive action을 수행하지 않는다.
- 모든 역할은 gate 실패를 우회하지 않는다.

## Resource Classes
- `Backlog Input`
  - GitHub issue
  - upstream source ref
- `Planning Artifact`
  - accepted task
  - atomic task list
  - execution plan
  - handoff packet
- `Runtime Artifact`
  - code or docs output
  - trace
  - execution evidence
  - verification result
  - feedback item
- `Policy Surface`
  - branch rule
  - git hook
  - CI
  - deploy path

## Role Matrix
### Router
- 권한 범위:
  - backlog input intake
  - ingress normalization
  - source summary 작성
- 읽기 가능 자원:
  - backlog input
  - issue label taxonomy
  - upstream source ref
  - 관련 decision/context 문서
- 쓰기 가능 자원:
  - ingress draft
  - source summary
  - intake 상태 메모
- 금지 행위:
  - code or docs implementation
  - atomic task 임의 확정
  - verification verdict 확정
  - destructive git action
- 승인 조건:
  - objective를 바꾸는 normalization
  - source ref가 불충분한데 ready로 올리는 행동
  - label/status taxonomy 수정 제안

### Planner
- 권한 범위:
  - atomic decomposition
  - execution planning
  - handoff packet 설계
- 읽기 가능 자원:
  - accepted task
  - source summary
  - 관련 context/policy 문서
  - prior trace and feedback
- 쓰기 가능 자원:
  - atomic task list
  - execution plan
  - handoff packet
  - dependency note
- 금지 행위:
  - runtime artifact 직접 생성
  - acceptance criteria 임의 축소
  - reviewer verdict 대체
  - destructive git action
- 승인 조건:
  - task scope expansion
  - owned path expansion
  - 새로운 external dependency 추가
  - 사람 판단 필요 task를 숨기고 자동 진행

### Worker
- 권한 범위:
  - packet 실행
  - owned path 내 산출물 생성/수정
  - trace와 execution evidence 기록
- 읽기 가능 자원:
  - handoff packet
  - execution plan
  - owned path 파일
  - 관련 테스트와 정책 문서
- 쓰기 가능 자원:
  - packet에 명시된 owned path 내 코드/문서
  - trace
  - execution evidence
  - 작업 중 발견한 block note
- 금지 행위:
  - objective, acceptance criteria, done condition 임의 수정
  - packet 밖 경로 수정
  - review pass 판정
  - destructive git action
- 승인 조건:
  - packet 밖 파일 수정 필요
  - schema or policy surface 수정 필요
  - branch switch, rebase, reset, force push 필요
  - 삭제, 대량 rename, migration 같은 파괴적 변경 필요

### Reviewer
- 권한 범위:
  - accepted task approval 지원
  - verification
  - feedback and improvement 정리
- 읽기 가능 자원:
  - accepted task
  - atomic task list
  - handoff packet
  - runtime artifact
  - trace and execution evidence
- 쓰기 가능 자원:
  - review result
  - verification result
  - bottleneck note
  - improvement recommendation
  - follow-up backlog suggestion
- 금지 행위:
  - 구현 수정으로 verdict 대체
  - acceptance criteria 재정의
  - destructive git action
- 승인 조건:
  - blocker를 무시하고 pass 처리
  - 정책 위반을 예외 승인
  - follow-up issue 없이 runtime observation을 종료 처리

### Human Control Point
- 권한 범위:
  - 승인, 반려, 범위 조정, 우선순위 조정
  - destructive action 허가
  - policy surface 변경 승인
- 읽기 가능 자원:
  - 모든 artifact
- 쓰기 가능 자원:
  - 승인 기록
  - scope correction
  - policy decision
- 금지 행위:
  - 없음
- 승인 필요 대상:
  - objective 변경
  - scope expansion
  - destructive action
  - policy surface 변경
  - release or deploy 영향 변경

## Destructive Action Rule
- 아래 항목은 공통적으로 사람 승인 필요.
  - file or directory 삭제
  - large rename or move
  - `git reset --hard`
  - force push
  - branch switch or rebase
  - hook, CI, deploy path 수정
  - migration or irreversible data transform

## Practical Read And Write Rule
- `Router`
  - read-heavy
  - write는 intake artifact까지만
- `Planner`
  - planning artifact write 가능
  - runtime output write 금지
- `Worker`
  - runtime output write 가능
  - planning objective rewrite 금지
- `Reviewer`
  - verdict와 feedback write 가능
  - implementation write 금지

## Boundary Failure Examples
- `Router`가 acceptance criteria를 새로 만들어 확정하는 경우
- `Planner`가 테스트 결과 없이 완료로 간주하는 경우
- `Worker`가 packet에 없는 파일을 수정하는 경우
- `Reviewer`가 문제를 직접 고치고 검토를 생략하는 경우

## Open Point
- issue remote update를 어느 역할의 기본 write로 둘지는 handoff/interface 설계 단계에서 다시 닫는다.
