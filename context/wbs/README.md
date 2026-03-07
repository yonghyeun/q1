# WBS Context

WBS(Work Breakdown Structure) 단계에서 사용하는 운영 문서를 저장한다.

권장 항목:
- WBS 구조 정의 문서
- slice별 planned flow / routing graph
- 단계별 산출물/검증 체크리스트
- 병렬 작업 분기 및 병합 기준
- 에이전트 handoff packet / trace schema
- run ledger schema
- structured output enforcement
- templates / schemas / validators

작업 종료 후 장기 보존이 필요한 내용은 `docs/` 또는 `context/core/`로 승격한다.

현재 문서:
- `planned-flow.md`: packet 생성 전에 고정해야 하는 node / transition / loop 규칙
- `agent-handoff-schema.md`: 수동 오케스트레이션용 handoff packet / trace summary 표준
- `operator-decision-schema.md`: operator state transition을 남기는 decision event 표준
- `orchestration-flow.md`: WBS / packet / trace / operator decision / run ledger가 움직이는 전체 흐름
- `run-artifact-conventions.md`: run 내부 파일 구조, `seq`, lineage 규칙
- `run-ledger-schema.md`: 현재 상태 SoT로서의 run ledger 구조와 운영 규칙
- `structured-output-enforcement.md`: template vs schema enforcement 운영 기준
- `open-questions.md`: 2026-03-07 기준으로 합의된 운영 쟁점과 결정 요약
- `examples/README.md`: packet / trace / operator decision / run ledger 연결 예시

디렉터리:
- `flows/`: slice별 planned flow artifact와 버전 관리 위치
- `templates/`: 사람이 읽고 채우는 packet / trace / operator decision / current/snapshot ledger 템플릿
- `schemas/`: `codex exec --output-schema`와 validator가 사용하는 JSON Schema
- `examples/`: 실제 흐름을 설명하는 예시 artifact
