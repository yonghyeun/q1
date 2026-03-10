# Operating Context (Core)

## 운영 목표
- 단일 에이전트 워크플로우를 안정적으로 유지한다.
- 필요 시 수동 병렬 실행을 통해 처리량을 보완한다.

## 정책 포인터

운영 "규칙/게이트"의 정본(single source of truth)은 `policies/`에 둔다.

- 커밋 규칙/훅: `policies/commit-convention.md`, `.githooks/README.md`
- Git workspace 규칙: `policies/git-workspace-policy.md`
- 브랜치/워크트리 이름 규칙: `policies/branch-naming.md`, `policies/worktree-naming.md`
- 품질 게이트: `policies/quality-gates.md`
- 보안/시크릿: `policies/security-secrets.md`
- 보관 정책: `policies/retention-policy.md`

## 운영 메모

- 반복 실패는 프롬프트보다 프로세스/구조 개선을 우선한다.
