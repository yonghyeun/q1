# Repository Scripts

루트 `scripts/`는 **리포 전역에서 재사용되는 스크립트만** 둔다.

## 규칙
- 도메인 전용 스크립트는 해당 도메인 내부에 둔다.
  - 예: `agent-team/scripts/`, `apps/web/scripts/`
- 2개 이상 도메인에서 공통 사용될 때만 루트로 승격한다.

## 구조
- `repo/`: 저장소 전체 오케스트레이션
- `lib/`: 공통 유틸 함수
