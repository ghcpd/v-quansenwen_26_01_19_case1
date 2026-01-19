class FlowTaskError(Exception):
    """Base exception for FlowTask."""


class ConfigError(FlowTaskError):
    """Raised when configuration is invalid."""


class ExecutionError(FlowTaskError):
    """Raised when a task fails to execute."""
