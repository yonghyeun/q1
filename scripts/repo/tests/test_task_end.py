from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPT_NAMES = [
    "task_end.sh",
    "task_end_interactive.sh",
    "pr_finalize.sh",
    "pr_merge.sh",
    "post_merge_branch_cleanup.sh",
    "post_merge_cleanup.sh",
    "worktree_cleanup.sh",
    "gh_preflight.sh",
    "branch_guard.py",
    "detached_head_guard.py",
    "protected_branch_write_guard.py",
    "dirty_worktree_guard.py",
    "worktree_config_bootstrap.sh",
    "worktree_issue_metadata.sh",
    "worktree_pr_metadata.sh",
]


class TaskEndTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path, Path, Path, dict[str, str]]:
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

        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(origin)], cwd=root, check=True)

        readme = root / "README.md"
        readme.write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md", "scripts/repo"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "base commit"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=root, check=True, capture_output=True)

        branch = "config/task-end-flow"
        subprocess.run(["git", "branch", branch], cwd=root, check=True, capture_output=True)

        worktree = workspace / "config-task-end-flow--impl"
        subprocess.run(["git", "worktree", "add", str(worktree), branch], cwd=root, check=True, capture_output=True)

        metadata_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_issue_metadata.sh",
                "write",
                "--number",
                "19",
                "--url",
                "https://example.test/issues/19",
                "--title",
                "Issue 19",
                "--status-at-record",
                "status:active",
                "--branch",
                branch,
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=False,
        )
        if metadata_result.returncode != 0:
            raise RuntimeError(metadata_result.stderr)

        pr_metadata_result = subprocess.run(
            [
                "bash",
                "./scripts/repo/worktree_pr_metadata.sh",
                "write",
                "--number",
                "42",
                "--url",
                "https://example.test/pull/42",
                "--title",
                "[config] task end test",
                "--state",
                "OPEN",
                "--base-branch",
                "main",
                "--head-branch",
                branch,
                "--worktree",
                str(worktree),
                "--recorded-at",
                "2026-03-11T15:00:00Z",
            ],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=False,
        )
        if pr_metadata_result.returncode != 0:
            raise RuntimeError(pr_metadata_result.stderr)

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
if [[ "$1" == "pr" && "$2" == "view" ]]; then
  shift 2
  target="${1:-}"
  shift || true
  jq_expr=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --json)
        shift 2
        ;;
      --jq)
        jq_expr="${2:-}"
        shift 2
        ;;
      *)
        shift
        ;;
    esac
  done
  case "${jq_expr}" in
    .number) echo "42" ;;
    .title) echo "[config] task end test" ;;
    *) : ;;
  esac
  exit 0
fi
if [[ "$1" == "pr" && "$2" == "merge" ]]; then
  printf '%s\\n' "$*" >> "${FAKE_GH_LOG}"
  exit 0
fi
if [[ "$1" == "issue" && "$2" == "view" ]]; then
  shift 2
  issue_number="${1:-}"
  state="${FAKE_GH_ISSUE_STATE:-CLOSED}"
  status="${FAKE_GH_ISSUE_STATUS:-status:active}"
  second_status="${FAKE_GH_SECOND_ISSUE_STATUS:-}"
  labels_json=""
  if [[ -n "${status}" ]]; then
    labels_json="{\\"name\\":\\"${status}\\"}"
  fi
  if [[ -n "${second_status}" ]]; then
    if [[ -n "${labels_json}" ]]; then
      labels_json="${labels_json},"
    fi
    labels_json="${labels_json}{\\"name\\":\\"${second_status}\\"}"
  fi
  printf '{"number":%s,"title":"Issue %s","url":"https://example.test/issues/%s","state":"%s","labels":[%s]}\\n' "${issue_number}" "${issue_number}" "${issue_number}" "${state}" "${labels_json}"
  exit 0
fi
if [[ "$1" == "issue" && "$2" == "edit" ]]; then
  printf '%s\\n' "$*" >> "${FAKE_GH_LOG}"
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

        return root, worktree, gh_log, env

    def run_script(
        self,
        cwd: Path,
        script_name: str,
        env: dict[str, str],
        *args: str,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", f"./scripts/repo/{script_name}", *args],
            cwd=cwd,
            env=env,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_default_is_dry_run(self) -> None:
        _root, worktree, _gh_log, env = self.make_repo()
        env = dict(env)
        env["PATH"] = env["PATH"].split(":", 1)[1]
        result = self.run_script(worktree, "task_end.sh", env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("task end 계획", result.stdout)
        self.assertIn("<PR_TITLE_FROM_GH>", result.stdout)
        self.assertIn("Linked issue: #19", result.stdout)
        self.assertIn("Issue close status cleanup: remove status:* after linked issue closes", result.stdout)

    def test_apply_requires_yes(self) -> None:
        _root, worktree, _gh_log, env = self.make_repo()
        result = self.run_script(worktree, "task_end.sh", env, "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--apply --yes", result.stderr)

    def test_apply_yes_flow_merges_and_cleans_up(self) -> None:
        root, worktree, gh_log, env = self.make_repo()
        result = self.run_script(worktree, "task_end.sh", env, "--apply", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(worktree.exists())

        branches = subprocess.run(
            ["git", "branch", "--list", "config/task-end-flow"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(branches, "")

        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(current_branch, "main")

        logged = gh_log.read_text(encoding="utf-8")
        self.assertIn("pr merge", logged)
        self.assertIn("--squash", logged)
        self.assertIn("[config] task end test", logged)
        self.assertNotIn("--delete-branch", logged)
        self.assertIn("issue edit 19 --remove-label status:active", logged)

    def test_apply_yes_clears_issue_metadata_when_worktree_is_kept(self) -> None:
        _root, worktree, _gh_log, env = self.make_repo()
        result = self.run_script(worktree, "task_end.sh", env, "--apply", "--yes", "--no-worktree-remove", "--no-branch-cleanup")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(worktree.exists())

        metadata = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.issue.number"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=False,
        ).stdout.strip()
        self.assertEqual(metadata, "")

        pr_metadata = subprocess.run(
            ["git", "config", "--worktree", "--get", "q1.pr.number"],
            cwd=worktree,
            text=True,
            capture_output=True,
            check=False,
        ).stdout.strip()
        self.assertEqual(pr_metadata, "")

    def test_apply_yes_stops_cleanup_when_linked_issue_is_not_closed(self) -> None:
        root, worktree, gh_log, env = self.make_repo()
        env = dict(env)
        env["FAKE_GH_ISSUE_STATE"] = "OPEN"

        result = self.run_script(worktree, "task_end.sh", env, "--apply", "--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("linked issue #19 가 닫히지 않았습니다", result.stderr)
        self.assertTrue(worktree.exists())

        branches = subprocess.run(
            ["git", "branch", "--list", "config/task-end-flow"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertIn("config/task-end-flow", branches)

        logged = gh_log.read_text(encoding="utf-8")
        self.assertIn("pr merge", logged)
        self.assertNotIn("issue edit 19", logged)

    def test_task_end_uses_branch_helper_scripts_when_primary_lacks_them(self) -> None:
        root, worktree, gh_log, env = self.make_repo()
        subprocess.run(["git", "switch", "main"], cwd=root, check=True, capture_output=True)
        subprocess.run(
            ["git", "rm", "scripts/repo/post_merge_branch_cleanup.sh", "scripts/repo/worktree_cleanup.sh"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "remove helper scripts from primary"],
            cwd=root,
            check=True,
            capture_output=True,
        )

        result = self.run_script(worktree, "task_end.sh", env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("task end 계획", result.stdout)

        apply_result = self.run_script(worktree, "task_end.sh", env, "--apply", "--yes")
        self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
        self.assertFalse(worktree.exists())
        self.assertIn("pr merge", gh_log.read_text(encoding="utf-8"))

    def test_interactive_wrapper_prompts_and_applies(self) -> None:
        root, worktree, gh_log, env = self.make_repo()
        result = self.run_script(worktree, "task_end_interactive.sh", env, input_text="y\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(worktree.exists())
        self.assertIn("Proceed? [y/N]", result.stdout)
        self.assertIn("task end 완료", result.stdout)
        self.assertIn("pr merge", gh_log.read_text(encoding="utf-8"))

    def test_interactive_wrapper_cancels_on_no(self) -> None:
        root, worktree, gh_log, env = self.make_repo()
        result = self.run_script(worktree, "task_end_interactive.sh", env, input_text="n\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(worktree.exists())
        self.assertIn("취소", result.stdout)
        self.assertFalse(gh_log.exists())


if __name__ == "__main__":
    unittest.main()
