from __future__ import annotations

import sys
from pathlib import Path

import pytest
from mcp import Client, StdioServerParameters


@pytest.mark.asyncio
async def test_stdio_transport_discovers_and_invokes_tools(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("NEXORA stdio smoke test", encoding="utf-8")
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "nexora.server"],
        env={
            "NEXORA_WORKSPACE": str(tmp_path),
            "NEXORA_LOG_LEVEL": "ERROR",
        },
    )

    async with Client(server) as client:
        tools = await client.list_tools()
        result = await client.call_tool("read_project_file", {"path": "README.md"})

    assert {tool.name for tool in tools.tools} == {
        "list_project_files",
        "read_project_file",
        "search_project_code",
        "inspect_data_file",
    }
    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["content"] == "NEXORA stdio smoke test"
