from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]


class GhPreflightTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, dict[str, str]]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        workspace = Path(temp_dir.name)
        root = workspace / "repo"
        root.mkdir(parents=True)
        scripts_dir = root / "scripts/repo"
        scripts_dir.mkdir(parents=True)

        source = ROOT_DIR / "scripts/repo/gh_preflight.sh"
        target = scripts_dir / "gh_preflight.sh"
        shutil.copy2(source, target)
        target.chmod(0o755)

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", "https://example.test/repo.git"], cwd=root, check=True)

        bin_dir = workspace / "bin"
        bin_dir.mkdir()
        gh_script = bin_dir / "gh"
        gh_script.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "auth" && "$2" == "status" ]]; then
  if [[ "${FAKE_GH_AUTH_FAIL:-0}" == "1" ]]; then
    exit 1
  fi
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
echo "unexpected gh args: $*" >&2
exit 1
""",
            encoding="utf-8",
        )
        gh_script.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        return root, env

    def run_script(self, cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/gh_preflight.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_require_api_succeeds_when_auth_and_api_are_available(self) -> None:
        root, env = self.make_repo()
        result = self.run_script(root, env, "--require-api")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("origin/gh auth/API OK", result.stdout)

    def test_require_api_reports_sandbox_retry_hint_on_connect_error(self) -> None:
        root, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_API_FAIL"] = "1"
        result = self.run_script(root, env, "--require-api")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GitHub API 연결 확인에 실패했습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)


if __name__ == "__main__":
    unittest.main()
