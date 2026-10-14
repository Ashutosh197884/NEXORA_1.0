# NEXORA Console

Responsive React + TypeScript frontend prototype for NEXORA Core.

## Current status

This is an **interactive demo using embedded sample data**. Workspace browsing, code search, data previews, navigation, and simulated JSON tool responses work in the browser. It does not read your computer's files or invoke the MCP server.

NEXORA Core remains a local-first Python MCP server using stdio. A future integration phase should add a controlled local bridge that acts as an MCP client, calls the existing server tools, validates requests, and returns bounded results to the browser.

## Run locally

Requirements: Node.js 20+ and npm.

```bash
cd frontend
npm install
npm run dev
```

Open the loopback URL printed by Vite. The development server binds to `127.0.0.1`.

Build and preview:

```bash
npm run build
npm run preview
```

## Included screens

- **Overview** — capabilities, security principles, and quick links
- **Workspace** — sample file tree and text preview
- **Code search** — live literal, case-insensitive search across demo files
- **Data inspector** — sample CSV preview and JSON switch
- **Tool playground** — simulated input/output examples for all four MCP tools

## Integration and security requirements

- Do not expose arbitrary filesystem access from the browser.
- Do not add shell execution or write/mutation capabilities to the MCP core.
- Keep the local bridge bound to loopback and validate `Origin` and host headers.
- Avoid permissive CORS; protect against DNS rebinding and cross-site requests.
- Reuse the MCP server's path policy and configured read/search/inspection limits.
- Label live versus simulated data clearly; remove demo claims only after real integration tests pass.
- Do not expose a local bridge on a public hosting provider.

The UI is intentionally separate from the Python package so the MCP server can remain independently usable by compatible MCP hosts.