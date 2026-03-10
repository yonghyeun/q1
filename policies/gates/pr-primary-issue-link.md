# Gate: pr-primary-issue-link

## Purpose
- PR 본문에 primary issue를 닫는 close keyword가 존재하는지 검증.
- PR과 primary issue의 연결을 강제.
- 검증 범위는 `Primary Issue` 섹션으로 한정.

## Trigger
- `scripts/repo/pr_create.sh` 실행 직전.

## Status
- `active`

## SoT
- [../branch-pr-convention.md](../branch-pr-convention.md)
- [../../.github/pull_request_template.md](../../.github/pull_request_template.md)

## Enforcer
- [../../scripts/repo/pr_issue_guard.py](../../scripts/repo/pr_issue_guard.py)

## Dependencies
- [../../scripts/repo/pr_create.sh](../../scripts/repo/pr_create.sh)
- [../../.github/pull_request_template.md](../../.github/pull_request_template.md)
- [../../scripts/repo/body_guard_common.py](../../scripts/repo/body_guard_common.py)

## Failure Mode
- 실패 시 PR 생성 차단.

## Tests
- [../../scripts/repo/tests/test_pr_issue_guard.py](../../scripts/repo/tests/test_pr_issue_guard.py)
