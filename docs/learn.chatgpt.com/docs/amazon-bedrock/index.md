---
source_type: 'learn'
source_area: 'learn_amazon_bedrock'
source_url: 'https://learn.chatgpt.com/docs/amazon-bedrock'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Use ChatGPT Work and Codex with Amazon Bedrock

Source: https://learn.chatgpt.com/docs/amazon-bedrock

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Configure local ChatGPT Work and Codex surfaces to use OpenAI models available
through Amazon Bedrock. In this setup, the local client sends model requests to
Bedrock using AWS-managed authentication and access controls.

## How it works

When you configure a local ChatGPT Work or Codex surface with Amazon Bedrock as
the model provider, the OpenAI-hosted Responses API isn't in the request path.
The local client sends model requests to Amazon Bedrock, and Bedrock provides an
OpenAI-compatible Responses API implementation for supported OpenAI models.

Authentication is AWS-native. Users authenticate with a Bedrock API key or AWS
  IAM credentials. They do not use ChatGPT sign-in or `OPENAI_API_KEY` for this
  provider.

## Before you start

Make sure you have:

- Access to supported OpenAI models in Amazon Bedrock.
- An AWS Region where the selected model is available.
- Authentication for the Amazon Bedrock Mantle path configured for the AWS
  account.

## Configure the provider

Add the `amazon-bedrock` model provider for the Amazon Bedrock Mantle path to
`~/.codex/config.toml`. The ChatGPT desktop app, Codex CLI, IDE extension, and
SDK read the same local configuration layers. Supplying a model is optional.
Select a supported model explicitly when needed.

```toml
model_provider = "amazon-bedrock"
```

This guide covers the Amazon Bedrock Mantle path in supported commercial AWS
  Regions. Local ChatGPT Work and Codex surfaces don't support Bedrock Mantle
  endpoints in AWS GovCloud Regions.

## Authentication options

Local ChatGPT Work and Codex surfaces support two Bedrock authentication paths.
They check them in this order:

1. Bedrock API key.
2. AWS SDK credential chain.

### Option 1: Bedrock API key

Set the Bedrock API key in the environment the local client reads. You must
specify a Region when using API-key authentication.

```shell
export AWS_BEARER_TOKEN_BEDROCK=<your-bedrock-api-key>
export AWS_REGION=us-east-2
```

### Option 2: AWS SDK credentials

Use this path when your organization manages Bedrock access through the AWS SDK
credential chain. The local client can use these standard AWS SDK credential
sources:

#### Shared AWS configuration files

Configure the shared AWS `config` and `credentials` files:

```shell
aws configure
```

#### Environment variables

Set the standard AWS SDK credential environment variables:

```shell
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
export AWS_SESSION_TOKEN=<your-session-token>
```

#### AWS Management Console credentials

Log in with AWS Management Console credentials:

```shell
aws login
```

#### AWS SSO or a named profile

Log in with AWS SSO and select the named profile:

```shell
aws sso login --profile codex-bedrock
export AWS_PROFILE=codex-bedrock
```

#### Federated identity

For corporate SSO or OIDC federation, configure a federated identity with
`credential_process` outside the local client and let the AWS SDK resolve
credentials. Put browser login, token exchange, caching, and refresh in your
AWS profile's `credential_process` helper.

## Desktop app and IDE extension

Desktop apps and IDE extensions may not inherit environment variables from the
shell. Put required values in `~/.codex/.env`, then restart the app or
extension.

```shell
export AWS_BEARER_TOKEN_BEDROCK=<your-bedrock-api-key>
export AWS_REGION=us-east-2
```

## Verify setup

- In Codex CLI, open `/status` and confirm Codex is using the
  `amazon-bedrock` model provider.
- In the ChatGPT desktop app, select Work or Codex and start a new task after
  restarting the app.
- In the IDE extension, start a new session after restarting the extension.
- Confirm the selected model is available in the configured AWS Region and that
  the AWS identity has permission to access it.

## Supported models

Use exact model IDs:

```text
openai.gpt-5.6-sol
openai.gpt-5.6-terra
openai.gpt-5.6-luna
openai.gpt-5.5
openai.gpt-5.4
```

Model availability varies by AWS Region. Before selecting a model, see [model
support by AWS
Region](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html).

## Feature availability

This configuration supports local ChatGPT Work and Codex workflows. Hosted
ChatGPT Work on the web, Codex cloud, and features that depend on OpenAI-hosted
cloud services, hosted tools, or cloud-managed discovery aren't currently
available.

Fast Mode isn't available with Amazon Bedrock. Fast Mode uses priority
  processing, and the initial Amazon Bedrock offering supports on-demand
  inference only.

<ToggleSection title="Detailed feature availability">
  <CodexPlanFeatureMatrix
    client:load
    data={{
      plans: [
        {
          id: "bedrock",
          shortLabel: "Amazon Bedrock",
          label: "Amazon Bedrock",
        },
      ],
      sections: [
        {
          title: "Access and surfaces",
          features: [
            {
              name: "ChatGPT Work on the web",
              href: "/codex/get-started-with-work",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Codex cloud",
              href: "/codex/cloud",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "ChatGPT Work or Codex in the ChatGPT desktop app",
              shortName: "ChatGPT desktop app",
              href: "/codex/app",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Codex CLI",
              href: "/codex/cli",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "IDE extension",
              href: "/codex/ide",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Codex SDK, `codex exec`, and scriptable workflows",
              shortName: "Codex SDK and scripting",
              href: "/codex/codex-sdk",
              availability: {
                bedrock: "available",
              },
            },
          ],
        },
        {
          title: "Models and multimodal",
          features: [
            {
              name: "Bedrock-backed inference with supported OpenAI models",
              shortName: "Bedrock-backed inference",
              href: "/codex/amazon-bedrock",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Fast mode",
              href: "/codex/agent-configuration/speed",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Image generation and editing",
              href: "/codex/image-generation?surface=app",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Voice dictation",
              href: "/codex/prompting#use-voice-dictation",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Web search",
              href: "/codex/web-search?surface=app",
              availability: {
                bedrock: "unavailable",
              },
            },
          ],
        },
        {
          title: "Local features",
          features: [
            {
              name: "Local code review with `/review`",
              shortName: "Local code review",
              href: "/codex/prompting#do-a-local-code-review",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Auto-review for approval requests",
              href: "/codex/sandboxing/auto-review",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Sandboxing and permission controls",
              href: "/codex/permissions",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Project and standalone scheduled tasks",
              shortName: "Scheduled tasks",
              href: "/codex/automations",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Scheduled tasks",
              href: "/codex/automations",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Worktrees and built-in Git tools",
              shortName: "Built-in Git tools",
              href: "/codex/environments/git-worktrees",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Local environments and repeatable actions",
              shortName: "Repeatable actions",
              href: "/codex/environments/local-environment",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Appshots",
              href: "/codex/appshots",
              availability: {
                bedrock: "available",
              },
            },
          ],
        },
        {
          title: "Browser and remote control",
          features: [
            {
              name: "Built-in browser previews and comments",
              shortName: "Built-in browser",
              href: "/codex/browser?surface=app",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Computer Use in the browser",
              href: "/codex/browser?surface=app#app-computer-use-in-the-browser",
              availability: {
                bedrock: "limited",
              },
            },
            {
              name: "Use ChatGPT with Chrome",
              shortName: "Chrome browser control",
              href: "/codex/chrome-extension",
              availability: {
                bedrock: "limited",
              },
            },
            {
              name: "Computer Use",
              href: "/codex/computer-use",
              availability: {
                bedrock: "limited",
              },
            },
            {
              name: "SSH remote connections",
              shortName: "SSH remote",
              href: "/codex/remote-connections#connect-to-an-ssh-host",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Mobile remote control",
              href: "/codex/remote-connections",
              availability: {
                bedrock: "unavailable",
              },
            },
          ],
        },
        {
          title: "Customization and extensions",
          features: [
            {
              name: "Custom instructions with `AGENTS.md`",
              shortName: "Custom instructions",
              href: "/codex/agent-configuration/agents-md",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Skills",
              href: "/codex/build-skills",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Plugins",
              href: "/codex/plugins",
              availability: {
                bedrock: "limited",
              },
              limitedFootnote: "plugins",
            },
            {
              name: "Plugin sharing",
              href: "https://developers.openai.com/plugins/build/plugins#share-a-local-plugin-with-your-workspace",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Connectors",
              href: "/codex/plugins",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "MCP",
              href: "/codex/extend/mcp",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Subagents and custom agents",
              shortName: "Subagents",
              href: "/codex/agent-configuration/subagents",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Memories",
              href: "/codex/customization/memories",
              availability: {
                bedrock: "limited",
              },
            },
            {
              name: "Chronicle",
              href: "/codex/customization/chronicle",
              availability: {
                bedrock: "unavailable",
              },
            },
          ],
        },
        {
          title: "Cloud and integrations",
          features: [
            {
              name: "Codex cloud chats",
              shortName: "Cloud chats",
              href: "/codex/cloud",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Sites",
              href: "/codex/sites",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "GitHub issue and PR delegation with `@codex`",
              shortName: "GitHub delegation",
              href: "/codex/third-party/github#give-codex-other-tasks",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "GitHub code review and automatic PR reviews",
              shortName: "GitHub PR reviews",
              href: "/codex/third-party/github",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Slack cloud integration",
              shortName: "Slack integration",
              href: "/codex/third-party/slack",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Linear cloud integration",
              shortName: "Linear integration",
              href: "/codex/third-party/linear",
              availability: {
                bedrock: "unavailable",
              },
            },
          ],
        },
        {
          title: "Admin, security, and analytics",
          features: [
            {
              name: "SAML SSO, MFA, and workspace user management",
              shortName: "Workspace management",
              href: "/codex/enterprise/admin-setup",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "`requirements.toml` managed config",
              shortName: "`requirements.toml` config",
              href: "/codex/enterprise/managed-configuration",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Cloud-managed config policies",
              shortName: "Cloud-managed policies",
              href: "/codex/enterprise/managed-configuration#cloud-managed-requirements",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "ChatGPT workspace RBAC and custom roles",
              shortName: "RBAC and roles",
              href: "/codex/enterprise/roles-and-workspace-permissions",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "SCIM, EKM, and domain verification",
              shortName: "SCIM, EKM, and domains",
              href: "/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Enterprise retention and residency controls",
              shortName: "Retention and residency",
              href: "/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "No training on API or business data by default",
              shortName: "No default training",
              href: "https://openai.com/business-data/",
              availability: {
                bedrock: "available",
              },
            },
            {
              name: "Analytics dashboard",
              href: "/codex/enterprise/workspace-analytics",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Analytics API",
              href: "/codex/enterprise/analytics-api",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Compliance API and audit logs",
              shortName: "Compliance and audit logs",
              href: "/codex/enterprise/compliance-api",
              availability: {
                bedrock: "unavailable",
              },
            },
            {
              name: "Codex Security for connected GitHub repositories",
              shortName: "Codex Security",
              href: "/codex/security",
              availability: {
                bedrock: "unavailable",
              },
            },
          ],
        },
      ],
    }}
  />

  <div
    id="codex-plan-region-limits"
    className="not-prose mt-3 text-sm text-secondary"
  >
    <sup>*</sup> Feature is currently limited to only specific regions. Check
    the individual feature documentation to learn more about geo restrictions.

  <div
    id="codex-plan-plugin-limits"
    className="not-prose mt-1 text-sm text-secondary"
  >
    <sup>†</sup> Local plugin bundles are supported when their capabilities do
    not require ChatGPT authentication. OpenAI-curated plugin discovery and
    features that depend on connectors or cloud-hosted sharing aren't
    available.

</ToggleSection>

## Troubleshooting

If setup fails, check the following:

- The model ID exactly matches a supported model.
- You specify an AWS Region where the model is available.
- The Bedrock API key or AWS credentials are valid and not expired.
- The AWS identity has permission to access the selected Bedrock model.
- `AWS_BEARER_TOKEN_BEDROCK` isn't set to an expired or unintended key.
- For desktop app or IDE extension usage, required environment variables are
  present in `~/.codex/.env`.

## Support boundaries

OpenAI Support can help with ChatGPT Work and Codex client setup,
configuration, local CLI behavior, desktop app behavior, IDE extension behavior,
and the local product experience.

For AWS credentials, IAM permissions, Bedrock model access, quotas, billing,
regional availability, Bedrock request failures, AWS service logs, or Bedrock
service behavior, contact the customer's AWS administrator or AWS Support.
