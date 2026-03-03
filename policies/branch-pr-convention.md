# Branch & PR Convention

## 목적
- 브랜치 이름만으로 GitHub Issue와 작업 단위(`task-id`)를 함께 식별한다.
- 단일 에이전트 워크플로우에서도 로컬 훅/CI/PR 게이트를 동일 규칙으로 유지한다.

## 브랜치 모델 (Issue + Task 이중키)
- 기본 브랜치: `main`
- 작업 브랜치: `task/i<issue-number>-<task-id>-<short-topic>`
  - 정규식: `^task/i[0-9]+-T-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$`
  - 예시: `task/i1234-T-0007-single-agent-governance`
- 보호 브랜치(`main`) 직접 커밋/직접 푸시 금지

## 표준 흐름 (Issue-Driven)
1. GitHub issue 생성 (`feature|bug|chore` 템플릿)
2. 작업 브랜치 생성
   - `git switch main`
   - `git pull --ff-only`
   - `git switch -c task/i1234-T-0007-single-agent-governance`
3. task 컨텍스트 폴더 준비
   - `context/tasks/<task-id>/`
   - 최소 파일: `context.md`, `result.md`
4. PR 생성 시 본문에 `Closes #1234`를 반드시 포함
5. Merge 후 remote head branch 삭제 + local cleanup

## PR 원칙
- 대상 브랜치: `main` 고정
- PR 본문에 브랜치 issue 번호와 동일한 auto-close 키워드 필수
- 작업 목적/범위/검증 방법을 명시
- 수동 병렬 작업이 있었다면 결과 병합 기준을 PR에 기록

## 자동 강제 지점
- 로컬
  - `.githooks/pre-commit`: 브랜치 이름 검증
  - `.githooks/pre-push`: 브랜치 이름 + task 컨텍스트 검증
- CI
  - `scripts/repo/ci-branch-gate.sh`: 이름/컨텍스트/필수 파일 검증
  - `scripts/repo/pr_issue_guard.py`: PR 본문 close 키워드 검증
- 공통 검증 엔진
  - `scripts/repo/branch_guard.py`
  - 규칙 SoT: `policies/branch-policy.rules.json`

## Merge 이후 정리
- Remote: GitHub `Automatically delete head branches` 권장
- Local:
  1. `git switch main`
  2. `git fetch origin --prune`
  3. `git pull --rebase origin main`
  4. `git branch -d <merged-branch>`

## 예외 정책
- 긴급 대응이어도 브랜치 네이밍 예외를 만들지 않는다.
- 예외적 운영이 발생하면 PR 본문에 이유와 후속 조치를 남긴다.
