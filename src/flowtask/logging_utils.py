from __future__ import annotations

from dataclasses import dataclass
from rich.console import Console


@dataclass(frozen=True)
class LogConfig:
    quiet: bool = False


def get_console(cfg: LogConfig) -> Console:
    return Console(stderr=True, quiet=cfg.quiet)
