# T-0004 Result

## 변경 요약
- 브랜치/PR 거버넌스를 단일 에이전트 운영 정책으로 재정의함.
- `agent-team/` 및 `.codex/` 추적 파일을 모두 제거함.
- 훅/스크립트/테스트를 `context/tasks/<task-id>/` 기반으로 정렬함.

## 검증
- `python3 -m unittest scripts.repo.tests.test_branch_guard scripts.repo.tests.test_pr_issue_guard -v`
- `./scripts/repo/check-all.sh`

## 후속 조치
- 필요 시 멀티 에이전트 재도입 기준을 별도 ADR로 정의.
