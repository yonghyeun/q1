# Q1 Repository

이 저장소는 **SaaS 제품 개발을 위한 단일 에이전트 중심 모노레포 베이스라인**이다.

- 제품 방향: `Next.js` 단일 앱 중심(MVP)
- 운영 방향: 브랜치/PR 거버넌스 + 수동 병렬 단일 에이전트
- 목표: 낮은 인지 부하로 반복 가능한 개발 운영 체계 유지

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
├─ docs/                        # 설명 문서(아키텍처/제품)
├─ context/                     # 실행 입력 컨텍스트
│  ├─ core/                     # 장기 유지 핵심 컨텍스트
│  └─ tasks/                    # task-id 단위 작업 기록/결과
├─ policies/                    # 저장소 운영 정책(커밋/PR/품질/보관)
├─ skills/                      # 재사용 가능한 Codex 스킬
├─ scripts/                     # 리포 전역 공통 스크립트
├─ README.md
├─ AGENTS.md
└─ SOUL.md
```

## 브랜치 거버넌스

- 규칙 SoT: `policies/branch-policy.rules.json`
- 운영 정책: `policies/branch-pr-convention.md`
- 검증 엔진: `scripts/repo/branch_guard.py`
- PR-이슈 링크 검증: `scripts/repo/pr_issue_guard.py`
- 로컬 강제: `.githooks/pre-commit`, `.githooks/pre-push`
- CI 강제: `.github/workflows/branch-governance.yml`
- 시작 플로우:
  - `issue 생성 -> task/i<issue>-T-<task>-<slug> 브랜치 -> context/tasks/<task-id> 준비 -> PR(Closes #issue)`

## task 컨텍스트 최소 기준

`context/tasks/<task-id>/`에 아래 파일을 유지한다.

1. `context.md` - 작업 배경/제약/결정 근거
2. `result.md` - 실행 결과/검증 요약/후속 조치

## 확장 원칙

- 멀티 에이전트 체계는 기본값이 아니다.
- 필요성이 확인되면 별도 설계 문서와 승인 절차를 거쳐 도입한다.
