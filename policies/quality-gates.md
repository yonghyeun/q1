# Quality Gates

## 기본 원칙
- ADLC(Explore/Design/Execute/Improve) 전 단계는 초기 정책상 수동 승인한다.

## 코드 품질 게이트(점진 도입)
1. Stage 1: lint / typecheck / build 권고
2. Stage 2: CI warning
3. Stage 3: CI blocking

## 운영 품질 게이트
- 필수 운영 산출물 누락 시 다음 단계 진행 금지
- reviewer 검토가 필요한 고위험 변경은 별도 승인 기록 필요
