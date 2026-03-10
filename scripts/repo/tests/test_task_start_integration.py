from __future__ import annotations

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
    "branch_guard.py",
    "worktree_name_guard.py",
]


class TaskStartIntegrationTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, Path, Path]:
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
        return root, scripts_dir / "task_start.sh", scripts_dir / "task_start_interactive.sh"

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
        root, script, _interactive = self.make_repo()
        result = self.run_script(root, script, "--branch", "feature/signup-flow")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[git-task-start] Dry run", result.stdout)
        self.assertIn("브랜치: feature/signup-flow", result.stdout)
        self.assertIn("생성 예정 경로: ../signup-flow--impl", result.stdout)
        self.assertIn("다음 이동 경로", result.stdout)
        self.assertFalse((root.parent / "signup-flow--impl").exists())

    def test_apply_requires_yes(self) -> None:
        root, script, _interactive = self.make_repo()
        result = self.run_script(root, script, "--branch", "feature/signup-flow", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--apply --yes", result.stderr)

    def test_apply_yes_creates_branch_and_worktree(self) -> None:
        root, script, _interactive = self.make_repo()
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
        root, script, _interactive = self.make_repo()
        result = self.run_script(root, script, "--branch", "task/signup-flow")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("브랜치 이름이 정책과 다릅니다", result.stderr)

    def test_existing_branch_reuse_is_shown_in_plan(self) -> None:
        root, script, _interactive = self.make_repo()
        subprocess.run(
            ["git", "branch", "feature/signup-flow", "main"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        result = self.run_script(root, script, "--branch", "feature/signup-flow")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("기존 branch `feature/signup-flow` 재사용", result.stdout)

    def test_fails_when_branch_is_checked_out_in_other_worktree(self) -> None:
        root, script, _interactive = self.make_repo()
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

    def test_interactive_wrapper_prompts_and_applies(self) -> None:
        root, _script, interactive = self.make_repo()
        result = self.run_script(root, interactive, "--branch", "feature/signup-flow", input_text="y\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Proceed? [y/N]", result.stdout)
        self.assertIn("task start 완료", result.stdout)
        self.assertTrue((root.parent / "signup-flow--impl").exists())

    def test_interactive_wrapper_cancels_on_no(self) -> None:
        root, _script, interactive = self.make_repo()
        result = self.run_script(root, interactive, "--branch", "feature/signup-flow", input_text="n\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("취소", result.stdout)
        self.assertFalse((root.parent / "signup-flow--impl").exists())


if __name__ == "__main__":
    unittest.main()
