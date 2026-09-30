---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway'
source_kind: 'learn_markdown'
---

# Deploy Codex through a gateway

Source: https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Deploy Codex through your organization’s LLM gateway. Configure model routes, issue developer credentials, and distribute a verified Codex configuration.

To configure Codex on your own machine with values you were given, see
  [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway). Before
  choosing or rolling out a gateway, review the [gateway compatibility
  requirements](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility).

## Prerequisites

Before deploying Codex to developers, confirm that you have:

- A gateway serving HTTPS at the exact base URL you will distribute.
- An upstream provider credential held by the gateway.
- Approved Codex-facing model aliases mapped to intended upstream models.
- A scoped test gateway credential.
- A secret delivery mechanism or a tested credential helper.
- A way to distribute configuration, helper executables, and any catalog files.

## Gateway requirements

Before connecting Codex, verify that the gateway product preserves these required behaviors:

- Accept Codex Responses API requests at `POST /v1/responses`.
- Stream SSE events without buffering and end with `response.completed`.
- Preserve follow-up continuation with replayed input.
- Preserve `previous_response_id` only when WebSocket or incremental transport is enabled.
- Preserve function calls and matching `function_call_output` items.
- Route each Codex-facing model alias to the intended upstream model.
- Authenticate users separately and return useful errors without hiding the cause.

A health endpoint, `/v1/models`, Chat Completions response, or one plain-text reply does not qualify the gateway. See [Gateway compatibility requirements](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility) for the detailed contract.

Need an implementation starting point? The [Codex deployment guidance repository](https://github.com/openai-on-aws/guidance-codex/tree/adbc00f353effbf0252e667ba41eb89c99324c8f) includes worked setups for different LLM gateway products. Use it as a reference after confirming your gateway meets the requirements above.

## Roll out the gateway

To move from a deployed gateway to a verified developer experience, complete these five checkpoints in order:

1. [Choose model names and verify routes](#choose-model-names-and-routes).
2. [Issue developer credentials](#issue-developer-credentials).
3. [Test Codex through the gateway](#test-the-client-and-gateway).
4. [Distribute the configuration](#distribute-the-configuration).
5. [Verify from a developer machine](#verify-and-operate-the-rollout).

## Choose model names and routes

Set Codex's `model` to the gateway's model name. Configure the gateway to route that name to the approved upstream model.

| Gateway model name                                                                                                     | Codex configuration                                                                                |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| A [built-in model name](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility#recognized-model-names) included in your Codex version | Set `model` in `config.toml` to this exact name.                                                   |
| A custom alias, such as `company-coding-model`                                                                         | Set `model_catalog_json` to a catalog containing the alias and the corresponding model's metadata. |

<a id="supply-metadata-for-a-custom-alias"></a>

### Use a model catalog for custom names

Use [`model_catalog_json`](https://learn.chatgpt.com/docs/config-file/config-reference) when your gateway uses a model name Codex does not recognize. The catalog supplies the instructions, reasoning options, context limits, and tool capabilities Codex uses for that name. Without a matching entry, a request can reach the intended upstream model while Codex uses generic settings.

For example, to use `company-coding-model` as an alias for `gpt-6-luna`:

1. Create the `company-coding-model` alias on the gateway and route it to the approved upstream `gpt-6-luna` model.
2. Download the [Codex model catalog](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json) for your Codex version and save a copy as `gateway-models.json`. Use this file as your starting point.
3. Edit the `gpt-6-luna` entry in your copy: set `slug` to `company-coding-model` and check that the remaining metadata matches the upstream model and gateway capabilities. For an alias without a model migration, set `upgrade` to `null`.
4. Keep the entries in the top-level `models` array and distribute the file to each client. A custom catalog replaces the bundled catalog, so include every model users need to select.

To use a catalog for a specific Codex version, check `codex --version` and select the matching `rust-v<version>` tag. For a custom build, use its exact source commit. For a desktop deployment, match the bundled CLI version.

For Bedrock through LiteLLM, apply the [required catalog edits](https://learn.chatgpt.com/docs/enterprise/bedrock-through-litellm#prepare-the-client-catalog).

Set the gateway alias, catalog `slug`, and Codex `model` to `company-coding-model`. Add these settings before the first TOML table in the Codex configuration you distribute, using the file's actual absolute path:

```toml
model = "company-coding-model"
model_catalog_json = "/absolute/path/to/gateway-models.json"
```

Restart the CLI or desktop app after changing the catalog because Codex loads it at startup.

### Verify model routes

For each model, verify the route with a real Responses request and gateway
records. A `/v1/models` response can help discover names but doesn't prove that a
model supports the required request and tool behavior.

Model routing and tool authorization are separate parts of the rollout. Configure
MCP connections, plugin distribution, and their policies separately.

## Issue developer credentials

1. Issue one scoped gateway credential per developer so you can attribute usage
   and revoke access individually.
2. Set the approved models, rate limits, budget, expiration, and renewal period
   for each credential.
3. Deliver credentials through your secret manager or an installed credential
   helper. Keep upstream provider and gateway administrator credentials off
   developer machines.
4. If you use a helper, follow the
   [command-backed authentication contract](https://learn.chatgpt.com/docs/config-file/config-advanced#custom-model-providers)
   and test token retrieval and refresh before distribution.
5. Tell developers how to renew their credentials and whom to contact for help.

<a id="test-the-client-and-gateway"></a>

## Test Codex through the gateway

Before distributing anything, follow [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway) to configure one isolated test user with the provider block and credential mechanism you plan to distribute.

Run the checks below from the same CLI or desktop surface developers will use:

| Check                  | Action                                                                                                       | Passing evidence                                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Connection             | Follow [Verify the connection](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway#verify-the-connection).                | The expected provider and alias are active, the test prompt succeeds, and gateway logs identify the test user.                                                  |
| Streaming              | Ask for a short multi-paragraph answer.                                                                      | The gateway forwards SSE events without buffering, text arrives incrementally, and the stream ends with `response.completed`.                                   |
| Local tool loop        | In a disposable folder with read-only permissions, ask Codex to list the top-level files and summarize them. | Codex issues a local tool call, returns the result, and produces a final answer without edits.                                                                  |
| Follow-up              | Ask a follow-up in the same thread.                                                                          | The answer uses the prior turn; the gateway accepts replayed input. If WebSocket or incremental transport is enabled, it also preserves `previous_response_id`. |
| Errors and attribution | Repeat with an intentionally invalid test alias or expired test credential.                                  | The client receives a useful routing or authentication error, and valid requests remain attributed to the test user.                                            |

After these checks succeed, direct developers to [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway) to configure and verify their own machine.

## Distribute the configuration

To give every machine the same connection path, distribute the gateway base URL,
provider ID, approved model alias, and credential mechanism.

### What to distribute

To set provider defaults, distribute this `config.toml` block through the configuration layer you chose. Use a model recognized by your Codex version, or supply the matching catalog described above. Install your token resolver at the configured command path:

Put `model` and `model_provider` before the first TOML table. If you set
  `model_catalog_json`, keep it there too. TOML treats keys after
  `[model_providers...]` as part of that table, not as top-level Codex
  configuration.

```toml
model = "gpt-6-sol"
model_provider = "enterprise-gateway"
web_search = "disabled"

[model_providers.enterprise-gateway]
name = "Organization Gateway"
base_url = "https://gateway.example.com/v1"
wire_api = "responses"

[model_providers.enterprise-gateway.auth]
command = "/usr/local/bin/fetch-codex-gateway-token"
args = ["print-token"]
timeout_ms = 30000
refresh_interval_ms = 300000
```

For a short-lived static test key, remove the auth block and put `env_key = "CODEX_GATEWAY_API_KEY"` inside `[model_providers.enterprise-gateway]` and set that variable outside TOML. Do not combine `env_key` with command-backed auth.

### Distribute defaults and requirements

Use [Configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence)
to choose where to distribute defaults. For enforced settings and macOS MDM
payloads, see [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml).

For host-wide defaults on macOS or Linux, use `/etc/codex/config.toml`. On
Windows, place `config.toml` in `%ProgramData%\OpenAI\Codex\`. Users and
profiles can override these defaults. The linked references describe supported
requirements and their file locations.

Distribute any referenced helper executables and catalog files separately.

`model_catalog_json` points to a local JSON file. If you enforce it through
`requirements.toml`, the requirement pins the path; it doesn't distribute the
file. Put the catalog at that absolute path before Codex starts.

Write resolved absolute Windows paths in TOML. Codex doesn't expand
`%ProgramData%` inside `model_catalog_json` or provider auth `command` values. For
example, use these paths only if your deployment placed the files there:

```toml
model_catalog_json = 'C:\ProgramData\OpenAI\Codex\models.json'

[model_providers.enterprise-gateway.auth]
command = 'C:\ProgramData\OpenAI\Codex\fetch-gateway-token.cmd'
args = ["print-token"]
```

A CLI inside WSL reads Linux paths and Linux `CODEX_HOME`; it doesn't automatically
inherit native Windows configuration.

### Hand developers the configuration values

If you do not have managed distribution, give each developer the gateway URL, provider ID, model alias, credential variable or resolver, and any catalog path. Send them to [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway) to configure and verify their own machine.

Manual setup is not an enforcement channel. Project-local `.codex/config.toml` cannot override sensitive provider or authentication routing keys.

<a id="verify-and-operate-the-rollout"></a>

## Verify from a developer machine

To confirm that the distributed settings reached a developer machine:

1. Restart Codex and confirm the expected provider and model.
2. Run the short test in [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway#verify-the-connection).
3. Ask one follow-up to confirm continuation, then check the gateway logs for that
   developer's request.

### Troubleshoot rollout failures

Use the issue to find the configuration, credential, or gateway layer that needs attention:

| Issue                                            | Remediation                                                                                                                                                                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Expected provider is missing after restart.      | Inspect the winning configuration layer. User or profile configuration can override system defaults.                                                                                                                            |
| Authentication fails for every user.             | Check gateway authentication and the upstream provider credential; identify which service rejected the request.                                                                                                                 |
| Authentication fails for one user.               | Check that user's gateway credential or token resolver.                                                                                                                                                                         |
| Streaming stalls.                                | Inspect gateway buffering and terminal `response.completed` forwarding.                                                                                                                                                         |
| A model is missing or uses generic capabilities. | For a custom alias, confirm the gateway alias, Codex `model`, and catalog `slug` match. Check the [catalog](#use-a-model-catalog-for-custom-names) path and compatibility with the installed Codex version, then restart Codex. |
| A Windows path fails.                            | Use resolved absolute paths. In TOML, use single-quoted strings for Windows paths with single backslashes.                                                                                                                      |

## Reuse an existing gateway deployment

If your organization already uses Claude Code through a gateway, you may be able
to reuse the gateway product, network path, logging, and Bedrock access. Add a
Codex-facing Responses route, credential, model aliases, and `config.toml` while
retaining the existing working setup. Claude client settings and the
`/v1/messages` contract don't configure Codex.

| Existing Claude deployment                                                                                         | Codex migration                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gateway product, DNS, TLS, private networking, logging, redaction, and monitoring                                  | Keep these services in place. Add a Codex-facing route that satisfies the [Gateway compatibility requirements](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility).                                                         |
| Bedrock account, provider credential, IAM boundary, inference profiles, and credential rotation                    | Keep them only when they authorize the upstream models behind the new Codex aliases. The provider credential remains on the gateway.                                                                             |
| Claude `/v1/messages` route, Bedrock InvokeModel shape, Anthropic headers, and Claude-specific retries or errors   | Do not reuse these as proof of compatibility. Codex needs `POST /v1/responses`, Responses streaming, continuation, tool calls, and useful errors.                                                                |
| `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, or `apiKeyHelper`                                                     | Codex does not support `apiKeyHelper`. Issue a scoped Codex gateway credential and configure it with `env_key` or a Codex command-backed token resolver.                                                         |
| Claude model names, `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`, `modelOverrides`, and Bedrock profile mappings | Have your gateway team [choose model names and configure any custom aliases](#choose-model-names-and-routes). Use the model name and any [model catalog JSON](https://learn.chatgpt.com/docs/config-file/config-reference) they provide. |
| Claude `settings.json`, `managed-settings.json`, JSON `env` blocks, `plist`, or registry payloads                  | Keep the same MDM or configuration-management channel, but distribute Codex `config.toml` and supported `requirements.toml` values instead.                                                                      |

To migrate safely, complete these steps in order:

1. Inventory the current Claude path: gateway URL, credential source, required headers, model aliases, Bedrock profile mappings, and managed delivery channel.
2. Add a parallel Codex-facing Responses route and Codex model aliases.
3. Issue one scoped Codex credential. If Codex will use a static credential, expose that new credential through `env_key`; if Claude uses a credential helper, implement and test the Codex command-backed resolver contract.
4. Configure that developer with the [provider block](#what-to-distribute). For a managed rollout, translate the payload into the Codex paths and precedence described in [Deploy Codex through a gateway](#distribute-the-configuration).
5. Run the short connection check on the developer's actual CLI or desktop surface, then run the full streaming, continuation, tool-call, error, logging, and alias-routing checks in [Test Codex through the gateway](#test-the-client-and-gateway).
6. After the pilot passes, [distribute the configuration](#distribute-the-configuration) to the remaining developers.

## Related docs

- [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway)
- [MCP](https://learn.chatgpt.com/docs/extend/mcp)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
