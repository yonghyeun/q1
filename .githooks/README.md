# Git Hooks

이 저장소는 `commit-msg`와 `pre-commit` hook을 사용합니다.

## 적용 방법
아래 명령으로 hooks 경로를 설정합니다.

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
chmod +x .githooks/pre-commit
```

## 검증 규칙 요약
- 메시지 내용 2줄(제목/설명)
- 제목 형식: `<카테고리>(<layer>) : <작업 내용>`
- 카테고리: `feat|fix|refactor|style|docs|config|chore|test`
- layer: `ui|api|domain|db|shared|infra|doc`
- 제목/설명에 한국어 포함

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
