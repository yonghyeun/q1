#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

EXIT_INVALID_NAME = 1
EXIT_CONTEXT_MISSING = 2
EXIT_ARTIFACT_MISSING = 3


class BranchPolicyError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class BranchMeta:
    branch: str
    issue_token: str
    issue_number: str
    task_id: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_rules_path() -> Path:
    return repo_root() / "policies/branch-policy.rules.json"


def load_rules(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required_keys = [
        "branch_regex",
        "issue_token_regex",
        "task_id_regex",
        "reserved_branches",
        "required_context_for_push",
        "required_artifacts_for_pr",
    ]
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise BranchPolicyError(
            f"branch 정책 파일에 필수 키가 없습니다: {', '.join(missing)}",
            EXIT_INVALID_NAME,
        )
    return data


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


def parse_task_id(branch: str, task_id_regex: str) -> str:
    match = re.search(r"T-\d{4}", branch)
    if not match:
        raise BranchPolicyError(
            f"브랜치에서 task-id를 찾을 수 없습니다: {branch}",
            EXIT_INVALID_NAME,
        )
    task_id = match.group(0)
    if not re.fullmatch(task_id_regex, task_id):
        raise BranchPolicyError(
            f"task-id 형식이 정책과 다릅니다: {task_id}",
            EXIT_INVALID_NAME,
        )
    return task_id


def parse_issue_token(branch: str, issue_token_regex: str) -> tuple[str, str]:
    match = re.search(r"i\d+", branch)
    if not match:
        raise BranchPolicyError(
            f"브랜치에서 issue 토큰을 찾을 수 없습니다: {branch}",
            EXIT_INVALID_NAME,
        )

    issue_token = match.group(0)
    if not re.fullmatch(issue_token_regex, issue_token):
        raise BranchPolicyError(
            f"issue 토큰 형식이 정책과 다릅니다: {issue_token}",
            EXIT_INVALID_NAME,
        )

    issue_number = issue_token.removeprefix("i")
    if not issue_number:
        raise BranchPolicyError(
            f"issue 번호를 파싱할 수 없습니다: {issue_token}",
            EXIT_INVALID_NAME,
        )

    return issue_token, issue_number


def parse_branch_meta(branch: str, rules: dict[str, Any]) -> BranchMeta:
    reserved = set(rules["reserved_branches"])
    if branch in reserved:
        raise BranchPolicyError(
            f"보호 브랜치({branch})에서 직접 작업할 수 없습니다.",
            EXIT_INVALID_NAME,
        )

    branch_regex = rules["branch_regex"]
    if not re.fullmatch(branch_regex, branch):
        raise BranchPolicyError(
            f"브랜치 이름이 정책과 다릅니다: {branch}\n허용 형식: {branch_regex}",
            EXIT_INVALID_NAME,
        )

    issue_token, issue_number = parse_issue_token(branch, rules["issue_token_regex"])
    task_id = parse_task_id(branch, rules["task_id_regex"])
    return BranchMeta(
        branch=branch,
        issue_token=issue_token,
        issue_number=issue_number,
        task_id=task_id,
    )


def validate_branch_name(branch: str, rules: dict[str, Any]) -> BranchMeta:
    return parse_branch_meta(branch, rules)


def validate_context(task_id: str, rules: dict[str, Any]) -> None:
    missing: list[str] = []
    root = repo_root()
    templates: list[str] = rules["required_context_for_push"]

    for template in templates:
        rel_path = template.format(task_id=task_id)
        target = root / rel_path
        if not target.exists():
            missing.append(rel_path)

    if missing:
        raise BranchPolicyError(
            "푸시 전 필수 컨텍스트가 누락되었습니다:\n- " + "\n- ".join(missing),
            EXIT_CONTEXT_MISSING,
        )


def validate_pr_artifacts(task_id: str, rules: dict[str, Any]) -> None:
    root = repo_root()
    task_dir = root / "context" / "tasks" / task_id
    required: list[str] = rules["required_artifacts_for_pr"]
    missing: list[str] = []

    for artifact in required:
        target = task_dir / artifact
        if not target.exists():
            missing.append(str(target.relative_to(root)))

    if missing:
        raise BranchPolicyError(
            "PR 필수 파일이 누락되었습니다:\n- " + "\n- ".join(missing),
            EXIT_ARTIFACT_MISSING,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate branch policy")
    parser.add_argument(
        "--rules",
        default=str(default_rules_path()),
        help="branch policy JSON path",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ["validate-name", "validate-context", "validate-pr"]:
        sub = subparsers.add_parser(name)
        sub.add_argument("--branch", help="branch name (default: current branch)")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    rules_path = Path(args.rules)

    try:
        rules = load_rules(rules_path)
        branch = args.branch or current_branch()

        if args.command == "validate-name":
            meta = validate_branch_name(branch, rules)
            print(
                "✅ branch name valid: "
                f"{branch} (issue={meta.issue_token}, task_id={meta.task_id})"
            )
            return 0

        meta = validate_branch_name(branch, rules)
        if args.command == "validate-context":
            validate_context(meta.task_id, rules)
            print(
                "✅ branch context valid: "
                f"{branch} -> issue={meta.issue_number}, task_id={meta.task_id}"
            )
            return 0

        if args.command == "validate-pr":
            validate_context(meta.task_id, rules)
            validate_pr_artifacts(meta.task_id, rules)
            print(
                "✅ PR gate artifacts valid: "
                f"{branch} -> issue={meta.issue_number}, task_id={meta.task_id}"
            )
            return 0

        parser.error(f"unknown command: {args.command}")
        return EXIT_INVALID_NAME
    except BranchPolicyError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
