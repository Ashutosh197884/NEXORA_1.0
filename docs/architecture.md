# NEXORA Core Architecture (v0.1)

## Request flow

1. An MCP client launches NEXORA as a stdio subprocess.
2. The official MCP Python SDK handles protocol lifecycle, discovery and tool invocation.
3. Tool handlers delegate to local service functions.
4. Services resolve paths against `NEXORA_WORKSPACE`, validate file type and size, and perform read-only inspection.
5. Results return as structured data through MCP; diagnostics are sent to stderr through logging.

## Layer boundaries

- `server.py`: protocol-facing registration and process entry point.
- `config.py`: environment-backed settings and validation.
- `policies/paths.py`: workspace path authorization.
- `services/project_service.py`: business logic for file listing, reading, search and data inspection.
- `tests/`: unit, integration and security tests.

## Trust boundaries

The MCP client and all workspace content are untrusted. The server restricts paths and result sizes and does not execute file content. A workspace directory should be treated as an explicit grant of read access to the connected model. Operating-system sandboxing remains recommended for higher-risk environments.

## Remote-ready path

The service layer does not depend on stdio. A future release may run the same MCP server over Streamable HTTP, but remote deployment must add authentication/authorization, HTTPS, host/origin protections, rate limits and operational monitoring before exposure.
