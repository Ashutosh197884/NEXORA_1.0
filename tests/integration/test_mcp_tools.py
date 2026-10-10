from __future__ import annotations

import pytest

mcp_module = pytest.importorskip("nexora.server")
Client = pytest.importorskip("mcp").Client


@pytest.mark.asyncio
async def test_tools_are_discoverable() -> None:
    async with Client(mcp_module.mcp) as client:
        tools = await client.list_tools()
    names = {tool.name for tool in tools.tools}
    assert {
        "list_project_files",
        "read_project_file",
        "search_project_code",
        "inspect_data_file",
    }.issubset(names)
