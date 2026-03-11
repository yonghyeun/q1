# Quality Gates

## Decision
- agent-team 품질 게이트는 `완료 정의`, `검증 게이트`, `우회 금지` 3축으로 정의한다.
- 저장소 공통 gate는 그대로 재사용하고, agent-team 문서는 task/packet/trace 관점의 완료 조건을 추가한다.
- 기본 원칙은 `검증 없는 완료 금지`, `근거 없는 pass 금지`, `gate 실패 우회 금지`다.

## Why
- 저장소 gate만으로는 packet, verification, evidence 기준이 충분히 드러나지 않는다.
- 반대로 agent-team이 별도 품질 체계를 만들면 repo gate와 충돌할 수 있다.
- 따라서 repo gate를 재사용하면서, agent-team 레벨 완료 정의만 얹는 구조가 가장 안정적이다.

## Definition Of Done
- task 또는 packet이 완료로 간주되려면 아래를 모두 만족해야 한다.
  - acceptance criteria 충족
  - required checks 통과
  - reviewer verdict 확보
  - evidence 기록 완료
  - follow-up 필요 시 backlog suggestion 또는 feedback item 기록

## Required Gate Set
### Test Pass
- 해당 packet의 `required_checks`에 포함된 테스트가 통과해야 한다.
- 테스트가 없다면, 왜 없는지와 대체 검증이 evidence에 남아야 한다.

### Format Pass
- formatter, lint, schema validator, body/label/title guard 등 적용 가능한 형식 게이트를 통과해야 한다.
- 문서 작업도 schema/structure/template 규칙을 벗어나면 완료로 보지 않는다.

### Review Approval
- `Reviewer`가 acceptance criteria와 evidence를 기준으로 pass 또는 rework를 판정해야 한다.
- `Worker`의 self-pass는 완료 정의로 인정하지 않는다.

### Evidence Link
- 완료 또는 차단 상태에는 항상 evidence가 있어야 한다.
- evidence 예:
  - changed file path
  - command result summary
  - validator result
  - review note
  - issue or source ref link

## Gate By Stage
### Intake / Normalization
- issue/body/label taxonomy 유효
- ingress draft 필수 필드 존재
- source ref 추적 가능

### Decomposition / Planning
- atomic task가 과대하지 않음
- handoff packet 필수 필드 존재
- owned path와 required checks 정의 완료

### Runtime Execution
- packet 범위 내 수정만 수행
- required checks 실행
- trace와 execution evidence 기록

### Verification
- reviewer verdict 존재
- acceptance criteria와 expected outputs 대조 완료
- 실패 시 rework 또는 feedback 분기 명시

## Gate Failure Handling
- gate 실패 시 상태는 `completed`로 올리지 않는다.
- 가능한 후속은 아래 중 하나다.
  - rework
  - blocked
  - rejected
- gate 실패 원인은 trace 또는 review result에 남긴다.

## No-Bypass Rules
- gate 실패 후 raw command나 수동 설명으로 우회 완료 처리 금지
- evidence 없이 `completed` 표기 금지
- reviewer 없이 `pass` 선언 금지
- required checks 생략 후 `문제 없어 보임` 식 종료 금지
- packet 밖 수정 후 `사소함`을 이유로 승인 생략 금지

## Relationship With Repo Gates
- 저장소의 active gate는 계속 선행 또는 병행 적용한다.
- 예:
  - branch name
  - detached HEAD write
  - protected branch write
  - dirty worktree write
  - issue title/body/label
  - commit message
- agent-team은 이 gate 위에 runtime quality gate를 추가로 얹는다.

## Minimal Initial Gate Set
- 초기 도입에서는 아래 4개를 최소 필수로 둔다.
  - relevant test pass
  - relevant format/schema pass
  - reviewer approval
  - evidence link

## Open Point
- `warning-only` 게이트와 `blocking` 게이트를 언제 분리할지는 파일럿 단계에서 다시 닫는다.
