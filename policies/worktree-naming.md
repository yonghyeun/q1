# Worktree Naming

## Purpose
- 이 문서는 worktree 이름을 실행 슬롯 중심으로 일관되게 관리하기 위한 규칙을 정의.

## Rule
- 권장 형식: `<branch-slug>--<purpose>`

## Purpose Values
- `impl`
- `review`
- `fix`
- `verify`
- `docs`
- `ops`

## Examples
- `signup-flow--impl`
- `signup-flow--review`
- `token-refresh-race--fix`
- `agent-router-structure--ops`

## Notes
- branch는 변경 목적, worktree는 실행 슬롯.
- 같은 branch에 여러 worktree 필요 시 purpose suffix로 구분.
- `agent-a`, `agent-b` 같은 이름 대신 작업 목적이 드러나는 suffix 사용.
- 하나의 worktree는 가능하면 하나의 실행 목적만 담당.
