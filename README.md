# Q1 Repository

이 저장소는 **SaaS 제품 개발을 위한 단일 에이전트 중심 모노레포 베이스라인**이다.

- 제품 방향: `Next.js` 단일 앱 중심(MVP)
- 운영 방향: Git 정책 기반 수동 병렬 단일 에이전트
- 목표: 낮은 인지 부하로 반복 가능한 개발 운영 체계 유지
- interface contracts(SoT, 임시): `docs/product/contracts/README.md`

## 아키텍처 원칙

1. **정석 분리**: 코드/문서/컨텍스트/정책을 분리해 책임 경계를 유지한다.
2. **가벼운 거버넌스**: 필수 게이트만 유지하고 불필요한 운영 복잡도는 제거한다.
3. **로컬 우선 스크립트**: 스크립트는 사용처 인근에 두고, 공통만 루트에 둔다.
4. **점진 자동화**: 불편이 반복되는 지점만 자동화한다.

## 폴더 구조

```txt
q1/
├─ .github/workflows/           # CI 게이트(브랜치 정책 등)
├─ .githooks/                   # commit-msg, pre-commit, pre-push 훅 규칙
├─ apps/                        # 제품 실행 코드 영역
│  └─ web/                      # Next.js MVP 앱
├─ docs/                        # 설명 문서(아키텍처/제품, contracts 포함)
├─ context/                     # 판단 입력 컨텍스트(배경/목표/가설/WBS)
│  ├─ core/                     # 장기 유지 핵심 컨텍스트
│  └─ wbs/                      # WBS 단계 운영 문서
├─ policies/                    # 저장소 운영 규칙(권한/절차/컨벤션/검증)
├─ .codex/skills/               # 저장소 로컬 Codex 스킬
├─ scripts/                     # 리포 전역 공통 스크립트
├─ README.md
├─ AGENTS.md
└─ SOUL.md
```

## Git 운영 정책

- workspace 규칙: `policies/git-workspace-policy.md`
- 브랜치 이름 규칙: `policies/branch-naming.md`
- 워크트리 이름 규칙: `policies/worktree-naming.md`
- 운영 정책: `policies/branch-pr-convention.md`
- 커밋 규칙: `policies/commit-convention.md`
- 검증 엔진: `scripts/repo/branch_guard.py`
- PR close-link 검증: `scripts/repo/pr_issue_guard.py`
- 로컬 강제: `.githooks/pre-commit`, `.githooks/pre-push`
- 시작 플로우:
  - `issue 생성 -> <scope>/<slug> 브랜치 -> PR(Closes #issue)`

## Agent 문서 분류

- `developer_instructions`: Agent의 공통 말투와 판단 태도
- `AGENTS.md`: 저장소 공통 권한 경계와 라우팅
- `context/`: Agent 판단 입력
- `policies/`: Agent 행동 규칙과 검증 기준
- `context/decisions/`: 문서 구조와 운영 선택의 판단 기록

## 확장 원칙

- 멀티 에이전트 체계는 기본값이 아니다.
- 필요성이 확인되면 별도 설계 문서와 승인 절차를 거쳐 도입한다.
