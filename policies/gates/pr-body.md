# Gate: pr-body

## Purpose
- PR 본문이 remote review ledger 구조를 따르는지 검증.
- 필수 섹션 누락, placeholder, 빈 섹션을 차단.
- `Primary Issue`의 close keyword 자체는 이 gate가 아니라 `pr-primary-issue-link` gate가 담당.

## Trigger
- `scripts/repo/pr_create.sh` 실행 직전.

## Status
- `active`

## SoT
- [../branch-pr-convention.md](../branch-pr-convention.md)
- [../../.github/pull_request_template.md](../../.github/pull_request_template.md)

## Enforcer
- [../../scripts/repo/pr_body_quality_guard.py](../../scripts/repo/pr_body_quality_guard.py)

## Dependencies
- [../../scripts/repo/body_guard_common.py](../../scripts/repo/body_guard_common.py)
- [../../scripts/repo/pr_create.sh](../../scripts/repo/pr_create.sh)
- [../../.github/pull_request_template.md](../../.github/pull_request_template.md)

## Failure Mode
- 실패 시 PR 생성 차단.

## Tests
- [../../scripts/repo/tests/test_pr_body_quality_guard.py](../../scripts/repo/tests/test_pr_body_quality_guard.py)
