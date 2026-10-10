"""Workspace path policy. All tool paths are relative to a configured root."""

from __future__ import annotations

from pathlib import Path


class PathPolicyError(ValueError):
    """Raised when a requested path is outside the configured workspace."""


def resolve_workspace_path(root: Path, requested: str, *, must_exist: bool = True) -> Path:
    if not isinstance(requested, str) or not requested.strip():
        raise PathPolicyError("path must be a non-empty relative path")
    if "\x00" in requested:
        raise PathPolicyError("path contains an invalid NUL character")

    candidate = Path(requested)
    if candidate.is_absolute():
        raise PathPolicyError("absolute paths are not allowed; use a workspace-relative path")

    resolved_root = root.resolve(strict=True)
    resolved = (resolved_root / candidate).resolve(strict=must_exist)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise PathPolicyError("requested path is outside the configured workspace") from exc

    if must_exist and not resolved.exists():
        raise FileNotFoundError("requested path does not exist")
    return resolved
