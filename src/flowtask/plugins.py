from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from .errors import ExecutionError


@dataclass(frozen=True)
class Plugin:
    name: str
    transform: Callable[[str, dict], str]


def _uppercase(text: str, params: dict) -> str:
    return text.upper()


def _lowercase(text: str, params: dict) -> str:
    return text.lower()


def _replace(text: str, params: dict) -> str:
    pattern = params.get("pattern")
    repl = params.get("repl")
    if pattern is None or repl is None:
        raise ExecutionError("replace plugin requires params: pattern and repl")
    return text.replace(str(pattern), str(repl))


BUILTIN_PLUGINS: Dict[str, Plugin] = {
    "builtin:uppercase": Plugin(name="builtin:uppercase", transform=_uppercase),
    "builtin:lowercase": Plugin(name="builtin:lowercase", transform=_lowercase),
    "builtin:replace": Plugin(name="builtin:replace", transform=_replace),
}


def get_plugin(name: str) -> Plugin:
    try:
        return BUILTIN_PLUGINS[name]
    except KeyError as exc:
        known = ", ".join(sorted(BUILTIN_PLUGINS.keys()))
        raise ExecutionError(f"Unknown plugin '{name}'. Known: {known}") from exc
