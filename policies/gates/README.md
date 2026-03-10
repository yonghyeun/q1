# Gates

이 디렉토리는 저장소에서 사용하는 gate 문서를 원자적 단위로 보관한다.
원칙: gate 하나 = 문서 하나.

## Active Gates
- [issue-title.md](issue-title.md)
- [issue-body.md](issue-body.md)
- [pr-title.md](pr-title.md)
- [pr-body.md](pr-body.md)
- [pr-primary-issue-link.md](pr-primary-issue-link.md)
- [branch-name-pre-commit.md](branch-name-pre-commit.md)
- [branch-name-pre-push.md](branch-name-pre-push.md)
- [commit-message.md](commit-message.md)
- [worktree-name.md](worktree-name.md)
- [protected-branch-write.md](protected-branch-write.md)
- [detached-head-write.md](detached-head-write.md)
- [dirty-worktree-write.md](dirty-worktree-write.md)

## Planned Gates
- 없음.

## Gate Document Schema
- `Purpose`: gate가 막거나 확인하려는 대상.
- `Trigger`: gate가 실행되는 시점.
- `Status`: `active|planned|deprecated`.
- `SoT`: gate가 따르는 policy 또는 template.
- `Enforcer`: 실제 강제 수단. hook, script, CI job 중 하나 이상.
- `Dependencies`: gate 구현이 의존하는 파일.
- `Failure Mode`: 실패 시 차단인지 경고인지.
- `Tests`: 대응 테스트 파일 또는 수동 검증 경로.
