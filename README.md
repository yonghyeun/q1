# Q1 Repository

이 저장소는 **SaaS 제품 개발**과 **ADLC 기반 에이전트 팀 오케스트레이션**을 강하게 결합해 운영하기 위한 모노레포 베이스라인이다.

- 제품 방향: `Next.js` 단일 앱 중심(MVP)
- 운영 방향: ADLC(Explore/Design/Execute/Improve) 전 단계 수동 승인
- 목표: 반복 가능한 에이전틱 개발 운영 체계 구축 → 점진 자동화

## 아키텍처 원칙

1. **정석 분리**: 코드/문서/컨텍스트/정책을 분리해 책임 경계를 명확히 유지한다.
2. **강결합 운영**: 에이전트 산출물은 제품 개발의 참고 자료가 아니라 필수 운영 증적이다.
3. **로컬 우선 스크립트**: 스크립트는 사용처 인근에 두고, 공통 스크립트만 루트로 승격한다.
4. **점진 자동화**: 초기에는 사람 승인 중심으로 운영하고, 반복 불편을 근거로 자동화 범위를 확장한다.

## 폴더 구조

```txt
q1/
├─ .codex/                      # Codex 런타임 산출물(에이전트 프롬프트/설정)
├─ .githooks/                   # commit-msg, pre-commit 등 Git 훅 규칙
├─ agent-team/                  # ADLC 오케스트레이션 SoT/운영 자산
│  ├─ protocol/                 # 팀 운영 규약(게이트, KPI, 라우팅)
│  ├─ interfaces/               # handoff/run-report 등 스키마
│  ├─ ops/                      # 운영 루프/템플릿/릴리즈 기준
│  ├─ runs/                     # task-id 실행 기록 저장소
│  ├─ scripts/                  # agent-team 전용 스크립트
│  ├─ sot/                      # .codex 생성 원천(SoT)
│  ├─ subagents/                # task 전용 서브에이전트 템플릿
│  ├─ maintenance/              # 컨텍스트 유지보수 가이드
│  ├─ examples/                 # 실행 예시 문서
│  └─ integration/              # 제품개발 강결합 정책/자동화 로드맵
├─ apps/                        # 제품 실행 코드 영역
│  └─ web/                      # Next.js MVP 앱
├─ docs/                        # 설명 문서(아키텍처/제품)
│  ├─ architecture/             # 구조/경계/설계 의도
│  └─ product/                  # 요구사항/시나리오/범위
├─ context/                     # 에이전트 실행 입력 컨텍스트
│  ├─ core/                     # 장기 유지 핵심 컨텍스트
│  └─ tasks/                    # task 단위 임시 컨텍스트
├─ policies/                    # 저장소 운영 정책(커밋/PR/품질/보안/보관)
├─ scripts/                     # 리포 전역 공통 스크립트
│  ├─ lib/                      # 공통 유틸 함수
│  └─ repo/                     # 저장소 오케스트레이션 실행 스크립트
├─ README.md                    # 저장소 아키텍처/운영 개요
├─ AGENTS.md                    # 루트 레벨 Codex 운영 규칙
└─ soul.md                      # 팀 운영 철학/불변 원칙
```

### 폴더별 설명(요약)

- `.codex/`: `agent-team/sot`를 기반으로 생성되는 Codex 실행 자산이다.
- `.githooks/`: 커밋 메시지/사전검증 같은 Git 훅 정책을 강제한다.
- `agent-team/`: ADLC 에이전트 팀 운영의 중심 폴더다.
- `apps/`: 실제 제품 코드가 위치하는 영역이다.
- `docs/`: 사람 중심 설명 문서(공유/의사결정 기록)의 기본 위치다.
- `context/`: 에이전트가 실행 시 직접 읽는 입력 컨텍스트 저장소다.
- `policies/`: 커밋/PR/품질/보안/보관 정책 등 규칙 문서의 단일 출처다.
- `scripts/`: 여러 영역에서 공통 사용되는 리포 전역 스크립트 저장소다.

## context, policies를 docs와 분리한 이유

- `docs/`는 설명/공유 중심 산출물이다.
- `context/`, `policies/`는 에이전트 실행 및 게이트 판단에 직접 사용되는 운영 입력값이다.
- 따라서 변경 통제, 자동화 연결, 책임 소유권을 명확히 하기 위해 별도 최상위 폴더로 유지한다.

## 에이전트 강결합 운영 기준(초기)

PR/머지 대상 작업은 아래 증적을 기본 단위로 관리한다.

1. `task-brief.json`
2. `trace.md`
3. `run-log.md`
4. `run-report.json`
5. 필요 시 `feedback-record.json`

상세 기준은 `agent-team/integration/required-artifacts.md`와 `agent-team/integration/pr-gate-policy.md`를 따른다.

## 확장 계획

- `docs/adr`, `docs/generated`는 현재 보류 상태이며, 에이전트 팀 운영 개선 단계에서 채택 여부를 재결정한다.
- MVP 이후 Next.js 앱이 안정화되면 API/Worker/Shared 패키지 분리 여부를 ADR로 기록한다.
