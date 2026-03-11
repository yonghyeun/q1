# Branch Naming

## Purpose
- 이 문서는 저장소의 공통 branch naming 규칙을 정의.
- branch는 실행 주체가 아니라 변경 목적 식별자.

## Rule
- 기본 형식: `<type>/<slug>`

## Allowed Types
- `feature`
- `fix`
- `docs`
- `config`
- `chore`
- `refactor`
- `hotfix`

## Slug Rules
- 소문자, 숫자, 하이픈만 사용.
- 변경 목적이 드러나야 함.
- 사람 이름, agent 이름, 임시 감정 표현은 넣지 않음.
- branch 하나에는 하나의 변경 의도 유지.

## Examples
- `feature/signup-flow`
- `fix/token-refresh-race`
- `config/agent-router-structure`
- `docs/policy-routing-refresh`

## Notes
- branch naming은 변경 목적 식별에 집중.
- 실행 슬롯 정보는 branch가 아니라 worktree에서 관리.
- 연결 issue 정보는 branch 이름이 아니라 worktree metadata에서 관리.
- PR 규칙과 훅 규칙은 [branch-pr-convention.md](branch-pr-convention.md) 참조.
