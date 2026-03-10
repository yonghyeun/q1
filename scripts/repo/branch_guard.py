#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import re
import subprocess
import sys

EXIT_INVALID_NAME = 1
BRANCH_REGEX = r"^(feature|fix|docs|config|chore|refactor|hotfix)/[a-z0-9]+(?:-[a-z0-9]+)*$"
RESERVED_BRANCHES = {"main"}


class BranchPolicyError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class BranchMeta:
    branch: str
    scope: str


def current_branch() -> str:
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise BranchPolicyError("현재 Git 브랜치를 확인할 수 없습니다.", EXIT_INVALID_NAME) from exc

    if not branch:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
            ).strip()
        )

    if not branch or branch == "HEAD":
        raise BranchPolicyError(
            "현재 브랜치를 판별할 수 없습니다(detached HEAD).",
            EXIT_INVALID_NAME,
        )

    return branch


def parse_scope(branch: str) -> str:
    if "/" not in branch:
        raise BranchPolicyError(
            f"브랜치 scope를 찾을 수 없습니다: {branch}\n"
            "다음 행동: `<scope>/<slug>` 형식의 정책 브랜치로 전환하거나 새 브랜치를 생성.",
            EXIT_INVALID_NAME,
        )
    return branch.split("/", 1)[0]


def parse_branch_meta(branch: str) -> BranchMeta:
    if branch in RESERVED_BRANCHES:
        raise BranchPolicyError(
            f"보호 브랜치({branch})에서 직접 작업할 수 없습니다.\n"
            "다음 행동: feature/fix/docs/config/chore/refactor/hotfix 중 하나의 작업 브랜치를 생성해 진행.",
            EXIT_INVALID_NAME,
        )

    if not re.fullmatch(BRANCH_REGEX, branch):
        raise BranchPolicyError(
            f"브랜치 이름이 정책과 다릅니다: {branch}\n허용 형식: {BRANCH_REGEX}",
            EXIT_INVALID_NAME,
        )

    return BranchMeta(branch=branch, scope=parse_scope(branch))


def validate_branch_name(branch: str) -> BranchMeta:
    try:
        return parse_branch_meta(branch)
    except BranchPolicyError as exc:
        if "허용 형식" in str(exc):
            raise BranchPolicyError(
                f"{exc}\n다음 행동: policies/branch-naming.md 규칙에 맞는 `<scope>/<slug>` 브랜치로 rename 또는 재생성.",
                EXIT_INVALID_NAME,
            ) from exc
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate branch policy")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ["validate-name"]:
        sub = subparsers.add_parser(name)
        sub.add_argument("--branch", help="branch name (default: current branch)")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        branch = args.branch or current_branch()

        if args.command == "validate-name":
            meta = validate_branch_name(branch)
            print(f"✅ branch name valid: {meta.branch} (scope={meta.scope})")
            return 0

        meta = validate_branch_name(branch)
        parser.error(f"unknown command: {args.command}")
        return EXIT_INVALID_NAME
    except BranchPolicyError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
