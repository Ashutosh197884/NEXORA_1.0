from __future__ import annotations

from pathlib import Path

import pytest

from nexora.policies.paths import PathPolicyError, resolve_workspace_path
from nexora.services.project_service import read_project_file


def test_parent_traversal_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    secret = tmp_path / "secret.txt"
    secret.write_text("not for the tool", encoding="utf-8")
    with pytest.raises(PathPolicyError):
        resolve_workspace_path(workspace, "../secret.txt")


def test_symlink_escape_rejected_when_supported(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    link = workspace / "escape.txt"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is not available on this platform")
    with pytest.raises(PathPolicyError):
        read_project_file(workspace, "escape.txt")


def test_nul_path_rejected(tmp_path: Path) -> None:
    with pytest.raises(PathPolicyError, match="NUL"):
        resolve_workspace_path(tmp_path, "bad\x00path")
