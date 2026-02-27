#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib


def toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    raise TypeError(f"지원하지 않는 TOML 값 타입: {type(value)}")


def read_manifest(manifest_path: Path) -> dict:
    with manifest_path.open("rb") as file:
        return tomllib.load(file)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_generated_markdown(source_path: str, body: str) -> str:
    return (
        "<!-- AUTO-GENERATED FILE. DO NOT EDIT. -->\n"
        f"<!-- Source: {source_path} -->\n\n"
        f"{body.rstrip()}\n"
    )


def render_generated_toml(source_path: str, body: str) -> str:
    return (
        "# AUTO-GENERATED FILE. DO NOT EDIT.\n"
        f"# Source: {source_path}\n\n"
        f"{body.rstrip()}\n"
    )


def generate_runtime(manifest_path: Path, output_dir: Path, repo_root: Path) -> None:
    manifest = read_manifest(manifest_path)
    runtime = manifest["runtime"]
    features = manifest.get("features", {})
    profiles = manifest["profiles"]
    agents = manifest["agents"]
    task_template = manifest["task_template"]

    config_lines: list[str] = []
    config_lines.append(f'profile = {toml_value(runtime["default_profile"])}')
    config_lines.append(
        "project_doc_fallback_filenames = "
        + toml_value(runtime["project_doc_fallback_filenames"])
    )
    config_lines.append("")
    config_lines.append("[features]")
    for feature_name, enabled in features.items():
        config_lines.append(f"{feature_name} = {toml_value(enabled)}")

    for profile_name, profile_cfg in profiles.items():
        config_lines.append("")
        config_lines.append(f"[profiles.{profile_name}]")
        for key in [
            "model",
            "model_reasoning_effort",
            "model_verbosity",
            "approval_policy",
            "sandbox_mode",
        ]:
            config_lines.append(f"{key} = {toml_value(profile_cfg[key])}")
        config_lines.append(
            f'model_instructions_file = "agents/{profile_cfg["prompt_output"]}"'
        )

    for agent_name, agent_cfg in agents.items():
        config_lines.append("")
        config_lines.append(f"[agents.{agent_name}]")
        config_lines.append(f"description = {toml_value(agent_cfg['description'])}")
        config_lines.append(f'config_file = "agents/{agent_cfg["toml_output"]}"')

    config_body = "\n".join(config_lines) + "\n"
    write_text(
        output_dir / "config.toml",
        render_generated_toml(str(manifest_path.relative_to(repo_root)), config_body),
    )

    for profile_name, profile_cfg in profiles.items():
        source_rel = profile_cfg["prompt_source"]
        source_abs = repo_root / source_rel
        body = source_abs.read_text(encoding="utf-8")
        write_text(
            output_dir / "agents" / profile_cfg["prompt_output"],
            render_generated_markdown(source_rel, body),
        )

    for agent_name, agent_cfg in agents.items():
        profile_name = agent_cfg["profile"]
        toml_body = (
            f'profile = "{profile_name}"\n'
            f'model_instructions_file = "{profiles[profile_name]["prompt_output"]}"\n'
        )
        write_text(
            output_dir / "agents" / agent_cfg["toml_output"],
            render_generated_toml(
                str(manifest_path.relative_to(repo_root)),
                toml_body,
            ),
        )

    task_source_rel = task_template["prompt_source"]
    task_source_abs = repo_root / task_source_rel
    task_body = task_source_abs.read_text(encoding="utf-8")
    write_text(
        output_dir / "agents" / task_template["prompt_output"],
        render_generated_markdown(task_source_rel, task_body),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate .codex runtime files from SoT")
    parser.add_argument(
        "--manifest",
        default="agent-team/sot/codex-runtime.manifest.toml",
        help="Manifest path",
    )
    parser.add_argument(
        "--output-dir",
        default=".codex",
        help="Runtime output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path.cwd()
    manifest_path = (repo_root / args.manifest).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    generate_runtime(manifest_path, output_dir, repo_root.resolve())


if __name__ == "__main__":
    main()
