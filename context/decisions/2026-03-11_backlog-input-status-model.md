# DEC: Backlog input issue의 status는 inbox ready active blocked cancelled로 제한

- Date: 2026-03-11
- Context: issue를 atomic execution task SoT가 아니라 remote backlog input으로 쓰기로 했기 때문에, execution lifecycle 전체를 반영하는 세밀한 status 집합은 오히려 경계를 흐릴 수 있다.
- Decision: issue status는 `inbox`, `ready`, `active`, `blocked`, `cancelled` 다섯 값으로 제한한다. 완료는 `status:done` 대신 issue close로 표현한다.
- Alternatives: `normalized`, `review`, `done`을 포함한 상세 execution status 사용. 상태 label 없이 close/open만 사용.
- Tradeoffs: issue 단위 진행 추적은 덜 세밀하다. 대신 backlog 입력 문서와 실행 artifact의 역할 경계가 유지된다.
- Revisit if: issue가 실제 실행 SoT로 승격되거나, backlog triage에서 현재 status 집합으로 반복적인 정보 부족이 발생할 때.
