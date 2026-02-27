# Task 전용 서브에이전트 운영 가이드

## 목적
- task 목적에 맞는 전용 서브에이전트를 템플릿 복제 방식으로 빠르게 생성한다.

## 생성 절차
1. 새 작업 ID를 확정한다. 예: `T-0002`
2. `_template/prompt.md`를 복제해 `T-0002-<purpose>.md`를 만든다.
3. 프롬프트에 task 범위/수용 기준/리스크 초점을 채운다.
4. `_template/config-snippet.toml`을 참고해 `agent-team/sot/codex-runtime.manifest.toml`에 agent 블록을 추가한다.
5. `python3 agent-team/scripts/generate_codex_runtime.py`를 실행한다.
6. `agent-team/runs/<task-id>/status.md`에 해당 서브에이전트 사용 사실을 기록한다.

## 네이밍 규칙
- 파일명: `T-000N-<purpose>.md`
- agent 키: `task_t_000n_<purpose>`
- `<purpose>`는 소문자와 하이픈만 사용한다.

## 유지보수
- 작업 종료 후 재사용성이 없으면 agent 블록과 프롬프트 파일을 아카이브 또는 제거한다.
- 변경 후 `python3 agent-team/scripts/verify_codex_runtime_sync.py`를 통과해야 한다.
