from __future__ import annotations

from pathlib import Path

import pytest
from mcp import Client

from nexora import server
from nexora.config import Settings


@pytest.mark.asyncio
async def test_client_discovers_expected_tools(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(server, "settings", Settings(workspace=tmp_path))

    async with Client(server.mcp) as client:
        result = await client.list_tools()

    assert {tool.name for tool in result.tools} == {
        "list_project_files",
        "read_project_file",
        "search_project_code",
        "inspect_data_file",
    }


@pytest.mark.asyncio
async def test_client_can_invoke_read_only_tool(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "README.md").write_text("NEXORA integration smoke test", encoding="utf-8")
    monkeypatch.setattr(server, "settings", Settings(workspace=tmp_path))

    async with Client(server.mcp) as client:
        result = await client.call_tool("read_project_file", {"path": "README.md"})

    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["content"] == "NEXORA integration smoke test"


@pytest.mark.asyncio
async def test_client_receives_error_for_workspace_escape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (tmp_path / "secret.txt").write_text("not for the tool", encoding="utf-8")
    monkeypatch.setattr(server, "settings", Settings(workspace=workspace))

    async with Client(server.mcp) as client:
        result = await client.call_tool("read_project_file", {"path": "../secret.txt"})

    assert result.is_error is True
