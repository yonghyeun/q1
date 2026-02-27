# ADLC Agent Team Kit

This folder implements a Codex-centered Core 4 agent team for SaaS exploration/ideation.

## Structure
- `protocol/`: Team routing, gate, KPI, and policy rules.
- `interfaces/`: JSON Schemas for handoff and telemetry contracts.
- `ops/`: Online and weekly feedback loop playbooks.
- `ops/templates/`: Ready-to-use JSON examples that match interface schemas.
- `maintenance/`: Context maintainer sub-agent rules.
- `subagents/`: Task 전용 서브에이전트 템플릿과 운영 가이드.
- `runs/`: task-id 단위 실행 로그와 상태 추적 문서.
- `sot/`: `.codex` 런타임 생성 원천(매니페스트 + 에이전트 프롬프트).
- `scripts/`: 런타임 생성/동기화 검증 스크립트.

## Quick Start
1. Start from `protocol/PROTOCOL.md`.
2. Load only needed persona file(s) for the current task.
3. Emit artifacts that validate against schemas in `interfaces/`.
4. Log every run with `RunReport`.
5. Create `FeedbackRecord` for failures and feed into weekly optimization.
6. After SoT changes, regenerate runtime via `scripts/generate_codex_runtime.py`.

## Operating Principles
- Keep context minimal and dynamic.
- Store only non-discoverable operating knowledge.
- Prefer structural fixes over prompt growth.
- Keep all ADLC stage approvals human-gated initially.
