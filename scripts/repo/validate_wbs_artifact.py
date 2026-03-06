#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


EXIT_INVALID_INPUT = 60
EXIT_INVALID_JSON = 61
EXIT_SCHEMA_VIOLATION = 62
EXIT_SEMANTIC_VIOLATION = 63

KIND_TO_SCHEMA = {
    "handoff-packet": "context/wbs/schemas/handoff-packet.schema.json",
    "trace-summary": "context/wbs/schemas/trace-summary.schema.json",
    "operator-decision": "context/wbs/schemas/operator-decision.schema.json",
    "run-ledger": "context/wbs/schemas/run-ledger.schema.json",
}


class WbsArtifactError(Exception):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_json(path: Path) -> object:
    if not path.exists():
        raise WbsArtifactError(f"artifact 파일을 찾을 수 없습니다: {path}", EXIT_INVALID_INPUT)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise WbsArtifactError(f"JSON 파싱 실패: {path}: {error}", EXIT_INVALID_JSON) from error


def load_schema(kind: str) -> dict:
    schema_path = repo_root() / KIND_TO_SCHEMA[kind]
    return load_json(schema_path)  # type: ignore[return-value]


def validate_against_schema(kind: str, payload: object) -> None:
    schema = load_schema(kind)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if not errors:
        return

    formatted: list[str] = []
    for error in errors:
        path = ".".join(str(part) for part in error.path) or "<root>"
        formatted.append(f"{path}: {error.message}")
    message = "; ".join(formatted)
    raise WbsArtifactError(f"schema 위반: {message}", EXIT_SCHEMA_VIOLATION)


def ensure_object(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise WbsArtifactError("artifact 최상위는 object 여야 합니다.", EXIT_SCHEMA_VIOLATION)
    return payload


def validate_handoff_semantics(payload: object) -> None:
    data = ensure_object(payload)
    if data["handoff_from"] == data["handoff_to"]:
        raise WbsArtifactError("handoff_from 과 handoff_to 는 같을 수 없습니다.", EXIT_SEMANTIC_VIOLATION)
    if data.get("supersedes_packet_id") == data["packet_id"]:
        raise WbsArtifactError(
            "supersedes_packet_id 는 packet_id 와 같을 수 없습니다.",
            EXIT_SEMANTIC_VIOLATION,
        )


def validate_trace_semantics(payload: object) -> None:
    data = ensure_object(payload)
    result = data["result"]
    failure_type = data["failure_type"]
    if result == "success" and failure_type != "none":
        raise WbsArtifactError(
            "result 가 success 이면 failure_type 은 none 이어야 합니다.",
            EXIT_SEMANTIC_VIOLATION,
        )
    if result in {"partial", "failed"} and failure_type == "none":
        raise WbsArtifactError(
            "result 가 partial/failed 이면 failure_type 을 구체적으로 지정해야 합니다.",
            EXIT_SEMANTIC_VIOLATION,
        )


def validate_operator_decision_semantics(payload: object) -> None:
    data = ensure_object(payload)
    decision = data["decision"]
    next_packet_id = data.get("next_packet_id")
    disposition_after = data["packet_disposition_after"]
    slice_state_after = data["slice_state_after"]

    if decision in {"rework", "dispatch", "remediate"} and not next_packet_id:
        raise WbsArtifactError(
            f"decision 이 {decision} 이면 next_packet_id 가 필요합니다.",
            EXIT_SEMANTIC_VIOLATION,
        )

    if decision in {"block", "cancel", "close"} and next_packet_id:
        raise WbsArtifactError(
            f"decision 이 {decision} 이면 next_packet_id 를 두지 않습니다.",
            EXIT_SEMANTIC_VIOLATION,
        )

    if disposition_after == "superseded" and not next_packet_id:
        raise WbsArtifactError(
            "packet_disposition_after 가 superseded 이면 next_packet_id 가 필요합니다.",
            EXIT_SEMANTIC_VIOLATION,
        )

    if slice_state_after == "done" and decision != "close":
        raise WbsArtifactError(
            "slice_state_after 가 done 이면 decision 은 close 여야 합니다.",
            EXIT_SEMANTIC_VIOLATION,
        )


def validate_run_ledger_semantics(payload: object) -> None:
    data = ensure_object(payload)
    if data["ledger_kind"] == "snapshot":
        if "source_decision_id" not in data or "source_seq" not in data:
            raise WbsArtifactError(
                "snapshot ledger 는 source_decision_id 와 source_seq 가 필요합니다.",
                EXIT_SEMANTIC_VIOLATION,
            )

    seen_slice_ids: set[str] = set()
    for entry in data["slice_entries"]:
        slice_id = entry["slice_id"]
        if slice_id in seen_slice_ids:
            raise WbsArtifactError(
                f"run ledger 에 중복 slice_id 가 있습니다: {slice_id}",
                EXIT_SEMANTIC_VIOLATION,
            )
        seen_slice_ids.add(slice_id)

        if entry["slice_state"] == "done" and entry["next_operator_decision"] != "close":
            raise WbsArtifactError(
                f"slice_state 가 done 인 entry 는 next_operator_decision 이 close 여야 합니다: {slice_id}",
                EXIT_SEMANTIC_VIOLATION,
            )

        if entry["active_packet_disposition"] == "active" and entry["latest_execution_state"] == "done":
            raise WbsArtifactError(
                f"active packet 이면서 latest_execution_state 가 done 으로 끝나면 disposition 정리가 필요합니다: {slice_id}",
                EXIT_SEMANTIC_VIOLATION,
            )

        for packet_history in entry["packet_history"]:
            recent_trace_refs = packet_history.get("recent_trace_refs", [])
            trace_count = packet_history["trace_count"]
            if trace_count < len(recent_trace_refs):
                raise WbsArtifactError(
                    f"trace_count 는 recent_trace_refs 길이보다 작을 수 없습니다: {slice_id}",
                    EXIT_SEMANTIC_VIOLATION,
                )


def validate_semantics(kind: str, payload: object) -> None:
    if kind == "handoff-packet":
        validate_handoff_semantics(payload)
        return
    if kind == "trace-summary":
        validate_trace_semantics(payload)
        return
    if kind == "operator-decision":
        validate_operator_decision_semantics(payload)
        return
    if kind == "run-ledger":
        validate_run_ledger_semantics(payload)
        return
    raise WbsArtifactError(f"지원하지 않는 kind 입니다: {kind}", EXIT_INVALID_INPUT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WBS artifact schema/semantic validator")
    parser.add_argument("--kind", choices=sorted(KIND_TO_SCHEMA), required=True)
    parser.add_argument("--file", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_json(Path(args.file))
    validate_against_schema(args.kind, payload)
    validate_semantics(args.kind, payload)
    print(f"✅ WBS artifact valid: {args.kind} -> {args.file}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WbsArtifactError as error:
        print(f"❌ {error}", file=sys.stderr)
        raise SystemExit(error.exit_code)
