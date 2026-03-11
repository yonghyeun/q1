# DEC: Issue label taxonomy를 type status priority area 축으로 고정

- Date: 2026-03-11
- Status: partially superseded by `2026-03-11_separate-area-and-source-type-labels.md`
- Context: remote backlog로 운영하려면 issue list에서 빠르게 필터링 가능한 공통 분류 축이 필요하다.
- Decision: label 축은 `type:*`, `status:*`, `priority:*`, `area:*` 네 가지로 둔다. status의 세부 값은 후속 decision에서 별도 고정한다.
- Alternatives: label 없이 type만 사용. 더 많은 축(`kind`, `severity`, `source`)을 초기부터 도입.
- Tradeoffs: label 관리 규율이 필요하다. 대신 backlog triage와 `gh issue list` 필터링이 쉬워진다.
- Revisit if: backlog 운영 중 필터링 정보가 부족하거나 특정 축이 거의 사용되지 않아 유지 비용이 더 커질 때.
