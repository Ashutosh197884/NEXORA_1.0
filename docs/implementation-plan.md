# NEXORA v0.1 Implementation Plan

## Repository foundation

- [x] Python package metadata and console entry point
- [x] Apache-2.0 license
- [x] Public repository and source files
- [x] README, architecture, development workflow, and security policy
- [x] GitHub Actions CI workflow
- [x] Sample CSV and JSON datasets

## Core implementation

- [x] Local stdio MCP server entry point
- [x] Four read-only developer tools
- [x] Workspace path checks
- [x] File-size and result-count limits
- [x] Unit and security test suites
- [x] MCP tool-discovery integration test

## Verification and release gates

- [ ] Resolve dependencies in a clean environment
- [ ] Run `uv run ruff check .` successfully
- [ ] Run `uv run pytest` successfully
- [ ] Verify all four tools manually with MCP Inspector
- [ ] Review GitHub Actions results and address failures
- [ ] Review package metadata and installation behavior
- [ ] Tag `v0.1.0` only after the checks above pass

## Future scope

- [ ] Expand adversarial path tests across operating systems
- [ ] Add more data formats only with explicit size and parsing limits
- [ ] Design authenticated Streamable HTTP deployment before enabling remote access
- [ ] Add release automation after the package and tests are stable

A checked item means the corresponding file or capability has been added to the repository. It does not imply that the runtime has been independently verified unless the item explicitly says so.
