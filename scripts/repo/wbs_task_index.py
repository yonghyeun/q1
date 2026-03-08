#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    yaml = None  # type: ignore[assignment]


EXIT_INVALID_INPUT = 70
EXIT_STALE_INDEX = 71
EXIT_UNSTAGED_CHANGES = 72
EXIT_GIT_ERROR = 73
EXIT_PARSE_ERROR = 74

MARKER_START = "<!-- wbs-task-summary:start -->"
MARKER_END = "<!-- wbs-task-summary:end -->"
TASKS_DIR_REL = Path("context/wbs/tasks")
INDEX_PATH_REL = TASKS_DIR_REL / "index.md"


class TaskIndexError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class RepoPaths:
    root: Path
    tasks_dir: Path
    index_path: Path


@dataclass(frozen=True)
class TaskSummary:
    slice_id: str
    file_name: str
    goal: str
    planning_status: str
    planned_flow: str | None
    run_id: str | None
    workspace_bindings: list[dict[str, Any]]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_paths(root: Path | None = None) -> RepoPaths:
    actual_root = root or repo_root()
    return RepoPaths(
        root=actual_root,
        tasks_dir=actual_root / TASKS_DIR_REL,
        index_path=actual_root / INDEX_PATH_REL,
    )


def run_git(paths: RepoPaths, *args: str, check: bool = True) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=paths.root,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise TaskIndexError("git 실행 파일을 찾을 수 없습니다.", EXIT_GIT_ERROR) from error

    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        detail = stderr or stdout or f"exit={result.returncode}"
        raise TaskIndexError(
            f"git 명령 실패 ({' '.join(args)}): {detail}",
            EXIT_GIT_ERROR,
        )

    return result.stdout


def ensure_yaml_available() -> None:
    if yaml is None:
        raise TaskIndexError(
            "PyYAML이 필요합니다. `python3 -c \"import yaml\"`가 성공하는 환경에서 실행하세요.",
            EXIT_INVALID_INPUT,
        )


def is_relevant_path(path_str: str) -> bool:
    normalized = path_str.strip()
    if not normalized:
        return False
    if normalized == INDEX_PATH_REL.as_posix():
        return True
    tasks_prefix = TASKS_DIR_REL.as_posix() + "/"
    return normalized.startswith(tasks_prefix) and normalized.endswith(".yaml")


def read_staged_paths(paths: RepoPaths) -> list[str]:
    output = run_git(paths, "ls-files", "--cached", "--full-name", "--", TASKS_DIR_REL.as_posix())
    return sorted(
        line.strip()
        for line in output.splitlines()
        if line.strip().endswith(".yaml") and is_relevant_path(line.strip())
    )


def parse_yaml_document(raw: str, source_name: str) -> dict[str, Any]:
    ensure_yaml_available()
    normalized = normalize_loose_yaml(raw)
    try:
        payload = yaml.safe_load(normalized)
    except yaml.YAMLError as error:  # type: ignore[union-attr]
        raise TaskIndexError(
            f"task YAML 파싱 실패: {source_name}: {error}",
            EXIT_PARSE_ERROR,
        ) from error

    if not isinstance(payload, dict):
        raise TaskIndexError(
            f"task YAML 최상위는 object 여야 합니다: {source_name}",
            EXIT_PARSE_ERROR,
        )

    return payload


def normalize_loose_yaml(raw: str) -> str:
    normalized_lines: list[str] = []
    pattern = re.compile(r"^(?P<prefix>\s*-\s+)(?P<value>`.+)$")

    for line in raw.splitlines():
        match = pattern.match(line)
        if not match:
            normalized_lines.append(line)
            continue

        value = match.group("value")
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        normalized_lines.append(f'{match.group("prefix")}"{escaped}"')

    suffix = "\n" if raw.endswith("\n") else ""
    return "\n".join(normalized_lines) + suffix


def require_string(payload: dict[str, Any], key: str, source_name: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TaskIndexError(
            f"task YAML 필수 문자열이 비어 있습니다: {source_name}: {key}",
            EXIT_PARSE_ERROR,
        )
    return value.strip()


def normalize_refs(payload: dict[str, Any], source_name: str) -> dict[str, Any]:
    refs = payload.get("refs", {})
    if refs is None:
        return {}
    if not isinstance(refs, dict):
        raise TaskIndexError(
            f"`refs`는 object 여야 합니다: {source_name}",
            EXIT_PARSE_ERROR,
        )
    return refs


def normalize_workspace_bindings(payload: dict[str, Any], source_name: str) -> list[dict[str, Any]]:
    bindings = payload.get("workspace_bindings", [])
    if bindings is None:
        return []
    if not isinstance(bindings, list):
        raise TaskIndexError(
            f"`workspace_bindings`는 list 여야 합니다: {source_name}",
            EXIT_PARSE_ERROR,
        )

    normalized: list[dict[str, Any]] = []
    for index, binding in enumerate(bindings, start=1):
        if not isinstance(binding, dict):
            raise TaskIndexError(
                f"`workspace_bindings[{index}]`는 object 여야 합니다: {source_name}",
                EXIT_PARSE_ERROR,
            )
        normalized.append(binding)
    return normalized


def build_task_summary(payload: dict[str, Any], source_name: str, file_name: str) -> TaskSummary:
    refs = normalize_refs(payload, source_name)
    workspace_bindings = normalize_workspace_bindings(payload, source_name)

    planned_flow = refs.get("planned_flow")
    if planned_flow is not None and not isinstance(planned_flow, str):
        raise TaskIndexError(
            f"`refs.planned_flow`는 문자열 또는 null 이어야 합니다: {source_name}",
            EXIT_PARSE_ERROR,
        )

    run_id = refs.get("run_id")
    if run_id is not None and not isinstance(run_id, str):
        raise TaskIndexError(
            f"`refs.run_id`는 문자열 또는 null 이어야 합니다: {source_name}",
            EXIT_PARSE_ERROR,
        )

    return TaskSummary(
        slice_id=require_string(payload, "slice_id", source_name),
        file_name=file_name,
        goal=require_string(payload, "goal", source_name),
        planning_status=require_string(payload, "planning_status", source_name),
        planned_flow=planned_flow.strip() if isinstance(planned_flow, str) and planned_flow.strip() else None,
        run_id=run_id.strip() if isinstance(run_id, str) and run_id.strip() else None,
        workspace_bindings=workspace_bindings,
    )


def load_tasks_from_working_tree(paths: RepoPaths) -> list[TaskSummary]:
    if not paths.tasks_dir.exists():
        raise TaskIndexError(
            f"tasks 디렉터리를 찾을 수 없습니다: {paths.tasks_dir}",
            EXIT_INVALID_INPUT,
        )

    task_summaries: list[TaskSummary] = []
    for file_path in sorted(paths.tasks_dir.glob("*.yaml")):
        source_name = file_path.relative_to(paths.root).as_posix()
        payload = parse_yaml_document(file_path.read_text(encoding="utf-8"), source_name)
        task_summaries.append(build_task_summary(payload, source_name, file_path.name))
    return validate_unique_slice_ids(task_summaries)


def load_tasks_from_staged(paths: RepoPaths) -> list[TaskSummary]:
    task_summaries: list[TaskSummary] = []
    for relative_path in read_staged_paths(paths):
        raw = run_git(paths, "show", f":{relative_path}")
        payload = parse_yaml_document(raw, relative_path)
        task_summaries.append(build_task_summary(payload, relative_path, Path(relative_path).name))
    return validate_unique_slice_ids(task_summaries)


def load_tasks(paths: RepoPaths, source: str) -> list[TaskSummary]:
    if source == "working-tree":
        return load_tasks_from_working_tree(paths)
    if source == "staged":
        return load_tasks_from_staged(paths)
    raise TaskIndexError(f"지원하지 않는 source 입니다: {source}", EXIT_INVALID_INPUT)


def validate_unique_slice_ids(tasks: list[TaskSummary]) -> list[TaskSummary]:
    seen: set[str] = set()
    for task in tasks:
        if task.slice_id in seen:
            raise TaskIndexError(
                f"중복 slice_id 가 있습니다: {task.slice_id}",
                EXIT_PARSE_ERROR,
            )
        seen.add(task.slice_id)
    return sorted(tasks, key=lambda task: task.slice_id)


def escape_table_text(value: str) -> str:
    compact = " ".join(value.strip().split())
    compact = compact.replace("|", r"\|")
    return compact


def render_repo_link(paths: RepoPaths, repo_relative: str, label: str | None = None) -> str:
    target = Path(repo_relative)
    if target.is_absolute():
        absolute_target = target
        display = label or repo_relative
    else:
        absolute_target = paths.root / target
        display = label or repo_relative

    relative_target = os.path.relpath(absolute_target, start=paths.index_path.parent)
    safe_label = escape_table_text(display)
    return f"[{safe_label}]({relative_target})"


def render_workspace_summary(bindings: list[dict[str, Any]]) -> str:
    rendered: list[str] = []
    for index, binding in enumerate(bindings, start=1):
        purpose = binding.get("purpose")
        branch = binding.get("branch")

        if purpose is not None and not isinstance(purpose, str):
            raise TaskIndexError(
                f"`workspace_bindings[{index}].purpose`는 문자열 또는 null 이어야 합니다.",
                EXIT_PARSE_ERROR,
            )
        if branch is not None and not isinstance(branch, str):
            raise TaskIndexError(
                f"`workspace_bindings[{index}].branch`는 문자열 또는 null 이어야 합니다.",
                EXIT_PARSE_ERROR,
            )

        if not isinstance(branch, str) or not branch.strip():
            continue

        branch_value = branch.strip().replace("`", r"\`")
        if isinstance(purpose, str) and purpose.strip():
            rendered.append(f"{escape_table_text(purpose)}: `{branch_value}`")
        else:
            rendered.append(f"`{branch_value}`")

    return ", ".join(rendered) if rendered else "-"


def render_table(paths: RepoPaths, tasks: list[TaskSummary]) -> str:
    lines = [
        "| slice_id | goal | planning_status | planned_flow | workspaces | run_id |",
        "|---|---|---|---|---|---|",
    ]

    for task in tasks:
        slice_cell = f"[{escape_table_text(task.slice_id)}](./{task.file_name})"
        goal_cell = escape_table_text(task.goal)
        planning_status_cell = escape_table_text(task.planning_status)
        planned_flow_cell = (
            render_repo_link(paths, task.planned_flow)
            if task.planned_flow
            else "-"
        )
        workspaces_cell = render_workspace_summary(task.workspace_bindings)
        run_id_cell = escape_table_text(task.run_id) if task.run_id else "-"
        lines.append(
            f"| {slice_cell} | {goal_cell} | {planning_status_cell} | "
            f"{planned_flow_cell} | {workspaces_cell} | {run_id_cell} |"
        )

    return "\n".join(lines)


def replace_marker_region(index_text: str, generated_table: str) -> str:
    start_count = index_text.count(MARKER_START)
    end_count = index_text.count(MARKER_END)
    if start_count != 1 or end_count != 1:
        raise TaskIndexError(
            "`index.md`에는 summary marker가 정확히 1쌍 있어야 합니다.",
            EXIT_INVALID_INPUT,
        )

    before, remainder = index_text.split(MARKER_START, maxsplit=1)
    middle, after = remainder.split(MARKER_END, maxsplit=1)
    if middle is None or after is None:
        raise TaskIndexError(
            "`index.md` marker 구간을 파싱할 수 없습니다.",
            EXIT_INVALID_INPUT,
        )

    generated_block = f"{MARKER_START}\n{generated_table.rstrip()}\n{MARKER_END}"
    return before + generated_block + after


def build_updated_index_text(paths: RepoPaths, source: str) -> str:
    if not paths.index_path.exists():
        raise TaskIndexError(
            f"`index.md`를 찾을 수 없습니다: {paths.index_path}",
            EXIT_INVALID_INPUT,
        )
    existing = paths.index_path.read_text(encoding="utf-8")
    table = render_table(paths, load_tasks(paths, source))
    return replace_marker_region(existing, table)


def write_index(paths: RepoPaths, updated_text: str) -> bool:
    current = paths.index_path.read_text(encoding="utf-8")
    if current == updated_text:
        return False
    paths.index_path.write_text(updated_text, encoding="utf-8")
    return True


def collect_changed_paths(paths: RepoPaths, staged: bool) -> list[str]:
    args = ["diff"]
    if staged:
        args.append("--cached")
    args.extend(["--name-only", "--", TASKS_DIR_REL.as_posix()])
    output = run_git(paths, *args)
    return [line.strip() for line in output.splitlines() if is_relevant_path(line)]


def stage_index_file(paths: RepoPaths) -> None:
    run_git(paths, "add", "--", INDEX_PATH_REL.as_posix())


def handle_generate(paths: RepoPaths, source: str, write: bool) -> int:
    updated_text = build_updated_index_text(paths, source)
    if write:
        changed = write_index(paths, updated_text)
        if changed:
            print(f"✅ WBS task index regenerated from {source}")
        else:
            print(f"✅ WBS task index already up to date ({source})")
        return 0

    table = render_table(paths, load_tasks(paths, source))
    print(table)
    return 0


def handle_check(paths: RepoPaths, source: str) -> int:
    current = paths.index_path.read_text(encoding="utf-8")
    expected = build_updated_index_text(paths, source)
    if current != expected:
        raise TaskIndexError(
            f"WBS task index 가 최신이 아닙니다. `python3 scripts/repo/wbs_task_index.py generate --source {source} --write`를 실행하세요.",
            EXIT_STALE_INDEX,
        )
    print(f"✅ WBS task index is up to date ({source})")
    return 0


def handle_pre_commit(paths: RepoPaths) -> int:
    staged_changes = collect_changed_paths(paths, staged=True)
    if not staged_changes:
        print("ℹ️ WBS task index pre-commit skipped: no staged task changes")
        return 0

    unstaged_changes = collect_changed_paths(paths, staged=False)
    if unstaged_changes:
        details = "\n- ".join(unstaged_changes)
        raise TaskIndexError(
            "WBS task 관련 unstaged 변경이 남아 있습니다. staged 기준 projection을 안전하게 만들 수 없습니다:\n- "
            + details,
            EXIT_UNSTAGED_CHANGES,
        )

    updated = build_updated_index_text(paths, "staged")
    changed = write_index(paths, updated)
    if changed:
        stage_index_file(paths)
        print("✅ WBS task index regenerated and staged")
    else:
        print("✅ WBS task index already staged and up to date")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate/check WBS task index projection")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate")
    generate.add_argument("--source", choices=["working-tree", "staged"], default="working-tree")
    generate.add_argument("--write", action="store_true")

    check = subparsers.add_parser("check")
    check.add_argument("--source", choices=["working-tree", "staged"], default="working-tree")

    subparsers.add_parser("pre-commit")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    paths = default_paths()

    if args.command == "generate":
        return handle_generate(paths, args.source, args.write)
    if args.command == "check":
        return handle_check(paths, args.source)
    if args.command == "pre-commit":
        return handle_pre_commit(paths)

    parser.error(f"unknown command: {args.command}")
    return EXIT_INVALID_INPUT


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TaskIndexError as error:
        print(f"❌ {error}", file=sys.stderr)
        raise SystemExit(error.exit_code)
