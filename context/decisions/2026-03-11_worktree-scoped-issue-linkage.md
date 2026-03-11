# DEC: 로컬 issue linkage는 branch naming이 아니라 worktree metadata로 기록

- Date: 2026-03-11
- Context: `task start`는 이미 `--issue`를 받아 branch/worktree 시작과 issue 상태 전이를 함께 처리하지만, 시작 이후 현재 worktree에서 연결된 issue를 즉시 확인하는 로컬 표준 경로는 없다. 이 공백을 branch 이름에 issue 번호를 넣어 메우는 방안도 검토했지만, 현재 branch 규칙은 변경 목적 식별에 집중하고 있고 issue는 remote backlog SoT로 분리돼 있다.
- Decision: branch naming 규칙은 `<type>/<slug>`로 유지하고, 현재 worktree와 연결된 issue 정보는 별도 local metadata 계층에 기록한다. 기록과 정리는 `task start`와 `task end` lifecycle에 붙인다.
- Alternatives: branch 이름에 issue 번호를 포함. repo 루트 공용 state file에 branch-issue 매핑 저장.
- Tradeoffs: local metadata 조회 커맨드와 cleanup 규율이 추가로 필요하다. 대신 branch rename 비용과 naming policy 충돌을 피하고, issue 번호 외 URL, title, 기록 시각 같은 부가 정보도 함께 유지할 수 있다.
- Revisit if: 하나의 branch에 여러 issue를 동시에 연결하는 운영으로 바뀌거나, worktree-scoped metadata가 checkout/cleanup 흐름에서 반복적으로 불안정하다고 확인될 때.
