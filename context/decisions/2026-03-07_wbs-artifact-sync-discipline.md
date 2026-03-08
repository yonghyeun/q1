# DEC: Sync discipline for WBS runtime artifacts

- Date: 2026-03-07
- Context: WBS orchestration 모델이 `packet + trace`에서 `packet + trace + operator decision + current/snapshot ledger`로 확장되는 동안, narrative 문서, schema, template, example, validator, test가 서로 다른 속도로 갱신되었다. 그 결과 `active`와 `current` 의미가 섞이고, `snapshot_ref` checkpoint 규칙이 schema와 문서에서 다르게 보이며, template 예시가 실제 schema shape와 어긋나는 drift가 발생했다.
- Decision: WBS runtime 모델 변경은 최소한 `narrative docs`, `schemas`, `templates`, `examples`, `validator`, `tests`, `docs index/README`를 한 묶음으로 갱신한다. ledger 용어는 `active_packet_*` 대신 `current_packet_*`로 통일해 최신 projection 기준 packet을 뜻하게 한다. `snapshot_ref`는 checkpoint decision에서 요구하고 `dispatch`에서는 기본 생략으로 둔다. 또한 machine field와 narrative field를 문서와 schema에서 명시적으로 분리한다.
- Alternatives: drift를 허용하고 validator만 정본으로 삼는다. 반대로 모든 설명 문서를 제거하고 schema/example만 남긴다.
- Tradeoffs: 변경 한 번당 수정 면적이 넓어져 문서 유지 비용이 늘어난다. 대신 WBS 작성 전에 모델 경계가 더 명확해지고, operator와 자동화가 같은 의미 체계를 공유할 수 있다.
- Revisit if: schema로부터 template/doc를 자동 생성하는 도구를 도입하거나, run ledger가 backlog까지 포함하도록 범위를 다시 정의할 때.
