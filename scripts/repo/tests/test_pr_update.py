from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "gh_failure_guard.sh",
    "pr_update.sh",
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
- PR 수정 경로를 REST API wrapper로 정리한다.

## Primary Issue
Closes #43

## Related Issues
- Related: #42

## Context
- `gh pr edit` 경로가 classic projects GraphQL 오류로 실패했다.

## Changes
- PR 수정 wrapper가 title/body gate 이후 REST API PATCH를 호출한다.

## Decisions Made
- Decision:
  - Context: PR 생성은 가능했지만 수정은 `gh pr edit` 오류로 운영 경로가 불안정했다.
  - Chosen: PR 수정 공식 경로를 `gh api -X PATCH` 기반 wrapper로 고정했다.
  - Rejected alternative: `gh pr edit` 예외 처리만 추가한다.
  - Rationale: 재현 가능한 성공 경로를 wrapper에 고정하는 편이 운영 일관성이 높다.
  - Reference: Issue #43

## Deferred / Not Included
- PR 생성 경로 재설계는 포함하지 않는다.

## Validation Notes
- fake gh 환경에서 PATCH payload와 metadata 갱신을 확인했다.

## Risks
- Impact: PR 수정 wrapper
- Residual risk: origin remote URL 형식이 GitHub 패턴이 아니면 endpoint 추출이 실패할 수 있다.
- Rollback note: update wrapper를 제거하면 이전 수동 수정 흐름으로 복귀한다.

## Reviewer Focus
- PR 번호 조회와 REST API PATCH 경로가 일관되게 연결되는지 확인.
"""


class PrUpdateTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, dict[str, str], Path, Path, Path]:
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
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/example-owner/example-repo.git"], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)

        branch = "fix/pr-update-rest-api-path"
        subprocess.run(["git", "branch", branch], cwd=root, check=True, capture_output=True)

        worktree = workspace / "pr-update-rest-api-path--fix"
        subprocess.run(["git", "worktree", "add", str(worktree), branch], cwd=root, check=True, capture_output=True)

        subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_pr_metadata.sh",
                "write",
                "--number",
                "41",
                "--url",
                "https://github.com/example-owner/example-repo/pull/41",
                "--title",
                "[fix] 이전 제목",
                "--state",
                "OPEN",
                "--base-branch",
                "main",
                "--head-branch",
                branch,
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-13T00:00:00Z",
                "--recorded-by",
                "pr_create",
            ],
            cwd=worktree,
            check=True,
            capture_output=True,
            text=True,
        )

        body_file = workspace / "pr.md"
        body_file.write_text(PR_BODY, encoding="utf-8")

        bin_dir = workspace / "bin"
        bin_dir.mkdir()
        gh_log = workspace / "gh.log"
        payload_log = workspace / "payload.json"
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
if [[ "$1" == "api" && "$2" == "-X" && "$3" == "PATCH" ]]; then
  if [[ "${FAKE_GH_PATCH_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
  endpoint="${4:-}"
  if [[ "${5:-}" != "--input" ]]; then
    echo "missing --input" >&2
    exit 1
  fi
  input_path="${6:-}"
  printf '%s\\n' "${endpoint}" > "${FAKE_GH_LOG}"
  cp "${input_path}" "${FAKE_GH_PAYLOAD_LOG}"
  python3 - "${input_path}" <<'PY'
import json
import pathlib
import sys

payload = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
print(json.dumps({
    "number": 41,
    "title": payload["title"],
    "html_url": "https://github.com/example-owner/example-repo/pull/41",
    "state": "OPEN",
    "base": {"ref": "main"},
    "head": {"ref": "fix/pr-update-rest-api-path"},
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
        env["FAKE_GH_PAYLOAD_LOG"] = str(payload_log)

        return worktree, env, body_file, gh_log, payload_log

    def run_script(self, cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/pr_update.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_update_uses_rest_patch_and_refreshes_metadata(self) -> None:
        worktree, env, body_file, gh_log, payload_log = self.make_repo()
        result = self.run_script(
            worktree,
            env,
            "--title",
            "[fix] PR 수정 경로 정리",
            "--body-file",
            str(body_file),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PR 수정 완료: #41", result.stdout)

        endpoint = gh_log.read_text(encoding="utf-8").strip()
        self.assertEqual(endpoint, "repos/example-owner/example-repo/pulls/41")

        payload = json.loads(payload_log.read_text(encoding="utf-8"))
        self.assertEqual(payload["title"], "[fix] PR 수정 경로 정리")
        self.assertIn("Closes #43", payload["body"])

        title = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.title"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        recorded_by = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.recordedBy"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(title, "[fix] PR 수정 경로 정리")
        self.assertEqual(recorded_by, "pr_update")

    def test_requires_pr_number_when_metadata_missing(self) -> None:
        worktree, env, body_file, _, _ = self.make_repo()
        subprocess.run(
            ["bash", "./scripts/repo/worktree_pr_metadata.sh", "clear"],
            cwd=worktree,
            check=True,
            capture_output=True,
            text=True,
        )
        result = self.run_script(
            worktree,
            env,
            "--title",
            "[fix] PR 수정 경로 정리",
            "--body-file",
            str(body_file),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("수정 대상 PR 번호를 확인할 수 없습니다", result.stderr)
        self.assertIn("--number", result.stderr)

    def test_fails_with_retry_hint_when_patch_hits_connect_error(self) -> None:
        worktree, env, body_file, _, _ = self.make_repo()
        env = dict(env)
        env["FAKE_GH_PATCH_FAIL"] = "1"
        result = self.run_script(
            worktree,
            env,
            "--title",
            "[fix] PR 수정 경로 정리",
            "--body-file",
            str(body_file),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PR 수정에 실패했습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)


if __name__ == "__main__":
    unittest.main()
