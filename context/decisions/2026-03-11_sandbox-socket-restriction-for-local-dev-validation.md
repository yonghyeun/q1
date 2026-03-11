# DEC: sandbox socket restriction for local dev validation

- Date: 2026-03-11
- Context: `apps/web`의 dev server를 확인할 때 일반 sandbox 세션에서는 `curl http://127.0.0.1:3000` 연결이 실패했고, `python3 -m http.server`도 `PermissionError: [Errno 1] Operation not permitted`로 바인딩 실패했다. 반면 권한 상승 세션에서는 로컬 HTTP 서버 기동과 `curl -I http://127.0.0.1:<port>` 응답 확인이 가능했다.
- Decision: 이 문제는 단순한 namespace 분리로 설명하지 않고, Codex sandbox의 socket 생성/localhost 접속 제한으로 기록한다. 로컬 dev server 실행과 HTTP 확인은 당분간 권한 상승 세션에서만 검증한다.
- Alternatives: localhost 연결 실패를 네트워크 namespace 분리 문제로 기록. 또는 재현 없이 일반적인 sandbox 제약으로만 추상화.
- Tradeoffs: 원인은 더 정확해지지만, 향후 sandbox 구현이 바뀌면 설명을 다시 갱신해야 한다. 또한 로컬 개발 서버 검증이 기본 경로가 아니라 예외 경로로 남는다.
- Revisit if: sandbox에서 socket 생성 또는 localhost 접속이 허용되거나, Codex 실행 컨텍스트 제약을 문서화한 공식 운영 가이드가 추가되면 재검토.
