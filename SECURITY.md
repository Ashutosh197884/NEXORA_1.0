# Security Policy

NEXORA v0.1 is local-first and read-only. Do not expose the server over a network or configure its workspace to include files you do not want available to the connected AI client.

## Supported release

Security fixes are currently intended for the latest v0.1.x release line.

## Reporting a vulnerability

Please do not publish secrets, personal data, or an exploit that exposes another person's data in a public issue. Until a dedicated private reporting channel is configured, contact the maintainers privately through the repository host and include the affected version, impact, and minimal reproduction steps.

## Security boundaries

- Tool paths are relative to a configured workspace root.
- Absolute paths, parent traversal and symlink escapes are rejected.
- File and result sizes are bounded.
- Tools are read-only and do not execute arbitrary commands.
- Remote transport and authentication are not enabled in v0.1.
