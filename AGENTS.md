# Layer 1 Protocol (Repository Scope)

## 목적
- 이 저장소의 Codex 운용은 ADLC Core 4 체계를 따른다.
- 이 파일은 라우팅/승인/KPI 같은 비발견 운영 규칙만 제공한다.

## 라우팅 규칙
- 기본 오케스트레이션 프로필: `adlc_leader`
- 문제정의/가설 정제: `planner_pm`
- 승인된 산출물 생성: `builder`
- 수용 기준 검증: `reviewer`

## 승인 게이트
- 초기 운영 정책에서는 ADLC 전 단계(Explore/Design/Execute/Improve)에 사람 승인을 요구한다.
- 자동 승격/생략은 주간 배치 검토에서 승인된 경우에만 허용한다.

## 컨텍스트 정책
- 코드/문서에서 바로 발견 가능한 정보는 AGENTS에 기록하지 않는다.
- 공통 규칙은 루트 AGENTS, 작업별 규칙은 하위 AGENTS 또는 task 전용 서브에이전트에 둔다.
- 작업 중 필요한 문서만 선택적으로 로드한다.
- `.codex/` 실행 파일은 `agent-team/` SoT에서 생성된 결과물로 취급한다.

## KPI
- Accuracy(승인 통과율), Rework Rate(재작업률), Token Cost(작업당 비용)를 기본 추적 지표로 사용한다.
