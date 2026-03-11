from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "worktree_config_bootstrap.sh",
    "worktree_pr_metadata.sh",
    "current_pr.sh",
    "gh_preflight.sh",
]


class CurrentPrTests(unittest.TestCase):
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

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", "https://example.test/repo.git"], cwd=root, check=True)

        worktree = workspace / "config-pr-number-metadata--impl"
        subprocess.run(
            ["git", "worktree", "add", str(worktree), "-b", "config/pr-number-metadata", "main"],
            cwd=root,
            check=True,
            capture_output=True,
        )

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
if [[ "$1" == "pr" && "$2" == "view" ]]; then
  if [[ "${FAKE_GH_PR_VIEW_FAIL:-0}" == "1" ]]; then
    echo "error connecting to api.github.com" >&2
    exit 1
  fi
  pr_number="${3:-}"
  python3 - "${pr_number}" <<'PY'
import json
import os
import sys

pr_number = sys.argv[1]
title = os.environ.get("FAKE_GH_PR_TITLE", f"PR {pr_number} live")
url = os.environ.get("FAKE_GH_PR_URL", f"https://example.test/pull/{pr_number}")
state = os.environ.get("FAKE_GH_PR_STATE", "OPEN")
is_draft = os.environ.get("FAKE_GH_PR_DRAFT", "false").lower() == "true"
base_ref = os.environ.get("FAKE_GH_PR_BASE", "main")
head_ref = os.environ.get("FAKE_GH_PR_HEAD", "config/pr-number-metadata")
print(json.dumps({"number": int(pr_number), "title": title, "url": url, "state": state, "isDraft": is_draft, "baseRefName": base_ref, "headRefName": head_ref}))
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
        return worktree, env

    def run_script(self, cwd: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "./scripts/repo/current_pr.sh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_prints_empty_message_when_metadata_missing(self) -> None:
        worktree, env = self.make_repo()
        result = self.run_script(worktree, env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("연결된 PR 없음", result.stdout)

    def test_prints_current_pr_from_metadata(self) -> None:
        worktree, env = self.make_repo()
        write_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_pr_metadata.sh",
                "write",
                "--number",
                "42",
                "--url",
                "https://example.test/pull/42",
                "--title",
                "pr title",
                "--state",
                "OPEN",
                "--base-branch",
                "main",
                "--head-branch",
                "config/pr-number-metadata",
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(write_result.returncode, 0, write_result.stderr)

        result = self.run_script(worktree, env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("- 번호: #42", result.stdout)
        self.assertIn("- 제목: pr title", result.stdout)
        self.assertIn("- 기록 state: OPEN", result.stdout)

    def test_live_mode_prints_current_github_state(self) -> None:
        worktree, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_PR_TITLE"] = "PR 42 live"
        env["FAKE_GH_PR_STATE"] = "MERGED"
        env["FAKE_GH_PR_DRAFT"] = "true"
        env["FAKE_GH_PR_BASE"] = "main"
        env["FAKE_GH_PR_HEAD"] = "config/pr-number-metadata"

        write_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_pr_metadata.sh",
                "write",
                "--number",
                "42",
                "--url",
                "https://example.test/pull/42",
                "--title",
                "pr title",
                "--state",
                "OPEN",
                "--base-branch",
                "main",
                "--head-branch",
                "config/pr-number-metadata",
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(write_result.returncode, 0, write_result.stderr)

        result = self.run_script(worktree, env, "--live")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("GitHub live 상태", result.stdout)
        self.assertIn("- 현재 state: MERGED", result.stdout)
        self.assertIn("- 현재 draft: True", result.stdout)
        self.assertIn("- 제목: PR 42 live", result.stdout)

    def test_live_mode_falls_back_to_snapshot_when_pr_view_fails(self) -> None:
        worktree, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_PR_VIEW_FAIL"] = "1"

        write_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_pr_metadata.sh",
                "write",
                "--number",
                "42",
                "--url",
                "https://example.test/pull/42",
                "--title",
                "pr title",
                "--state",
                "OPEN",
                "--head-branch",
                "config/pr-number-metadata",
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(write_result.returncode, 0, write_result.stderr)

        result = self.run_script(worktree, env, "--live")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("- 제목: pr title", result.stdout)
        self.assertIn("recorded snapshot만 표시", result.stdout)

    def test_live_mode_falls_back_to_snapshot_when_preflight_fails(self) -> None:
        worktree, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_AUTH_FAIL"] = "1"

        write_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_pr_metadata.sh",
                "write",
                "--number",
                "42",
                "--url",
                "https://example.test/pull/42",
                "--title",
                "pr title",
                "--state",
                "OPEN",
                "--head-branch",
                "config/pr-number-metadata",
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(write_result.returncode, 0, write_result.stderr)

        result = self.run_script(worktree, env, "--live")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("- 제목: pr title", result.stdout)
        self.assertIn("recorded snapshot만 표시", result.stdout)


if __name__ == "__main__":
    unittest.main()
