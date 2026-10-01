---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway'
source_kind: 'learn_markdown'
---

# Connect to a gateway

Source: https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Connect Codex to an LLM gateway using the gateway URL, model alias, and credential
or token resolver your organization provides.

To roll out a gateway for your organization, see [Deploy Codex through a
  gateway](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway). For the required API behavior,
  see [Gateway compatibility](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility). To
  connect directly to Bedrock without a gateway, see [Amazon
  Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock).

## Check for an existing configuration

Before adding anything, check whether your administrator already configured Codex.

- For the CLI, inspect the selected profile and run `codex doctor`. After startup,
  use `/status` to confirm the active model and provider.
- For the macOS app, inspect `~/.codex/config.toml` or the managed configuration
  your organization delivers.
- For the Windows app, inspect `%USERPROFILE%\.codex\config.toml` or the system
  configuration your organization delivers.

If the expected gateway provider and model are already active, continue to
[Verify the connection](#verify-the-connection).

## Get your gateway connection details

Install the [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) or the desktop app approved by your
organization. To configure Codex yourself, get these values from your gateway team:

- The HTTPS gateway base URL, including its API path, such as `https://gateway.example.com/v1`.
- The model name and provider ID to use.
- Your scoped gateway credential and its environment variable, or an installed
  token resolver and its configuration.
- Any required model catalog file and its absolute local path.

## Configure the provider

Open `config.toml` at `~/.codex/config.toml` on macOS or Linux, or
`%USERPROFILE%\.codex\config.toml` on Windows.

Merge this example into your existing configuration, replacing the URL and model
with the values your administrator supplied. Don't add a second definition of an
existing key or table. This example uses `gpt-6-sol`; use it without a custom
catalog only if your administrator confirms that your Codex version recognizes
the model and its bundled metadata matches the gateway.

Keep `model`, `model_provider`, `model_catalog_json`, and `web_search` before
  the first TOML table. Keys placed after a table header belong to that table,
  so Codex won't read them as top-level settings.

```toml
model = "gpt-6-sol"
model_provider = "enterprise-gateway"
web_search = "disabled"

[model_providers.enterprise-gateway]
name = "Organization Gateway"
base_url = "https://gateway.example.com/v1"
wire_api = "responses"
env_key = "CODEX_GATEWAY_API_KEY"
```

If your administrator supplies a model catalog, save it locally and add
`model_catalog_json` before the first TOML table, using the file's absolute path.
Custom aliases need matching catalog metadata. For example:

```toml
model_catalog_json = "/etc/codex/gateway-models.json"
```

Use the model name and catalog supplied together by your administrator. Don't
add a catalog path unless the file exists at that location.

`enterprise-gateway` is an illustrative provider ID. Use the same ID in
`model_provider`, `[model_providers.<id>]`, and `[model_providers.<id>.auth]`.
This example disables web search
for the initial connection test; your administrator should verify feature support
before enabling it.

Make your gateway credential available as `CODEX_GATEWAY_API_KEY` in the
environment of the process that launches Codex, using your organization's secret
delivery mechanism. Don't put the credential in TOML or a repository. A variable
set in a terminal may not be available to an app launched from the desktop.

### Use a custom authentication header

If your gateway requires a header such as `X-API-Key` instead of a bearer token,
replace `env_key` in the provider table with:

```toml
env_http_headers = { "X-API-Key" = "CODEX_GATEWAY_API_KEY" }
```

Use the exact header name your administrator provides. Codex reads the value from
the named environment variable; keep the credential out of the configuration file.
See the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) for
`model_providers.<id>.env_http_headers`.

### Use an organization credential helper

If your administrator provides command-backed authentication, use their installed
helper and configuration instead of `env_key`. Don't configure both mechanisms.
The helper must exist on your machine; Codex doesn't install it. For example,
replace the example `env_key` setting with this table, using the resolver path and
arguments your administrator supplies:

```toml
[model_providers.enterprise-gateway.auth]
command = "/usr/local/bin/fetch-codex-gateway-token"
args = ["print-token"]
timeout_ms = 30000
refresh_interval_ms = 300000
```

The [custom provider authentication reference](https://learn.chatgpt.com/docs/config-file/config-advanced#custom-model-providers)
defines the command, arguments, timeout, refresh interval, and token output
contract. Ask your administrator how to renew your sign-in if the helper can no
longer retrieve a token.

Use resolved absolute paths for helper executables and catalog files.

### Configure the CLI

The CLI reads `~/.codex/config.toml` by default on macOS or Linux. After saving
the provider settings, run `codex`. Inside WSL, use the Linux configuration and
paths unless `CODEX_HOME` points elsewhere.

### Configure the macOS app

The macOS app reads the same `~/.codex/config.toml`. After saving the provider
settings, restart the app. If you use an environment variable for the credential,
make sure it's available to the app process.

### Configure the Windows app

Place the provider settings in `%USERPROFILE%\.codex\config.toml`, then restart
the app. For command-backed authentication, use the resolver installed by your
administrator. For example, replace the Unix auth table with:

```toml
[model_providers.enterprise-gateway.auth]
command = 'C:\Program Files\OpenAI\Codex\fetch-codex-gateway-token.exe'
args = ["print-token"]
timeout_ms = 30000
refresh_interval_ms = 300000
```

In Windows TOML, single-quoted literal strings preserve backslashes. Replace
Unix catalog paths too, for example with
`'C:\ProgramData\OpenAI\Codex\models.json'`, using the actual path your
administrator supplied.

Configure MCP servers and plugins separately. A model gateway credential doesn't
authorize access to your tools or connected systems.

## Verify the connection

Restart the client after changing the configuration. In the CLI, start `codex`
and use `/status` to inspect the active model and provider. In the desktop app,
check the selected model and configuration.

Send this prompt in a new task:

```text
Reply with exactly: gateway-ok
```

Expect `gateway-ok`. A response alone doesn't prove which route handled it: ask
your administrator to confirm that the gateway recorded your user, model alias,
and intended upstream route. Don't identify the model by asking it its name.

This verifies an initial connection. Administrators should also complete the
[rollout checks](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#test-the-client-and-gateway)
for streaming, tools, and follow-up turns.

## Troubleshoot the connection

| Symptom                                 | What to check                                                                                                                                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The expected provider isn't active.     | Check the selected profile and configuration precedence. Confirm that top-level keys aren't inside a provider table.                                                                                                |
| Authentication fails.                   | Check that the credential variable reaches the client process, or that the installed helper can retrieve a current token. Ask the administrator to distinguish gateway authentication from upstream authentication. |
| The model isn't found.                  | Confirm the supplied model name and ask the administrator to check its route.                                                                                                                                       |
| The model uses unexpected capabilities. | Ask the administrator to check that the catalog metadata matches the model behind the alias.                                                                                                                        |
| Streaming stalls or follow-ups fail.    | Ask the gateway owner to check proxy buffering, the terminal `response.completed` event, and [Gateway compatibility](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility).                                                      |
| A catalog or helper path fails.         | Confirm that the file exists at the configured absolute path in the environment running Codex.                                                                                                                      |

When requesting help, include the error message with tokens and sensitive prompts removed.

## Use an existing gateway deployment

If your organization already uses a gateway with another coding tool, you may be
able to reuse its network path, logging, and provider access. Work with your
gateway team to configure and test a Codex connection:

1. Identify the existing gateway URL, credential mechanism, required headers,
   model routes, and configuration delivery method.
2. Ask your gateway team to confirm that the gateway supports the
   [API behavior Codex requires](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility) and to
   configure a Codex model route.
3. Obtain a scoped gateway credential or credential helper, the model name, and
   any required model catalog from your gateway team.
4. [Configure Codex](#configure-the-provider) with those values.
5. [Verify the connection](#verify-the-connection) in the CLI or desktop app you
   plan to use. Have your gateway team complete the
   [streaming, tool, and follow-up checks](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#test-the-client-and-gateway).
6. After the pilot passes, follow
   [Deploy Codex through a gateway](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway) to distribute the
   configuration to other developers.

For the administrator migration checklist and configuration mapping, see
[Reuse an existing gateway deployment](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#reuse-an-existing-gateway-deployment).

## Related docs

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [MCP servers](https://learn.chatgpt.com/docs/extend/mcp)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
