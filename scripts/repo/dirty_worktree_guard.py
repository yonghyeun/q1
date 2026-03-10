#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import subprocess
import sys

EXIT_DIRTY_WORKTREE = 1


class DirtyWorktreeError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_DIRTY_WORKTREE) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class WorktreeDelta:
    staged: int
    unstaged: int
    untracked: int

    @property
    def total(self) -> int:
        return self.staged + self.unstaged + self.untracked


def porcelain_lines() -> list[str]:
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise DirtyWorktreeError(
            "Git working tree 상태를 확인할 수 없습니다.\n"
            "다음 행동: 저장소 루트와 git status 동작 여부를 확인한 뒤 다시 실행."
        ) from exc
    return [line for line in output.splitlines() if line.strip()]


def summarize(lines: list[str]) -> WorktreeDelta:
    staged = 0
    unstaged = 0
    untracked = 0

    for line in lines:
        if line.startswith("?? "):
            untracked += 1
            continue

        index_status = line[0]
        worktree_status = line[1]

        if index_status != " ":
            staged += 1
        if worktree_status != " ":
            unstaged += 1

    return WorktreeDelta(staged=staged, unstaged=unstaged, untracked=untracked)


def validate_clean_worktree() -> WorktreeDelta:
    delta = summarize(porcelain_lines())
    if delta.total == 0:
        return delta

    parts = []
    if delta.staged:
        parts.append(f"staged={delta.staged}")
    if delta.unstaged:
        parts.append(f"unstaged={delta.unstaged}")
    if delta.untracked:
        parts.append(f"untracked={delta.untracked}")

    raise DirtyWorktreeError(
        "더티 워크트리에서는 이 작업을 진행할 수 없습니다. "
        f"현재 상태: {', '.join(parts)}\n"
        "다음 행동: 변경사항을 commit/stash/정리해 clean 상태를 만든 뒤 helper 경로를 다시 실행."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate dirty worktree policy")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-clean", help="fail if worktree is dirty")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "validate-clean":
            validate_clean_worktree()
            print("✅ worktree clean")
            return 0

        parser.error(f"unknown command: {args.command}")
        return EXIT_DIRTY_WORKTREE
    except DirtyWorktreeError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
