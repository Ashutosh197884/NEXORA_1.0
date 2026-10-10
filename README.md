# NEXORA Core

**Connect intelligence to action.** NEXORA is an independent, local-first MCP server for developers.

- License: Apache-2.0
- Python: 3.11+
- Protocol: official MCP Python SDK
- Default transport: stdio; no network listener by default

The v0.1 MVP provides read-only tools for listing workspace files, reading bounded UTF-8 text files, searching project code, and inspecting CSV/JSON data. All paths are scoped to `NEXORA_WORKSPACE`; traversal and symlink escapes are rejected.

## Quick start

Install Python 3.11+ and [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --extra dev
export NEXORA_WORKSPACE="$PWD"
uv run nexora-mcp
```

Run tests with `uv run pytest`. To inspect tools with MCP Inspector, run `uv run mcp dev src/nexora/server.py`.

See `docs/architecture.md`, `docs/implementation-plan.md`, and `SECURITY.md` for details. NEXORA v0.1 is local-only; authenticated remote transport is planned for a future release.