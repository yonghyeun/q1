# Feedback Governance Map

## 목적
- 실패 유형을 문서/설정 업데이트 대상으로 일관되게 매핑한다.
- 프롬프트 과증설을 막고 process/codebase 우선 개선 원칙을 강제한다.

## 실패 유형별 우선 업데이트 대상
- `unclear_scope`
  - 1순위: `task-brief.json`, `trace.md`
  - 2순위: `agent-team/ops/online-loop.md`
- `bad_handoff`
  - 1순위: `trace.md`의 span 입력/출력/지시 구간, `handoff.json`
  - 2순위: `agent-team/AGENTS.md`(라우팅 규칙)
- `weak_acceptance_criteria`
  - 1순위: `trace.md` acceptance 기준, `run-log.md` 판정 근거
  - 2순위: `builder/reviewer` 지시문
- `tool_misuse`
  - 1순위: process 문서(`online-loop.md`, `commit-policy.md`), `run-log.md`
  - 2순위: role instruction
- `missing_context`
  - 1순위: `trace.md` context refs 점검, 하위 AGENTS 분기 규칙 점검
  - 2순위: task 전용 서브에이전트 생성
- `quality_gap`, `risk_missed`
  - 1순위: reviewer 지시문, `trace.md` acceptance checks, `run-log.md`
  - 2순위: 주간 실험 안건 등록

## 변경 승인 규칙
1. 동일 실패 2회 누적 전에는 임시 수정으로 처리한다.
2. 2회 누적 시 `FeedbackRecord.change_target`을 명시한다.
3. 3회 누적 시 주간 배치 실험으로 승격하고 승격 결과만 영구 반영한다.

## change_target 사용 기준
- `process`: 운영 절차/체크리스트 변경
- `codebase`: 레포 구조/검증 자동화/테스트 보강
- `prompt`: 구조 개선 후에도 남는 판단 오류 보정
- `agents_doc`: AGENTS 계층 규칙 조정
- `config`: `agent-team/sot/codex-runtime.manifest.toml` 조정 후 런타임 재생성
