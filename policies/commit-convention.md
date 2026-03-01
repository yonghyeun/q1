# Commit Convention

## 목적
- 커밋 로그를 운영/개발 추적 가능한 단위로 유지한다.

## 형식
저장소 `.githooks/commit-msg` 규칙을 따른다.

- 총 2줄(제목/설명)
- 제목 형식: `<category>(<layer>) : <작업 내용>`
- category: `feat|fix|refactor|style|docs|config|chore|test`
- layer: `ui|api|domain|db|shared|infra|doc`
- 작업 내용/설명에는 한국어 포함

## 예시
- `docs(doc) : 아키텍처 베이스라인 문서 추가`
- `에이전트 팀 운영 구조와 정책 문서를 정리하고 루트 구조를 확정함`
