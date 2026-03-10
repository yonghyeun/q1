# DEC: Router-style `AGENTS.md` and modular policy documents

- Date: 2026-03-08
- Context: 프로젝트 공통 Agent 운영 규칙을 정리하면서, 루트 `AGENTS.md`에 모든 정책 본문을 직접 적으면 문서가 빠르게 비대해지고 매번 불필요한 텍스트를 읽게 될 가능성이 커졌다. 동시에 branch/worktree, artifact traceability, approval gate 같은 규칙은 주제별로 독립 관리하고 싶었다.
- Decision: 루트 `AGENTS.md`는 프로젝트 공통 Agent 운영의 라우터이자 인덱스로 유지하고, 실제 상세 지침은 주제별 모듈 문서로 분리한다.
  - 루트 `AGENTS.md`에는 반드시 지켜야 하는 최소 핵심 규칙만 직접 둔다.
  - 세부 정책 본문, 예시, 예외, naming spec, 운영 절차는 `context/core/` 또는 `policies/` 아래의 별도 문서로 관리한다.
  - `AGENTS.md`는 "언제 어떤 문서를 읽어야 하는지"를 안내하는 reference map 역할을 가진다.
  - `AGENTS.md`의 각 섹션은 단순 카테고리나 목차가 아니라 모듈 경계를 드러내는 boundary 역할을 가진다.
  - 섹션은 `Git and Workspace`, `Execution`, `Approval Gate`처럼 책임 영역이 분명한 이름으로 나누고, 각 섹션에서 해당 모듈 문서를 연결한다.
  - 이 구조를 통해 에이전트는 매번 전체 정책 본문을 읽기보다, 현재 작업과 관련된 boundary의 문서만 선택적으로 읽는 것을 기본 동작으로 삼는다.
  - branch/worktree 규칙, approval gate, naming convention 같은 세부 규칙은 개별 문서로 모듈화한다.
  - 하위 디렉토리의 `AGENTS.md`도 같은 패턴을 따라, 공통 규칙을 반복하지 않고 해당 서브트리 전용 라우팅과 추가 제약만 둔다.
  - 다만 `main` 직접 커밋 금지, destructive git 금지, 임의 revert 금지처럼 절대 규칙은 링크로만 숨기지 않고 `AGENTS.md` 본문에 남긴다.
- Alternatives: 루트 `AGENTS.md`에 모든 정책 본문을 직접 기록한다. 정책을 전부 `developer_instructions`로 이동한다. 별도 문서 없이 스크립트와 코드만 단일 정본으로 본다.
- Tradeoffs: 문서 수가 늘고, 세부 규칙을 보려면 링크 문서를 추가로 열어야 한다. 대신 `AGENTS.md`를 짧고 안정적으로 유지할 수 있고, context compact에 유리하며, 규칙을 주제별로 독립 수정하기 쉬워진다. 또한 하위 디렉토리에서 같은 패턴으로 확장하기 쉬워져 프로젝트 공통 규칙과 로컬 특수 규칙의 경계가 분명해진다. 섹션을 boundary 중심으로 설계하면 라우팅 정확도는 높아지지만, 섹션 이름과 문서 책임 범위를 일관되게 유지해야 하는 관리 규율이 추가된다.
- Revisit if: 실제 운영에서 에이전트가 링크 문서를 자주 놓쳐 핵심 규칙 누락이 반복되거나, 정책 문서 수가 과도하게 늘어 라우팅 비용이 다시 커지거나, 반대로 규칙 대부분이 항상 함께 읽혀야 해 인덱스 분리가 실질적 이득을 주지 못한다고 판단될 때.
