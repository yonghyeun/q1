# DEC: Classify Agent-facing documents by responsibility, authority, context, procedure, and output

- Date: 2026-03-09
- Context: 저장소의 Agent 운영 문서가 늘어나면서 `context/core`와 `policies`의 경계가 흐려 보였다. 동시에 루트 `AGENTS.md`, 공통 `developer_instructions`, `context/wbs`, `context/decisions`까지 함께 운영되고 있어, 각 문서가 Agent 구성 요소 중 무엇을 담당하는지 명시적인 분류 기준이 필요했다.
- Decision: Agent-facing 문서는 다섯 가지 운영 요소를 기준으로 분류한다.
  - `Responsibility`: Agent가 맡는 역할과 상호작용 성향. 공통 말투, 판단 태도, 역할 성향은 `developer_instructions`에 둔다.
  - `Authority`: Agent가 해도 되는 일과 금지되는 일. 저장소 공통 권한 경계와 승인 게이트는 루트 `AGENTS.md`와 `policies/`에 둔다.
  - `Context`: Agent가 판단에 사용해야 하는 사실, 배경, 목표, 가설. 장기 컨텍스트는 `context/core/`, WBS 전용 입력은 `context/wbs/`에 둔다.
  - `Procedure`: Agent가 작업을 수행하는 절차, naming rule, convention, 운영 흐름. Git workspace 규칙, branch/worktree naming, commit convention, quality gate는 `policies/`에 둔다.
  - `Output / Verification`: Agent가 남기는 산출물 형식과 검증 방식. commit 형식, 품질 게이트, structured output 규칙은 `policies/` 또는 작업별 전용 문서에 둔다.
  - `context/decisions/`는 위 다섯 요소 중 하나의 규칙 본문을 담는 곳이 아니라, 왜 그런 분류와 규칙을 택했는지 남기는 판단 기록으로 유지한다.
  - 정책 문서 라우팅은 별도 core 문서로 분리하지 않고, 루트 `AGENTS.md`의 boundary 섹션에서 직접 관리한다.
  - 문서를 새로 만들 때는 먼저 주된 요소 하나를 정하고, 그 요소에 맞는 저장 위치를 선택한다. 하나의 문서가 여러 요소를 동시에 강하게 담당하기 시작하면 문서를 분리한다.
- Alternatives: `context/core`와 `policies`를 하나의 폴더로 합친다. 문서 위치를 기능명만 기준으로 정하고 Agent 운영 요소 기준 분류는 만들지 않는다. 모든 운영 문서를 루트 `AGENTS.md`와 `developer_instructions` 안으로 끌어올린다.
- Tradeoffs: 분류 기준이 생겨 문서 위치 판단은 쉬워지지만, 새 문서를 만들 때 "주된 요소가 무엇인가"를 먼저 판단해야 하는 규율이 추가된다. 반대로 분류 기준이 없으면 초기에는 단순해 보이지만, 문서가 늘수록 경계가 무너지고 같은 내용을 여러 범주에 중복 기록할 가능성이 커진다.
- Revisit if: `context/core`와 `policies`의 경계가 실제 운영에서 반복적으로 무의미해지거나, 하나의 폴더로 합치는 편이 탐색성과 유지보수 비용 면에서 더 낫다고 판단될 때.
