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
    "gh_preflight.sh",
    "pr_merge.sh",
    "branch_guard.py",
    "detached_head_guard.py",
    "protected_branch_write_guard.py",
    "dirty_worktree_guard.py",
]


class PrMergeRuntimeTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, dict[str, str]]:
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

        branch = "config/merge-runtime"
        subprocess.run(["git", "switch", "-c", branch], cwd=root, check=True, capture_output=True)

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
  echo "5000"
  exit 0
fi
if [[ "$1" == "pr" && "$2" == "view" ]]; then
  if [[ "${FAKE_GH_PR_VIEW_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
  if [[ "${@: -1}" == ".title" ]]; then
    echo "[config] runtime merge"
  else
    printf '{"number":42,"state":"OPEN","mergeStateStatus":"CLEAN","isDraft":false}\\n'
  fi
  exit 0
fi
if [[ "$1" == "pr" && "$2" == "merge" ]]; then
  if [[ "${FAKE_GH_PR_MERGE_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
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
            ["bash", "./scripts/repo/pr_merge.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_view_failure_shows_retry_hint(self) -> None:
        root, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_PR_VIEW_FAIL"] = "1"
        result = self.run_script(root, env, "--method", "squash")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("merge 대상 PR을 조회할 수 없습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)

    def test_merge_failure_shows_retry_hint(self) -> None:
        root, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_PR_MERGE_FAIL"] = "1"
        result = self.run_script(root, env, "--method", "squash", "--subject", "[config] runtime merge")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PR merge에 실패했습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)


if __name__ == "__main__":
    unittest.main()
