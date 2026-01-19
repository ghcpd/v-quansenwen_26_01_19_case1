from __future__ import annotations

import argparse
from pathlib import Path

from rich.table import Table

from .config import load_pipeline_file
from .errors import ConfigError, ExecutionError
from .executor import run_pipeline
from .logging_utils import LogConfig, get_console
from .plugins import BUILTIN_PLUGINS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="flowtask", description="Run config-driven text pipelines")
    p.add_argument("--quiet", action="store_true", help="suppress non-error output")

    sub = p.add_subparsers(dest="command", required=True)

    exec_p = sub.add_parser("execute", help="execute a pipeline")
    exec_p.add_argument(
        "--config-file",
        required=True,
        help="Path to pipeline config (.yml/.yaml/.json)",
    )

    val_p = sub.add_parser("validate", help="validate a pipeline config")
    val_p.add_argument("--config-file", required=True)

    sub.add_parser("plugins", help="list available plugins")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    console = get_console(LogConfig(quiet=bool(args.quiet)))

    try:
        if args.command == "plugins":
            table = Table(title="FlowTask plugins")
            table.add_column("Name")
            for name in sorted(BUILTIN_PLUGINS.keys()):
                table.add_row(name)
            console.print(table)
            return 0

        if args.command == "validate":
            load_pipeline_file(Path(args.config_file))
            if not args.quiet:
                console.print("OK")
            return 0

        if args.command == "execute":
            spec = load_pipeline_file(Path(args.config_file))
            result = run_pipeline(spec)
            if not args.quiet:
                console.print(f"Executed pipeline: {result.pipeline}")
                console.print(f"Tasks: {len(spec.tasks)}")
            return 0

        raise AssertionError("unreachable")

    except (ConfigError, ExecutionError) as exc:
        console.print(f"ERROR: {exc}")
        return 2
