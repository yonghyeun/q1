# ADLC Agent Team Kit

This folder implements a Codex-centered Core 4 agent team for SaaS exploration/ideation.
Current operating baseline: **v0.1.0 (Natural-language Trace + Manual Span Logging)**.

## Structure
- `protocol/`: Team routing, gate, KPI, and policy rules.
- `interfaces/`: JSON Schemas for handoff and telemetry contracts.
- `ops/`: Online and weekly feedback loop playbooks.
- `ops/templates/`: Ready-to-use JSON/Markdown templates (task brief, trace, run-log, reports).
- `ops/v0.1.0-release.md`: 통합 운영 기준 변경 요약.
- `maintenance/`: Context maintainer sub-agent rules.
- `subagents/`: Task 전용 서브에이전트 템플릿과 운영 가이드.
- `runs/`: task-id 단위 실행 로그와 상태 추적 문서.
- `sot/`: `.codex` 런타임 생성 원천(매니페스트 + 에이전트 프롬프트).
- `scripts/`: 런타임 생성/동기화 검증 스크립트.

## Quick Start
1. Start from `protocol/PROTOCOL.md`.
2. Create `task-brief.json` (user intent + scope boundary).
3. Author `trace.md` (natural-language span map, gate rules, acceptance/evaluation criteria).
4. Execute spans manually and log each decision in `run-log.md`.
5. Summarize KPI and final decision in `run-report.json` + `status.md`.
6. Create `feedback-record.json` for failures/rework and feed weekly optimization.
7. After SoT changes, regenerate runtime via `scripts/generate_codex_runtime.py`.

## Operating Principles
- Keep context minimal and dynamic.
- Store only non-discoverable operating knowledge.
- Prefer structural fixes over prompt growth.
- Keep all ADLC stage approvals human-gated initially.
- Keep all **span-level** decisions human-logged in v0.1.0.
