# Contracts (Interfaces SoT)

이 폴더는 **WBS 작성/병렬 개발**을 위해 필요한 “접점(interface)”을 타입(contracts)으로 고정해두는 임시 위치다.

- 용어(도메인 언어) SoT: `docs/product/glossary.md`
- 왜 필요한가(결정 로그): `context/decisions/2026-03-04_contracts-why-needed.md`
- 이벤트 SoT: `context/analytics/events.md`
- MVP 경험/플로우 SoT: `docs/product/mvp-spec.md`

> 주의: 원래 contracts는 실제 프로젝트 코드베이스 내부에 두는 것이 맞다.
> 현재는 앱 코드가 없으므로 문서 디렉터리 아래에 임시로 보관한다.

## 포함 범위

- **Domain**: `Source`, `ChannelSource`, `Video`, `Note`, `Marker` 등
- **API**: `/api/youtube/*` request/response shape (프록시 기준)
- **Analytics**: 이벤트 이름/props 스키마
- **Storage**: LocalStorage 키/저장 스키마(버전 포함)

## 제외 범위

- UI 텍스트/레이아웃/컴포넌트 내부 구현 디테일
- 실험용 임시 데이터 구조(단발성)

## 파일 구성

- `primitives.ts`: 공통 원시 타입(시간/ID/URL 등) + TTL 캐시 래퍼
- `domain.ts`: 제품 도메인 모델(Glossary와 정렬)
- `analytics.ts`: 이벤트 계약(`context/analytics/events.md`와 정렬)
- `storage.ts`: LocalStorage 키/스키마(YouTube API Data는 TTL 권장)
- `api-youtube.ts`: YouTube 프록시 API 계약
- `index.ts`: 배럴 export

## 변경 원칙(간단)

- Glossary의 용어를 우선한다(이름 충돌 시 glossary를 먼저 수정).
- 이벤트/스토리지 키는 바꾸기 어렵다(바꿀 땐 버전/마이그레이션까지 같이 설계).
- YouTube API Data(타이틀/썸네일 등)는 장기 저장 대신 **TTL 캐시**를 기본으로 한다.

