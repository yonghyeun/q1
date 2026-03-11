from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "task_start.sh",
    "task_start_interactive.sh",
    "worktree_add.sh",
    "gh_preflight.sh",
    "branch_guard.py",
    "worktree_name_guard.py",
    "worktree_config_bootstrap.sh",
    "worktree_issue_metadata.sh",
]


class TaskStartIntegrationTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path, Path, dict[str, str], Path]:
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

        origin = workspace / "origin.git"
        subprocess.run(["git", "init", "--bare", str(origin)], check=True, capture_output=True)
        self.origin = origin

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(origin)], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=root, check=True, capture_output=True)

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
if [[ "$1" == "issue" && "$2" == "view" ]]; then
  issue_number="${3:-}"
  python3 - "${issue_number}" <<'PY'
import json
import os
import sys

issue_number = sys.argv[1]
status = os.environ.get("FAKE_GH_ISSUE_STATUS", "status:inbox")
second_status = os.environ.get("FAKE_GH_SECOND_STATUS", "")
state = os.environ.get("FAKE_GH_ISSUE_STATE", "OPEN")
url = os.environ.get("FAKE_GH_ISSUE_URL", f"https://example.test/issues/{issue_number}")
title = os.environ.get("FAKE_GH_ISSUE_TITLE", f"Issue {issue_number}")

labels = [{"name": status}]
if second_status:
    labels.append({"name": second_status})

print(json.dumps({"number": int(issue_number), "title": title, "state": state, "url": url, "labels": labels}))
PY
  exit 0
fi
if [[ "$1" == "issue" && "$2" == "edit" ]]; then
  printf '%s\\n' "$*" > "${FAKE_GH_LOG}"
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

        return root, scripts_dir / "task_start.sh", scripts_dir / "task_start_interactive.sh", env, gh_log

    def advance_remote_branch(self, branch: str, filename: str = "REMOTE_STATE.txt") -> None:
        if not hasattr(self, "origin"):
            raise AssertionError("origin fixture is not initialized")

        clone_dir = self.origin.parent / f"remote-{branch.replace('/', '-')}"
        subprocess.run(
            ["git", "clone", "--branch", branch, "--single-branch", str(self.origin), str(clone_dir)],
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "config", "user.name", "Remote User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "remote@example.com"], cwd=clone_dir, check=True)

        target = clone_dir / filename
        previous = target.read_text(encoding="utf-8") if target.exists() else ""
        target.write_text(previous + f"{branch}\n", encoding="utf-8")
        subprocess.run(["git", "add", filename], cwd=clone_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"advance {branch}"], cwd=clone_dir, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", branch], cwd=clone_dir, check=True, capture_output=True)

    def run_script(
        self,
        cwd: Path,
        script_path: Path,
        *args: str,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(script_path), *args],
            cwd=cwd,
            text=True,
            input=input_text,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_default_is_dry_run(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        result = self.run_script(root, script, "--branch", "feature/signup-flow")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[git-task-start] Dry run", result.stdout)
        self.assertIn("브랜치: feature/signup-flow", result.stdout)
        self.assertIn("생성 예정 경로: ../signup-flow--impl", result.stdout)
        self.assertIn("다음 이동 경로", result.stdout)
        self.assertFalse((root.parent / "signup-flow--impl").exists())

    def test_apply_requires_yes(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        result = self.run_script(root, script, "--branch", "feature/signup-flow", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--apply --yes", result.stderr)

    def test_apply_yes_creates_branch_and_worktree(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        result = self.run_script(root, script, "--branch", "feature/signup-flow", "--apply", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((root.parent / "signup-flow--impl").exists())
        self.assertIn("다음 이동: cd ../signup-flow--impl", result.stdout)

        refs = subprocess.run(
            ["git", "show-ref", "--verify", "refs/heads/feature/signup-flow"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(refs.returncode, 0, refs.stderr)

    def test_invalid_branch_fails(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        result = self.run_script(root, script, "--branch", "task/signup-flow")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("브랜치 이름이 정책과 다릅니다", result.stderr)

    def test_existing_branch_reuse_is_shown_in_plan(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        subprocess.run(
            ["git", "branch", "feature/signup-flow", "main"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        result = self.run_script(root, script, "--branch", "feature/signup-flow")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("기존 branch `feature/signup-flow` 재사용", result.stdout)

    def test_fails_when_base_branch_is_behind_origin(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        self.advance_remote_branch("main")

        result = self.run_script(root, script, "--branch", "feature/signup-flow")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("기준 branch `main` 가 원격 ref `origin/main` 와 일치하지 않습니다", result.stderr)

    def test_fails_when_existing_branch_is_behind_origin(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        branch = "fix/task-start-upstream-freshness"
        subprocess.run(["git", "branch", branch, "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "push", "-u", "origin", f"{branch}:{branch}"], cwd=root, check=True, capture_output=True)
        self.advance_remote_branch(branch, filename="REMOTE_BRANCH_STATE.txt")

        result = self.run_script(root, script, "--branch", branch)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"재사용 branch `{branch}` 가 원격 ref `origin/{branch}` 보다 뒤처져 있습니다", result.stderr)

    def test_fails_when_branch_is_checked_out_in_other_worktree(self) -> None:
        root, script, _interactive, _env, _gh_log = self.make_repo()
        other_worktree = root.parent / "existing-signup-flow"
        subprocess.run(
            ["git", "worktree", "add", "-b", "feature/signup-flow", str(other_worktree), "main"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        result = self.run_script(root, script, "--branch", "feature/signup-flow")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("이미 checkout 중입니다", result.stderr)
        self.assertIn(str(other_worktree), result.stderr)

    def test_issue_dry_run_shows_status_transition(self) -> None:
        root, script, _interactive, env, _gh_log = self.make_repo()
        result = self.run_script(root, script, "--branch", "chore/task-start-issue-transition", "--issue", "15", env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("연결 이슈: #15", result.stdout)
        self.assertIn("현재 이슈 상태: status:inbox", result.stdout)
        self.assertIn("apply 시 이슈 상태: status:inbox -> status:active", result.stdout)

    def test_issue_apply_updates_status_label(self) -> None:
        root, script, _interactive, env, gh_log = self.make_repo()
        result = self.run_script(
            root,
            script,
            "--branch",
            "chore/task-start-issue-transition",
            "--issue",
            "15",
            "--apply",
            "--yes",
            env=env,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((root.parent / "task-start-issue-transition--impl").exists())
        logged = gh_log.read_text(encoding="utf-8")
        self.assertIn("issue edit 15", logged)
        self.assertIn("--remove-label status:inbox", logged)
        self.assertIn("--add-label status:active", logged)

        linked_worktree = root.parent / "task-start-issue-transition--impl"
        number = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.issue.number"],
            cwd=linked_worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        title = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.issue.title"],
            cwd=linked_worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.issue.branch"],
            cwd=linked_worktree,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(number, "15")
        self.assertEqual(title, "Issue 15")
        self.assertEqual(branch, "chore/task-start-issue-transition")

    def test_issue_fails_when_multiple_status_labels_exist(self) -> None:
        root, script, _interactive, env, _gh_log = self.make_repo()
        env = dict(env)
        env["FAKE_GH_SECOND_STATUS"] = "status:ready"
        result = self.run_script(root, script, "--branch", "chore/task-start-issue-transition", "--issue", "15", env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("status label이 여러 개", result.stderr)

    def test_issue_fails_with_api_retry_hint_when_preflight_detects_network_block(self) -> None:
        root, script, _interactive, env, _gh_log = self.make_repo()
        env = dict(env)
        env["FAKE_GH_API_FAIL"] = "1"
        result = self.run_script(root, script, "--branch", "chore/task-start-issue-transition", "--issue", "15", env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GitHub API 연결 확인에 실패했습니다", result.stderr)
        self.assertIn("sandbox/network", result.stderr)
        self.assertIn("권한 상승으로 재실행", result.stderr)

    def test_interactive_wrapper_prompts_and_applies(self) -> None:
        root, _script, interactive, _env, _gh_log = self.make_repo()
        result = self.run_script(root, interactive, "--branch", "feature/signup-flow", input_text="y\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Proceed? [y/N]", result.stdout)
        self.assertIn("task start 완료", result.stdout)
        self.assertTrue((root.parent / "signup-flow--impl").exists())

    def test_interactive_wrapper_cancels_on_no(self) -> None:
        root, _script, interactive, _env, _gh_log = self.make_repo()
        result = self.run_script(root, interactive, "--branch", "feature/signup-flow", input_text="n\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("취소", result.stdout)
        self.assertFalse((root.parent / "signup-flow--impl").exists())


if __name__ == "__main__":
    unittest.main()
