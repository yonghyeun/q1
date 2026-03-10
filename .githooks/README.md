# Git Hooks

이 저장소는 `commit-msg`, `pre-commit`, `pre-push` hook을 사용합니다.
`pre-commit`은 dispatcher이며 실제 검증은 `.githooks/pre-commit.d/` 아래 독립 hooklet이 담당합니다.

## 적용 방법
아래 명령으로 hooks 경로를 설정합니다.

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
chmod +x .githooks/pre-commit
chmod +x .githooks/pre-commit.d/*
chmod +x .githooks/pre-push
```

또는 아래 스크립트를 사용합니다.

```bash
./scripts/repo/install-hooks.sh
```

## 검증 규칙 요약
- 메시지 내용 2줄(제목/설명)
- 제목 형식: `<카테고리>(<layer>) : <작업 내용>`
- 카테고리: `feat|fix|refactor|style|docs|config|chore|test`
- layer: `ui|api|domain|db|shared|infra|doc`
- 제목/설명에 한국어 포함

## 브랜치 정책 검증
- 브랜치 형식: `<scope>/<short-topic>`
- 허용 scope: `feature|fix|docs|config|chore|refactor|hotfix`
- 예시: `config/wbs-governance-reset`
- `main` 브랜치 직접 커밋/푸시 금지
- 공통 검증 스크립트: `scripts/repo/branch_guard.py`
- PR 본문 close keyword 검증은 hook이 아니라 PR 생성 스크립트 경로에서 수행한다.

## pre-commit hooklet
- `.githooks/pre-commit`은 `.githooks/pre-commit.d/` 아래 실행 파일을 이름순으로 실행한다.
- `.githooks/pre-commit.d/05-detached-head-write`: detached HEAD 직접 write 차단
- `.githooks/pre-commit.d/10-branch-name`: 브랜치 이름 검증
- `.githooks/pre-commit.d/15-protected-branch-write`: 보호 브랜치 직접 write 차단

## 예시
```bash
git commit -m "docs(doc) : 커밋 규칙 문서 정리" -m "커밋 메시지 검증 훅 적용 방법을 추가"
```
