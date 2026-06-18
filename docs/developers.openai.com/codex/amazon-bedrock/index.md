---
source_type: 'developers'
source_area: 'codex_amazon_bedrock'
source_url: 'https://developers.openai.com/codex/amazon-bedrock'
source_last_modified: '2026-06-12T18:23:38Z'
source_etag: 'W/"1304ef72db81997c868a0ab8cf996584"'
codex_cli_versions: ["0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Use Codex with Amazon Bedrock | OpenAI Developers

Source: https://developers.openai.com/codex/amazon-bedrock

Configure Codex to use OpenAI models available through Amazon Bedrock. In this
setup, Codex runs locally and sends model requests to Bedrock using
AWS-managed authentication and access controls.

## How it works

When you configure Codex with Amazon Bedrock as the model provider, the
OpenAI-hosted Responses API isn’t in the request path. Codex sends model
requests to Amazon Bedrock, and Bedrock provides an OpenAI-compatible Responses
API implementation for supported OpenAI models.

Authentication is AWS-native. Users authenticate with a Bedrock API key or AWS
IAM credentials. They do not use ChatGPT sign-in or `OPENAI_API_KEY` for this
provider.

## Before you start

Make sure you have:

- Access to supported OpenAI models in Amazon Bedrock.
- An AWS Region where the selected model is available.
- Authentication for the Amazon Bedrock Mantle path configured for the AWS
  account.

## Configure Codex

Add the `amazon-bedrock` model provider for the Amazon Bedrock Mantle path to
`~/.codex/config.toml`. Supplying a model is optional. Select a supported model
explicitly when needed.

```
model_provider = "amazon-bedrock"
```

This guide covers the Amazon Bedrock Mantle path in supported commercial AWS
Regions. Codex doesn’t support Bedrock Mantle endpoints in AWS GovCloud
Regions.

## Authentication options

Codex supports two Bedrock authentication paths. It checks them in this order:

1. Bedrock API key.
2. AWS SDK credential chain.

### Option 1: Bedrock API key

Set the Bedrock API key in the environment Codex reads. You must specify a
Region when using API-key authentication.

```
export AWS_BEARER_TOKEN_BEDROCK=<your-bedrock-api-key>
export AWS_REGION=us-east-2
```

### Option 2: AWS SDK credentials

Use this path when your organization manages Bedrock access through the AWS SDK
credential chain. Codex can use these standard AWS SDK credential sources:

1. Shared AWS `config` and `credentials` files.

   ```
   aws configure
   ```
2. Environment variables.

   ```
   export AWS_ACCESS_KEY_ID=<your-access-key-id>
   export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
   export AWS_SESSION_TOKEN=<your-session-token>
   ```
3. AWS Management Console credentials.

   ```
   aws login
   ```
4. AWS SSO or a named profile.

   ```
   aws sso login --profile codex-bedrock
   export AWS_PROFILE=codex-bedrock
   ```
5. Federated identity configured with `credential_process`. For corporate SSO or
   OIDC federation, configure the AWS profile outside Codex and let the AWS SDK
   resolve credentials. Put browser login, token exchange, caching, and refresh
   in your AWS profile’s `credential_process` helper.

## Desktop app and VS Code extension

Desktop apps and IDE extensions may not inherit environment variables from the
shell. Put required values in `~/.codex/.env`, then restart the app or
extension.

```
export AWS_BEARER_TOKEN_BEDROCK=<your-bedrock-api-key>
export AWS_REGION=us-east-2
```

## Verify setup

- In Codex CLI, open `/status` and confirm Codex is using the
  `amazon-bedrock` model provider.
- In the desktop app or VS Code extension, start a new session after restarting
  the app.
- Confirm the selected model is available in the configured AWS Region and that
  the AWS identity has permission to access it.

## Supported models

Use exact model IDs:

```
openai.gpt-5.5
openai.gpt-5.4
```

Model availability varies by AWS Region. Before selecting a model, see [model
support by AWS
Region](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html).

## Feature availability

This configuration supports local Codex workflows. Some features that depend on
OpenAI-hosted cloud services, hosted tools, or cloud-managed discovery aren’t
currently available.

Fast Mode isn’t available with Amazon Bedrock. Fast Mode uses priority
processing, and the initial Amazon Bedrock offering supports on-demand
inference only.

Detailed feature availability

| Feature | Amazon Bedrock |
| --- | --- |
| Access and surfaces | |
| --- | --- |
| [Codex web](/codex/cloud) | — |
| [Codex app for local tasks](/codex/app) |  |
| [Codex CLI](/codex/cli) |  |
| [IDE extension](/codex/ide) |  |
| [Codex SDK, `codex exec`, and scriptable workflows](/codex/sdk) |  |
| Models and multimodal | |
| [Bedrock-backed inference with supported OpenAI models](/codex/amazon-bedrock) |  |
| [Fast mode](/codex/speed) | — |
| [Image generation and editing](/codex/app/features#image-generation) | — |
| [Voice dictation](/codex/app/features#voice-dictation) | — |
| [Web search](/codex/app/features#web-search) | — |
| Local features | |
| [Local code review with `/review`](/codex/workflows#do-a-local-code-review) |  |
| [Auto-review for approval requests](/codex/concepts/sandboxing/auto-review) |  |
| [Sandboxing and permission controls](/codex/permissions) |  |
| [Project and standalone app automations](/codex/app/automations) |  |
| [Automations](/codex/app/automations) |  |
| [Worktrees and built-in Git tools](/codex/app/worktrees) |  |
| [Local environments and repeatable actions](/codex/app/local-environments) |  |
| [Appshots](/codex/appshots) |  |
| Browser and remote control | |
| [In-app browser previews and comments](/codex/app/browser) |  |
| [Browser Use automation](/codex/app/browser#browser-use) | [Limited\*](#codex-plan-region-limits "Available with regional limits") |
| [Chrome extension browser control](/codex/app/chrome-extension) | [Limited\*](#codex-plan-region-limits "Available with regional limits") |
| [Computer Use](/codex/app/computer-use) | [Limited\*](#codex-plan-region-limits "Available with regional limits") |
| [SSH remote connections](/codex/remote-connections#connect-to-an-ssh-host) |  |
| [Mobile remote control](/codex/remote-connections) | — |
| Customization and extensions | |
| [Custom instructions with `AGENTS.md`](/codex/guides/agents-md) |  |
| [Skills](/codex/skills) |  |
| [Plugins](/codex/plugins) | [Limited†](#codex-plan-plugin-limits "Available with plugin limits") |
| [Plugin sharing](/codex/plugins/build#share-a-local-plugin-with-your-workspace) | — |
| [App connectors](/codex/plugins) | — |
| [MCP](/codex/mcp) |  |
| [Subagents and custom agents](/codex/subagents) |  |
| [Memories](/codex/memories) | [Limited\*](#codex-plan-region-limits "Available with regional limits") |
| [Chronicle](/codex/memories/chronicle) | — |
| Cloud and integrations | |
| [Codex cloud tasks](/codex/cloud) | — |
| [Sites](/codex/sites) | — |
| [GitHub issue and PR delegation with `@codex`](/codex/integrations/github#give-codex-other-tasks) | — |
| [GitHub code review and automatic PR reviews](/codex/integrations/github) | — |
| [Slack cloud integration](/codex/integrations/slack) | — |
| [Linear cloud integration](/codex/integrations/linear) | — |
| Admin, security, and analytics | |
| [SAML SSO, MFA, and workspace user management](/codex/enterprise/admin-setup) | — |
| [`requirements.toml` managed config](/codex/enterprise/managed-configuration) |  |
| [Cloud-managed config policies](/codex/enterprise/managed-configuration#cloud-managed-requirements) | — |
| [Codex RBAC and custom roles](/codex/enterprise/admin-setup#step-2-set-up-custom-roles-rbac) | — |
| [SCIM, EKM, and domain verification](/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy) | — |
| [Enterprise retention and residency controls](/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy) | — |
| [No training on API or business data by default](https://openai.com/business-data/) |  |
| [Analytics dashboard](/codex/enterprise/governance#analytics-dashboard) | — |
| [Analytics API](/codex/enterprise/governance#analytics-api) | — |
| [Compliance API and audit logs](/codex/enterprise/governance#compliance-api) | — |
| [Codex Security for connected GitHub repositories](/codex/security) | — |

\* Feature is currently limited to only specific regions. Check
the individual feature documentation to learn more about geo restrictions.

† Local plugin bundles are supported when their capabilities do
not require ChatGPT authentication. OpenAI-curated plugin discovery and
features that depend on app connectors or cloud-hosted sharing aren’t
available.

## Troubleshooting

If setup fails, check the following:

- The model ID exactly matches a supported model.
- You specify an AWS Region where the model is available.
- The Bedrock API key or AWS credentials are valid and not expired.
- The AWS identity has permission to access the selected Bedrock model.
- `AWS_BEARER_TOKEN_BEDROCK` isn’t set to an expired or unintended key.
- For desktop app or VS Code extension usage, required environment variables
  are present in `~/.codex/.env`.

## Support boundaries

OpenAI Support can help with Codex client setup, configuration, local CLI
behavior, desktop app behavior, IDE extension behavior, and the local Codex
product experience.

For AWS credentials, IAM permissions, Bedrock model access, quotas, billing,
regional availability, Bedrock request failures, AWS service logs, or Bedrock
service behavior, contact the customer’s AWS administrator or AWS Support.

