# Branch & PR Convention

## 목적
- 브랜치 이름만으로 변경 성격(scope)과 주제를 식별한다.
- 단일 에이전트 워크플로우 기준으로 로컬 훅/CI/PR 게이트를 동일 규칙으로 유지한다.

## 브랜치 모델
- 기본 브랜치: `main`
- 작업 브랜치: `<scope>/<short-topic>`
  - 정규식: `^(feature|fix|docs|config|chore|refactor|hotfix)/[a-z0-9]+(?:-[a-z0-9]+)*$`
  - 예시: `config/wbs-governance-reset`, `feature/signup-flow`
- 보호 브랜치(`main`) 직접 커밋/직접 푸시 금지

## 표준 흐름
1. GitHub issue 생성 (`feature|bug|chore` 템플릿)
2. 작업 브랜치 생성
   - `git switch main`
   - `git pull --ff-only`
   - `git switch -c config/wbs-governance-reset`
3. 변경 구현 및 검증
4. PR 생성 시 본문에 `Closes #1234` 포함
5. Merge 후 remote head branch 삭제 + local cleanup

## PR 원칙
- 대상 브랜치: `main` 고정
- PR 본문에 close keyword(`Closes/Fixes/Resolves #N`) 필수
- 작업 목적/범위/검증 방법을 명시

## 자동 강제 지점
- 로컬
  - `.githooks/pre-commit`: 브랜치 이름 검증
  - `.githooks/pre-push`: 브랜치 이름 및 컨텍스트 검증
- CI
  - `scripts/repo/ci-branch-gate.sh`: 이름/컨텍스트/필수 파일 검증
  - `scripts/repo/pr_issue_guard.py`: PR 본문 close keyword 검증
- 공통 검증 엔진
  - `scripts/repo/branch_guard.py`
  - 규칙 SoT: `policies/branch-policy.rules.json`

## 예외 정책
- 긴급 대응이어도 브랜치 네이밍 예외를 만들지 않는다.
- 예외 운영이 발생하면 PR 본문에 이유와 후속 조치를 기록한다.
