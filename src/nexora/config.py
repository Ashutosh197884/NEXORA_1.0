"""Environment-backed configuration for NEXORA."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    workspace: Path
    max_read_bytes: int = 1_048_576
    max_inspect_bytes: int = 10_485_760
    max_search_results: int = 100
    max_search_file_bytes: int = 1_048_576
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        workspace_raw = os.getenv("NEXORA_WORKSPACE", ".")
        workspace = Path(workspace_raw).expanduser().resolve()
        if not workspace.exists() or not workspace.is_dir():
            raise ValueError("NEXORA_WORKSPACE must point to an existing directory")
        level = os.getenv("NEXORA_LOG_LEVEL", "INFO").upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("NEXORA_LOG_LEVEL must be a valid logging level")
        return cls(
            workspace=workspace,
            max_read_bytes=_positive_int("NEXORA_MAX_READ_BYTES", 1_048_576),
            max_inspect_bytes=_positive_int("NEXORA_MAX_INSPECT_BYTES", 10_485_760),
            max_search_results=_positive_int("NEXORA_MAX_SEARCH_RESULTS", 100),
            max_search_file_bytes=_positive_int("NEXORA_MAX_SEARCH_FILE_BYTES", 1_048_576),
            log_level=level,
        )
