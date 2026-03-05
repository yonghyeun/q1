# DEC: Why we need "contracts" (interface SoT) for parallel agent dev

- Date: 2026-03-04
- Context: 이 프로젝트는 WBS를 task 단위로 쪼개고(병렬), task마다 에이전트를 붙여 구현한 뒤 AC를 하네스로 검증하는 방식을 목표로 한다. 병렬 개발에서는 작은 용어/형식 불일치가 통합(merge) 시 큰 재작업으로 커진다. `glossary.md`는 "개념의 이름(유비쿼터스 언어)"을 정렬해주지만, 타입/응답형식/이벤트 스키마/저장 포맷 같은 "접점(interface)"까지 강제해주지는 못한다. 또한 YouTube Data API는 Next.js 서버 라우트로 프록시하기로 했고, 이때의 요청/응답 형식도 프론트-서버 간 계약이 된다.
- Decision: 병렬 task 개발의 통합 비용을 낮추기 위해, "contracts"를 cross-task 접점의 Source of Truth(SoT)로 둔다.
  - contracts에 포함되는 것(예): Domain 타입(`ChannelSource`, `Video`, `Note`, `Marker`), API request/response(`/api/youtube/*`), Analytics 이벤트 스키마(`open_method`, `feed_filter` 등), LocalStorage 저장 스키마/키 네이밍.
  - contracts에 포함하지 않는 것(예): 화면 UI 디테일, 개별 컴포넌트 내부 구현, 임시 실험 코드.
  - 지금 단계에서는 코드(타입)로 먼저 고정하기보다 문서 기반으로 얇게 시작하고, 프로젝트 구성이 잡히면 코드 계약(타입/런타임 validation)으로 점진 승격한다.
- Alternatives: contracts 없이 `mvp-spec`/glossary만으로 진행한다. task마다 개별적으로 인터페이스를 정하고 맞춘다. 처음부터 모든 계약을 코드로만 관리한다.
- Tradeoffs: 계약을 추가로 관리해야 하므로 약간의 문서/변경 비용이 생긴다. 문서 contracts는 drift 위험이 있다(그래서 이후 코드 계약으로 승격). 대신 병렬 작업에서의 충돌/불일치/재작업을 줄이고, 하네스(AC 검증)를 결정적으로 만들 수 있다.
- Revisit if: 병렬 개발을 중단하고 단일 에이전트/순차 개발로 전환하는 경우. 코드 계약(타입/validation)으로 완전히 대체되어 문서 contracts가 중복이 되는 경우.

