# Git Hooks

이 저장소는 `commit-msg`, `pre-commit`, `pre-push` hook을 사용합니다.

## 적용 방법
아래 명령으로 hooks 경로를 설정합니다.

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
chmod +x .githooks/pre-commit
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
- 브랜치 형식: `task/i1234-T-0001-short-topic`
- 정규식: `^task/i[0-9]+-T-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$`
- `main` 브랜치 직접 커밋/푸시 금지
- `pre-push`에서 `agent-team/runs/<task-id>/` 존재 여부를 확인
- 공통 검증 스크립트: `scripts/repo/branch_guard.py`
- PR에서는 브랜치 issue 번호와 동일한 `Closes #<issue>` 문구가 필수

## SoT 동기화 검증
- `pre-commit`은 SoT 관련 파일 변경 시 `.codex` 생성 결과와 동기화를 검사합니다.
- 불일치 시 아래 명령으로 재생성 후 다시 커밋합니다.

```bash
python3 agent-team/scripts/generate_codex_runtime.py
python3 agent-team/scripts/verify_codex_runtime_sync.py
```

## 예시
```bash
git commit -m "docs(doc) : 커밋 규칙 문서 정리" -m "커밋 메시지 검증 훅 적용 방법을 추가"
```
