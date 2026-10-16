---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/prisma-airs'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Prisma AIRS

Source: https://learn.chatgpt.com/docs/enterprise/prisma-airs

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Connect Palo Alto Networks Prisma AIRS to apply your security policies to
Codex prompts before they reach the model. Workspace admins configure the
integration once for their workspace.

Prisma AIRS can apply the protections configured in your security profile, such
as data loss prevention, prompt injection detection, and malicious URL
detection.

## Before you begin

You need:

- A ChatGPT workspace with Prisma AIRS access enabled. Contact your OpenAI
  account team to request access.
- Workspace administrator permissions.
- A Prisma AIRS API key, a configured security profile, and the service endpoint
  for your deployment.

## Connect Prisma AIRS

1. Open [Admin Console](https://admin.openai.com)
   as a workspace administrator and select your workspace.
2. Under **Policy & security**, select **External guardrails** and find
   **Prisma AIRS**. If this entry isn't available, ask your OpenAI account team
   to enable access for your workspace.
3. Enter your **API key**, **Security profile** name or ID, and **Endpoint
   URL**.
4. Choose an **Enforcement mode** and the behavior **On AIRS failure**.
5. Select **Save connection**. Codex validates the connection and encrypts your
   API key.
6. Select **Test connection** to verify the saved configuration.
7. Turn on **Enable Prisma AIRS** to start scanning prompts across the
   workspace.

Saving the connection doesn't enable scanning. You must also turn on **Enable
Prisma AIRS**.

## Choose an endpoint

Use the approved endpoint for your Prisma AIRS deployment:

| Region        | Endpoint                                                 |
| ------------- | -------------------------------------------------------- |
| United States | `https://service.api.aisecurity.paloaltonetworks.com`    |
| Germany       | `https://service-de.api.aisecurity.paloaltonetworks.com` |
| India         | `https://service-in.api.aisecurity.paloaltonetworks.com` |
| Singapore     | `https://service-sg.api.aisecurity.paloaltonetworks.com` |

Codex uses the United States endpoint by default. Workspace data-residency
requirements can restrict which endpoint you can use.

## Choose how to handle prompts

**Enforcement mode** determines what happens when Prisma AIRS flags a prompt:

- **Block**: Stop the prompt before it reaches the model. This is the default.
- **Alert only**: Record the detection and allow the prompt to continue.

**On AIRS failure** determines what happens if Prisma AIRS is unavailable or
doesn't respond:

- **Allow prompts**: Continue without a completed scan. This is the default.
- **Block prompts**: Stop the prompt until Prisma AIRS can scan it.

Choose **Block prompts** when your security policy requires every covered prompt
to receive a scan decision.

## Understand what gets scanned

Codex sends newly submitted prompt text to the configured Prisma AIRS endpoint
for inspection. This applies to covered Codex workflows, including the app, CLI,
IDE extension, and cloud, when users authenticate to the configured ChatGPT
workspace. Sessions authenticated with a Platform API key aren't covered. See
[Enforce a login method or workspace](https://learn.chatgpt.com/docs/auth#enforce-a-login-method-or-workspace)
to require the intended sign-in method and workspace.

Prisma AIRS doesn't scan assistant responses, tool calls, tool results, files,
or images through this integration. Your configured security profile determines
which threats and sensitive data Prisma AIRS detects.

Codex encrypts your API key and never displays it after you save it. Review Palo
Alto Networks' data-handling, retention, and residency policies before enabling
prompt inspection. Those policies apply to prompts sent to Prisma AIRS.

## Manage the connection

Return to [Admin Console](https://admin.openai.com),
select your workspace, and open **Policy & security** > **External guardrails**
to manage the integration:

- Select **Test connection** to verify your saved API key, security profile,
  and endpoint.
- Enter a new key and select **Rotate API key** to replace the saved key
  without changing the other settings.
- Turn off **Enable Prisma AIRS** to stop scanning while preserving the saved
  configuration.
- Select **Disconnect**, then confirm, to stop scanning and delete the saved
  connection and API key.

### Disable or disconnect without a sidebar entry

If **External guardrails** doesn't appear for a workspace with a saved
configuration, a workspace administrator can open the limited recovery view at
`https://admin.openai.com/workspace/<workspace-id>/external-guardrails`.
Replace `<workspace-id>` with the workspace ID from your Admin Console URL.

This view lets you see the saved configuration, turn off **Enable Prisma AIRS**,
or select **Disconnect** and confirm. It doesn't allow setup, configuration
changes, connection testing, key rotation, or turning the integration back on.
Contact your OpenAI account team to restore configuration access.

For broader workspace setup and policy management, see the
[Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup) and
[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration).
