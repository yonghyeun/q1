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
