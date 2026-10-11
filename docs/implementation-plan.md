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
- [x] End-to-end stdio transport smoke test

## Verification and release gates

- [x] Resolve dependencies in clean GitHub Actions environments
- [x] Run `uv run ruff check .` successfully
- [x] Run `uv run pytest` successfully on Python 3.11, 3.12, and 3.13
- [x] Verify MCP client discovery and tool invocation through automated integration tests
- [x] Review GitHub Actions failures and address the reported lint and test issues
- [x] Review package metadata and installation behavior
- [ ] Optional manual MCP Inspector walkthrough for developer-experience review
- [ ] Merge the release-readiness pull request
- [ ] Tag `v0.1.0` after merge and final release review

## Future scope

- [ ] Expand adversarial path tests across operating systems
- [ ] Add more data formats only with explicit size and parsing limits
- [ ] Design authenticated Streamable HTTP deployment before enabling remote access
- [ ] Add release automation after the package and tests are stable

A checked item means the corresponding file or capability exists and has been verified as described. CI checks are automated; the manual Inspector walkthrough remains an optional follow-up, not a substitute for the automated stdio transport test.
