# Branch & PR Convention

## 목적
- 브랜치 이름만으로 작업 단위(`task-id`)를 식별하고 ADLC 산출물 추적을 강제한다.
- 로컬 훅/CI/PR 게이트에서 동일 규칙을 사용해 우회 없는 운영을 보장한다.

## 브랜치 모델 (task 단일형)
- 기본 브랜치: `main`
- 작업 브랜치: `task/<task-id>-<short-topic>`
  - 정규식: `^task/T-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$`
  - 예시: `task/T-0007-adlc-gate-check`
- 보호 브랜치(`main`) 직접 커밋/직접 푸시 금지

## 브랜치 생성 규칙
1. `main` 최신화 후 작업 브랜치 생성
   - `git switch main`
   - `git pull --ff-only`
   - `git switch -c task/T-0007-adlc-gate-check`
2. 브랜치의 `task-id`에 대응하는 경로를 준비한다.
   - `agent-team/runs/<task-id>/`
3. 단일 브랜치에는 단일 task만 포함한다.

## PR 원칙
- 대상 브랜치: `main` 고정
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
- 공통 검증 엔진
  - `scripts/repo/branch_guard.py`
  - 규칙 SoT: `policies/branch-policy.rules.json`

## 예외 정책
- 긴급 대응이어도 브랜치 네이밍 예외를 두지 않는다.
- 예외적 승인 흐름은 PR에서 명시하고 사후 `feedback-record.json`으로 재발 방지안을 기록한다.
