# Context

에이전트 실행 시 직접 로드할 운영 컨텍스트를 보관한다.
이 디렉토리는 규칙 저장소가 아니라 판단 입력 저장소다.

- `core/`: 장기적으로 유지되는 핵심 컨텍스트
- `analytics/`: 계측(이벤트/지표) 정의
- `experiments/`: 배포 기반 가설 검증 로그(실험 단위)
- `decisions/`: 의사결정 로그
- `wbs/`: WBS 단계 운영 문서

`docs/`와 달리, 실행 입력값으로 사용되므로 변경 시 영향도를 검토한다.
금지, 승인, naming, convention, workflow 같은 운영 규칙은 `policies/`에 둔다.

정책 문서 라우팅은 루트 `AGENTS.md`의 boundary 섹션에서 직접 관리한다.
