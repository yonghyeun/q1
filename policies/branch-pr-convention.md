# Branch & PR Convention

## 목적
- 브랜치 이름만으로 GitHub Issue와 작업 단위(`task-id`)를 함께 식별한다.
- 로컬 훅/CI/PR 게이트에서 동일 규칙을 사용해 우회 없는 운영을 보장한다.

## 브랜치 모델 (Issue + Task 이중키)
- 기본 브랜치: `main`
- 작업 브랜치: `task/i<issue-number>-<task-id>-<short-topic>`
  - 정규식: `^task/i[0-9]+-T-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$`
  - 예시: `task/i1234-T-0007-adlc-gate-check`
- 보호 브랜치(`main`) 직접 커밋/직접 푸시 금지

## 표준 흐름 (Issue-Driven)
1. GitHub issue 생성 (`feature|bug|chore` 템플릿)
   - 템플릿 위치: `.github/ISSUE_TEMPLATE/`
   - CLI 예시: `./scripts/repo/issue_create.sh --type feature --task-id T-0007 --title "작업 제목" --body-file /tmp/issue.md`
   - 본문은 템플릿 섹션을 모두 채운 markdown 파일로 작성한다.
2. 작업 브랜치 생성
   - `git switch main`
   - `git pull --ff-only`
   - `git switch -c task/i1234-T-0007-adlc-gate-check`
3. 브랜치의 `task-id`에 대응하는 경로를 준비한다.
   - `agent-team/runs/<task-id>/`
4. PR 생성 시 본문에 `Closes #1234`를 반드시 포함한다.
   - CLI 예시: `./scripts/repo/pr_create.sh --title "[T-0007] 작업 제목" --body-file /tmp/pr.md`
   - 본문은 `.github/pull_request_template.md` 필수 섹션을 모두 채운 markdown 파일로 작성한다.
5. Remote merge 후 head branch 자동 삭제
6. 로컬에서 `fetch --prune`, `pull --rebase`, merged branch 삭제

## PR 원칙
- 대상 브랜치: `main` 고정
- PR 본문에 브랜치 issue 번호와 동일한 auto-close 키워드 필수
  - 예: `Closes #1234`
- PR 설명에 작업 목적/범위/비범위 명시
- ADLC 산출물 링크 포함
- 리뷰어가 재현 가능한 검증 절차 포함

## 강결합 체크
머지 전 아래 산출물을 확인한다.
- `task-brief.json`
- `trace.md`
- `run-log.md`
- `run-report.json`
- 필요 시 `feedback-record.json`

## 자동 강제 지점
- 로컬
  - `.githooks/pre-commit`: 브랜치 이름 검증
  - `.githooks/pre-push`: 브랜치 이름 + task 컨텍스트 검증
- CI
  - `scripts/repo/ci-branch-gate.sh`: 이름/컨텍스트/필수 산출물 검증
  - `scripts/repo/pr_issue_guard.py`: PR 본문 close 키워드와 브랜치 issue 번호 일치 검증
- 공통 검증 엔진
  - `scripts/repo/branch_guard.py`
  - 규칙 SoT: `policies/branch-policy.rules.json`

## Merge 이후 정리
- Remote: GitHub `Automatically delete head branches` 활성화
- Local:
  1. `git switch main`
  2. `git fetch origin --prune`
  3. `git pull --rebase origin main`
  4. `git branch -d <merged-branch>`
  - 스크립트: `scripts/repo/post_merge_cleanup.sh <merged-branch>`

## 예외 정책
- 긴급 대응이어도 브랜치 네이밍 예외를 두지 않는다.
- 예외적 승인 흐름은 PR에서 명시하고 사후 `feedback-record.json`으로 재발 방지안을 기록한다.
