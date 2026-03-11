#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from body_guard_common import BodyQualityError, with_next_action  # type: ignore
from issue_label_taxonomy import (  # type: ignore
    AREA_VALUES,
    PRIORITY_VALUES,
    SOURCE_TYPE_VALUES,
    STATUS_VALUES,
    TYPE_VALUES,
)


def _validate_single_axis(name: str, value: str, allowed: set[str]) -> str:
    if value in allowed:
        return value

    joined = ", ".join(sorted(allowed))
    raise BodyQualityError(
        with_next_action(
            f"{name} 값이 허용 목록에 없습니다: {value}",
            f"{name}를 {joined} 중 하나로 다시 지정.",
        )
    )


def build_issue_labels(
    issue_type: str,
    status: str,
    priority: str,
    areas: list[str],
    source_type: str,
) -> list[str]:
    canonical_type = _validate_single_axis("type", issue_type, TYPE_VALUES)
    canonical_status = _validate_single_axis("status", status, STATUS_VALUES)
    canonical_priority = _validate_single_axis("priority", priority, PRIORITY_VALUES)
    canonical_source_type = _validate_single_axis(
        "source_type",
        source_type,
        SOURCE_TYPE_VALUES,
    )

    if not areas:
        raise BodyQualityError(
            with_next_action(
                "area가 비어 있습니다.",
                "최소 하나 이상의 --area 값을 전달.",
            )
        )

    canonical_areas: list[str] = []
    seen_areas: set[str] = set()
    for area in areas:
        canonical_area = _validate_single_axis("area", area, AREA_VALUES)
        if canonical_area in seen_areas:
            continue
        seen_areas.add(canonical_area)
        canonical_areas.append(canonical_area)

    labels = [
        f"type:{canonical_type}",
        f"status:{canonical_status}",
        f"priority:{canonical_priority}",
        f"source_type:{canonical_source_type}",
    ]
    labels.extend(f"area:{area}" for area in canonical_areas)
    return labels


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue label taxonomy guard")
    parser.add_argument("--type", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--priority", required=True)
    parser.add_argument("--area", action="append", default=[])
    parser.add_argument("--source-type", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    labels = build_issue_labels(
        issue_type=args.type,
        status=args.status,
        priority=args.priority,
        areas=args.area,
        source_type=args.source_type,
    )
    for label in labels:
        print(label)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BodyQualityError as error:
        print(f"❌ {error}", file=sys.stderr)
        raise SystemExit(41)
