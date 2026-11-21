---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway'
source_kind: 'learn_markdown'
---

# Connect to a gateway

Source: https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Connect Codex to your organization's model gateway using the provider settings and authentication method your gateway team supplies. The gateway routes model requests to your backend, such as Amazon Bedrock.

For an organization-wide rollout, see [Roll out a
  gateway](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway). For the required API behavior,
  see [Gateway compatibility](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility). To
  connect directly to Bedrock without a gateway, see [Amazon
  Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock).

## Check for an existing configuration

Install the Codex client and version your administrator tested. If your organization manages the settings, open that client and complete the sign-in steps in your handoff. You can skip the provider configuration examples below.

- For the CLI, inspect the selected profile and run `codex doctor`. After startup,
  use `/status` to confirm the active model and provider.
- For the macOS app, inspect `~/.codex/config.toml` or the managed configuration
  your organization delivers.
- For the Windows app, inspect `%USERPROFILE%\.codex\config.toml` or the system
  configuration your organization delivers.

If the expected gateway provider and model are already active, complete any sign-in steps supplied by your administrator, then continue to [Verify the connection](#verify-the-connection). Avoid adding a second provider configuration to a managed machine. If the settings differ from your administrator's handoff, ask which configuration layer should supply them before editing local files.

## Get your gateway connection details

For manual setup, confirm whether you need ChatGPT workspace sign-in, gateway authentication, or both.

To configure Codex yourself, get these values from your gateway team:

- The HTTPS gateway base URL, including its API path, such as `https://gateway.example.com/v1`.
- The model name and provider ID to use.
- The authentication method: [native gateway OAuth](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway?gateway-auth=oauth#use-native-gateway-oauth),
  a scoped API key and its environment variable, or an installed credential helper.
- For OAuth, the authorization URL, token URL, public client ID, and any required scopes. For gateways that use a cookie or custom header, its name.
- Any required model catalog URL, or a catalog file and its absolute local path.

<a id="without-chatgpt-sign-in"></a>

## Configure the provider

<Tabs
  id="gateway-provider-setup"
  param="setup"
  ariaLabel="Gateway provider setup by client"
  tabs={[
    { id: "cli", label: "CLI" },
    { id: "desktop", label: "Desktop" },
  ]}
>

1. Run `/config` and open **Sessions** > **Model providers**.

![CLI provider list with Company gateway highlighted and Space available to set the default.](https://developers.openai.com/images/codex/gateways/cli-provider-list.webp)

2. If you don't see your gateway, select **Create a custom provider or gateway**. Enter its **Name** and **Base URL**. If the gateway uses an API key, enter the environment variable name in **API key variable**. Select **Save**.

![CLI gateway form with Name, Base URL, and API key variable fields.](https://developers.openai.com/images/codex/gateways/cli-add-provider.webp)

3. If your organization lets you change the default, highlight your gateway and press <kbd>Space</kbd>.
4. Start a chat with `/new` and [verify the connection](#verify-the-connection).

To edit a saved gateway, open its details and select **Edit configuration** if available.

To set up a gateway during CLI sign-in, start `codex --enable gateway_setup_wizard`
and choose **Sign in another way** > **Use a custom provider or gateway**.
This optional sign-in flow is off by default. It appears in a signed-out CLI
using the embedded app server when the default provider is OpenAI, API-key
sign-in is allowed, and no managed setting or launch override selects a provider.

Open **Settings** and select **Model Providers**. If your gateway is listed, open its menu and select **Switch provider** if available. Skip this step if the gateway is already your current provider. Then start a new chat and [verify the connection](#verify-the-connection).

If you don't see your gateway and you can add providers, follow these steps.

1. On **Model Providers & Gateways**, select **Add** > **Gateway or custom provider**.

![Model Providers & Gateways with the Add menu open and Gateway or custom provider at the bottom.](https://developers.openai.com/images/codex/gateways/desktop-model-providers.webp)

2. Enter a **Name** for the gateway and the **Base URL** from your administrator, including the API path.
3. Under **Authentication**, choose the method your administrator specified. For **Environment variable**, enter the variable name (for example, `COMPANY_GATEWAY_API_KEY`) in **API key environment variable**.
4. To use the gateway for new chats, turn on **Set as current provider** if available. Select **Save**.

![Completed gateway form with an example base URL, environment variable authentication, and Set as current provider enabled.](https://developers.openai.com/images/codex/gateways/desktop-add-provider.webp)

5. Start a new chat with the gateway and [verify the connection](#verify-the-connection).

</Tabs>

For manual setup or additional authentication settings, open
`config.toml` at `~/.codex/config.toml` on macOS or Linux, or
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
requires_openai_auth = false
```

Then add the [authentication settings](#choose-an-authentication-method) your
gateway team supplies.

`enterprise-gateway` is an illustrative provider ID. Use the same ID in
`model_provider` and its provider and authentication tables.
This example disables web search
for the initial connection test; your administrator should verify feature support
before enabling it.

## Configure your model catalog

Confirm with your gateway team how Codex gets the capabilities and instructions for your selected model:

- **Built-in name:** If the gateway accepts the exact model name bundled with your Codex version and routes it to the matching model, set `model` to that name. Codex already has its metadata.
- **Catalog endpoint:** If the gateway serves Codex-compatible metadata, use its full catalog URL. This can be a `/v1/models` endpoint that implements the [Codex catalog response](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#implement-the-catalog-endpoint). A response that only lists model IDs is insufficient for custom aliases.
- **Catalog file:** If your gateway uses custom aliases and your administrator distributes a file, use the [local models.json example](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#start-with-a-local-modelsjson-file).

If your administrator supplies a catalog URL, add it to the existing
`[model_providers.enterprise-gateway]` table:

```toml
model_catalog_url = "https://gateway.example.com/codex/models.json"
```

If gateway OAuth is your only credential, the catalog URL must use the same
scheme, host, and port as `base_url`. Sign in to the gateway first. Codex uses
your existing gateway session to fetch the catalog.

Remove any effective `model_catalog_json` setting; it takes precedence over the
URL. Administrators can find endpoint requirements in
[remote catalog setup](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#serve-a-remote-catalog).

If your administrator supplies a local model catalog file, save it and add
`model_catalog_json` before the first TOML table, using the file's absolute path.
Custom aliases need matching catalog metadata. For example:

```toml
model_catalog_json = "/etc/codex/gateway-models.json"
```

Use the model name and catalog supplied together by your administrator. Don't
add a catalog path unless the file exists at that location.

## Choose an authentication method

Use native gateway OAuth for browser or device-code sign-in, an API key for a scoped credential, or a credential helper if your organization supplies a command.

{/* prettier-ignore */}
<Tabs
  id="gateway-authentication"
  ariaLabel="Gateway authentication method"
  param="gateway-auth"
  defaultTab="oauth"
  tabs={[
    { id: "oauth", label: "Gateway OAuth" },
    { id: "api-key", label: "API key" },
    { id: "helper", label: "Credential helper" },
  ]}
>

<a id="option-b-use-native-gateway-oauth"></a>

### Use native gateway OAuth

Gateway OAuth works independently of ChatGPT sign-in. Use it when your gateway accepts access tokens issued by your
organization's identity provider, such as Microsoft Entra ID. Codex handles the
browser sign-in, encrypted credential storage, and token refresh when the
authorization server issues a refresh token.

For gateway-only authentication, Codex CLI 0.166.0 and later sends the access token in `Authorization: Bearer <gateway access token>` by default. Remove any `Authorization` entry from this provider's `http_headers` or `env_http_headers`.

Your gateway team must register a public OAuth client that supports the
authorization code flow with PKCE. Add this table to the provider configuration
in `config.toml`, replacing the URLs and client ID with their values:

```toml
[model_providers.enterprise-gateway.gateway_oauth]
authorization_url = "https://login.example.com/oauth/authorize"
token_url = "https://login.example.com/oauth/token"
client_id = "YOUR_PUBLIC_CLIENT_ID"
# redirect_port = 43127
# device_authorization_url = "https://login.example.com/oauth/device"
```

Add `scopes` and, if required, `resource` to this table using the values your
identity provider and gateway require. Request the scopes needed for refresh
tokens if your provider requires them. Codex uses an available loopback port by default.
If your identity provider requires a fixed redirect URI, set `redirect_port` and
register `http://127.0.0.1:43127/callback` for this example.

If your gateway expects a cookie or custom header, set the optional `delivery` field in the OAuth table. Choose the method your gateway validates:

```toml
delivery = { kind = "cookie", name = "auth-openid" }
```

```toml
delivery = { kind = "header", name = "X-Gateway-Token", scheme = "Bearer" }
```

If your deployment also requires ChatGPT sign-in, use the cookie or a separate
gateway header shown above. See [Enable ChatGPT sign-in](#enable-chatgpt-sign-in-recommended).

A gateway that accepts only a static API key must add support for the OAuth token
and its delivery method before you can use this flow. The gateway continues to
manage its own upstream credentials, such as its AWS credentials for Bedrock.

When OAuth is your only credential, keep `requires_openai_auth = false` and remove the
previous `env_key`, `experimental_bearer_token`, or `auth` settings used for the
gateway credential.

Restart the desktop app and follow its gateway sign-in prompt to open the browser.
In the CLI, start `codex` and follow its sign-in prompt. Complete your
organization's sign-in and MFA, then return to Codex. If the grant expires or
Codex can't refresh it, sign in again when prompted.

For SSH or a terminal without a browser, set `device_authorization_url` to the
device authorization endpoint your identity provider supplies. When you need to
sign in, the interactive CLI shows a verification URL and a one-time code. Open
the URL in a browser and enter the code. This flow doesn't require port forwarding.

If your provider only supports browser sign-in and the CLI runs over SSH, set
`redirect_port = 43127` and register the matching redirect URI. From the machine
with your browser, forward the port before starting Codex:

```shell
ssh -L 43127:127.0.0.1:43127 user@remote
```

In that SSH session, start `codex` and open the gateway sign-in URL in your local
browser. For browser sign-in inside a container, the callback must also be
reachable from the browser. If you can't reach it, use device authorization,
an API key, or a credential helper.

### Use an API key

Use this setting when the gateway expects an API key in the `Authorization` header.

Add the following setting inside the existing
`[model_providers.enterprise-gateway]` table:

```toml
env_key = "CODEX_GATEWAY_API_KEY"
```

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

With ChatGPT sign-in, use the custom header for the gateway key so Codex can send the user's OpenAI credential in `Authorization`.

If the custom header is your only authentication mechanism, use
`model_catalog_json`; remote catalog discovery won't run.

### Use an organization credential helper

If the helper supplies your primary provider credential, use your administrator's
installed helper and configuration instead of `env_key`. Don't configure both mechanisms.
The helper must exist on your machine; Codex doesn't install it. For example,
add this table without `env_key`, using the resolver path and
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

<a id="option-a-reuse-your-credential-command-with-a-helper"></a>

If your helper supplies a gateway token alongside ChatGPT sign-in, omit the
provider's `auth` table and set `requires_openai_auth = true`. Configure a
gateway credential export command and the header or cookie your gateway accepts:

```toml
[model_providers.enterprise-gateway.gateway_oauth]
delivery = { kind = "cookie", name = "gateway_session" }

[model_providers.enterprise-gateway.gateway_oauth.credential_export]
command = "/usr/local/bin/fetch-codex-gateway-token"
args = ["print-token"]
```

The command must print one access token to standard output. Codex runs it on
first use and caches the token in memory. If the gateway rejects an inference
request with HTTP 401, Codex runs the command again and retries once.
When using `credential_export`, omit the OAuth client ID and endpoint settings.

You can also run the helper before starting Codex and pass the token in a
[custom gateway header](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway?gateway-auth=api-key#use-a-custom-authentication-header).
Renew the token and restart Codex when it expires.

Use resolved absolute paths for helper executables and catalog files.

</Tabs>

<a id="why-you-would-want-this"></a>
<a id="how-to-set-it-up"></a>

<a id="sign-in-with-chatgpt-through-a-gateway"></a>
<a id="enable-chatgpt-sign-in-optional"></a>

## Enable ChatGPT sign-in (recommended)

If your organization uses a ChatGPT workspace, signing in gives users access to eligible features such as first-party plugins. Your workspace controls apply, and your gateway still handles model requests. [Compare feature availability](https://learn.chatgpt.com/docs/pricing#feature-availability).

For manual setup, update the existing `[model_providers.enterprise-gateway]` table before signing in:

1. Set `requires_openai_auth = true` and keep `base_url` pointing to your gateway. Remove any `env_key`, `experimental_bearer_token`, and provider `auth` settings so Codex uses your OpenAI credential for primary authentication.
2. Send the gateway credential separately. For [native gateway OAuth](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway?gateway-auth=oauth#use-native-gateway-oauth) or a [gateway credential export command](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway?gateway-auth=helper#use-an-organization-credential-helper), configure `gateway_oauth.delivery` to use the cookie or custom header your gateway accepts. For a static API key, use a [custom authentication header](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway?gateway-auth=api-key#use-a-custom-authentication-header). Reserve `Authorization` for the OpenAI credential.

Sign in to the ChatGPT workspace your administrator named. Complete the gateway sign-in if prompted, then [verify your connection](#verify-the-connection).

Administrators can [distribute managed provider settings](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#distribute-the-configuration) and [verify credential forwarding](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#test-codex-through-the-gateway).

<a id="keep-the-credentials-on-their-own-paths"></a>

### Handle credentials at the gateway

The gateway receives two credentials on each model request. For example, when Codex sends the gateway OAuth token in a cookie:

```http
POST /backend-api/codex/responses
Authorization: Bearer <ChatGPT token>
ChatGPT-Account-ID: <workspace ID, when available>
Cookie: auth-openid=<gateway token>
```

Validate the gateway credential and strip its cookie or custom header. Redact credentials and sensitive request data from logs. Choose which credential to use upstream:

- **Forward the user's credential for direct OpenAI inference (recommended).** This lets OpenAI attribute usage and apply inference settings for that user. For this route, the gateway must proxy `/models` and `/responses` to `https://chatgpt.com/backend-api/codex` and forward `Authorization` and any `ChatGPT-Account-ID` header unchanged.
- **Let the gateway authenticate to the inference provider.** Use the credentials configured on the gateway for that provider. Leave the user's OpenAI token and any `ChatGPT-Account-ID` header out of the upstream request.

These diagrams show the recommended route for OpenAI inference.

<details>
<summary>How a gateway key works with ChatGPT sign-in</summary>

![Reuse the credential command through a launch helper. The same gateway key moves from Authorization to X-Gateway-Key while ChatGPT sign-in supplies Authorization.](<https://developers.openai.com/images/codex/gateways/chatgpt-gateway-before-after-header-light.webp>)

![The gateway validates and removes X-Gateway-Key, then forwards ChatGPT Authorization and any account ID unchanged to the Codex backend.](<https://developers.openai.com/images/codex/gateways/chatgpt-gateway-runtime-header-light.webp>)

</details>

<details>
<summary>How gateway OAuth works with ChatGPT sign-in</summary>

![Replace API-key gateway auth with native gateway OAuth alongside ChatGPT sign-in.](<https://developers.openai.com/images/codex/gateways/chatgpt-gateway-before-after-light.webp>)

![The gateway consumes its OAuth cookie and forwards the ChatGPT credential to the Codex backend.](<https://developers.openai.com/images/codex/gateways/chatgpt-gateway-runtime-light.webp>)

</details>

### Add routing headers (optional)

Use the routing settings supplied by your administrator. Gateway operators can [distribute these settings](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#distribute-the-configuration) and check the selected route in gateway logs.

<a id="caveats-and-limitations"></a>
<a id="voice-through-a-gateway"></a>

Only model-provider requests use this gateway route. [Voice sessions](https://learn.chatgpt.com/docs/features/voice) use a separate route. Workspace sign-in, MCP servers, and plugins can also use other network paths.

## Start the client

With ChatGPT sign-in, start the client and sign in to the workspace that provides the managed configuration. If you use native gateway OAuth, also complete your organization's gateway sign-in when prompted. Then [verify the connection](#verify-the-connection).

If you edited `config.toml` manually, follow the instructions for your client.

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

Use the provider ID and model alias in your administrator's handoff. The provider identifies the configured connection; the model alias identifies a model routed through that connection. ChatGPT sign-in and gateway authentication control access and may both be required.

In the CLI, use `/status` to inspect the active model and provider. In the desktop app,
check the selected model and configuration.

Send this prompt in a new task:

```text
Reply with exactly: gateway-ok
```

Expect `gateway-ok`. A response alone doesn't prove which route handled it: ask
your administrator to confirm that the gateway recorded your user, model alias,
and intended upstream route. Don't identify the model by asking it its name.

## Troubleshoot the connection

| Symptom                                 | What to check                                                                                                                                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The expected provider isn't active.     | Check the selected profile and configuration precedence. Confirm that top-level keys aren't inside a provider table.                                                                                                |
| OAuth sign-in or token delivery fails.  | Check the public client registration, redirect URI, scopes, and configured cookie or header. Confirm that the gateway accepts the issued access token.                                                              |
| API-key or helper authentication fails. | Check that the credential variable reaches the client process, or that the installed helper can retrieve a current token. Ask the administrator to distinguish gateway authentication from upstream authentication. |
| The model isn't found.                  | Confirm the supplied model name and ask the administrator to check its route.                                                                                                                                       |
| The model uses unexpected capabilities. | Ask the administrator to check that the catalog metadata matches the model behind the alias.                                                                                                                        |
| Streaming stalls or follow-ups fail.    | Ask the gateway owner to check proxy buffering, the terminal `response.completed` event, and [Gateway compatibility](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility).                                                      |
| A catalog or helper path fails.         | Confirm that the file exists at the configured absolute path in the environment running Codex.                                                                                                                      |

When requesting help, include your client version, operating system, expected provider and model alias, authentication method, and the step that failed. Include the error message and request time so the gateway owner can locate the request. Remove tokens, cookies, authorization headers, and sensitive prompts. Don't send credential files or a configuration dump containing secrets.

## Use an existing gateway deployment

Ask your gateway team for the Codex provider settings and approved model alias. If the team still needs to enable a Codex route, share the [administrator migration checklist](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#reuse-an-existing-gateway-deployment).

## Related docs

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [MCP servers](https://learn.chatgpt.com/docs/extend/mcp)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
