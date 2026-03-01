# Git Branch Governance Architecture

## 목표
- 브랜치 규칙을 문서 합의가 아니라 실행 가능한 정책으로 운영한다.
- 로컬 훅/CI/에이전트가 동일한 규칙 SoT를 참조하게 만들어 정책 드리프트를 방지한다.
- GitHub issue → branch → PR → merge 흐름을 자동 추적으로 연결한다.

## 구성 요소
1. **사람용 정책**
   - `policies/branch-pr-convention.md`
2. **기계용 정책 SoT**
   - `policies/branch-policy.rules.json`
3. **공통 검증 엔진**
   - `scripts/repo/branch_guard.py`
4. **강제 지점**
   - 로컬 훅: `.githooks/pre-commit`, `.githooks/pre-push`
   - CI 게이트: `scripts/repo/ci-branch-gate.sh`, `scripts/repo/pr_issue_guard.py`, `.github/workflows/branch-governance.yml`
5. **에이전트 토큰 최적화 라우팅**
   - `context/core/policy-routing.md`

## 데이터 흐름
1. 개발자가 GitHub issue 생성 후 `task/i<issue>-T-000N-...` 브랜치 생성
2. 커밋 시 `pre-commit`이 브랜치 이름 검증
3. 푸시 시 `pre-push`가 브랜치 이름 + `agent-team/runs/<task-id>/` 존재 여부 검증
4. PR CI에서 이름/컨텍스트/필수 산출물 + `Closes #<issue>` 일치 검증
5. PR 게이트 문서(`agent-team/integration/pr-gate-policy.md`)와 동일 기준으로 승인
6. Merge 후 remote head branch 자동 삭제 + local cleanup

## 설계 원칙
- 정책 본문을 AGENTS에 중복하지 않는다.
- 규칙 변경 시 `branch-policy.rules.json`만 수정하고 훅/CI/에이전트가 재사용한다.
- 긴급 상황에서도 브랜치 네이밍 예외를 만들지 않는다.
