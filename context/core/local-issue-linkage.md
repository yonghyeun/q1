# Local Issue Linkage

## 목표
- 현재 branch/worktree에서 연결된 issue를 로컬에서 즉시 확인 가능하게 만든다.
- `task start`에서 linkage를 기록하고 `task end`에서 정리하는 lifecycle을 맞춘다.
- branch naming과 remote backlog SoT 경계를 유지한다.

## 비목표
- branch naming에 issue 번호를 강제하지 않는다.
- 하나의 branch에 여러 issue를 동시에 연결하는 모델을 도입하지 않는다.
- GitHub issue를 backlog SoT에서 다른 저장소로 옮기지 않는다.

## 선택 방향
- branch는 계속 변경 목적 식별자다.
- issue linkage는 execution metadata다.
- linkage는 현재 worktree 문맥에 붙어야 한다.
- 조회는 branch 이름 해석이 아니라 전용 명령으로 제공한다.

## 저장 후보 비교

### branch naming 확장
- 장점: 사람 눈에 즉시 보임.
- 단점: naming policy와 역할 충돌. branch guard, 테스트, rename 비용 증가. issue 변경 시 이름이 stale해지기 쉬움.

### repo 공용 state file
- 장점: 구현 단순.
- 단점: 여러 worktree 동시 사용 시 충돌 가능. cleanup 누락 시 stale mapping 축적 위험.

### worktree-scoped metadata
- 장점: 현재 운영 모델과 가장 잘 맞음. branch 목적과 issue linkage를 분리 가능. URL, title, recorded_at 같은 부가 정보 저장 가능.
- 단점: backend 선택 필요. 조회/정리 command를 함께 설계해야 함.

## 확정 backend
- backend는 `git config --worktree` 로 고정.
- 공통 repo config에 `extensions.worktreeConfig=true` 를 선행 설정.
- 실제 저장 위치는 각 linked worktree admin dir의 `config.worktree`.
- namespace는 `q1.issue.*` 사용.

## 권장 모델
- `task start --issue <n>` 시 `git config --worktree` 로 metadata 기록.
- `task end` 시 같은 namespace를 정리.
- 별도 조회 command를 추가해 현재 문맥 issue를 출력.

## 기록할 최소 필드
- `q1.issue.number`
- `q1.issue.url`
- `q1.issue.title`
- `q1.issue.statusAtRecord`
- `q1.issue.branch`
- `q1.issue.worktree`
- `q1.issue.recordedAt`
- `q1.issue.recordedBy=task_start`

## 조회 표면
- 예시 command: `./scripts/repo/current_issue.sh`
- 기대 출력:
  - 연결 issue 번호
  - issue URL
  - issue 제목
  - metadata 기록 시점
- metadata가 없으면 "현재 worktree에 연결된 issue 없음"을 명시적으로 출력.
- 기본 조회는 recorded snapshot 기준.
- 필요 시 후속 옵션으로 remote live 조회를 추가 검토.

## lifecycle
1. `task start --issue <n>`가 issue 조회 후 metadata를 기록한다.
2. 작업 중 사용자는 조회 command로 현재 issue를 확인한다.
3. `task end`가 cleanup 단계에서 metadata를 제거한다.
4. 정리 실패 시 재시도 가능한 명령과 상태를 출력한다.

## 실패/예외 처리 초안
- metadata 없음: hard fail 대신 empty 상태를 명시적으로 반환.
- branch와 metadata 불일치: 우선 경고. 반복되면 guard 승격 검토.
- issue 없이 시작한 task: metadata 미기록 허용.
- title/status snapshot stale: 조회 command는 recorded snapshot과 remote live 조회를 분리해 다룬다.

## 남은 설계 쟁점
- 조회 command가 snapshot만 보여줄지, `gh`로 live 상태를 추가 조회할지 결정 필요.
- `task end`가 metadata 없음을 정상 종료로 볼지 경고로 볼지 결정 필요.

## 구현 메모
- write:
  - `git config --worktree q1.issue.number <n>`
  - `git config --worktree q1.issue.url <url>`
- read:
  - `git config --worktree --get q1.issue.number`
- cleanup:
  - `git config --worktree --unset-all q1.issue.number`
  - namespace 전 key 반복 정리 helper 필요.
- bootstrap:
  - repo당 1회 `git config extensions.worktreeConfig true`
  - helper에서 미설정 시 안내 또는 자동 설정 경로 결정 필요.

## 초기 구현 순서
1. `extensions.worktreeConfig` bootstrap helper 추가.
2. writer/reader/cleanup helper 추가.
3. `task start`에 기록 단계 추가.
4. `task end`에 정리 단계 추가.
5. 조회 command 추가.
6. 정책 문서와 테스트 보강.
