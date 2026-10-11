from __future__ import annotations

from pathlib import Path

import pytest

from nexora.policies.paths import PathPolicyError, resolve_workspace_path


def test_rejects_parent_traversal(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("private", encoding="utf-8")

    with pytest.raises(PathPolicyError, match="outside the configured workspace"):
        resolve_workspace_path(workspace, "../secret.txt")


def test_rejects_absolute_paths(tmp_path: Path) -> None:
    with pytest.raises(PathPolicyError, match="absolute paths"):
        resolve_workspace_path(tmp_path, str(tmp_path / "secret.txt"))


def test_rejects_nul_character(tmp_path: Path) -> None:
    with pytest.raises(PathPolicyError, match="NUL"):
        resolve_workspace_path(tmp_path, "bad\x00name.txt")


def test_rejects_symlink_escape(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("private", encoding="utf-8")
    link = workspace / "outside-link.txt"

    try:
        link.symlink_to(outside)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks are not available in this environment: {exc}")

    with pytest.raises(PathPolicyError, match="outside the configured workspace"):
        resolve_workspace_path(workspace, "outside-link.txt")


def test_rejects_missing_paths(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="does not exist"):
        resolve_workspace_path(tmp_path, "missing.txt")
