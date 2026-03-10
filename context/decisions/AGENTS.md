# Decisions Agent Rules

## Purpose
- 이 문서는 `context/decisions/` 아래 decision 문서를 생성하거나 수정할 때 따라야 하는 로컬 규칙을 정의한다.
- 목표는 각 decision 문서를 원자적 단위로 유지하고, 서로 다른 결정을 한 문서에 섞지 않는 것이다.

## Scope
- 이 규칙은 `context/decisions/` 아래의 decision 문서와 보조 문서에 적용된다.
- 루트 `AGENTS.md`의 공통 규칙 위에 추가되는 로컬 규칙으로 본다.

## Atomicity Rules
- 각 decision 문서는 하나의 결정만 다룬다.
- 서로 독립적으로 설명 가능한 결정은 별도 문서로 분리한다.
- 하나의 문서에서 여러 질문에 동시에 답하지 않는다.
- 제목, 파일명 slug, `Decision:` 항목의 범위는 서로 일치해야 한다.

## Update Rules
- 기존 decision 문서의 의미를 크게 바꾸는 수정은 지양한다.
- 후속 결정, 예외, 방향 전환은 기존 문서를 덮어쓰기보다 새 decision 문서로 추가한다.
- 기존 문서와의 관계가 필요하면 `Status`, `related to`, `superseded by` 같은 방식으로 명시한다.
- 기존 문서의 수정은 오탈자 정정, 표현 명확화, 링크 보완 같은 비의미적 변경을 기본값으로 한다.

## Writing Rules
- 문서는 짧고 명확하게 유지한다.
- `Context`, `Decision`, `Alternatives`, `Tradeoffs`, `Revisit if` 범위를 하나의 결정 주제 안에서만 작성한다.
- 구현 세부 절차, 운영 매뉴얼, 장문 배경설명은 decision 문서에 과도하게 넣지 않는다.
- 상세 운영 규칙은 `context/core/`, `context/wbs/`, `policies/` 문서로 분리하고 decision에서는 결정 사실과 이유만 남긴다.

## File Rules
- 파일명은 `YYYY-MM-DD_slug.md` 형식을 따른다.
- 하나의 문서를 여러 결정의 묶음 로그처럼 사용하지 않는다.
- 비슷한 주제라도 결정 시점과 판단 기준이 다르면 별도 문서로 분리한다.

## References
- 사람용 템플릿: [README.md](README.md)
