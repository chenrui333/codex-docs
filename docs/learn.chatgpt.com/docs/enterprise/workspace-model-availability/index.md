---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/workspace-model-availability'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
---

# Workspace model availability

Source: https://learn.chatgpt.com/docs/enterprise/workspace-model-availability

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Model availability depends on the product surface and authentication boundary.
A ChatGPT workspace model setting isn't a universal model switch for Codex in
the ChatGPT desktop app, Codex CLI, IDE extension, Codex cloud, or Platform API.

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
