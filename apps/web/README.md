# Web App (Next.js)

이 디렉터리는 SaaS MVP용 Next.js 앱을 위한 공간이다.

## 현재 상태
- 아키텍처 초기 설계 단계
- DB 로직은 MVP 초기 범위에서 제외
- 추후 Supabase 연동 여부를 단계적으로 결정

## 원칙
- 앱 내부 스크립트가 필요하면 `apps/web/scripts/`에 둔다.
- 전역 공통 스크립트로 승격할 경우 루트 `scripts/`로 이동한다.
