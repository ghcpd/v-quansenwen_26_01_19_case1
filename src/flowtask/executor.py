from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from .config import PipelineSpec, TaskSpec
from .errors import ExecutionError
from .plugins import get_plugin


@dataclass
class RunResult:
    pipeline: str
    produced: Dict[str, Dict[str, Any]]


def run_pipeline(spec: PipelineSpec) -> RunResult:
    produced: Dict[str, Dict[str, Any]] = {}

    for task in spec.tasks:
        produced[task.id] = _run_task(task, produced)

    return RunResult(pipeline=spec.name, produced=produced)


def _resolve_ref(value: str, produced: Dict[str, Dict[str, Any]]) -> str:
    # Reference format: @task_id.field
    if not value.startswith("@"):
        return value

    ref = value[1:]
    if "." not in ref:
        raise ExecutionError(f"Invalid reference '{value}'. Use @task_id.field")

    task_id, field = ref.split(".", 1)
    if task_id not in produced:
        raise ExecutionError(f"Unknown reference task '{task_id}' in '{value}'")

    if field not in produced[task_id]:
        raise ExecutionError(f"Unknown reference field '{field}' in '{value}'")

    resolved = produced[task_id][field]
    if not isinstance(resolved, str):
        raise ExecutionError(f"Reference '{value}' did not resolve to text")

    return resolved


def _run_task(task: TaskSpec, produced: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    if task.type == "read_text":
        path = Path(task.path or "")
        text = path.read_text(encoding="utf-8")
        return {"text": text, "path": str(path)}

    if task.type == "write_text":
        path = Path(task.path or "")
        text = _resolve_ref(task.input or "", produced)
        path.write_text(text, encoding="utf-8")
        return {"text": text, "path": str(path)}

    if task.type == "transform":
        plugin = get_plugin(task.plugin or "")
        text = _resolve_ref(task.input or "", produced)
        out = plugin.transform(text, task.params or {})
        return {"text": out, "plugin": plugin.name}

    raise ExecutionError(f"Unsupported task type: {task.type}")
