---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/access-tokens'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
---

# Access tokens

Source: https://learn.chatgpt.com/docs/enterprise/access-tokens

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex access tokens are ChatGPT workspace credentials scoped to Codex permissions. They authenticate trusted non-interactive local workflows, including Codex CLI and app-server-based automation, with a ChatGPT workspace identity. Use them when a script, scheduled job, or CI runner needs repeatable local access.

Codex access tokens are currently supported for ChatGPT Business and
  Enterprise workspaces.

Access tokens are created in the ChatGPT admin console at [Access tokens](https://chatgpt.com/admin/access-tokens). They're tied to the ChatGPT user who creates them and that user's workspace. The tokens act as agent identities for programmatic local workflows.

If a Platform API key works for your automation, keep using API key auth. Use
  Codex access tokens when a trusted local workflow specifically needs ChatGPT
  workspace access, workspace-managed entitlements, or enterprise controls.

Need to trigger a published ChatGPT workspace agent from your own system? Use
  a Workspace Agent access token for the Workspace Agents API instead. Codex
  access tokens authenticate trusted local workflows through Codex CLI or an
  app-server client; they do not authenticate workspace agent trigger calls. See
  [Authenticate with Workspace Agent access
  tokens](https://developers.openai.com/workspace-agents/authentication).

## How access tokens work

Use an access token when Codex CLI or an app-server client needs to run without a user completing a browser sign-in. The token represents the ChatGPT workspace user who created it, so runs can use that user's access and appear in workspace governance data.

The client checks the token when a run starts and ties the run to that workspace identity. Treat the token like any other automation secret: store it in a secret manager, keep it out of logs, and rotate it regularly.

Use access tokens for:

- `codex exec` jobs that run from trusted automation.
- Local scripts that need repeatable, non-interactive Codex CLI runs.
- Trusted app-server-based automation.
- Enterprise workflows where usage should be associated with a ChatGPT workspace user instead of an API organization key.

Main risks to avoid:

- **Leaked secrets:** anyone with the token can start local runs through Codex CLI or an app-server client as the token creator. Store tokens in a secret manager, keep them out of logs, and rotate them regularly.
- **Runner trust:** public CI, forked pull requests, or shared machines can expose tokens to people outside your workspace. Use access tokens only on trusted runners.
- **Shared identities:** one person's token reused across unrelated teams makes ownership and audit trails harder to interpret. Create tokens for a specific workflow owner.
- **Stale credentials:** long-lived tokens can remain active after the workflow changes. Prefer time-limited tokens and revoke tokens that are no longer used.
- **Wrong credential type:** Codex access tokens are for trusted local automation through Codex CLI or an app-server client. Use Workspace Agent access tokens to trigger published ChatGPT workspace agents, and use Platform API keys for general OpenAI API calls.

## Enable access token creation

Use the access token permission in workspace settings to turn on access token creation for allowed members.

The access token permission controls token creation. It doesn't grant access to
the ChatGPT desktop app, Codex CLI, or IDE extension, and it doesn't change a
member's seat type, built-in workspace role, or local runtime permission
profile. Configure those controls as needed.

For the relationship between these controls, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

<CodexScreenshot
  alt="Access token access permission in ChatGPT workspace RBAC settings"
  lightSrc="/images/codex/enterprise/rbac_access_token_access_permission.png"
  darkSrc="/images/codex/enterprise/rbac_access_token_access_permission_dark.png"
  maxWidth={847}
  variant="no-wallpaper"
/>

1. Go to [Workspace Settings > Permissions & roles](https://chatgpt.com/admin/settings).
2. In the **Access tokens** section, turn on **Allow users to create access tokens** if all allowed members should be able to create access tokens.
3. If the workflow also needs a covered local surface, make sure **Allow members to use Codex Local** is turned on in the **Codex Local** section. This control covers local use in the ChatGPT desktop app, Codex CLI, and IDE extension.

Keep access token creation limited to people or service owners who understand where the token will be stored, which automation will use it, and how it will be rotated.

## Set an access token expiration limit

Workspace owners and admins can set the longest expiration that members can choose when they create a Codex access token. Go to [Workspace Settings > Permissions & roles](https://chatgpt.com/admin/settings), then set **Access token expiration limit** in the **Codex Local** section.

<CodexScreenshot
  alt="Access token expiration limit in ChatGPT workspace permissions settings"
  lightSrc="/images/codex/enterprise/access_token_expiration_limit.png"
  darkSrc="/images/codex/enterprise/access_token_expiration_limit_dark.png"
  maxWidth={847}
  variant="no-wallpaper"
/>

The limit applies to new access tokens. Existing tokens keep their current expiration.

## Create an access token

Use the Access tokens page to name the token and choose when it expires.

1. Go to [Access tokens](https://chatgpt.com/admin/access-tokens).
2. Select **Create**.

<CodexScreenshot
  alt="Access tokens page with the Create button"
  lightSrc="/images/codex/enterprise/access_token_create_header.png"
  darkSrc="/images/codex/enterprise/access_token_create_header_dark.png"
  maxWidth={942}
  variant="no-wallpaper"
/>

3. Enter a descriptive name, such as `release-ci` or `nightly-docs-check`.

<CodexScreenshot
  alt="Create access token modal with fields for name and expiration"
  lightSrc="/images/codex/enterprise/access_token_creation_modal.png"
  darkSrc="/images/codex/enterprise/access_token_creation_modal_dark.png"
  maxWidth={544}
  variant="no-wallpaper"
/>

4. Choose an expiration. Prefer a finite expiration such as 7, 30, 60, or 90 days. If you choose **No expiration**, rotate the token on a regular schedule.
5. Select **Create**.
6. Copy the generated access token immediately. You can't view it again after you close the modal.
7. Store the token in your secret manager or CI secret store.

The shortest custom expiration is one day. Revoked and expired tokens can't be used to start new authenticated runs.

## Use an access token with Codex CLI

For ephemeral automation, store the token in `CODEX_ACCESS_TOKEN` and run Codex CLI normally:

```bash
export CODEX_ACCESS_TOKEN="<access-token>"
codex exec --json "review this repository and summarize the top risks"
```

For a persistent local login, pipe the token to `codex login --with-access-token`:

```bash
printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token
codex exec "summarize the last release diff"
```

`codex login --with-access-token` stores an agent identity credential in Codex CLI auth storage. If you prefer not to persist credentials on the machine, use the `CODEX_ACCESS_TOKEN` environment variable instead.

`codex app-server` can use the same credential through `CODEX_ACCESS_TOKEN` or
a login created with `codex login --with-access-token` to authenticate its
OpenAI requests. That credential is separate from client-to-app-server
transport authentication. For a remote WebSocket connection, configure a
separate bearer or capability token as described in
[App server](https://learn.chatgpt.com/docs/app-server); don't reuse the Codex access token as the
transport token. See
[Authentication and network environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables#authentication-and-network).

## Rotate or revoke a token

Rotate access tokens the same way you rotate other automation secrets:

1. Create a replacement token.
2. Update the secret in the runner, scheduler, or secret manager.
3. Run a smoke test with the new token.
4. Revoke the old token from [Access tokens](https://chatgpt.com/admin/access-tokens).

From the Access tokens page, workspace owners and admins can revoke any workspace token. Members with access token permission can revoke only the tokens they created.

## Permission model

The workspace access token permission controls token creation. The **Allow
members to use Codex Local** workspace permission separately gates access to
local use in the ChatGPT desktop app, Codex CLI, and IDE extension. A member can
have that local access without permission to create access tokens.

| Capability                                                    | Workspace owners and admins                      | Member with access token permission           | Member without access token permission |
| ------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------- | -------------------------------------- |
| Open [Access tokens](https://chatgpt.com/admin/access-tokens) | Yes                                              | Yes                                           | No                                     |
| Create access tokens                                          | Yes, for their own ChatGPT workspace identity    | Yes, for their own ChatGPT workspace identity | No                                     |
| List access tokens                                            | Workspace list, including who created each token | Only tokens they created                      | No                                     |
| Revoke access tokens from the Access tokens page              | Any token in the workspace                       | Only tokens they created                      | No page access                         |
| Grant or remove access token permission                       | Yes                                              | No                                            | No                                     |
| Manage other local-client or Codex cloud settings             | Yes, based on workspace admin permissions        | No, unless separately granted                 | No                                     |

In short: workspace owners and admins manage access at the workspace level.
Members need the access token permission to create and manage their own tokens,
but that permission grants neither admin rights nor access to other members'
tokens.

## Troubleshooting

### The access tokens page returns 404 or forbidden

Ask a workspace owner or admin to confirm that your role includes **Allow users to create access tokens**. If your workflow also needs a covered local surface, confirm that **Allow members to use Codex Local** is enabled for local use in the ChatGPT desktop app, Codex CLI, and IDE extension.

### `codex login --with-access-token` fails

Confirm that you copied the generated access token, not a browser session token or Platform API key. Also confirm that the token hasn't expired or been revoked.

## Related docs

- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning)
- [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions)
- [Governance](https://learn.chatgpt.com/docs/enterprise/governance)
