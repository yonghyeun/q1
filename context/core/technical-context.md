# Technical Context (Core)

## 기술 스택
- Frontend/App: Next.js (`apps/web`)
- Video Player: YouTube embed(IFrame) + Player API 기반 제어
- Persistence: 초기 MVP는 브라우저 로컬 저장소(LocalStorage)만 사용한다(백엔드/DB 없음).
- Auth: 초기 MVP는 회원가입/로그인 없이 사용한다.
- Backend/DB: 필요해지면 Supabase를 고려한다.

## 아키텍처 원칙
- 단일 앱으로 시작하되 확장 가능한 디렉터리 경계 유지
- 공통 규칙/정책은 루트에서 관리
