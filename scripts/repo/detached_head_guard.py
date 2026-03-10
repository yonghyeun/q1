#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys

EXIT_DETACHED_HEAD = 1


class DetachedHeadError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def current_head_name() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise DetachedHeadError(
            "현재 HEAD 상태를 확인할 수 없습니다.\n"
            "다음 행동: Git 저장소 상태를 확인하고, HEAD가 유효한 브랜치를 가리키는지 점검.",
            EXIT_DETACHED_HEAD,
        ) from exc


def validate_not_detached(head_name: str) -> None:
    if not head_name or head_name == "HEAD":
        raise DetachedHeadError(
            "detached HEAD 상태에서는 쓰기 작업을 수행할 수 없습니다.\n"
            "다음 행동: 작업 브랜치로 switch 하거나 새 브랜치를 만든 뒤 다시 실행.",
            EXIT_DETACHED_HEAD,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Block writes on detached HEAD")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sub = subparsers.add_parser("validate-write")
    sub.add_argument("--head-name", help="HEAD name (default: current HEAD)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        head_name = args.head_name or current_head_name()

        if args.command == "validate-write":
            validate_not_detached(head_name)
            print(f"✅ detached HEAD check passed: {head_name}")
            return 0

        parser.error(f"unknown command: {args.command}")
        return EXIT_DETACHED_HEAD
    except DetachedHeadError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
