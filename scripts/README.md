# Repository Scripts

루트 `scripts/`는 **리포 전역에서 재사용되는 스크립트만** 둔다.

## 규칙
- 도메인 전용 스크립트는 해당 도메인 내부에 둔다.
  - 예: `apps/web/scripts/`
- 2개 이상 도메인에서 공통 사용될 때만 루트로 승격한다.

## 구조
- `repo/`: 저장소 전체 오케스트레이션
- `lib/`: 공통 유틸 함수

## 주요 스크립트 (`repo/`)
- `check-all.sh`: 저장소 기본 구조 점검
- `install-hooks.sh`: `.githooks` 설치/권한 설정
- `branch_guard.py`: 브랜치/컨텍스트/PR 필수 파일 정책 검증
- `body_quality_guard.py`: issue/PR 본문 품질 검증
- `ci-branch-gate.sh`: CI에서 브랜치 정책 차단 게이트 실행
- `pr_issue_guard.py`: PR 본문 close 키워드 존재 검증
- `gh_preflight.sh`: `origin` remote/`gh auth` 사전 점검
- `issue_create.sh`: gh CLI로 issue 생성 (`--body-file` 필수)
- `pr_create.sh`: 정책/본문 검증 후 PR 생성 (`--body-file` 필수)
- `pr_title_guard.sh`: PR 제목 컨벤션 생성/검증 (`[scope] 요약`)
- `pr_merge.sh`: PR merge + remote branch 삭제 + local cleanup 연계
- `post_merge_cleanup.sh`: merge 후 로컬 브랜치 정리 (`pull --rebase origin main`)

## 테스트
- 브랜치 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_branch_guard -v`
- PR issue 링크 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_issue_guard -v`
- PR 제목 컨벤션 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_title_guard -v`
- PR merge dry-run 동작 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_merge_dry_run -v`
