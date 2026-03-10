# DEC: Split shared `developer_instructions` and root `AGENTS.md` by responsibility

- Date: 2026-03-09
- Context: 프로젝트 공통 Agent 규칙을 정리하면서, 말투와 판단 태도 같은 에이전트 기본 상호작용 성향을 `AGENTS.md`에 둘지, 저장소 운영 규칙과 함께 관리할지 혼동이 생겼다. 동시에 브랜치/커밋/승인 게이트 같은 저장소 규칙은 repo 안에 드러나야 했고, 나중에는 WBS 기반 에이전트와 일반 작업 에이전트의 profile도 분리할 계획이 있었다.
- Decision: 공통 `developer_instructions`와 루트 `AGENTS.md`는 역할을 분리한다.
  - 공통 `developer_instructions`는 말투, 응답 구조, 판단 태도, 비판적 사고 보조처럼 에이전트의 기본 상호작용 성향만 다룬다.
  - 루트 `AGENTS.md`는 브랜치, 커밋, 승인 게이트, 저장소 운영 규칙처럼 프로젝트 공통 작업 규칙만 다룬다.
  - 조건부 traceability, WBS 문맥, 특정 작업 흐름처럼 일부 에이전트에만 필요한 규칙은 공통 레이어에 넣지 않고, 나중에 개별 profile의 `developer_instructions`나 더 좁은 범위의 `AGENTS.md`로 내린다.
- Alternatives: 공통 규칙을 모두 루트 `AGENTS.md`에 기록한다. 공통 규칙을 모두 `developer_instructions`에 기록한다. profile 분리를 기다리지 않고 조건부 규칙까지 공통 레이어에 미리 넣는다.
- Tradeoffs: 책임과 재사용성은 좋아지지만, 규칙 위치가 두 군데가 되어 중복 작성과 우선순위 충돌을 조심해야 한다. 반대로 분리를 하지 않으면 초기 설정은 단순해지지만, 저장소 규칙과 에이전트 성향이 뒤섞여 확장성과 가시성이 떨어진다.
- Revisit if: profile 분리를 하지 않는 방향으로 운영이 바뀌거나, 공통 `developer_instructions`와 루트 `AGENTS.md`의 경계가 실제 운영에서 반복적으로 모호해져 다른 분리 기준이 더 적합하다고 판단될 때.
