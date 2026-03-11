#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT_DIR}"

HELPER_TMP_DIR="$(mktemp -d)"
cleanup_helpers() {
  rm -rf "${HELPER_TMP_DIR}"
}
trap cleanup_helpers EXIT

mkdir -p "${HELPER_TMP_DIR}/scripts/repo"
cp "${ROOT_DIR}/scripts/repo/worktree_cleanup.sh" "${HELPER_TMP_DIR}/scripts/repo/worktree_cleanup.sh"
cp "${ROOT_DIR}/scripts/repo/post_merge_branch_cleanup.sh" "${HELPER_TMP_DIR}/scripts/repo/post_merge_branch_cleanup.sh"
cp "${ROOT_DIR}/scripts/repo/dirty_worktree_guard.py" "${HELPER_TMP_DIR}/scripts/repo/dirty_worktree_guard.py"
chmod +x "${HELPER_TMP_DIR}/scripts/repo/worktree_cleanup.sh" "${HELPER_TMP_DIR}/scripts/repo/post_merge_branch_cleanup.sh"

usage() {
  cat <<'EOF'
사용법:
  ./scripts/repo/task_end.sh [--pr <number-or-url>] [--branch <branch>] [--worktree <path>] [--method <squash|merge|rebase>] [--subject "<merge-subject>"] [--apply --yes] [--no-worktree-remove] [--no-branch-cleanup]

예시:
  ./scripts/repo/task_end.sh
  ./scripts/repo/task_end.sh --apply --yes
  ./scripts/repo/task_end.sh --apply --yes --no-worktree-remove
  ./scripts/repo/task_end.sh --pr 42 --worktree ../signup-flow--impl
EOF
}

fail() {
  local message="$1"
  local next_action="$2"
  echo "❌ ${message}" >&2
  echo "정책: task end core는 dry-run이 기본이며, 실제 실행은 --apply --yes로만 수행합니다." >&2
  echo "다음 행동: ${next_action}" >&2
  exit 1
}

extract_json_field() {
  local json_input="$1"
  local field_name="$2"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
field = sys.argv[2]
value = data.get(field, "")
if value is None:
    value = ""
print(value)
' "${json_input}" "${field_name}"
}

extract_issue_status_labels() {
  local json_input="$1"
  python3 -c '
import json
import sys

data = json.loads(sys.argv[1])
for label in data.get("labels", []):
    name = label.get("name", "")
    if name.startswith("status:"):
        print(name)
' "${json_input}"
}

read_issue_metadata() {
  (
    cd "${WORKTREE}" &&
    ./scripts/repo/worktree_issue_metadata.sh read
  ) 2>/dev/null || true
}

read_pr_metadata() {
  (
    cd "${WORKTREE}" &&
    ./scripts/repo/worktree_pr_metadata.sh read
  ) 2>/dev/null || true
}

get_metadata_value() {
  local metadata_output="$1"
  local key="$2"
  printf '%s\n' "${metadata_output}" | sed -n "s/^${key}=//p" | head -n 1
}

refresh_pr_metadata_cache() {
  PR_METADATA="$(read_pr_metadata)"
  RECORDED_PR_NUMBER=""
  RECORDED_PR_TITLE=""

  if [[ -n "${PR_METADATA}" ]]; then
    RECORDED_PR_NUMBER="$(get_metadata_value "${PR_METADATA}" "q1.pr.number")"
    RECORDED_PR_TITLE="$(get_metadata_value "${PR_METADATA}" "q1.pr.title")"
  fi
}

lookup_pr_number() {
  local target="${1:-}"

  [[ -n "${target}" ]] || return 0
  gh pr view "${target}" --json number --jq .number 2>/dev/null || true
}

lookup_pr_title() {
  local pr_number="${1:-}"

  [[ -n "${pr_number}" ]] || return 0
  gh pr view "${pr_number}" --json title --jq .title 2>/dev/null || true
}

lookup_pr_json() {
  local pr_number="${1:-}"

  [[ -n "${pr_number}" ]] || return 0
  gh pr view "${pr_number}" --json number,title,state,mergedAt,url 2>/dev/null || true
}

ensure_remote_branch_exists() {
  if git ls-remote --exit-code --heads origin "${BRANCH}" >/dev/null 2>&1; then
    return 0
  fi

  git push -u origin "${BRANCH}" >/dev/null 2>&1 || {
    fail "remote branch 생성에 실패했습니다: origin/${BRANCH}" "원격 push 권한과 branch 상태를 확인한 뒤 다시 실행하세요."
  }
}

is_valid_title_for_branch() {
  local candidate="${1:-}"

  [[ -n "${candidate}" ]] || return 1
  ./scripts/repo/pr_title_guard.sh validate --title "${candidate}" --branch "${BRANCH}" >/dev/null 2>&1
}

build_auto_pr_title() {
  local candidate=""
  local scope=""
  local summary=""

  candidate="${RECORDED_PR_TITLE:-}"
  if is_valid_title_for_branch "${candidate}"; then
    printf '%s\n' "${candidate}"
    return 0
  fi

  candidate="${LINKED_ISSUE_TITLE:-}"
  if is_valid_title_for_branch "${candidate}"; then
    printf '%s\n' "${candidate}"
    return 0
  fi

  scope="${BRANCH%%/*}"
  if [[ -n "${LINKED_ISSUE_TITLE}" ]]; then
    summary="$(printf '%s\n' "${LINKED_ISSUE_TITLE}" | sed -E 's/^\[[^]]+\][[:space:]]*//')"
  fi
  if [[ -z "${summary}" ]]; then
    summary="$(printf '%s\n' "${BRANCH#*/}" | tr '-' ' ')"
  fi

  ./scripts/repo/pr_title_guard.sh generate --scope "${scope}" --summary "${summary}"
}

collect_auto_pr_changes() {
  local changes=""

  changes="$(git log --format='- %s' "main..${BRANCH}" 2>/dev/null || true)"
  if [[ -z "${changes}" ]]; then
    changes="$(git log -1 --format='- %s' "${BRANCH}" 2>/dev/null || true)"
  fi
  if [[ -z "${changes}" ]]; then
    changes="- 현재 브랜치 변경 요약을 자동 수집하지 못했다."
  fi

  printf '%s\n' "${changes}"
}

write_auto_pr_body() {
  local body_file="$1"
  local auto_changes="$2"

  cat > "${body_file}" <<EOF
## Summary
- branch \`${BRANCH}\` 의 로컬 변경을 remote PR로 승격한다.
- task end apply 경로가 merge 가능한 remote 문맥을 자동으로 복구한다.

## Primary Issue
Closes #${LINKED_ISSUE_NUMBER}

## Related Issues
- Related: 없음

## Context
- 현재 worktree에는 merge 대상 변경이 있지만 remote branch 또는 원격 PR 문맥이 없을 수 있다.
- task end는 merge 전에 remote branch와 PR을 확보해야 cleanup까지 같은 흐름으로 이어질 수 있다.

## Changes
${auto_changes}

## Decisions Made
- Decision:
  - Context: task end가 원격 branch나 PR을 찾지 못하면 종료 자동화가 merge 전에 중단됐다.
  - Chosen: 누락된 remote branch를 먼저 push하고 PR이 없으면 자동 생성한 뒤 기존 merge 흐름을 이어간다.
  - Rejected alternative: remote artifact 부재를 즉시 실패로만 처리한다.
  - Rationale: branch -> PR -> merge lifecycle을 task end에서 복구하는 편이 운영 비용이 낮다.
  - Reference: issue #${LINKED_ISSUE_NUMBER}

## Deferred / Not Included
- 자동 생성된 PR 본문 이후의 세부 서술 보강은 이번 task end 경로에 포함하지 않는다.

## Validation Notes
- task end apply 경로에서 remote branch 조회, PR 조회, 필요 시 PR 생성 단계를 순차 실행한다.

## Risks
- Impact: task end 자동화와 merge 직전 remote 준비 단계
- Residual risk: 자동 생성된 PR 본문이 작업 배경을 충분히 담지 못할 수 있다.
- Rollback note: 생성된 PR 본문을 수동 수정하거나 task end 전에 수동 PR 생성 흐름으로 되돌릴 수 있다.

## Reviewer Focus
- 자동 생성된 PR 제목과 본문이 현재 브랜치 목적 및 linked issue와 맞는지 확인.
EOF
}

create_missing_pr() {
  local auto_pr_title=""
  local auto_pr_body_file=""
  local auto_changes=""

  if [[ -n "${PR_TARGET}" ]]; then
    fail "명시한 PR 대상이 존재하지 않습니다: ${PR_TARGET}" "올바른 PR 번호/URL을 지정하거나 --pr 없이 다시 실행하세요."
  fi

  if [[ -z "${LINKED_ISSUE_NUMBER}" ]]; then
    fail "linked issue metadata 없이 PR을 자동 생성할 수 없습니다." "task start issue metadata를 확인하거나 PR을 먼저 생성한 뒤 다시 실행하세요."
  fi

  auto_pr_title="$(build_auto_pr_title)"
  auto_pr_body_file="${HELPER_TMP_DIR}/auto-pr-body.md"
  auto_changes="$(collect_auto_pr_changes)"
  write_auto_pr_body "${auto_pr_body_file}" "${auto_changes}"

  PYTHONDONTWRITEBYTECODE=1 ./scripts/repo/pr_create.sh --title "${auto_pr_title}" --body-file "${auto_pr_body_file}" >/dev/null || {
    fail "누락된 PR 자동 생성에 실패했습니다." "PR title/body gate와 gh 인증 상태를 확인한 뒤 다시 실행하세요."
  }

  refresh_pr_metadata_cache
}

run_worktree_cleanup() {
  if [[ "${WORKTREE}" == "${CURRENT_WORKTREE}" && "${WORKTREE}" != "${PRIMARY_WORKTREE}" ]]; then
    (
      cd "${PRIMARY_WORKTREE}" &&
      REPO_ROOT_OVERRIDE="${PRIMARY_WORKTREE}" \
      "${HELPER_TMP_DIR}/scripts/repo/worktree_cleanup.sh" "$@"
    )
    return
  fi

  ./scripts/repo/worktree_cleanup.sh "$@"
}

run_branch_cleanup() {
  if [[ "${PRIMARY_WORKTREE}" != "${CURRENT_WORKTREE}" ]]; then
    (
      cd "${PRIMARY_WORKTREE}" &&
      REPO_ROOT_OVERRIDE="${PRIMARY_WORKTREE}" \
      "${HELPER_TMP_DIR}/scripts/repo/post_merge_branch_cleanup.sh" "$@"
    )
    return
  fi

  ./scripts/repo/post_merge_branch_cleanup.sh "$@"
}

run_issue_metadata_cleanup() {
  (
    cd "${WORKTREE}" &&
    ./scripts/repo/worktree_issue_metadata.sh clear
  )
}

run_pr_metadata_cleanup() {
  (
    cd "${WORKTREE}" &&
    ./scripts/repo/worktree_pr_metadata.sh clear
  )
}

METHOD="squash"
PR_TARGET=""
BRANCH=""
WORKTREE=""
SUBJECT=""
APPLY=0
ASSUME_YES=0
NO_WORKTREE_REMOVE=0
NO_BRANCH_CLEANUP=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pr)
      PR_TARGET="${2:-}"
      shift 2
      ;;
    --branch)
      BRANCH="${2:-}"
      shift 2
      ;;
    --worktree)
      WORKTREE="${2:-}"
      shift 2
      ;;
    --method)
      METHOD="${2:-}"
      shift 2
      ;;
    --subject)
      SUBJECT="${2:-}"
      shift 2
      ;;
    --apply)
      APPLY=1
      shift
      ;;
    --yes)
      ASSUME_YES=1
      shift
      ;;
    --no-worktree-remove)
      NO_WORKTREE_REMOVE=1
      shift
      ;;
    --no-branch-cleanup)
      NO_BRANCH_CLEANUP=1
      shift
      ;;
    --dry-run)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "알 수 없는 옵션: $1" "사용법을 확인한 뒤 다시 실행하세요."
      ;;
  esac
done

case "${METHOD}" in
  squash|merge|rebase) ;;
  *)
    fail "--method 는 squash|merge|rebase 중 하나여야 합니다." "--method 값을 squash, merge, rebase 중 하나로 수정해서 다시 실행하세요."
    ;;
esac

if [[ ${ASSUME_YES} -eq 1 && ${APPLY} -eq 0 ]]; then
  fail "--yes 는 --apply 와 함께만 사용할 수 있습니다." "--apply --yes 조합으로 다시 실행하거나 기본 dry-run만 수행하세요."
fi

if [[ ${APPLY} -eq 1 && ${ASSUME_YES} -eq 0 ]]; then
  fail "core task end는 interactive prompt를 제공하지 않습니다." "--apply --yes 를 함께 사용하거나 task_end_interactive.sh 를 사용하세요."
fi

python3 scripts/repo/detached_head_guard.py validate-write
python3 scripts/repo/dirty_worktree_guard.py validate-clean

CURRENT_BRANCH="$(git branch --show-current)"
if [[ -z "${CURRENT_BRANCH}" ]]; then
  fail "현재 브랜치를 확인할 수 없습니다." "브랜치가 checkout된 worktree에서 다시 실행하거나 --branch 를 명시하세요."
fi

CURRENT_WORKTREE="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${CURRENT_WORKTREE}" ]]; then
  fail "현재 worktree 경로를 확인할 수 없습니다." "Git worktree 내부에서 실행하거나 --worktree 로 대상 경로를 명시하세요."
fi

PRIMARY_WORKTREE="$(git worktree list --porcelain | awk '/^worktree /{print substr($0,10); exit}')"
if [[ -z "${PRIMARY_WORKTREE}" ]]; then
  fail "primary worktree 경로를 확인할 수 없습니다." "git worktree list 결과를 확인한 뒤 다시 실행하세요."
fi

BRANCH="${BRANCH:-${CURRENT_BRANCH}}"
WORKTREE="${WORKTREE:-${CURRENT_WORKTREE}}"
PR_VIEW_TARGET="${PR_TARGET:-${BRANCH}}"

PR_LABEL="${PR_VIEW_TARGET}"
PR_NUMBER=""
PR_TITLE=""
PR_STATE=""
PR_MERGED_AT=""
ISSUE_METADATA=""
PR_METADATA=""
LINKED_ISSUE_NUMBER=""
LINKED_ISSUE_TITLE=""
LINKED_ISSUE_STATUS_AT_RECORD=""
RECORDED_PR_NUMBER=""
RECORDED_PR_TITLE=""

ISSUE_METADATA="$(read_issue_metadata)"
if [[ -n "${ISSUE_METADATA}" ]]; then
  LINKED_ISSUE_NUMBER="$(get_metadata_value "${ISSUE_METADATA}" "q1.issue.number")"
  LINKED_ISSUE_TITLE="$(get_metadata_value "${ISSUE_METADATA}" "q1.issue.title")"
  LINKED_ISSUE_STATUS_AT_RECORD="$(get_metadata_value "${ISSUE_METADATA}" "q1.issue.statusAtRecord")"
fi

refresh_pr_metadata_cache

if [[ -z "${PR_TARGET}" && -n "${RECORDED_PR_NUMBER}" ]]; then
  PR_VIEW_TARGET="${RECORDED_PR_NUMBER}"
  PR_LABEL="#${RECORDED_PR_NUMBER}"
fi

if [[ ${APPLY} -eq 1 ]]; then
  ./scripts/repo/gh_preflight.sh >/dev/null

  ensure_remote_branch_exists

  PR_NUMBER="$(lookup_pr_number "${PR_VIEW_TARGET}")"
  if [[ -z "${PR_NUMBER}" || "${PR_NUMBER}" == "null" ]]; then
    if [[ -z "${PR_TARGET}" && -n "${RECORDED_PR_NUMBER}" ]]; then
      PR_NUMBER="$(lookup_pr_number "${BRANCH}")"
    fi
  fi
  if [[ -z "${PR_NUMBER}" || "${PR_NUMBER}" == "null" ]]; then
    create_missing_pr
    PR_NUMBER="${RECORDED_PR_NUMBER}"
  fi
  if [[ -z "${PR_NUMBER}" || "${PR_NUMBER}" == "null" ]]; then
    fail "현재 문맥에서 merge 대상 PR을 자동 추론할 수 없습니다." "--pr <number-or-url> 를 명시하거나 PR metadata를 확인한 뒤 다시 실행하세요."
  fi
  PR_VIEW_TARGET="${PR_NUMBER}"
  PR_LABEL="#${PR_NUMBER}"
  PR_VIEW_OUTPUT="$(lookup_pr_json "${PR_NUMBER}")"
  if [[ -z "${PR_VIEW_OUTPUT}" ]]; then
    fail "PR 상세 상태를 조회할 수 없습니다: #${PR_NUMBER}" "gh auth 상태와 PR 접근 권한을 확인한 뒤 다시 실행하세요."
  fi
  PR_TITLE="$(extract_json_field "${PR_VIEW_OUTPUT}" "title")"
  PR_STATE="$(extract_json_field "${PR_VIEW_OUTPUT}" "state")"
  PR_MERGED_AT="$(extract_json_field "${PR_VIEW_OUTPUT}" "mergedAt")"
  if [[ -z "${PR_TITLE}" || "${PR_TITLE}" == "null" ]]; then
    fail "PR 제목을 조회할 수 없습니다: #${PR_NUMBER}" "--subject 를 명시하거나 gh auth 상태를 확인한 뒤 다시 실행하세요."
  fi
fi

MERGE_SUBJECT="${SUBJECT}"
if [[ -z "${MERGE_SUBJECT}" && "${METHOD}" != "rebase" ]]; then
  if [[ -n "${PR_TITLE}" ]]; then
    MERGE_SUBJECT="${PR_TITLE}"
  else
    MERGE_SUBJECT="<PR_TITLE_FROM_GH>"
  fi
fi

MERGE_PR_TARGET="${PR_TARGET}"
if [[ -z "${MERGE_PR_TARGET}" && -n "${PR_NUMBER}" ]]; then
  MERGE_PR_TARGET="${PR_NUMBER}"
elif [[ -z "${MERGE_PR_TARGET}" && -n "${RECORDED_PR_NUMBER}" ]]; then
  MERGE_PR_TARGET="${RECORDED_PR_NUMBER}"
fi

MERGE_DRY_ARGS=(--method "${METHOD}" --dry-run)
MERGE_RUN_ARGS=(--method "${METHOD}")
if [[ -n "${MERGE_PR_TARGET}" ]]; then
  MERGE_DRY_ARGS+=(--pr "${MERGE_PR_TARGET}")
  MERGE_RUN_ARGS+=(--pr "${MERGE_PR_TARGET}")
fi
if [[ -n "${MERGE_SUBJECT}" && "${METHOD}" != "rebase" ]]; then
  MERGE_DRY_ARGS+=(--subject "${MERGE_SUBJECT}")
  MERGE_RUN_ARGS+=(--subject "${MERGE_SUBJECT}")
fi

BRANCH_CLEANUP_DRY_ARGS=(--branch "${BRANCH}" --dry-run)
BRANCH_CLEANUP_RUN_ARGS=(--branch "${BRANCH}")

WORKTREE_DRY_ARGS=(--worktree "${WORKTREE}" --expected-branch "${BRANCH}" --dry-run)
WORKTREE_RUN_ARGS=(--worktree "${WORKTREE}" --expected-branch "${BRANCH}")

MERGE_PLAN_OUTPUT="$(./scripts/repo/pr_merge.sh "${MERGE_DRY_ARGS[@]}" 2>&1)" || {
  echo "${MERGE_PLAN_OUTPUT}" >&2
  fail "merge dry-run 검증에 실패했습니다." "위 실패 메시지의 다음 행동을 먼저 수행한 뒤 다시 실행하세요."
}

WORKTREE_CLEANUP_OUTPUT=""
if [[ ${NO_WORKTREE_REMOVE} -eq 0 ]]; then
  WORKTREE_CLEANUP_OUTPUT="$(run_worktree_cleanup "${WORKTREE_DRY_ARGS[@]}" 2>&1)" || {
    echo "${WORKTREE_CLEANUP_OUTPUT}" >&2
    fail "worktree cleanup dry-run 검증에 실패했습니다." "위 실패 메시지의 다음 행동을 먼저 수행한 뒤 다시 실행하세요."
  }
fi

BRANCH_CLEANUP_OUTPUT=""
if [[ ${NO_BRANCH_CLEANUP} -eq 0 ]]; then
  BRANCH_CLEANUP_OUTPUT="$(run_branch_cleanup "${BRANCH_CLEANUP_DRY_ARGS[@]}" 2>&1)" || {
    echo "${BRANCH_CLEANUP_OUTPUT}" >&2
    fail "branch cleanup dry-run 검증에 실패했습니다." "위 실패 메시지의 다음 행동을 먼저 수행한 뒤 다시 실행하세요."
  }
fi

echo "✅ dry-run: task end 계획"
echo "- PR: ${PR_LABEL}"
echo "- Branch: ${BRANCH}"
echo "- Worktree: ${WORKTREE}"
echo "- Cleanup order: worktree cleanup -> branch cleanup"
echo "- Remote branch ensure: origin/${BRANCH} 확인 후 없으면 생성"
if [[ -n "${PR_TARGET}" ]]; then
echo "- PR ensure: 명시 target 사용 (${PR_TARGET})"
elif [[ -n "${RECORDED_PR_NUMBER}" ]]; then
echo "- PR ensure: recorded PR #${RECORDED_PR_NUMBER} 우선, 없으면 branch 기준 조회 후 생성"
else
echo "- PR ensure: branch 기준 조회 후 없으면 생성"
fi
echo "- Method: ${METHOD}"
echo "- Recovery path: apply 시 merged PR이면 merge step을 건너뛰고 남은 cleanup만 수행"
if [[ -n "${MERGE_SUBJECT}" ]]; then
echo "- Merge subject: ${MERGE_SUBJECT}"
else
echo "- Merge subject: <not-used>"
fi
if [[ -n "${LINKED_ISSUE_NUMBER}" ]]; then
echo "- Linked issue: #${LINKED_ISSUE_NUMBER}"
if [[ -n "${LINKED_ISSUE_STATUS_AT_RECORD}" ]]; then
echo "- Linked issue recorded status: ${LINKED_ISSUE_STATUS_AT_RECORD}"
fi
echo "- Issue close status cleanup: remove status:* after linked issue closes"
else
echo "- Linked issue: <none>"
echo "- Issue close status cleanup: skip"
fi
echo "- Issue metadata cleanup: run"
echo "- PR metadata cleanup: run"
echo "- Branch cleanup: $([[ ${NO_BRANCH_CLEANUP} -eq 1 ]] && echo skip || echo run)"
echo "- Worktree cleanup: $([[ ${NO_WORKTREE_REMOVE} -eq 1 ]] && echo skip || echo run)"
echo
echo "[merge]"
echo "${MERGE_PLAN_OUTPUT}"
if [[ -n "${WORKTREE_CLEANUP_OUTPUT}" ]]; then
  echo
  echo "[worktree cleanup]"
  echo "${WORKTREE_CLEANUP_OUTPUT}"
fi
if [[ -n "${BRANCH_CLEANUP_OUTPUT}" ]]; then
  echo
  echo "[branch cleanup]"
  echo "${BRANCH_CLEANUP_OUTPUT}"
fi

if [[ ${APPLY} -eq 0 ]]; then
  exit 0
fi

if [[ -n "${PR_MERGED_AT}" && "${PR_MERGED_AT}" != "null" ]]; then
  echo "ℹ️ partial completion 감지: ${PR_LABEL} 는 이미 merged 상태입니다."
  echo "ℹ️ recovery mode: merge step을 건너뛰고 남은 cleanup만 수행합니다."
else
  ./scripts/repo/pr_merge.sh "${MERGE_RUN_ARGS[@]}"
fi

if [[ -n "${LINKED_ISSUE_NUMBER}" ]]; then
  ISSUE_VIEW_OUTPUT="$(gh issue view "${LINKED_ISSUE_NUMBER}" --json state,labels,url,title 2>&1)" || {
    fail "merge 후 linked issue #${LINKED_ISSUE_NUMBER} 를 조회할 수 없습니다." "gh 인증과 issue 접근 권한을 확인한 뒤 issue 상태를 수동으로 점검하세요."
  }

  LINKED_ISSUE_STATE="$(extract_json_field "${ISSUE_VIEW_OUTPUT}" "state")"
  if [[ "${LINKED_ISSUE_STATE}" != "CLOSED" ]]; then
    fail "merge 후 linked issue #${LINKED_ISSUE_NUMBER} 가 닫히지 않았습니다." "PR body close keyword 또는 issue close 상태를 정리한 뒤 status label을 수동으로 정리하세요."
  fi

  ISSUE_STATUS_REMOVE_ARGS=()
  while IFS= read -r issue_status_label; do
    [[ -n "${issue_status_label}" ]] || continue
    ISSUE_STATUS_REMOVE_ARGS+=(--remove-label "${issue_status_label}")
  done < <(extract_issue_status_labels "${ISSUE_VIEW_OUTPUT}")

  if [[ ${#ISSUE_STATUS_REMOVE_ARGS[@]} -gt 0 ]]; then
    gh issue edit "${LINKED_ISSUE_NUMBER}" "${ISSUE_STATUS_REMOVE_ARGS[@]}" >/dev/null || {
      fail "closed issue #${LINKED_ISSUE_NUMBER} 의 status label 정리에 실패했습니다." "GitHub에서 남은 status:* label을 수동으로 제거한 뒤 다시 정리하세요."
    }
  fi
fi

run_issue_metadata_cleanup >/dev/null || {
  fail "issue metadata cleanup에 실패했습니다: ${WORKTREE}" "대상 worktree에서 worktree_issue_metadata.sh clear 가 동작하는지 확인한 뒤 metadata를 수동으로 정리하세요."
}

run_pr_metadata_cleanup >/dev/null || {
  fail "PR metadata cleanup에 실패했습니다: ${WORKTREE}" "대상 worktree에서 worktree_pr_metadata.sh clear 가 동작하는지 확인한 뒤 metadata를 수동으로 정리하세요."
}

if [[ ${NO_WORKTREE_REMOVE} -eq 0 ]]; then
  run_worktree_cleanup "${WORKTREE_RUN_ARGS[@]}"
fi

if [[ ${NO_BRANCH_CLEANUP} -eq 0 ]]; then
  run_branch_cleanup "${BRANCH_CLEANUP_RUN_ARGS[@]}"
fi

echo "✅ task end 완료: ${PR_LABEL}"
