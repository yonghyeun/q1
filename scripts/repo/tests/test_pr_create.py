from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "gh_failure_guard.sh",
    "pr_create.sh",
    "gh_preflight.sh",
    "pr_title_guard.sh",
    "pr_body_quality_guard.py",
    "pr_issue_guard.py",
    "body_guard_common.py",
    "detached_head_guard.py",
    "protected_branch_write_guard.py",
    "branch_guard.py",
    "dirty_worktree_guard.py",
    "worktree_config_bootstrap.sh",
    "worktree_pr_metadata.sh",
]

PR_BODY = """## Summary
- PR metadata를 worktree에 기록한다.

## Primary Issue
Closes #24

## Related Issues
- Related: #19

## Context
- PR 생성 후 후속 수정에서 PR 번호 재조회 비용이 있다.

## Changes
- PR 생성 직후 local metadata를 기록한다.

## Decisions Made
- Decision:
  - Context: 후속 PR 수정에서 대상 PR을 안정적으로 다시 찾을 경로가 필요했다.
  - Chosen: PR 생성 시 worktree metadata에 PR 번호와 식별 정보를 기록한다.
  - Rejected alternative: PR 번호를 매번 remote 조회로 다시 찾는다.
  - Rationale: 현재 worktree 문맥에 붙는 metadata가 후속 수정 경로와 가장 잘 맞는다.
  - Reference: Issue #24

## Deferred / Not Included
- task end 이후 추가 정책 변경은 이번 테스트에 포함하지 않는다.

## Validation Notes
- fake gh 환경에서 PR 생성 후 metadata 기록 여부를 확인했다.

## Risks
- Impact: PR 생성 스크립트
- Residual risk: remote PR은 생성됐지만 local metadata 기록이 실패할 수 있다.
- Rollback note: PR metadata write 단계를 제거하면 기존 동작으로 되돌릴 수 있다.

## Reviewer Focus
- PR 번호 추출과 metadata write 연결이 적절한지 확인.
"""


class PrCreateTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, dict[str, str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        workspace = Path(temp_dir.name)
        root = workspace / "repo"
        root.mkdir(parents=True)
        scripts_dir = root / "scripts/repo"
        scripts_dir.mkdir(parents=True)

        for script_name in SCRIPT_NAMES:
            source = ROOT_DIR / "scripts/repo" / script_name
            target = scripts_dir / script_name
            shutil.copy2(source, target)
            target.chmod(0o755)

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://example.test/repo.git"], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)

        branch = "config/pr-number-metadata"
        subprocess.run(["git", "branch", branch], cwd=root, check=True, capture_output=True)

        worktree = workspace / "pr-number-metadata--impl"
        subprocess.run(["git", "worktree", "add", str(worktree), branch], cwd=root, check=True, capture_output=True)

        body_file = workspace / "pr.md"
        body_file.write_text(PR_BODY, encoding="utf-8")

        bin_dir = workspace / "bin"
        bin_dir.mkdir()
        gh_log = workspace / "gh.log"
        gh_script = bin_dir / "gh"
        gh_script.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "auth" && "$2" == "status" ]]; then
  exit 0
fi
if [[ "$1" == "api" && "$2" == "rate_limit" ]]; then
  if [[ "${FAKE_GH_API_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
  echo "5000"
  exit 0
fi
if [[ "$1" == "pr" && "$2" == "create" ]]; then
  if [[ "${FAKE_GH_PR_CREATE_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
  printf '%s\\n' "$*" > "${FAKE_GH_LOG}"
  echo "https://example.test/pull/42"
  exit 0
fi
if [[ "$1" == "pr" && "$2" == "view" ]]; then
  pr_number="${3:-}"
  python3 - "${pr_number}" <<'PY'
import json
import os
import sys

pr_number = sys.argv[1]
print(json.dumps({
    "number": int(pr_number),
    "title": os.environ.get("FAKE_GH_PR_TITLE", "[config] PR metadata 저장"),
    "url": os.environ.get("FAKE_GH_PR_URL", f"https://example.test/pull/{pr_number}"),
    "state": os.environ.get("FAKE_GH_PR_STATE", "OPEN"),
    "baseRefName": os.environ.get("FAKE_GH_PR_BASE", "main"),
    "headRefName": os.environ.get("FAKE_GH_PR_HEAD", "config/pr-number-metadata"),
}))
PY
  exit 0
fi
echo "unexpected gh args: $*" >&2
exit 1
""",
            encoding="utf-8",
        )
        gh_script.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        env["FAKE_GH_LOG"] = str(gh_log)

        return worktree, env, body_file

    def run_script(self, cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/pr_create.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_create_records_pr_metadata(self) -> None:
        worktree, env, body_file = self.make_repo()
        result = self.run_script(
            worktree,
            env,
            "--title",
            "[config] PR metadata 저장",
            "--body-file",
            str(body_file),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PR 생성 완료", result.stdout)
        self.assertIn("number: 42", result.stdout)

        number = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.number"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        title = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.title"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        base_branch = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.baseBranch"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        head_branch = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.headBranch"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(number, "42")
        self.assertEqual(title, "[config] PR metadata 저장")
        self.assertEqual(base_branch, "main")
        self.assertEqual(head_branch, "config/pr-number-metadata")

    def test_fails_with_retry_hint_when_api_preflight_detects_network_block(self) -> None:
        worktree, env, body_file = self.make_repo()
        env = dict(env)
        env["FAKE_GH_API_FAIL"] = "1"
        result = self.run_script(
            worktree,
            env,
            "--title",
            "[config] PR metadata 저장",
            "--body-file",
            str(body_file),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GitHub API 연결 확인에 실패했습니다", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)

    def test_fails_with_retry_hint_when_pr_create_hits_connect_error(self) -> None:
        worktree, env, body_file = self.make_repo()
        env = dict(env)
        env["FAKE_GH_PR_CREATE_FAIL"] = "1"
        result = self.run_script(
            worktree,
            env,
            "--title",
            "[config] PR metadata 저장",
            "--body-file",
            str(body_file),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PR 생성에 실패했습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)


if __name__ == "__main__":
    unittest.main()
