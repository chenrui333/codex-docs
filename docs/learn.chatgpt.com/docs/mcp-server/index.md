---
source_type: 'learn'
source_area: 'learn_mcp_server'
source_url: 'https://learn.chatgpt.com/docs/mcp-server'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex MCP server removal

Source: https://learn.chatgpt.com/docs/mcp-server

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

The `codex mcp-server` command and the standalone `codex-mcp-server` binary have
been removed. Integrations that launch either command must migrate before
upgrading Codex. The previous MCP tool reference and Agents SDK examples on this
page are no longer supported.

## Use the Codex app server

Use the [Codex app server](https://learn.chatgpt.com/docs/app-server) for integrations that need
authentication, conversation history, approvals, and streamed agent events.

The app server uses its own [JSON-RPC protocol](https://learn.chatgpt.com/docs/app-server#protocol). It
isn't an MCP server or a drop-in replacement for an MCP client: update your
integration to use the app-server protocol instead of MCP tool calls.
The app-server command is experimental and isn't supported for production
workloads.

## Connect Codex to MCP tools

Codex continues to support [external MCP servers](https://learn.chatgpt.com/docs/extend/mcp).
Use `codex mcp` to manage those connections. The removal affects hosting Codex
as an MCP server.
