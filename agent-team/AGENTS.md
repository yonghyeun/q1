# Layer 2 Persona / Skill Policy

## 목적
- `agent-team/` 범위에서 페르소나 선택, task 전용 서브에이전트 생성, 컨텍스트 로딩 기준을 정의한다.

## 페르소나 선택 규칙
- 모호한 요청/우선순위/승인 흐름 결정: `adlc_leader`
- 문제정의/검증 설계/범위 조정: `planner_pm`
- 산출물 작성/실행: `builder`
- 품질 판정/리스크 검토: `reviewer`

## Task 전용 서브에이전트 규칙
- 생성 조건:
  - 동일 목적의 반복 작업이 2회 이상 발생
  - 공통 페르소나만으로 품질 편차가 큰 경우
- 생성 방법:
  1. `agent-team/subagents/_template/prompt.md` 복제
  2. `agent-team/subagents/T-000N-<purpose>.md` 작성
  3. `agent-team/sot/codex-runtime.manifest.toml`에 agent 블록 추가
  4. `python3 agent-team/scripts/generate_codex_runtime.py` 실행
- 폐기 조건:
  - 2주 이상 미사용 또는 상위 페르소나로 흡수 가능한 경우

## 동적 로딩 규칙
- task에 직접 필요한 persona 문서와 스키마만 로드한다.
- 실패 회고 시 최근 관련 run(기본 3개)만 참조한다.
- 브랜치/PR 정책 질의는 `context/core/policy-routing.md`에 정의된 순서로 최소 문서만 로드한다.
