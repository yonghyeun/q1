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
- `branch_guard.py`: 브랜치 이름 정책 검증
- `detached_head_guard.py`: detached HEAD 상태 차단
- `protected_branch_write_guard.py`: 보호 브랜치 직접 write 차단
- `dirty_worktree_guard.py`: dirty worktree 상태 차단
- `issue_title_guard.sh`: 이슈 제목 컨벤션 생성/검증 (`[type] 요약`)
- `issue_body_quality_guard.py`: issue 본문 품질 검증
- `issue_label_taxonomy.py`: issue label taxonomy SoT
- `issue_label_guard.py`: issue label taxonomy 검증 + label 인자 생성
- `issue_label_sync.py`: GitHub 원격 label 생성/갱신
- `pr_body_quality_guard.py`: PR 본문 품질 검증
- `pr_issue_guard.py`: PR 본문 `Primary Issue` close 키워드 존재 및 local linked issue metadata 일치 검증
- `gh_preflight.sh`: `origin` remote/`gh auth` 사전 점검. `--require-api` 사용 시 GitHub API 연결 가능 여부까지 확인
- `gh_failure_guard.sh`: `gh` 실행 실패 stderr를 분류해 sandbox/API 차단 재시도 힌트를 공통 제공
- `issue_create.sh`: gh CLI로 issue 생성 (`--body-file` 필수). GitHub API 차단 시 권한 상승 재시도 힌트를 출력
- `pr_create.sh`: 정책/본문 검증 후 PR 생성 (`--body-file` 필수). local linked issue metadata를 필수 요구하며, 성공 시 현재 worktree에 PR metadata 기록. GitHub API 차단 시 권한 상승 재시도 힌트를 출력
- `pr_title_guard.sh`: PR 제목 컨벤션 생성/검증 (`[scope] 요약`)
- `pr_merge.sh`: PR merge leaf (`gh pr merge` wrapper). remote merge만 담당하고 local cleanup은 수행하지 않음
- `task_start.sh`: 새 작업용 branch/worktree 준비 core wrapper. base ref와 재사용 branch의 origin 최신성을 확인한 뒤 진행. `--issue <number>` 지정 시 issue status를 `active`로 전이 가능. 기본 dry-run, 실제 실행은 `--apply --yes`
- `task_start_interactive.sh`: 사람용 interactive wrapper. dry-run 후 `y/N` 확인, 승인 시 `task_start.sh --apply --yes`
- `task_end.sh`: task 종료 core wrapper. 기본 dry-run, 실제 실행은 `--apply --yes`. local cleanup 순서는 `worktree -> branch`, partial completion이면 recovery cleanup만 수행
- `task_end_interactive.sh`: 사람용 interactive wrapper. dry-run 후 `y/N` 확인, 승인 시 `task_end.sh --apply --yes`
- `pr_finalize.sh`: legacy compatibility wrapper → `task_end.sh`
- `post_merge_branch_cleanup.sh`: merge 후 base branch sync + merged local branch 정리. linked worktree가 남아 있으면 선행 cleanup 필요
- `post_merge_cleanup.sh`: legacy compatibility wrapper → `post_merge_branch_cleanup.sh`
- `current_issue.sh`: 현재 worktree에 기록된 issue metadata 조회. `--live` 지원
- `current_pr.sh`: 현재 worktree에 기록된 PR metadata 조회. `--live` 지원
- `worktree_name_guard.py`: worktree 이름 정책 검증
- `worktree_add.sh`: worktree 생성 전 이름 정책 검증 wrapper
- `worktree_cleanup.sh`: removable linked worktree 검증 후 안전한 제거. orphan worktree 디렉토리는 감지만 하고 자동 삭제하지 않음
- `worktree_issue_metadata.sh`: worktree-scoped issue metadata read/write/clear helper
- `worktree_pr_metadata.sh`: worktree-scoped PR metadata read/write/clear helper
- `codex_wbs_emit.sh`: `codex exec --output-schema`로 WBS artifact 생성 + 검증
- `validate_wbs_artifact.py`: WBS packet/trace/operator decision/run ledger schema + semantic 검증
- `wbs_task_index.py`: WBS task YAML에서 `context/wbs/tasks/index.md` summary projection 생성/검사

## 테스트
- 브랜치 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_branch_guard -v`
- detached HEAD 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_detached_head_guard -v`
- 보호 브랜치 write 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_protected_branch_write_guard -v`
- dirty worktree 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_dirty_worktree_guard -v`
- 이슈 제목 컨벤션 테스트:
  - `python3 -m unittest scripts.repo.tests.test_issue_title_guard -v`
- 이슈 본문 품질 테스트:
  - `python3 -m unittest scripts.repo.tests.test_issue_body_quality_guard -v`
- 이슈 label taxonomy 테스트:
  - `python3 -m unittest scripts.repo.tests.test_issue_label_guard -v`
- 이슈 label sync 테스트:
  - `python3 -m unittest scripts.repo.tests.test_issue_label_sync -v`
- PR 본문 품질 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_body_quality_guard -v`
- PR 생성 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_create -v`
- PR issue 링크 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_issue_guard -v`
- PR 제목 컨벤션 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_title_guard -v`
- current issue 조회 테스트:
  - `python3 -m unittest scripts.repo.tests.test_current_issue -v`
- current PR 조회 테스트:
  - `python3 -m unittest scripts.repo.tests.test_current_pr -v`
- PR merge dry-run 동작 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pr_merge_dry_run -v`
- post-merge branch cleanup 테스트:
  - `python3 -m unittest scripts.repo.tests.test_post_merge_branch_cleanup -v`
- worktree cleanup 테스트:
  - `python3 -m unittest scripts.repo.tests.test_worktree_cleanup -v`
- task end 테스트:
  - `python3 -m unittest scripts.repo.tests.test_task_end -v`
- task start 테스트:
  - `python3 -m unittest scripts.repo.tests.test_task_start_integration -v`
- worktree issue metadata 테스트:
  - `python3 -m unittest scripts.repo.tests.test_worktree_issue_metadata -v`
- worktree PR metadata 테스트:
  - `python3 -m unittest scripts.repo.tests.test_worktree_pr_metadata -v`
- worktree 이름 검증 테스트:
  - `python3 -m unittest scripts.repo.tests.test_worktree_name_guard -v`
- WBS artifact validator 테스트:
  - `python3 -m unittest scripts.repo.tests.test_validate_wbs_artifact -v`
- WBS task index projection 테스트:
  - `python3 -m unittest scripts.repo.tests.test_wbs_task_index -v`
- pre-commit dispatcher 테스트:
  - `python3 -m unittest scripts.repo.tests.test_pre_commit_dispatcher -v`
