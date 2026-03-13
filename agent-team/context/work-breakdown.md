# Work Breakdown

## Decision
- agent-team 구축 작업은 시스템 레이어 기준이 아니라 실제 운영 순서 기준으로 분해한다.
- 이유는 이후 역할 설계, handoff, 검증, 관측성이 모두 이 순서를 따라 연결되기 때문이다.

## Operating Sequence
1. Issue Intake
- GitHub issue backlog input을 읽는다.
- issue 제목, 본문, label, 관련 링크를 확인한다.
- upstream source가 WBS인지, 사람 요청인지, runtime observation인지 파악한다.

2. Ingress Normalization
- issue를 공통 task ingress spec 초안으로 정규화한다.
- 추론으로 채울 수 있는 내용은 draft로 만들고, 불명확한 것은 `open_points`로 남긴다.
- 사람 승인과 구조 검증 전까지는 확정하지 않는다.

3. Accepted Task Approval
- 사람이 ingress draft를 검토한다.
- 승인, 수정, 반려 중 하나를 결정한다.
- 승인된 task만 다음 단계로 넘긴다.

4. Atomic Decomposition
- accepted task를 반복 가능한 atomic task 목록으로 자른다.
- 의존성과 선후관계를 표시한다.
- 사람 판단이 필요한 atomic task를 분리한다.

5. Execution Planning
- atomic task를 trace node 흐름으로 계획한다.
- 어떤 node를 거칠지, 어떤 evidence와 handoff packet이 필요한지 정한다.

6. Runtime Execution
- packet을 실행한다.
- 실행 중 산출물과 trace를 남긴다.
- 실패, partial, block 여부를 기록한다.

7. Verification
- 결과가 acceptance criteria와 node exit evidence를 만족하는지 확인한다.
- 통과, 재작업, 차단 여부를 판정한다.

8. Feedback And Improvement
- 병목과 실패 원인을 기록한다.
- 동일 병목 재발 여부를 추적한다.
- 다음 run에 반영할 수정 항목을 남긴다.

## Breakdown Output
- 1~3단계 산출물:
  - backlog input issue
  - ingress draft
  - accepted task
- 4단계 산출물:
  - atomic task list
- 5단계 산출물:
  - execution plan
  - handoff packet
- 6~8단계 산출물:
  - trace
  - verification result
  - feedback item

## Why This Order
- issue intake가 먼저 닫혀야 입력 drift를 줄일 수 있다.
- normalization과 approval이 먼저 있어야 decomposition 품질이 흔들리지 않는다.
- decomposition이 먼저 있어야 packet과 trace를 과도하게 크게 만들지 않는다.
- verification과 feedback이 뒤에 있어야 품질 측정과 개선 루프가 자연스럽게 이어진다.

## Boundary
- issue 자체는 backlog input이다.
- accepted task는 intake가 끝난 planning 입력이다.
- atomic task는 decomposition 산출물이다.
- handoff packet은 execution planning/runtime 산출물이다.
- trace와 feedback은 runtime 이후 산출물이다.
