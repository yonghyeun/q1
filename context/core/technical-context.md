# Technical Context (Core)

## 기술 스택
- Frontend/App: Next.js
- Backend/DB: 초기 MVP는 DB 로직을 강제하지 않는다(검증 우선). 필요해지면 Supabase를 고려한다.

## 아키텍처 원칙
- 단일 앱으로 시작하되 확장 가능한 디렉터리 경계 유지
- 공통 규칙/정책은 루트에서 관리
