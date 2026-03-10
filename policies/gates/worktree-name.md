# Gate: worktree-name

## Purpose
- worktree 이름이 저장소 naming 규칙을 따르는지 검증.
- branch 목적과 worktree 실행 슬롯을 구분 가능하게 유지.

## Trigger
- `git worktree add` wrapper 또는 worktree 생성 helper 실행 시점.

## Status
- `active`

## SoT
- [../worktree-naming.md](../worktree-naming.md)

## Enforcer
- [../../scripts/repo/worktree_name_guard.py](../../scripts/repo/worktree_name_guard.py)
- [../../scripts/repo/worktree_add.sh](../../scripts/repo/worktree_add.sh)
- Git hook으로는 생성 시점 interception이 어려우므로 wrapper 기반 enforcement 우선.

## Dependencies
- [../worktree-naming.md](../worktree-naming.md)

## Failure Mode
- worktree 이름이 `<branch-slug>--<purpose>` 형식을 벗어나면 실패.
- worktree slug가 대상 branch slug와 다르면 실패.

## Tests
- [../../scripts/repo/tests/test_worktree_name_guard.py](../../scripts/repo/tests/test_worktree_name_guard.py)
