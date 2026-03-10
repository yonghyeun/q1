# DEC: Keep local skills split into frontmatter, `SKILL.md`, `references/`, and `scripts/`

- Date: 2026-03-09
- Related to: `2026-03-09_skill-owned-action-routing-instead-of-policy-doc.md`
- Context: 로컬 skill을 `.codex/skills/` 아래에 만들기 시작하면서, `SKILL.md` 본문만으로도 모든 설명을 담을 수 있는데 왜 `references/`와 `scripts/`, `agents/openai.yaml`을 분리해야 하는지에 대한 판단이 필요해졌다. 특히 skill이 트리거되면 관련 문서를 읽게 되므로, 본문과 참조 문서를 나누는 것이 실제로 의미가 있는지 명확히 해야 했다.
- Decision: 로컬 skill은 progressive disclosure와 책임 분리를 기준으로 아래 구조를 유지한다.
  - frontmatter는 trigger 판단에 필요한 `name`과 `description`에 집중한다.
  - `SKILL.md` 본문은 짧은 실행 playbook과 라우팅 지침만 둔다.
  - `references/`는 필요할 때만 읽는 세부 규칙, 명령 예시, 보조 설명을 둔다.
  - `scripts/`는 가능한 경우 설명보다 실행을 우선하는 deterministic entrypoint를 둔다.
  - `agents/openai.yaml`은 UI 메타데이터로 보고, trigger SoT나 실행 절차 SoT로 쓰지 않는다.
- Alternatives: 모든 지침을 `SKILL.md` 본문 하나에 몰아 넣는다. `references/` 없이 모든 세부 규칙을 본문에 중복 기록한다. wrapper 호출도 본문 설명만 남기고 별도 `scripts/`를 두지 않는다.
- Tradeoffs: 구조가 분리되므로 파일 수는 늘어나지만, skill 트리거 후에도 세부 문서를 전부 읽지 않아도 되어 context를 더 작게 유지할 수 있다. 본문은 workflow 변화에 맞춰 짧게 유지하고, 세부 규칙이나 예시는 `references/`에서 독립적으로 수정할 수 있다. 반대로 모든 내용을 본문에 몰면 구조는 단순해 보이지만, trigger 이후 매번 긴 본문을 읽게 되고 responsibility boundary가 흐려진다.
- Revisit if: skill 수가 매우 적고 세부 규칙도 거의 없어 `references/` 분리 이점이 사라지거나, skill loader 동작이 바뀌어 모든 참조 문서를 항상 자동 로드하는 구조가 되어 progressive disclosure 이점이 없어질 때.
