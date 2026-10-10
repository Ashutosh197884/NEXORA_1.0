# Contributing

1. Create a focused branch for each change.
2. Add or update tests for behavior and security boundaries.
3. Run `uv run pytest` and `uv run ruff check .` before opening a pull request.
4. Keep protocol handling in the official MCP SDK; do not implement a parallel JSON-RPC stack.
5. Do not add write-capable or command-execution tools without an explicit threat model and review.

By submitting a contribution, you agree that it is provided under the repository's Apache-2.0 license, subject to applicable law and any separate written agreement.
