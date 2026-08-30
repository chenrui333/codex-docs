---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/workload-identity'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.149.0", "0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.149.0", "codex-cli 0.151.0"]
---

# Workload identity federation

Source: https://learn.chatgpt.com/docs/enterprise/workload-identity

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Workload identity federation lets trusted automation use Codex without storing
a personal access token or another long-lived OpenAI credential. Your workload
presents a short-lived identity token from a provider you already operate.
OpenAI verifies that token and returns a short-lived access token for a user or
service account in your managed ChatGPT workspace.

Use workload identity for unattended Codex processes in cloud platforms,
Kubernetes, CI systems, and other environments that can issue OIDC tokens or
SPIFFE JWT-SVIDs. For the shared trust model and the separate OpenAI API flow,
see the [workload identity overview](https://developers.openai.com/api/docs/guides/workload-identity-federation).

Codex workload identity federation is in beta and must be enabled for your
  workspace. To request access, contact your OpenAI representative or [OpenAI
  Support](https://help.openai.com/en/articles/6614161-how-can-i-contact-support).

## Before you begin

You need:

- Permission to manage workload identity in the OpenAI Admin Portal.
- A managed ChatGPT workspace.
- A ChatGPT user or service account that is an active member of that workspace,
  or permission to create one during setup.
- An OIDC token or SPIFFE JWT-SVID whose issuer, audience, and identifying
  claims you know.
- A runtime that can keep that token current in a protected file at an absolute
  path.
- Codex 0.148.0 or later.
- An effective Codex authentication policy that permits ChatGPT authentication
  and the workspace selected by the federation rule. See [Enforce a login
  method or workspace](https://learn.chatgpt.com/docs/auth#enforce-a-login-method-or-workspace).

OpenAI does not create a principal or workspace membership during token
exchange. An administrator selects or creates the principal before the workload
connects. Creating a human user consumes a workspace seat and follows the
membership rules for that workspace.

On native Windows, use the **elevated**
[Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox). Other Windows sandbox modes
cannot protect the identity-token file from model-controlled commands.

## Get an identity token

Your workload runtime gets and refreshes the upstream identity token. Codex does
not call cloud metadata services or identity-provider client libraries on your
behalf.

| Runtime                          | Recommended token-file source                                                                                                   |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Kubernetes, AKS, EKS, or GKE     | Mount a projected service-account token and point Codex at that file. The platform rotates it.                                  |
| Microsoft Entra managed identity | Run a trusted host process or sidecar that requests a token from Azure IMDS and replaces the file before expiry.                |
| AWS outbound identity federation | Run a trusted host process that calls regional STS `GetWebIdentityToken` and replaces the file before expiry.                   |
| Google Cloud                     | Run a trusted host process that requests an identity token from the metadata server and replaces the file before expiry.        |
| Oracle Cloud Infrastructure      | Run a trusted host process that uses an instance principal to request an IDCS access token and replaces the file before expiry. |
| GitHub Actions                   | Request the job's OIDC token, write it to a protected file, and request a new token before a later exchange.                    |
| SPIFFE                           | Use the SPIFFE Workload API or an approved helper to write a current JWT-SVID to the file.                                      |
| Custom OIDC provider             | Use the issuer's workload flow to get a JWT, then refresh the protected file before the JWT expires.                            |

Follow the guide for your provider to configure token issuance and inspect a
sample token:

- [Microsoft Azure](https://developers.openai.com/api/docs/guides/workload-identity-federation/microsoft-azure)
- [AWS](https://developers.openai.com/api/docs/guides/workload-identity-federation/aws)
- [Google Cloud](https://developers.openai.com/api/docs/guides/workload-identity-federation/google-cloud)
- [Oracle Cloud Infrastructure](https://developers.openai.com/api/docs/guides/workload-identity-federation/oracle-cloud)
- [GitHub Actions](https://developers.openai.com/api/docs/guides/workload-identity-federation/github-actions)
- [Kubernetes](https://developers.openai.com/api/docs/guides/workload-identity-federation/kubernetes)
- [SPIFFE](https://developers.openai.com/api/docs/guides/workload-identity-federation/spiffe)

Decode a sample token locally and record its `iss`, `aud`, `sub`, and any other
claims you plan to trust. Decoding does not verify the signature. Do not paste a
production token into a website or write it to logs.

## Connect the workload

An administrator creates the provider and federation rule before starting
Codex.

1. Open [Workload identity](https://admin.openai.com/workload-identity) in the
   OpenAI Admin Portal, then select **Connect workload**.
2. Reuse a provider configured for Codex, or create one. Provider presets fill
   in common settings for GitHub Actions, Microsoft Entra ID, Google Cloud,
   AWS, Kubernetes, SPIFFE, and custom OIDC providers.
3. Select **Codex** and the managed workspace the workload may use.
4. Add the narrowest conditions that identify the workload. Match a subject,
   exact claims, a CEL condition, or a combination. Add accepted audiences to
   restrict which tokens the rule accepts. Every configured matcher must pass.
5. Map the rule to one existing ChatGPT user or service account, or create one
   during setup.
6. Review the provider, conditions, workspace, principal, scopes, and access
   token lifetime. Select **Connect workload**, then **Download config**.

The downloaded file contains a non-secret federation rule ID and the path where
Codex will read the identity token. It does not contain a credential.

To automate setup, use the [workload identity Admin
API](https://developers.openai.com/api/docs/guides/workload-identity-federation/admin-api). For matcher
behavior and examples, see [Federation rule
reference](https://developers.openai.com/api/docs/guides/workload-identity-federation/federation-rules).

## Configure the Codex process

The process that starts Codex requires these two workload identity variables:

```bash
export OPENAI_FEDERATION_RULE_ID="idpm_..."
export OPENAI_IDENTITY_TOKEN_FILE="/var/run/secrets/openai.com/identity-token"
```

`OPENAI_FEDERATION_RULE_ID` is not a secret. The token file is. Use an absolute
path in a dedicated directory, such as `/var/run/secrets/openai.com`, owned by
the workload account with mode `0700`. Only trusted host processes should write
there. Keep the directory outside repositories and other paths available to
Codex tools. Keep credentials out of logs, shell history, and build artifacts.

### Add audit attribution

When runtime instances share a federation rule, you can identify each instance
in token-issuance audit events. Set the optional
`OPENAI_WORKLOAD_IDENTITY_CONTEXT` variable to a JSON object encoded as a
string:

```bash
export OPENAI_WORKLOAD_IDENTITY_CONTEXT='{
  "instance_id": "runner-42",
  "display_name": "payments-prod",
  "labels": {
    "environment": "production",
    "region": "us-west-2"
  }
}'
```

The object requires `instance_id`. It can also contain `display_name` and up to
eight labels. The encoded object can be up to 1,024 bytes. `instance_id` and
`display_name` can be up to 128 characters. Label keys can be up to 64
characters, and label values can be up to 256 characters.

Identifiers must start with an ASCII letter or number. Values can then contain
letters, numbers, `.`, `_`, `:`, `/`, `@`, and `-`. Label keys support letters,
numbers, `.`, `_`, and `-`.

OpenAI treats this context as client-reported audit attribution, not as verified
workload identity. It does not affect authentication, authorization, rule
matching, scopes, rate limits, revocation, feature gates, or metrics. Do not put
credentials, secrets, personal data, prompts, model output, or other Customer
Content in it.

For valid context, OpenAI derives a stable attribution ID scoped to the tenant,
provider, federation rule, and `instance_id`. For attribution, the access token
contains the ID but not the context. The successful token-issuance audit event
contains the ID and the normalized context. Context that exceeds a limit or
violates this schema makes the exchange fail with `invalid_grant`.

Codex reads the context when the process starts and does not pass it, the rule
ID, or the token-file path to model-controlled shells, hooks, or MCP servers.
Restart Codex after changing the context.

### Protect and rotate the token file

For managed Linux, macOS, and WSL deployments, add the entire token directory to
[`permissions.filesystem.deny_read`](https://learn.chatgpt.com/docs/enterprise/managed-configuration#enforce-deny-read-requirements)
in managed requirements:

```toml
[permissions.filesystem]
deny_read = ["/var/run/secrets/openai.com"]
```

This blocks model-controlled commands from reading the active token or a
temporary replacement while the Codex host process can still use the token for
exchange. For projected-token volumes, deny the entire token mount and any
backing or resolved target paths outside it. File modes and environment-variable
scrubbing alone do not protect credentials from another process running as the
same user. On native Windows, use the elevated sandbox described above.

For token sources that do not project a file, have a trusted host process write
each replacement inside that protected directory and rename it into place. An
atomic rename prevents Codex from reading a partial token. For example, adapt
this host-owned refresh script to your provider's token command. Provision the
directory before running the script:

```bash
set -eu
TOKEN_DIR="/var/run/secrets/openai.com"
TOKEN_FILE="$TOKEN_DIR/identity-token"
umask 077
TOKEN_TEMP="$(mktemp "$TOKEN_DIR/.identity-token.XXXXXX")"
trap 'rm -f -- "$TOKEN_TEMP"' EXIT
trap 'exit 1' HUP INT TERM
your-identity-provider-command > "$TOKEN_TEMP"
test -s "$TOKEN_TEMP"
mv -f -- "$TOKEN_TEMP" "$TOKEN_FILE"
```

Run the refresh process outside any shell or tool that Codex can control. Keep
the read denial in place during refresh and cleanup. Even if a forced stop
leaves a temporary file behind, that file must remain inside the denied
directory. Do not put workload identity settings in `config.toml`.

## Verify the connection

Load the downloaded environment and inspect the selected authentication method:

```bash
. ./workload-identity-idpm_example.env
codex login status
```

In PowerShell:

```powershell
$env:OPENAI_FEDERATION_RULE_ID = "idpm_..."
$env:OPENAI_IDENTITY_TOKEN_FILE = "C:\run\openai\identity-token"
codex login status
```

A successful check prints `Logged in using workload identity`. This confirms
that Codex exchanged a token through the configured federation rule. The command
does not print the resolved workspace, principal, or rule. Confirm those values
in the Admin Portal before you start the workload. If Codex reports another
authentication method, the two required WIF variables did not reach the process.

If the provider uses **Prevent assertion replay** and the assertion has a `jti`
claim, this check consumes that `jti`. Write a newly issued assertion with a new
`jti` before starting another Codex process.

Run a small request from the same environment:

```bash
codex exec "Reply with only: workload identity is working"
```

Codex exchanges the upstream token and keeps the OpenAI access token in memory.
It does not write either credential to `auth.json`, the system keyring, or
`config.toml`.

## Keep the token current

Refresh the identity-token file before the upstream token expires. Codex rereads
the file when it needs another OpenAI access token. The OpenAI token expires at
the earlier of the upstream token's expiry or the federation rule's lifetime,
and never lasts longer than one hour.

When an administrator turns on replay protection, each upstream JWT must have a
unique `jti`. Write a newly issued assertion with a new `jti` before each
exchange, including refreshes in a long-running process. Assertions without
`jti` do not receive replay protection.

Codex shares one in-memory exchange session inside each host process. Concurrent
requests in that process reuse a valid OpenAI access token and share one refresh
when it expires. Separate processes perform separate exchanges, so they need
assertions that the provider permits them to use.

## Credential precedence

The two required workload identity variables take precedence over every other
credential source:

1. If either `OPENAI_FEDERATION_RULE_ID` or
   `OPENAI_IDENTITY_TOKEN_FILE` is present, Codex selects workload identity.
2. If only one required variable is present, Codex returns an error. It does not
   fall back to an API key, access token, or stored login.
3. `OPENAI_WORKLOAD_IDENTITY_CONTEXT` alone does not select workload identity.
4. When neither required WIF variable is present, Codex applies the normal
   credential rules for that surface. For surfaces that allow API key
   authentication, `CODEX_API_KEY` takes precedence on `codex exec`,
   `codex review`, the TypeScript SDK, and `codex exec-server --remote`. Other
   surfaces can use `CODEX_ACCESS_TOKEN` or a stored login.

An SDK `apiKey` option becomes `CODEX_API_KEY`, but WIF still takes precedence
when either required WIF variable is present. Omit the option when using WIF so
the workload does not carry an unused long-lived credential.

To move an existing workload without downtime, configure WIF while its current
credential is still available. Start a new process with both required WIF
variables; WIF takes precedence even if the old credential is still present.
After the workload succeeds with WIF, remove the old credential from its runtime
and secrets store, then revoke it. Before revocation, you can roll back by
removing both required WIF variables and starting a new process.

## Supported Codex surfaces

Configure workload identity on the machine that owns the Codex process.

| Surface                                         | Support and host boundary                                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Interactive `codex`, `resume`, and `fork`       | Supported. Start the CLI in the configured environment.                                                 |
| `codex exec`, `exec resume`, and `codex review` | Supported. Either required WIF variable makes WIF take precedence.                                      |
| TypeScript SDK                                  | Supported. The parent process supplies the required WIF variables and any optional attribution context. |
| `codex app-server`                              | Supported. Configure WIF on the app-server host, not on a remote client.                                |
| `codex exec-server --remote`                    | Supported for authentication to the remote environment registry. Configure WIF on the exec-server host. |
| Local exec-server process operations            | Do not use WIF authentication. They run through the local exec-server protocol.                         |
| `codex mcp-server`                              | Not supported.                                                                                          |

Remote app-server and exec-server clients never send the upstream identity
token over their protocols.

## Change or remove access

Changes to a rule's subjects, audiences, claims, CEL condition, scopes, or token
lifetime apply to new exchanges. A token issued before the change can remain
valid until its lifetime ends.

Disable a provider or rule to stop access immediately. Disablement blocks new
exchanges and revokes OpenAI access tokens already issued through that resource.
Archiving has the same access effect and cannot be undone. Changing provider
trust also revokes issued tokens before the new trust takes effect.

## Audit changes

Provider and federation rule creation, updates, and archival generate audit
events. Use the [Compliance API and audit event
guidance](https://learn.chatgpt.com/docs/enterprise/compliance-api) to export the events your workspace
supports. Correlate them with your identity provider's issuance logs, and do not
record upstream assertions or OpenAI access tokens in either system.

When the process supplies `OPENAI_WORKLOAD_IDENTITY_CONTEXT`, successful
token-issuance audit events also contain the stable attribution ID and
normalized context described above.

## Troubleshoot

| Symptom                                                               | Check                                                                                                              |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Codex reports incomplete workload identity configuration              | Set both required variables in the same process and use an absolute token-file path.                               |
| Codex reports that its login policy does not permit workload identity | Allow ChatGPT authentication in the effective policy and include the rule's workspace in its permitted workspaces. |
| Codex reports another credential                                      | Load both required WIF variables into the Codex process, then start a new process and rerun `codex login status`.  |
| OpenAI rejects workload context                                       | Check its JSON shape, size, allowed characters, and field limits. Remove sensitive or Customer Content.            |
| OpenAI rejects the token                                              | Compare `iss`, `aud`, expiry, signature key, and assertion lifetime with the provider configuration.               |
| The rule does not match                                               | Confirm the client uses the intended rule ID and that every subject, audience, exact-claim, and CEL check passes.  |
| OpenAI rejects the principal                                          | Confirm the user or service account is active and is an active member of the selected workspace.                   |
| OpenAI rejects a repeated assertion                                   | Get a new JWT with a new `jti`; do not retry the same replay-protected assertion.                                  |
| A long-running process stops refreshing                               | Confirm the host refresh process is still replacing the token file before expiry.                                  |

For provider verification, limits, and CEL details, see the [federation rule
reference](https://developers.openai.com/api/docs/guides/workload-identity-federation/federation-rules).
