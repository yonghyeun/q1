# DEC: WBS task index is a generated projection with pre-commit regeneration

- Date: 2026-03-07
- Context: `context/wbs/tasks/index.md`는 개별 task YAML의 요약 projection이지만, 사람이 표를 직접 수정하면 정본인 `context/wbs/tasks/*.yaml`과 쉽게 어긋난다. 특히 병렬 개발과 에이전트 기반 planning에서 stale summary는 단순 문서 오차가 아니라 잘못된 task 선택과 planning 오류로 이어질 수 있다. 동시에 `index.md`는 사람이 빠르게 backlog를 읽는 진입점이므로 완전히 없애기보다는 정합성을 유지하는 운영 규칙이 필요하다.
- Decision: `context/wbs/tasks/index.md`의 표 영역은 generated projection으로 관리한다.
  - 정본은 계속 `context/wbs/tasks/*.yaml`이다.
  - `index.md`의 설명 텍스트는 사람이 유지할 수 있지만, task summary 표 영역은 자동 생성 대상으로 본다.
  - 로컬 자동화의 기본 위치는 `pre-commit` hook으로 둔다.
  - task YAML이 커밋될 때 `pre-commit`이 index 생성 스크립트를 실행하고, 갱신된 `index.md`를 다시 stage해 같은 커밋에 포함시키는 방식을 기본 운영으로 본다.
  - 가능하면 생성 기준은 working tree가 아니라 staged task YAML이어야 한다.
  - exact 구현이 어렵다면 최소한 관련 task YAML이나 `index.md`에 unstaged 변경이 남아 있을 때 commit을 막는 방식으로 정합성을 보호한다.
  - `index.md`는 표 전체가 아니라 marker로 감싼 summary 구간만 재작성한다.
  - `index.md`용 별도 `note` 또는 `index_note` 필드는 현재 두지 않는다.
  - 향후 CI를 도입하면 index를 생성하지 않고, 생성 결과가 최신 상태인지 검사만 하는 방향을 우선 검토한다.
- Alternatives: `index.md`를 계속 사람이 직접 유지한다. `index.md`를 제거하고 task 디렉터리만 본다. CI만 두고 로컬 hook은 두지 않는다.
- Tradeoffs: generated projection으로 바꾸면 로컬 hook과 생성 스크립트를 유지해야 한다. 대신 task YAML과 index summary의 drift를 줄일 수 있고, 사람이 overview를 빠르게 읽는 장점은 유지하면서 정합성도 확보할 수 있다. 또한 `index.md`를 정본처럼 착각하는 위험을 줄이고, 나중에 CI 검증까지 자연스럽게 확장할 수 있다.
- Revisit if: backlog 규모가 매우 작아 수동 유지 비용이 무시 가능하다고 확인되거나, 반대로 task 수가 커져 Markdown index보다 다른 projection artifact가 더 적합해질 때, 혹은 staged 기준 생성 구현 복잡도가 운영 이익보다 크다고 판단될 때.
