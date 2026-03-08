from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wbs_task_index  # noqa: E402


INDEX_TEMPLATE = """# WBS Task Index

설명 문단은 marker 밖에 있다.

## Task Summary

정확한 branch/worktree path는 각 task YAML이 정본이며,
이 표는 workspace 요약만 보여준다.

<!-- wbs-task-summary:start -->
| stale | stale |
|---|---|
| old | old |
<!-- wbs-task-summary:end -->

footer text
"""


TASK_ONE = """slice_id: MVP-ALPHA
parent_wbs: mvp-wbs/v1
planning_status: ready_for_flow
goal: 사용자가 | 문자를 포함한 목표를 볼 수 있다.
why: 설명
contracts:
  - docs/product/contracts/domain.ts
acceptance_criteria:
  - 확인 가능하다
owned_scope:
  - 경계
verification_requirements:
  - 단위 검증 증거 필요
dependencies: []
non_goals: []
risks: []
assumptions: []
open_questions: []
workspace_bindings:
  - purpose: 구현
    branch: feat/mvp-alpha
    worktree: /worktrees/q1-mvp-alpha
refs:
  planned_flow: context/wbs/flows/MVP-ALPHA.md
  run_id: RUN-2026-03-07-A
  related_docs: []
notes: []
"""


TASK_TWO = """slice_id: MVP-BETA
parent_wbs: mvp-wbs/v1
planning_status: planned
goal: 사용자가 두 번째 작업을 본다.
why: 설명
contracts:
  - docs/product/contracts/domain.ts
acceptance_criteria:
  - 확인 가능하다
owned_scope:
  - 경계
verification_requirements:
  - 단위 검증 증거 필요
dependencies: []
non_goals: []
risks: []
assumptions: []
open_questions: []
workspace_bindings: []
refs:
  planned_flow: null
  run_id: null
  related_docs: []
notes: []
"""


class WbsTaskIndexTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, wbs_task_index.RepoPaths]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        root = Path(temp_dir.name)
        tasks_dir = root / "context/wbs/tasks"
        flows_dir = root / "context/wbs/flows"
        tasks_dir.mkdir(parents=True)
        flows_dir.mkdir(parents=True)
        (flows_dir / "MVP-ALPHA.md").write_text("# flow\n", encoding="utf-8")
        (tasks_dir / "index.md").write_text(INDEX_TEMPLATE, encoding="utf-8")
        (tasks_dir / "MVP-ALPHA.yaml").write_text(TASK_ONE, encoding="utf-8")
        (tasks_dir / "MVP-BETA.yaml").write_text(TASK_TWO, encoding="utf-8")

        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, capture_output=True)

        return root, wbs_task_index.default_paths(root)

    def test_render_table_escapes_goal_and_renders_links(self) -> None:
        _, paths = self.make_repo()
        tasks = wbs_task_index.load_tasks(paths, "working-tree")

        table = wbs_task_index.render_table(paths, tasks)

        self.assertIn(r"사용자가 \| 문자를 포함한 목표를 볼 수 있다.", table)
        self.assertIn("[context/wbs/flows/MVP-ALPHA.md](../flows/MVP-ALPHA.md)", table)
        self.assertIn("구현: `feat/mvp-alpha`", table)
        self.assertIn("| [MVP-BETA](./MVP-BETA.yaml) |", table)

    def test_build_updated_index_preserves_text_outside_marker(self) -> None:
        _, paths = self.make_repo()

        updated = wbs_task_index.build_updated_index_text(paths, "working-tree")

        self.assertIn("설명 문단은 marker 밖에 있다.", updated)
        self.assertIn("footer text", updated)
        self.assertIn(wbs_task_index.MARKER_START, updated)
        self.assertIn(wbs_task_index.MARKER_END, updated)
        self.assertNotIn("| old | old |", updated)

    def test_check_passes_when_index_is_current(self) -> None:
        _, paths = self.make_repo()
        updated = wbs_task_index.build_updated_index_text(paths, "working-tree")
        paths.index_path.write_text(updated, encoding="utf-8")

        exit_code = wbs_task_index.handle_check(paths, "working-tree")

        self.assertEqual(exit_code, 0)

    def test_check_rejects_stale_index(self) -> None:
        _, paths = self.make_repo()

        with self.assertRaises(wbs_task_index.TaskIndexError) as ctx:
            wbs_task_index.handle_check(paths, "working-tree")

        self.assertEqual(ctx.exception.exit_code, wbs_task_index.EXIT_STALE_INDEX)

    def test_check_rejects_missing_marker(self) -> None:
        _, paths = self.make_repo()
        paths.index_path.write_text("# broken\n", encoding="utf-8")

        with self.assertRaises(wbs_task_index.TaskIndexError) as ctx:
            wbs_task_index.handle_check(paths, "working-tree")

        self.assertEqual(ctx.exception.exit_code, wbs_task_index.EXIT_INVALID_INPUT)

    def test_normalize_loose_yaml_supports_backtick_prefixed_list_items(self) -> None:
        raw = "acceptance_criteria:\n  - `timestamp_inserted` 이벤트를 남길 수 있다.\n"

        payload = wbs_task_index.parse_yaml_document(raw, "inline")

        self.assertEqual(
            payload["acceptance_criteria"],
            ["`timestamp_inserted` 이벤트를 남길 수 있다."],
        )

    def test_pre_commit_skips_without_relevant_staged_changes(self) -> None:
        _, paths = self.make_repo()

        exit_code = wbs_task_index.handle_pre_commit(paths)

        self.assertEqual(exit_code, 0)

    def test_pre_commit_regenerates_and_stages_index_for_staged_yaml(self) -> None:
        root, paths = self.make_repo()
        subprocess.run(
            ["git", "add", "context/wbs/tasks/MVP-ALPHA.yaml", "context/wbs/tasks/MVP-BETA.yaml", "context/wbs/tasks/index.md"],
            cwd=root,
            check=True,
            capture_output=True,
        )

        exit_code = wbs_task_index.handle_pre_commit(paths)
        staged_index = subprocess.run(
            ["git", "show", ":context/wbs/tasks/index.md"],
            cwd=root,
            text=True,
            check=True,
            capture_output=True,
        ).stdout

        self.assertEqual(exit_code, 0)
        self.assertIn("[MVP-ALPHA](./MVP-ALPHA.yaml)", staged_index)
        self.assertNotIn("| old | old |", staged_index)

    def test_pre_commit_blocks_when_relevant_unstaged_changes_exist(self) -> None:
        root, paths = self.make_repo()
        subprocess.run(
            ["git", "add", "context/wbs/tasks/MVP-ALPHA.yaml", "context/wbs/tasks/MVP-BETA.yaml", "context/wbs/tasks/index.md"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        (root / "context/wbs/tasks/MVP-BETA.yaml").write_text(
            TASK_TWO.replace("planned", "planning_blocked"),
            encoding="utf-8",
        )

        with self.assertRaises(wbs_task_index.TaskIndexError) as ctx:
            wbs_task_index.handle_pre_commit(paths)

        self.assertEqual(ctx.exception.exit_code, wbs_task_index.EXIT_UNSTAGED_CHANGES)

    def test_pre_commit_uses_staged_snapshot_for_added_and_deleted_tasks(self) -> None:
        root, paths = self.make_repo()
        (root / "context/wbs/tasks/MVP-GAMMA.yaml").write_text(
            TASK_TWO.replace("MVP-BETA", "MVP-GAMMA").replace("두 번째", "세 번째"),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "git",
                "add",
                "context/wbs/tasks/index.md",
                "context/wbs/tasks/MVP-ALPHA.yaml",
                "context/wbs/tasks/MVP-BETA.yaml",
                "context/wbs/tasks/MVP-GAMMA.yaml",
            ],
            cwd=root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "rm", "--cached", "--force", "context/wbs/tasks/MVP-BETA.yaml"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        (root / "context/wbs/tasks/MVP-BETA.yaml").unlink()

        exit_code = wbs_task_index.handle_pre_commit(paths)
        staged_index = subprocess.run(
            ["git", "show", ":context/wbs/tasks/index.md"],
            cwd=root,
            text=True,
            check=True,
            capture_output=True,
        ).stdout

        self.assertEqual(exit_code, 0)
        self.assertIn("[MVP-GAMMA](./MVP-GAMMA.yaml)", staged_index)
        self.assertNotIn("[MVP-BETA](./MVP-BETA.yaml)", staged_index)


if __name__ == "__main__":
    unittest.main()
