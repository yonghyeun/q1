# Project Agent Router

## Purpose
- 이 문서는 이 저장소의 공통 Agent 운영 규칙과 참조 경로를 정의하는 라우터다.
- 세부 정책 본문은 전용 문서에 두고, 여기에는 최소 핵심 규칙과 boundary만 유지한다.

## Scope
- 이 문서는 저장소 루트 기준 공통 규칙에 적용된다.
- 하위 디렉토리에 더 구체적인 `AGENTS.md`가 있으면 해당 규칙을 추가 적용한다.

## Core Non-Negotiables
- 이 저장소의 Codex 운용은 단일 에이전트 기본 운영을 따른다.
- 병렬 처리가 필요하면 사용자가 명시적으로 요청한 범위에서만 수동 병렬로 확장한다.
- `main` branch에 직접 커밋하지 않는다.
- 사용자 승인 없이 destructive git 명령을 수행하지 않는다.
- 사용자 변경사항이나 더티 워크트리를 임의로 되돌리거나 삭제하지 않는다.
- 코드나 문서에서 바로 확인 가능한 내용을 `AGENTS.md`에 중복 기록하지 않는다.

## Git And Workspace Boundary
- 모든 쓰기 작업은 현재 worktree에 checkout된 branch를 기준으로 수행한다.
- `main` branch 직접 커밋 금지.
- 사용자 승인 없이 destructive git 명령 수행 금지.
- 사용자 변경사항이나 더티 워크트리를 임의로 되돌리거나 삭제하지 않는다.
- issue 생성, PR 생성, PR merge, worktree 생성은 저장소 wrapper 스크립트를 우선 사용한다.
- 같은 기능의 raw `gh` 또는 raw `git worktree` 명령보다 wrapper 경로를 우선한다.
- 브랜치, worktree, 커밋, PR, 훅 관련 세부 규칙은 필요한 문서만 선택 로드한다.
- 관련 참조:
  [policies/git-workspace-policy.md](policies/git-workspace-policy.md)
  [policies/branch-naming.md](policies/branch-naming.md)
  [policies/worktree-naming.md](policies/worktree-naming.md)
  [policies/commit-convention.md](policies/commit-convention.md)
  [policies/gates/README.md](policies/gates/README.md)

## Execution Boundary
- 저장소에 제공된 스크립트와 정책 문서를 우선 사용한다.
- 검증 가능한 변경은 테스트, 린트, 검증 스크립트를 우선 실행한다.
- gate 실패 시 우회하지 않는다.
- gate 실패 메시지의 `다음 행동:`을 따라 입력이나 상태를 수정한 뒤 동일 경로로 재시도한다.
- 세부 절차와 예시는 전용 문서에서 관리하고, 이 문서에는 boundary만 유지한다.

## Approval Boundary
- 고위험 변경은 사람 승인 후 진행한다.
- 브랜치 정책, git hook, CI, 배포 경로 변경은 승인 후 진행한다.
- 승인 생략이나 자동 승격은 별도 합의가 있을 때만 허용한다.

## Local Extension Rule
- 서브도메인 전용 규칙은 해당 디렉토리의 `AGENTS.md`에만 정의한다.
- 루트 `AGENTS.md`에는 프로젝트 공통 규칙과 boundary만 유지한다.
