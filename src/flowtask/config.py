from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import yaml

from .errors import ConfigError


TaskType = Literal["read_text", "write_text", "transform"]


@dataclass(frozen=True)
class TaskSpec:
    id: str
    type: TaskType
    path: Optional[str] = None
    input: Optional[str] = None
    plugin: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class PipelineSpec:
    name: str
    tasks: List[TaskSpec]


def load_pipeline_file(path: str | Path) -> PipelineSpec:
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"Config file not found: {p}")

    raw: Any
    if p.suffix.lower() in {".yml", ".yaml"}:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    elif p.suffix.lower() == ".json":
        raw = json.loads(p.read_text(encoding="utf-8"))
    else:
        raise ConfigError("Config must be .yml/.yaml or .json")

    return parse_pipeline(raw)


def parse_pipeline(raw: Any) -> PipelineSpec:
    if not isinstance(raw, dict):
        raise ConfigError("Config root must be an object")

    pipeline = raw.get("pipeline")
    if not isinstance(pipeline, dict):
        raise ConfigError("Missing required object: pipeline")

    name = pipeline.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ConfigError("pipeline.name must be a non-empty string")

    tasks_raw = pipeline.get("tasks")
    if not isinstance(tasks_raw, list) or not tasks_raw:
        raise ConfigError("pipeline.tasks must be a non-empty list")

    tasks: List[TaskSpec] = []
    seen: set[str] = set()

    for i, item in enumerate(tasks_raw):
        if not isinstance(item, dict):
            raise ConfigError(f"pipeline.tasks[{i}] must be an object")

        task_id = item.get("id")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ConfigError(f"pipeline.tasks[{i}].id must be a non-empty string")
        if task_id in seen:
            raise ConfigError(f"Duplicate task id: {task_id}")
        seen.add(task_id)

        ttype = item.get("type")
        if ttype not in {"read_text", "write_text", "transform"}:
            raise ConfigError(
                f"pipeline.tasks[{i}].type must be one of read_text/write_text/transform"
            )

        spec = TaskSpec(
            id=task_id,
            type=ttype,
            path=item.get("path"),
            input=item.get("input"),
            plugin=item.get("plugin"),
            params=item.get("params") if isinstance(item.get("params"), dict) else None,
        )

        _validate_task_spec(spec, index=i)
        tasks.append(spec)

    return PipelineSpec(name=name, tasks=tasks)


def _validate_task_spec(spec: TaskSpec, index: int) -> None:
    if spec.type == "read_text":
        if not spec.path:
            raise ConfigError(f"pipeline.tasks[{index}] read_text requires 'path'")
        if spec.input is not None:
            raise ConfigError(f"pipeline.tasks[{index}] read_text does not take 'input'")
    elif spec.type == "write_text":
        if not spec.path or not spec.input:
            raise ConfigError(f"pipeline.tasks[{index}] write_text requires 'path' and 'input'")
    elif spec.type == "transform":
        if not spec.input:
            raise ConfigError(f"pipeline.tasks[{index}] transform requires 'input'")
        if not spec.plugin:
            raise ConfigError(f"pipeline.tasks[{index}] transform requires 'plugin'")
