---
source_type: 'learn'
source_area: 'learn_agent_configuration'
source_url: 'https://learn.chatgpt.com/docs/agent-configuration/speed'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Fast and Ultrafast modes

Source: https://learn.chatgpt.com/docs/agent-configuration/speed

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

> Illustration: An animated starfield illustrates Ultrafast mode.

In ChatGPT Work and Codex, **Fast** and **Ultrafast** generate tokens faster
than **Standard** on the same model. Both use more of your plan's allowance
or credits.

## Choose a speed in the composer

In ChatGPT Work on the web or in the Codex desktop app, open the model or
effort picker at the bottom of the composer.

- If **Ultrafast** is available to you, select the lightning bolt to open the
  speed menu, then choose a speed.
- If your only options are **Standard** and **Fast**, selecting the lightning
  bolt switches between them immediately.

In the advanced picker, select **Speed**. In ChatGPT Work on mobile, open the
model picker and use the speed setting.

> Illustration: GPT-6.2 Astra speed picker with Standard, Fast, and Ultrafast.

## Fast mode

Fast mode supports GPT-6.2 Astra and GPT-6.2 Sol. You can also use it with
GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Astra, GPT-6 Sol, and GPT-6 Luna. On
GPT-6.2 Astra and GPT-5.6, Fast generates tokens at about 1.5 times the
speed of Standard.

With ChatGPT sign-in, you can also use Fast in the Codex CLI and IDE extension.
See [Fast pricing](https://learn.chatgpt.com/docs/pricing?codex-pricing-speed=fast#speed-multipliers)
for the usage rate for your model.

<a
  id="astra-ultrafast"
  className="block scroll-mt-[var(--docs-scroll-offset)]"
></a>

## Ultrafast mode

<a
  id="gpt-62-speed-options"
  className="block scroll-mt-[var(--docs-scroll-offset)]"
></a>

On GPT-6.2 Astra and GPT-6.2 Sol, Ultrafast generates tokens at up to
4.5 times the speed of Standard on the same model. Choose Ultrafast in the
[composer](#choose-a-speed-in-the-composer) in ChatGPT Work or the Codex app,
or use the [Codex CLI](#codex-cli-controls).

- **Pro.** The models you can use with Ultrafast depend on your plan. See
  [GPT-6.2 Ultrafast availability by Pro plan](https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol).
  On Pro $500, both models are available. Ultrafast uses your included
  allowance first, then any available credits.
- **Enterprise and Edu.** Both models support Ultrafast in eligible workspaces.
  If you don't see it, ask your workspace owner to check
  [model access and Ultrafast permissions](#ultrafast-plan-and-workspace-requirements).

ChatGPT Work and Codex share pricing, credits, and usage limits. See
[Ultrafast pricing](https://learn.chatgpt.com/docs/pricing?codex-pricing-speed=ultrafast#speed-multipliers)
for included usage, purchased credits, and eligible pay-as-you-go rates.

GPT-6 Astra and GPT-6.1 Sol also support Ultrafast on Pro $500 and eligible
Enterprise and Edu plans. In Codex, GPT-6 Astra generates tokens at up to
eight times its Standard speed with Ultrafast.

<a id="availability-and-billing-details"></a>

### Ultrafast plan and workspace requirements

Enterprise workspaces need a credit-based or USD usage-based agreement. Edu
workspaces need a credit-based plan.

Workspace owners must enable [the GPT-6.2 models they want members to use](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability#gpt-62-astra-and-gpt-62-sol-in-enterprise-and-edu).
Ultrafast is a separate permission and is off by default. Owners can enable it
for selected users or the whole workspace in
[workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).
[Per-user spend controls](https://learn.chatgpt.com/docs/enterprise/usage-limits) apply.

For GPT-6.2 Astra, GPT-6.2 Sol, and GPT-6 Astra, Ultrafast supports inference
residency only in the United States. For GPT-6.1 Sol, it also supports Europe
(EEA and Switzerland).

## Codex CLI controls

In the CLI, type `/` to see which commands are available for your model.
Use `/fast` or `/ultrafast` to choose a speed. Repeat the active command to
return to Standard. The CLI saves your selection. To show Fast mode in the
footer, use `/statusline`.

## API billing

When you sign in to Codex with an API key, you pay API token rates. ChatGPT credit
multipliers apply only when you sign in with ChatGPT. See
[Ultrafast mode in the API](https://developers.openai.com/api/docs/guides/ultrafast-mode) for supported
models, request configuration, and pricing.

## Retirement and migration

[GPT-5.5 retired from Codex](https://learn.chatgpt.com/docs/models#gpt-55-retirement) for users signed
in with ChatGPT on October 14, 2026, at noon PDT (19:00 UTC).
