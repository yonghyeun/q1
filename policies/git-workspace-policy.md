# Git Workspace Policy

## Purpose
- 이 문서는 저장소에서 Git branch, worktree, write action을 어떻게 운영할지 정의.
- naming rule이 아니라 작업 행동 규칙 담당.

## Core Rules
- 모든 쓰기 작업은 현재 worktree에 checkout된 branch를 기준으로 수행.
- branch, upstream, worktree 상태는 추측하지 않고 실제 상태를 확인.
- `main` branch 직접 커밋 금지.
- 사용자 승인 없이 destructive git 명령 수행 금지.
- 사용자 변경사항이나 더티 워크트리를 임의로 되돌리거나 삭제하지 않음.

## Pre-Write Check
- Git 쓰기 작업 전 아래 항목 확인.
- 현재 branch.
- upstream 존재 여부.
- 현재 worktree 경로.
- working tree status.
- 현재 작업이 기존 변경사항과 충돌하는지 여부.

## Detached HEAD
- detached HEAD 상태에서는 커밋, PR 생성, branch 기반 작업 진행 금지.
- 필요한 경우 먼저 상태 보고 후 다음 작업 경로 확인.

## Dirty Worktree
- 더티 워크트리 발견 시 임의 정리 금지.
- 현재 작업과 충돌 가능성 먼저 확인.
- 충돌 소지 존재 시 사용자에게 보고 후 진행.

## Branch Switching
- 사용자 지시 없이 `git switch`, `git checkout`, `git rebase`, `git reset --hard` 수행 금지.
- branch 전환 필요 시 이유와 영향을 먼저 설명.

## Worktree Usage
- worktree는 branch와 연결된 실행 공간으로 사용.
- 다른 branch 작업은 가능하면 별도 worktree에서 수행.
- 하나의 worktree 안에서 여러 목적의 작업을 섞지 않음.

## Issue Linkage
- 현재 worktree와 연결된 issue 정보는 worktree metadata로 관리.
- 기록은 `task start --issue <number>` lifecycle에서 수행.
- 조회 표준 경로는 `./scripts/repo/current_issue.sh`.
- 종료 시 정리는 `task end` lifecycle에서 수행.
- live 상태 확인이 필요하면 `./scripts/repo/current_issue.sh --live` 사용.

## PR Linkage
- 현재 worktree와 연결된 PR 정보는 worktree metadata로 관리.
- 기록은 `pr_create` 성공 직후 수행.
- 조회 표준 경로는 `./scripts/repo/current_pr.sh`.
- 종료 시 정리는 `task end` lifecycle에서 수행.
- live 상태 확인이 필요하면 `./scripts/repo/current_pr.sh --live` 사용.

## Commit Readiness
- 커밋 전 변경 범위 확인.
- 관련 없는 변경 혼입 여부 확인.
- 검증 가능한 변경이면 테스트, 린트, 점검 절차 우선 수행.

## Related Documents
- branch naming 규칙: [branch-naming.md](branch-naming.md)
- worktree naming 규칙: [worktree-naming.md](worktree-naming.md)
- commit 규칙: [commit-convention.md](commit-convention.md)
