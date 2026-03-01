## Task ID
- T-0001

## Problem / Opportunity
- 브랜치/이슈/PR 운영 규칙은 정의되어 있지만, 에이전트가 issue 본문을 작성할 때 근거 없이 추상 문장을 쓰는 경우가 발생한다.
- 이로 인해 리뷰 단계에서 작업 범위와 수용 기준을 재해석해야 하며, 재작업 비용이 증가한다.

## Goal
- issue 본문을 근거 기반으로 작성하도록 스킬 지침을 표준화한다.
- Scope/Acceptance Criteria를 실행 가능한 수준으로 명시해, PR 단계의 품질 편차를 줄인다.

## In Scope
- `skills/public/gh-issue-create/SKILL.md` 지침 보강
- `skills/public/gh-issue-create/references/commands.md`에 자기검증 절차 명시
- 필요 시 관련 PR 스킬 문서와 참조 규칙 동기화

## Out of Scope
- GitHub 브랜치 보호 설정 자동화
- 테스트 파이프라인 구축/운영

## Acceptance Criteria
- [ ] issue 본문 작성 전에 참조해야 할 근거 목록이 스킬 문서에 명시되어 있다.
- [ ] 미확인 메타데이터(assignee/외부 승인)를 단정적으로 작성하지 않는 규칙이 문서화되어 있다.
- [ ] 본문 품질 가드(`body_quality_guard.py`)를 통과하는 예시 본문이 references에 포함되어 있다.

## Risks
- 템플릿이 바뀌면 예시 문서와 가드 규칙의 불일치가 발생할 수 있다.
- 완화: 템플릿 변경 시 references 예시와 가드 테스트를 함께 업데이트한다.
