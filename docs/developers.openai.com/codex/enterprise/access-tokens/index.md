---
source_type: 'developers'
source_area: 'codex_enterprise'
source_url: 'https://developers.openai.com/codex/enterprise/access-tokens'
source_last_modified: '2026-05-14T23:16:34Z'
source_etag: 'W/"e6f5ef1e7e16eaeda69719dfb2988501"'
codex_cli_versions: ["0.130.0"]
codex_cli_versions_raw: ["codex-cli 0.130.0"]
---

# Access tokens – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/enterprise/access-tokens

Codex access tokens let trusted automation run Codex local with a ChatGPT workspace identity. Use them when a script, scheduled job, or CI runner needs repeatable, non-interactive Codex access.

Codex access tokens are currently supported for ChatGPT Business and
Enterprise workspaces.

Access tokens are created in the ChatGPT admin console at [Access tokens](https://chatgpt.com/admin/access-tokens). They are tied to the ChatGPT user and workspace that create them, and Codex uses them as agent identities for programmatic local workflows.

If a Platform API key works for your automation, keep using API key auth. Use
Codex access tokens when the workflow specifically needs ChatGPT workspace
access, ChatGPT-managed Codex entitlements, or enterprise workspace controls.

## How access tokens work

Use an access token when Codex needs to run without a user completing a browser sign-in. The token represents the ChatGPT workspace user who created it, so runs can use that user’s Codex access and appear in workspace governance data.

Codex checks the token when a run starts and ties the run to that workspace identity. Treat the token like any other automation secret: store it in a secret manager, keep it out of logs, and rotate it regularly.

Use access tokens for:

- `codex exec` jobs that run from trusted automation.
- Local scripts that need repeatable, non-interactive Codex runs.
- Enterprise workflows where usage should be associated with a ChatGPT workspace user instead of an API organization key.

Main risks to avoid:

- **Leaked secrets:** anyone with the token can start Codex runs as the token creator. Store tokens in a secret manager, keep them out of logs, and rotate them regularly.
- **Untrusted runners:** public CI, forked pull requests, or shared machines can expose tokens to people outside your workspace. Use access tokens only on trusted runners.
- **Shared identities:** one person’s token reused across unrelated teams makes ownership and audit trails harder to interpret. Create tokens for a specific workflow owner.
- **Stale credentials:** long-lived tokens can remain active after the workflow changes. Prefer finite expirations and revoke tokens that are no longer used.
- **Wrong credential type:** access tokens are for Codex local workflows. Use Platform API keys for general OpenAI API calls.

## Enable access token creation

Use the Codex Local controls in workspace settings to turn on access token creation for allowed members.

![Access token access permission in ChatGPT workspace RBAC settings](/images/codex/enterprise/rbac_access_token_access_permission.png)

1. Go to [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings).
2. In the Codex Local section, make sure **Allow members to use Codex Local** is turned on.
3. Turn on **Allow members to use Codex access tokens** if all allowed members should be able to create access tokens.
4. If you use custom roles for a narrower rollout, assign the access token permission only to groups that need to create tokens.

Keep access token creation limited to people or service owners who understand where the token will be stored, which automation will use it, and how it will be rotated.

## Create an access token

Use the Access tokens page to name the token and choose when it expires.

1. Go to [Access tokens](https://chatgpt.com/admin/access-tokens).
2. Select **Create**.

![Access tokens page with the Create button](/images/codex/enterprise/access_token_create_header.png)

3. Enter a descriptive name, such as `release-ci` or `nightly-docs-check`.

![Create access token modal with fields for name and expiration](/images/codex/enterprise/access_token_creation_modal.png)

4. Choose an expiration. Prefer a finite expiration such as 7, 30, 60, or 90 days. If you choose **No expiration**, rotate the token on a regular schedule.
5. Select **Create**.
6. Copy the generated access token immediately. You cannot view it again after you close the modal.
7. Store the token in your secret manager or CI secret store.

The shortest custom expiration is one day. Revoked and expired tokens cannot be used to start new Codex runs.

## Use an access token with Codex CLI

For ephemeral automation, store the token in `CODEX_ACCESS_TOKEN` and run Codex normally:

```
export CODEX_ACCESS_TOKEN="<access-token>"
codex exec --json "review this repository and summarize the top risks"
```

For a persistent local login, pipe the token to `codex login --with-access-token`:

```
printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token
codex exec "summarize the last release diff"
```

`codex login --with-access-token` stores an agent identity credential in Codex auth storage. If you prefer not to persist credentials on the machine, use the `CODEX_ACCESS_TOKEN` environment variable instead.

## Rotate or revoke a token

Rotate access tokens the same way you rotate other automation secrets:

1. Create a replacement token.
2. Update the secret in the runner, scheduler, or secret manager.
3. Run a smoke test with the new token.
4. Revoke the old token from [Access tokens](https://chatgpt.com/admin/access-tokens).

From the Access tokens page, workspace owners and admins can revoke any workspace token. Members with access token permission can revoke only the tokens they created.

## Permission model

Access token permissions are separate from the general Codex local permission. A member can have access to the Codex app, CLI, or IDE extension without being allowed to create access tokens.

| Capability | Workspace owners and admins | Member with access token permission | Member without access token permission |
| --- | --- | --- | --- |
| Open [Access tokens](https://chatgpt.com/admin/access-tokens) | Yes | Yes | No |
| Create access tokens | Yes, for their own ChatGPT workspace identity | Yes, for their own ChatGPT workspace identity | No |
| List access tokens | Workspace list, including who created each token | Only tokens they created | No |
| Revoke access tokens from the Access tokens page | Any token in the workspace | Only tokens they created | No page access |
| Grant or remove access token permission | Yes | No | No |
| Manage other Codex enterprise settings | Yes, based on admin role and Codex admin permissions | No, unless separately granted | No |

In short: workspace owners and admins manage access at the workspace level. Members need the access token permission to create and manage their own tokens, but the permission does not grant admin rights or access to other members’ tokens.

## Troubleshooting

### The access tokens page returns 404 or forbidden

Ask a workspace owner or admin to confirm that Codex access tokens are enabled and that your role includes the access token permission.

### `codex login --with-access-token` fails

Confirm that you copied the generated access token, not a browser session token or Platform API key. Also confirm that the token has not expired or been revoked.

## Related docs

- [Authentication](/codex/auth)
- [Non-interactive mode](/codex/noninteractive)
- [Admin setup](/codex/enterprise/admin-setup)
- [Governance](/codex/enterprise/governance)

