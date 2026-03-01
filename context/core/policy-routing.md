# Policy Routing Context (Core)

## 목적
- 에이전트가 작업 의도별로 필요한 정책 문서만 선택 로드하도록 라우팅 기준을 제공한다.
- AGENTS에 정책 본문을 중복 기록하지 않고 토큰 사용량을 줄인다.

## 라우팅 규칙
### `git_branching` 또는 브랜치/PR/훅 관련 요청
1. `policies/branch-policy.rules.json` (기계 검증 규칙)
2. `policies/branch-pr-convention.md` (운영 규칙/예외)
3. `agent-team/integration/pr-gate-policy.md` (승인 게이트)

### `commit_message` 관련 요청
1. `policies/commit-convention.md`
2. `.githooks/README.md`

### `adlc_gate` 관련 요청
1. `agent-team/protocol/PROTOCOL.md`
2. `agent-team/integration/pr-gate-policy.md`
3. `agent-team/integration/required-artifacts.md`

## 운영 규칙
- 에이전트는 기본적으로 라우팅된 문서만 우선 로드한다.
- 규칙 해석이 충돌할 때는 `policies/`의 기계 규칙 파일을 우선한다.
