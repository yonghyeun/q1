#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

EXIT_INVALID_NAME = 1
WORKTREE_NAME_REGEX = r"^(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)--(?P<purpose>impl|review|fix|verify|docs|ops)$"


class WorktreeNameError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_INVALID_NAME) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class WorktreeMeta:
    name: str
    slug: str
    purpose: str
    branch: str


def current_branch() -> str:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        text=True,
    ).strip()
    if not branch:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
        ).strip()
    if not branch or branch == "HEAD":
        raise WorktreeNameError(
            "현재 브랜치를 확인할 수 없습니다.\n"
            "다음 행동: scoped branch에서 실행하거나 `--branch`로 대상 브랜치를 명시."
        )
    return branch


def branch_slug(branch: str) -> str:
    if "/" not in branch:
        raise WorktreeNameError(
            f"브랜치 slug를 추출할 수 없습니다: {branch}\n"
            "다음 행동: `<scope>/<slug>` 형식의 브랜치를 사용하거나 `--branch` 값을 수정."
        )
    return branch.split("/", 1)[1]


def parse_worktree_name(name: str) -> tuple[str, str]:
    match = re.fullmatch(WORKTREE_NAME_REGEX, name)
    if not match:
        raise WorktreeNameError(
            f"worktree 이름이 정책과 다릅니다: {name}\n"
            "허용 형식: <branch-slug>--<purpose>\n"
            "다음 행동: policies/worktree-naming.md 규칙에 맞는 path basename으로 수정."
        )
    return match.group("slug"), match.group("purpose")


def validate_worktree_name(name: str, branch: str) -> WorktreeMeta:
    slug, purpose = parse_worktree_name(name)
    expected_slug = branch_slug(branch)
    if slug != expected_slug:
        raise WorktreeNameError(
            f"worktree slug가 현재 branch와 다릅니다: {slug} != {expected_slug}\n"
            "다음 행동: worktree 이름의 slug를 브랜치 slug와 일치시키거나 `--branch`를 올바르게 지정."
        )
    return WorktreeMeta(name=name, slug=slug, purpose=purpose, branch=branch)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate worktree naming policy")
    parser.add_argument("path", help="target worktree path")
    parser.add_argument(
        "--branch",
        help="branch name to validate against (default: current branch)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        branch = args.branch or current_branch()
        name = Path(args.path).name
        meta = validate_worktree_name(name, branch)
        print(
            f"✅ worktree name valid: {meta.name} "
            f"(branch={meta.branch}, purpose={meta.purpose})"
        )
        return 0
    except WorktreeNameError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
