---
name: decision-log
description: Create a decision log entry under context/decisions (DEC) and commit it using this repo's 2-line commit convention. Use when the user asks to record a decision, decision rationale, or governance note.
---

# Decision Log Workflow (Repo)

이 스킬은 저장소의 `context/decisions/`에 결정 로그(DEC)를 남기고 커밋까지 만드는 절차를 표준화한다.

## When To Use

- 사용자가 "결정 로그 남겨줘", "decisions 폴더에 기록해줘" 같은 요청을 했을 때
- 구조/규칙/스코프처럼 "나중에 왜 이렇게 했는지"가 중요한 결정을 내렸을 때

## Output

1. 새 결정 로그 파일 1개 생성: `context/decisions/YYYY-MM-DD_slug.md`
2. (필요 시) 결정 로그 템플릿/운영 규칙은 `context/decisions/README.md`를 따른다.
3. 변경사항을 커밋 컨벤션에 맞춰 커밋한다.

## File Naming

- 파일명: `YYYY-MM-DD_slug.md`
- slug는 짧고 구체적으로: `context-docs-split`, `mvp-scope-cut` 등

## Content Template

아래 항목을 채운다(길게 쓰지 않는다).

- Date: YYYY-MM-DD
- Context: 왜 이 결정이 필요했나
- Decision: 무엇을 결정했나(명령문으로)
- Alternatives: 고려한 대안 1~2개
- Tradeoffs: 무엇을 포기했나
- Revisit if: 재검토 조건

## Commit Rules (Repo)

이 저장소 커밋 메시지는 2줄을 사용한다.

- 제목: `docs(doc) : <작업 내용>`
- 설명: 한국어로 한 줄 요약(무엇을 왜 했는지)

필요하면 커밋 규칙 문서를 확인한다.

- `policies/commit-convention.md`
- `.githooks/README.md`

