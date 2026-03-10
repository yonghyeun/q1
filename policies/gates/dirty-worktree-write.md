# Gate: dirty-worktree-write

## Purpose
- 더티 워크트리에서 의도치 않은 쓰기 작업이 누적되는 것을 차단 또는 경고.
- 기존 변경사항과 현재 작업의 충돌 가능성을 조기에 드러냄.

## Trigger
- helper 기반 write action 직전 preflight 시점.
- commit hook에는 연결하지 않음. staged change 자체와 충돌하기 때문.

## Status
- `active`

## SoT
- [../git-workspace-policy.md](../git-workspace-policy.md)

## Enforcer
- [../../scripts/repo/dirty_worktree_guard.py](../../scripts/repo/dirty_worktree_guard.py)
- `git status --porcelain` 기반으로 clean worktree 여부만 검증.
- [../../scripts/repo/pr_create.sh](../../scripts/repo/pr_create.sh)
- [../../scripts/repo/pr_merge.sh](../../scripts/repo/pr_merge.sh)
- trigger 연결은 helper script 경로에서 담당.

## Dependencies
- [../git-workspace-policy.md](../git-workspace-policy.md)

## Failure Mode
- 차단형 gate.
- dirty 상태가 감지되면 helper 경로에서 즉시 실패.
- staged, unstaged, untracked 변경을 모두 dirty로 간주.

## Tests
- [../../scripts/repo/tests/test_dirty_worktree_guard.py](../../scripts/repo/tests/test_dirty_worktree_guard.py)
