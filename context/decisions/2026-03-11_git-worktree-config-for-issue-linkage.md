# DEC: issue linkage backend는 git config --worktree 를 사용

- Date: 2026-03-11
- Context: 로컬 issue linkage를 worktree metadata로 기록하기로 결정한 뒤, 실제 backend로 `git config --worktree`, repo 공용 state file, worktree 내부 전용 metadata file 중 무엇을 사용할지 확정할 필요가 생겼다. 현재 저장소는 linked worktree를 기본 운영 모델로 사용하고 있어 metadata가 working tree 파일로 노출되지 않고 worktree lifecycle과 함께 정리되는 성질이 중요하다.
- Decision: issue linkage backend는 `git config --worktree` 로 고정한다. 공통 repo config에는 `extensions.worktreeConfig=true` 를 설정하고, issue linkage는 `q1.issue.*` namespace 아래 key로 기록한다.
- Alternatives: repo 루트 공용 state file 사용. worktree 루트 내부 숨김 metadata file 사용. `.git/worktrees/<name>/` 아래 custom file 직접 관리.
- Tradeoffs: repo local config에 `extensions.worktreeConfig` 전환이 필요하고, 최소 Git 버전 전제가 생긴다. 대신 metadata가 untracked 파일로 노출되지 않고, worktree별 admin dir에 자연스럽게 격리되며, worktree 제거 시 cleanup 모델이 단순해진다.
- Revisit if: 지원해야 하는 Git 환경에서 `extensions.worktreeConfig` 호환성 문제가 반복되거나, worktree-scoped config가 예상보다 조회/정리 자동화에 불편하다고 확인될 때.
