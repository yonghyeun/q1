#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys

EXIT_PROTECTED_BRANCH = 1
PROTECTED_BRANCHES = {"main"}


class ProtectedBranchWriteError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def current_branch() -> str:
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise ProtectedBranchWriteError(
            "현재 Git 브랜치를 확인할 수 없습니다.",
            EXIT_PROTECTED_BRANCH,
        ) from exc

    if not branch:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
            ).strip()
        )

    if not branch or branch == "HEAD":
        raise ProtectedBranchWriteError(
            "현재 브랜치를 판별할 수 없습니다(detached HEAD).\n"
            "다음 행동: detached HEAD를 해소한 뒤 작업 브랜치에서 다시 실행.",
            EXIT_PROTECTED_BRANCH,
        )

    return branch


def validate_protected_branch_write(branch: str) -> None:
    if branch in PROTECTED_BRANCHES:
        raise ProtectedBranchWriteError(
            f"보호 브랜치({branch})에서 직접 쓰기 작업을 수행할 수 없습니다.\n"
            "다음 행동: 작업 브랜치를 생성하거나 전환한 뒤 helper/script 경로를 다시 실행.",
            EXIT_PROTECTED_BRANCH,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Block writes on protected branches")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sub = subparsers.add_parser("validate-write")
    sub.add_argument("--branch", help="branch name (default: current branch)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        branch = args.branch or current_branch()

        if args.command == "validate-write":
            validate_protected_branch_write(branch)
            print(f"✅ protected branch write check passed: {branch}")
            return 0

        parser.error(f"unknown command: {args.command}")
        return EXIT_PROTECTED_BRANCH
    except ProtectedBranchWriteError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
