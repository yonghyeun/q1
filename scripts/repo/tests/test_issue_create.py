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
    "issue_create.sh",
    "gh_preflight.sh",
    "issue_title_guard.sh",
    "issue_body_quality_guard.py",
    "issue_label_guard.py",
    "body_guard_common.py",
]

ISSUE_BODY = """## Summary
- sandbox에서 GitHub API 재시도 경로가 길다.

## Context
- issue wrapper e2e 검증 중 sandbox 네트워크 제약이 끼어든다.

## Observed Behavior
- GitHub API 호출이 중단되면 같은 wrapper 재시도 경로를 바로 알기 어렵다.

## Expected Behavior
- sandbox 차단 시 다음 행동이 곧바로 드러나야 한다.

## Impact
- 이슈 생성 검증 흐름이 늘어진다.

## Reproduction Clues
- `./scripts/repo/issue_create.sh`

## Suspected Area
- gh preflight와 wrapper 실패 메시지

## Constraints
- raw gh 호출로 우회하지 않는다.

## Decision Candidates
- preflight에서 API 차단을 먼저 드러낸다.

## Done Signal
- 권한 상승 재시도 안내가 출력된다.

## Related Links
- Issue #14
"""


class IssueCreateTests(unittest.TestCase):
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

        body_file = workspace / "issue.md"
        body_file.write_text(ISSUE_BODY, encoding="utf-8")

        bin_dir = workspace / "bin"
        bin_dir.mkdir()
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
if [[ "$1" == "issue" && "$2" == "create" ]]; then
  if [[ "${FAKE_GH_ISSUE_CREATE_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
  echo "https://example.test/issues/14"
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
        return root, env, body_file

    def run_script(self, cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/issue_create.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_creates_issue_when_api_is_available(self) -> None:
        root, env, body_file = self.make_repo()
        result = self.run_script(
            root,
            env,
            "--type",
            "bug",
            "--status",
            "inbox",
            "--priority",
            "p2",
            "--source-type",
            "runtime-observation",
            "--area",
            "repo",
            "--title",
            "[bug] sandbox 권한 상승 재시도 안내 개선",
            "--body-file",
            str(body_file),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Issue 생성 완료", result.stdout)
        self.assertIn("number: 14", result.stdout)

    def test_fails_with_retry_hint_when_api_preflight_detects_network_block(self) -> None:
        root, env, body_file = self.make_repo()
        env = dict(env)
        env["FAKE_GH_API_FAIL"] = "1"
        result = self.run_script(
            root,
            env,
            "--type",
            "bug",
            "--status",
            "inbox",
            "--priority",
            "p2",
            "--source-type",
            "runtime-observation",
            "--area",
            "repo",
            "--title",
            "[bug] sandbox 권한 상승 재시도 안내 개선",
            "--body-file",
            str(body_file),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GitHub API 연결 확인에 실패했습니다", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)

    def test_fails_with_retry_hint_when_issue_create_hits_connect_error(self) -> None:
        root, env, body_file = self.make_repo()
        env = dict(env)
        env["FAKE_GH_ISSUE_CREATE_FAIL"] = "1"
        result = self.run_script(
            root,
            env,
            "--type",
            "bug",
            "--status",
            "inbox",
            "--priority",
            "p2",
            "--source-type",
            "runtime-observation",
            "--area",
            "repo",
            "--title",
            "[bug] sandbox 권한 상승 재시도 안내 개선",
            "--body-file",
            str(body_file),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("issue 생성에 실패했습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)


if __name__ == "__main__":
    unittest.main()
