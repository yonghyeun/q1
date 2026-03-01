# Task Contexts

태스크별 임시 컨텍스트를 저장한다.

권장 형식:
- `T-0001-context.md`
- 태스크 종료 후 핵심 내용만 `context/core` 또는 `docs`로 승격

## 역할 경계 (`agent-team/runs`와 구분)
- `context/tasks/`는 **실행 입력값**(배경, 가설, 참고자료, 제약)을 담는다.
- `agent-team/runs/`는 **실행 증적**(task-brief, trace, run-log, run-report, status)을 담는다.

즉, 같은 task를 다루더라도 목적이 다르다.
- 입력/준비: `context/tasks/T-000N-*`
- 실행/판정/감사 추적: `agent-team/runs/T-000N/`
