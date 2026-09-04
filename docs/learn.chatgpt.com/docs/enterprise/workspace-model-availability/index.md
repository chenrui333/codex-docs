---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/workspace-model-availability'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Workspace model availability

Source: https://learn.chatgpt.com/docs/enterprise/workspace-model-availability

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

The models available to someone depend on the product surface and how they
signed in. A model setting in your ChatGPT workspace doesn't automatically
apply to Codex in the ChatGPT desktop app, Codex CLI, the IDE extension, Codex
cloud, or the OpenAI API.

For the complete administration model, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

## Identify the model boundary

| Product or authentication boundary                                                         | Model access follows                                                                                  | Current source                                                                                                                |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| ChatGPT workspace                                                                          | The workspace plan, member access, workspace settings, and supported role permissions                 | [ChatGPT Enterprise and Edu models and limits](https://help.openai.com/en/articles/11165333-chatgpt-enterprise-models-limits) |
| Codex in the ChatGPT desktop app, Codex CLI, and IDE extension with ChatGPT sign-in        | Models supported by the specific client and the access available to the signed-in ChatGPT identity    | [Codex models](https://learn.chatgpt.com/docs/models) and current workspace guidance                                                                  |
| Codex cloud                                                                                | Models supported by hosted Codex workflows and the access available to the signed-in ChatGPT identity | [Codex models](https://learn.chatgpt.com/docs/models) and [Codex cloud](https://learn.chatgpt.com/docs/cloud)                                                                 |
| Codex in the ChatGPT desktop app, Codex CLI, and IDE extension with API-key authentication | The OpenAI API organization and project associated with the key                                       | [Authentication](https://learn.chatgpt.com/docs/auth) and the [OpenAI API Platform](https://platform.openai.com/docs/overview)                        |

Check the current source for the surface the user is actually using. Don't
copy a model catalog or assume that a ChatGPT model-picker setting has the same
effect for Codex in the ChatGPT desktop app, Codex CLI, IDE extension, Codex
cloud, and the API Platform.

## Set a clear starting experience for employees

Review [Models settings](https://help.openai.com/en/articles/8411955) for your
workspace before inviting a pilot group. Workspace owners and admins can
configure separate starting defaults for Chat and for Work and Codex. Where
supported, choose a starting model, reasoning level, speed, and new-chat
behavior for Chat, Work, and local Codex surfaces.

Treat these choices as defaults, not permissions. Available models still depend
on the member's seat, role, workspace or API identity, enforced workspace
requirements, and the specific surface they're using. Starting defaults don't
grant access to unavailable models or override those requirements. Codex cloud
doesn't support changing its default model.

Fast mode availability depends on the workspace, product surface, and any
enforced `features.fast_mode` setting in
[`requirements.toml`](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml).
This setting can pin Fast mode on or off for managed local Codex clients; it
isn't a starting default and can't override workspace or product availability.

## GPT-6 Astra in Enterprise

GPT‑6 Astra is rolling out today for enterprises in our [Trusted Access Program⁠](https://openai.com/form/enterprise-trusted-access-for-cyber/), with access through API and our Plus, Pro, Business and Enterprise plans coming in the coming days.

During the initial rollout, your organization must have Daybreak access before
an administrator can enable Astra. Astra is off by default for ChatGPT
Enterprise for the first two weeks after launch. Administrators in eligible
workspaces can enable Astra for users or groups
across Chat, Work, and Codex. Existing product eligibility still applies. Review your
[workspace model settings](https://help.openai.com/en/articles/8411955) and
confirm availability on each client used by your pilot group.

Enabling access and choosing a starting model are separate decisions. Check the
applicable seat, role, and billing arrangement before setting Astra as a default.
See [pricing](https://learn.chatgpt.com/docs/pricing) for allowance and billing
guidance and [safety monitoring](https://learn.chatgpt.com/docs/agent-approvals-security#safety-monitoring-and-paused-tasks)
for tasks that pause for review.

For API-key sign-in, Astra access follows the API organization and project
associated with the key. Enabling Astra in a ChatGPT workspace doesn't grant
API access. Early access with an API key also requires client configuration;
ask your OpenAI account team for setup instructions. Selecting a
model or changing local configuration doesn't grant access by itself.

## Prepare for the GPT-5.4 retirement

On August 31, 2026, GPT-5.4 and GPT-5.4 mini retire from Codex for users signed
in with ChatGPT. Update affected workspace defaults, saved model settings,
managed configurations, custom agents, and scheduled tasks before then:

- Replace `gpt-5.4` with `gpt-5.6-terra` (GPT-5.6 Terra).
- Replace `gpt-5.4-mini` with `gpt-5.6-luna` (GPT-5.6 Luna).

The OpenAI API and Codex authenticated with your own API key aren't affected.
See [Codex models](https://learn.chatgpt.com/docs/models#deprecated-codex-models) and
[managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
for migration details.

## Separate access from runtime permissions

Model access determines whether a model is available to the authenticated user
on a supported surface. Local permission profiles and managed requirements
determine what an agent can do after a local run starts, such as which files it
can change or which network destinations it can reach.

A permission profile can't grant model access. Model access also can't weaken
the sandbox, approval policy, network controls, or source-system permissions
that apply to a run.

## Troubleshoot model access

If a user can't select an expected model:

- Confirm the product surface and sign-in method.
- Confirm the ChatGPT workspace or Platform API organization and project.
- Review the current access controls for that authentication boundary.
- Check whether the selected local client or Codex cloud supports the model.

## Current sources

- [ChatGPT Enterprise and Edu models and limits](https://help.openai.com/en/articles/11165333-chatgpt-enterprise-models-limits)
- [Manage workspace settings](https://help.openai.com/en/articles/8411955)
- [Role-based access control](https://help.openai.com/en/articles/11750701-rbac)
- [Codex models](https://learn.chatgpt.com/docs/models)
- [Codex feature availability by plan](https://learn.chatgpt.com/docs/pricing#feature-availability)
- [Authentication](https://learn.chatgpt.com/docs/auth)

## Related docs

- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning)
- [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions)
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
