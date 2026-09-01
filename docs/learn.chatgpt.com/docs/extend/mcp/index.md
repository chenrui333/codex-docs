---
source_type: 'learn'
source_area: 'learn_extend'
source_url: 'https://learn.chatgpt.com/docs/extend/mcp'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0"]
---

# Model Context Protocol

Source: https://learn.chatgpt.com/docs/extend/mcp

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Model Context Protocol (MCP) connects models to tools and context. Use it to
give ChatGPT or Codex access to third-party documentation, or to let it
interact with developer tools like your browser or Figma.

ChatGPT web can use remote MCP-backed tools supplied by plugins. Local Codex
clients can also connect directly to MCP servers and share their configuration.

<a id="supported-mcp-features"></a>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

The ChatGPT desktop app, Codex CLI, and IDE extension support MCP servers and
share MCP configuration for the same Codex host.

The supported server features below apply to MCP servers configured on a Codex
host. Hosted plugin tools can have different capabilities.

## Supported MCP features

- **STDIO servers**: Servers that run as a local process (started by a command).
  - Environment variables
- **Streamable HTTP servers**: Servers that you access at an address.
  - Bearer token authentication
  - OAuth authentication, including Client ID Metadata Documents (CIMD) and
    Dynamic Client Registration (DCR)
  - ChatGPT session authentication for trusted first-party servers
- **Server instructions**: Codex reads the MCP `instructions` field returned during initialization and uses it as server-wide guidance alongside the server's tools.

If you build or maintain an MCP server for Codex, use `instructions` for cross-tool workflows, constraints, and rate limits that apply across the server. Keep the first 512 characters self-contained so the most important guidance is available when Codex is deciding how to use the server.

## Connect Codex to an MCP server

Codex stores MCP configuration in `config.toml` alongside other Codex configuration settings. By default this is `~/.codex/config.toml`, but you can also scope MCP servers to a project with `.codex/config.toml` (trusted projects only).

The ChatGPT desktop app, Codex CLI, and IDE extension share this configuration.
Once you configure your MCP servers, you can switch among those clients without
redoing setup.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

### Configure in the ChatGPT desktop app

1. Open **Settings**, then select **MCP servers**.
2. Select **Add server**.
3. Enter a name, choose **STDIO** or **Streamable HTTP**, and provide the
   server's command or URL.
4. Save the server, then select **Restart**.

The server list shows which servers are enabled and which require OAuth. Select
**Authenticate** when an OAuth server requires sign-in. In the composer, type `/mcp`
to view connected servers.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

## Use MCP-backed tools in ChatGPT web

In a hosted ChatGPT Work chat, install a [plugin](https://learn.chatgpt.com/docs/plugins) to use its
bundled connectors and remote MCP tools. After installation, Chat and Work can
use those tools. Workspace administrators can control which plugins and tools
are available.

ChatGPT web doesn't read local Codex configuration files or expose the local
Codex command menu. Open the **Plugins** tab to browse and manage available
tools.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

### Configure with the CLI

#### Add an MCP server

```bash
codex mcp add <server-name> --env VAR1=VALUE1 --env VAR2=VALUE2 -- <stdio server-command>
```

For example, to add Context7 (a free MCP server for developer documentation), you can run the following command:

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

#### Other CLI commands

Run `codex mcp list` to see configured servers. To see all available MCP
commands, run `codex mcp --help`. For a server that supports OAuth, run
`codex mcp login <server-name>`.

#### Terminal UI (TUI)

In the `codex` TUI, use `/mcp` to see your active MCP servers.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

### Configure in the IDE extension

1. Open the gear menu, then select **MCP servers**.
2. Select **Add server**.
3. Enter a name, choose **STDIO** or **Streamable HTTP**, and provide the
   server's command or URL.
4. Save the server, then select **Restart extension**.

The MCP server list shows which servers are enabled and which require OAuth.
Select **Authenticate** when an OAuth server requires sign-in.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

### Configure with config.toml

For more fine-grained control, edit `~/.codex/config.toml` or a project-scoped
`.codex/config.toml`. See the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
for a searchable list of every supported MCP option.

Configure each MCP server with a `[mcp_servers.<server-name>]` table in the configuration file.

</ContentModeSwitch>

<a id="stdio-servers"></a>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

#### STDIO servers

- `command` (required): The command that starts the server.
- `args` (optional): Arguments to pass to the server.
- `env` (optional): Environment variables to set for the server.
- `env_vars` (optional): Environment variables to allow and forward.
- `cwd` (optional): Working directory to start the server from.
- `experimental_environment` (optional): Set to `remote` to start the stdio
  server through a remote executor environment when one is available.

`env_vars` can contain plain variable names or objects with a source:

```toml
env_vars = ["LOCAL_TOKEN", { name = "REMOTE_TOKEN", source = "remote" }]
```

String entries and `source = "local"` read from Codex's local environment.
`source = "remote"` reads from the remote executor environment and requires
remote MCP stdio.

</ContentModeSwitch>

<a id="streamable-http-servers"></a>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

#### Streamable HTTP servers

- `url` (required): The server address.
- `auth` (optional): Authentication to try after configured bearer tokens and
  authorization headers. Use `oauth` (the default) for stored MCP OAuth
  credentials. Use `chatgpt` to use the current ChatGPT session for the trusted
  first-party ChatGPT origin, with stored OAuth as a fallback.
- `bearer_token_env_var` (optional): Environment variable name for a bearer token to send in `Authorization`.
- `http_headers` (optional): Map of header names to static values.
- `env_http_headers` (optional): Map of header names to environment variable names (values pulled from the environment).

If no credential source resolves, Codex can connect to the server without
authentication. Run `codex mcp login <server-name>` separately to start an MCP
OAuth login.

#### Other configuration options

- `startup_timeout_sec` (optional): Timeout (seconds) for the server to start. Default: `10`.
- `tool_timeout_sec` (optional): Timeout (seconds) for the server to run a tool. Default: `60`.
- `enabled` (optional): Set `false` to disable a server without deleting it.
- `required` (optional): Set `true` to make startup fail if this enabled server can't initialize.
- `enabled_tools` (optional): Tool allow list.
- `disabled_tools` (optional): Tool deny list (applied after `enabled_tools`).
- `default_tools_approval_mode` (optional): Default approval behavior for
  tools from this server. Supported values are `auto`, `prompt`, `writes`, and
  `approve`. The `writes` mode prompts for tools that aren't marked read-only.
- `tools.<tool>.approval_mode` (optional): Per-tool approval behavior override.

#### OAuth client registration and callbacks

When your authorization server requires a pre-registered OAuth client, provide
its client ID when adding the MCP server:

```bash
codex mcp add example --url https://mcp.example.com --oauth-client-id my-client
```

Codex displays the complete callback URL to register with your provider:

```text
OAuth callback URL: http://127.0.0.1/callback
```

Codex saves the callback alongside the client ID in `config.toml` for later
logins:

```toml
[mcp_servers.example]
url = "https://mcp.example.com"

[mcp_servers.example.oauth]
client_id = "my-client"
callback_url = "http://127.0.0.1/callback"
```

Newly added pre-registered clients use a stable callback only when the
authorization server advertises
`authorization_response_iss_parameter_supported: true` and provides a metadata
`issuer`. If issuer support isn't advertised, Codex appends a server-specific
callback ID, such as `http://127.0.0.1/callback/XuuuHAzzHOni`. Existing clients
without a saved callback continue using their callback-ID-specific redirect.

During login, callback selection depends on the OAuth configuration and
authorization server metadata:

| OAuth configuration                                                | Issuer support           | Callback used                                                                                                                                      |
| ------------------------------------------------------------------ | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `callback_url` without `client_id`                                 | Supported                | The configured callback is used for client registration.                                                                                           |
| `callback_url` without `client_id`                                 | Unsupported              | The configured callback is used for client registration with the server-specific callback ID appended.                                             |
| `client_id` and `callback_url`                                     | Supported                | The configured callback is reused; the authorization response must contain the matching `iss`.                                                     |
| `client_id` and a `callback_url` ending in the correct callback ID | Unsupported              | The configured callback is reused unchanged.                                                                                                       |
| `client_id` and a `callback_url` missing the correct callback ID   | Unsupported              | The configured callback is ignored. Codex uses `mcp_oauth_callback_url`, or `http://127.0.0.1/callback` when unset, with the callback ID appended. |
| `client_id` without a configured `callback_url`                    | Supported or unsupported | Codex uses the global or default callback with the server-specific callback ID appended.                                                           |

The fallback doesn't modify the stored callback URL. Codex derives the callback
ID from the MCP server URL, including its path and query string. The same
selection rules apply to automatic and explicit login.

Set `mcp_oauth_callback_url` when you need a custom callback path or remote
Devbox ingress URL. Newly added pre-registered clients use that URL unchanged
when their provider supports issuer identification. Otherwise, they use the
configured URL with the server-specific callback ID appended. Always register
the exact callback displayed by `codex mcp add`.

For portless `http://127.0.0.1` callbacks, Codex omits the listener port from
the URL it displays and stores, then inserts the active listener port during
authorization. This substitution doesn't apply to `localhost`, IPv6 hosts,
HTTPS URLs, or callbacks that already include a port. Authorization servers
must accept variable loopback ports under
[RFC 8252, Section 7.3](https://www.rfc-editor.org/rfc/rfc8252#section-7.3).

Set `mcp_oauth_callback_port` to choose a fixed global listener port, or set
`mcp_servers.<server-name>.oauth.callback_port` to override it for one server.
An explicit port in the callback URL doesn't configure the listener. For a
direct loopback callback, use portless `http://127.0.0.1` or configure the same
explicit port for both the callback URL and listener. A proxied callback can
intentionally use an external URL port that differs from the local listener
port. Local callback URLs bind to the local interface; non-local callback URLs
bind to `0.0.0.0`.

Codex validates any returned `iss` before exchanging the authorization code. A
mismatched `iss` always rejects the response. When issuer support is advertised,
a missing `iss` also rejects it. Neither failure exchanges the code or falls
back to another callback. A malformed callback URL or issuer support advertised
without a metadata issuer also remains a hard failure. See
[Authenticate users](https://developers.openai.com/plugins/build/auth).

If the MCP server advertises `scopes_supported`, Codex prefers those
server-advertised scopes during OAuth login. Otherwise, Codex falls back to the
scopes configured in `config.toml`.

#### OAuth client registration

Codex supports [OAuth Client ID Metadata Documents (CIMD)](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/)
and Dynamic Client Registration (DCR). By default, Codex automatically chooses
CIMD when the authorization server advertises
`client_id_metadata_document_supported: true`, includes `none` in
`token_endpoint_auth_methods_supported`, and the callback uses a supported
loopback URL. Otherwise, Codex uses DCR when available. A configured OAuth client
ID always takes precedence and skips client registration.

For CIMD, Codex uses a ChatGPT-hosted metadata document specific to the MCP
server:

```text
https://chatgpt.com/oauth/codex/<callback_id>/client.json
```

Codex derives `<callback_id>` from the MCP server URL and includes it in the
loopback redirect URI, such as
`http://127.0.0.1:<port>/callback/<callback_id>`. The metadata document registers
the matching loopback URI without a port. Authorization servers must accept the
port selected at login while matching the host and path exactly, as required by
[RFC 8252](https://www.rfc-editor.org/rfc/rfc8252.html#section-7.3). Custom
callback hosts, paths, or query parameters require DCR or a configured OAuth
client ID.

Support for a stable, shared CIMD document is in development and coming soon:

```text
https://chatgpt.com/oauth/codex/client.json
```

Codex will use the stable document with the shared `/callback` path when the
authorization server advertises
`authorization_response_iss_parameter_supported: true`, provides a valid
`issuer` in its metadata, and includes a matching `iss` in authorization
responses. Servers without issuer-bound responses will continue using the
callback-specific document.

To choose a registration method for one CLI login, use
`--oauth-client-registration`:

```bash
codex mcp login <server-name> --oauth-client-registration cimd
codex mcp login <server-name> --oauth-client-registration dcr
```

The default is `auto`. Registration choices apply only to the current login and
aren't stored in `config.toml`.

#### config.toml examples

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
env_vars = ["LOCAL_TOKEN"]

[mcp_servers.context7.env]
MY_ENV_VAR = "MY_ENV_VALUE"
```

```toml
# Optional MCP OAuth callback overrides (used by `codex mcp login`)
mcp_oauth_callback_port = 5555
mcp_oauth_callback_url = "https://devbox.example.internal/callback"
```

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
```

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
disabled_tools = ["screenshot"] # applied after enabled_tools
default_tools_approval_mode = "prompt"
startup_timeout_sec = 20
tool_timeout_sec = 45
enabled = true

[mcp_servers.chrome_devtools.tools.open]
approval_mode = "approve"
```

### Plugin-provided MCP servers

Installed plugins can bundle MCP servers in their plugin manifest. Those
servers are launched from the plugin, so user config doesn't set their
transport command. User config can still control on/off state and tool policy
under `plugins.<plugin>.mcp_servers.<server>`.

```toml
[plugins."sample@test".mcp_servers.sample]
enabled = true
default_tools_approval_mode = "prompt"
enabled_tools = ["read", "search"]

[plugins."sample@test".mcp_servers.sample.tools.search]
approval_mode = "approve"
```

Plugin-provided HTTP MCP servers can also declare OAuth settings in `.mcp.json`.
Plugin manifests use the camelCase field names `clientId`, `callbackUrl`, and
`callbackPort`:

```json
{
  "mcpServers": {
    "sample": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "clientId": "my-pre-registered-client",
        "callbackUrl": "http://127.0.0.1/callback/registered"
      }
    }
  }
}
```

Plugin-provided MCP servers follow the same callback-selection rules as other
MCP servers. If a plugin provides a `clientId`, its provider doesn't support
issuer-bound callbacks, and `callbackUrl` lacks the server-specific callback
ID, Codex ignores that URL for the login and uses `mcp_oauth_callback_url`, or
`http://127.0.0.1/callback` when unset, with the callback ID appended. The
configured `callbackUrl` remains unchanged.

A plugin's `oauth.callbackPort` overrides the global
`mcp_oauth_callback_port`; if neither is set, Codex chooses an ephemeral port.
The port embedded in `callbackUrl` doesn't select the listener port. For a
direct loopback callback with a fixed port, configure both values to match:

```json
{
  "callbackUrl": "http://127.0.0.1:4321/callback/registered",
  "callbackPort": 4321
}
```

For remote ingress or another proxy, the callback URL port and local listener
port can intentionally differ when the proxy forwards to the configured
listener.

## Examples of useful MCP servers

The list of MCP servers keeps growing. Here are a few common ones:

- [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp): Search and read OpenAI developer docs.
- [Context7](https://github.com/upstash/context7): Connect to up-to-date developer documentation.
- Figma [Local](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/) and [Remote](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/): Access your Figma designs.
- [Playwright](https://www.npmjs.com/package/@playwright/mcp): Control and inspect a browser using Playwright.
- [Chrome Developer Tools](https://github.com/ChromeDevTools/chrome-devtools-mcp/): Control and inspect Chrome.
- [Sentry](https://docs.sentry.io/product/sentry-mcp/#codex): Access Sentry logs.
- [GitHub](https://github.com/github/github-mcp-server): Manage GitHub beyond what `git` supports (for example, pull requests and issues).

</ContentModeSwitch>
