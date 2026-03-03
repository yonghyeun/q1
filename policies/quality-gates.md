# Quality Gates

## 기본 원칙
- 단일 에이전트 실행을 기본으로 하며, 핵심 변경은 사람 검토를 거친다.
- 수동 병렬 실행 시 결과 충돌 여부를 반드시 확인한다.

## 코드 품질 게이트(점진 도입)
1. Stage 1: lint / typecheck / build 권고
2. Stage 2: CI warning
3. Stage 3: CI blocking

## 운영 품질 게이트
- PR 전 `context/tasks/<task-id>/`의 최소 산출물(`context.md`, `result.md`)을 준비한다.
- 고위험 변경은 PR 본문에 롤백 계획을 포함한다.
