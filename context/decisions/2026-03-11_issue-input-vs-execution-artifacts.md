# DEC: Issue는 what why 입력을 담고 실행 how는 별도 artifact로 분리

- Date: 2026-03-11
- Context: issue에 실행 계획과 해결 과정을 함께 넣으면 원문 입력과 실행 로그가 섞여 backlog readability가 빠르게 떨어진다.
- Decision: issue는 문제/요청의 `what`, `why`, 제약, 쟁점을 담고, 실제 실행 `how`는 branch, PR, WBS 등 별도 artifact로 분리한다. issue에는 얇은 종료 조건으로 `Done Signal`만 둔다.
- Alternatives: issue 안에 acceptance criteria와 실행 checklist를 상세히 유지. decision 문서에 실행 선택까지 모두 기록.
- Tradeoffs: issue만 보고 바로 구현에 들어가기엔 정보가 덜 구체적일 수 있다. 대신 backlog 입력 문서와 실행 산출물의 역할 경계가 선명해진다.
- Revisit if: 후속 실행 artifact가 일관되게 생성되지 않아 issue 하나만으로도 충분한 운영이 더 효율적이라고 판단될 때.
