---
source_type: 'learn'
source_area: 'learn_models'
source_url: 'https://learn.chatgpt.com/docs/models'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Models

Source: https://learn.chatgpt.com/docs/models

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Choosing a model is about finding the right balance of speed, cost, and capability
for your task. Sometimes you need a quick first draft. Other times, a complex
problem calls for more careful reasoning. This guide introduces our latest
models, shows where each one shines, and helps you find a starting point for
your work.

GPT-5.5 retirement: [See replacement models and migration
  steps](#gpt-55-retirement).

<ContentModeSwitch group="codex-surface" id="app">

## Choose a model

In Work or Codex in the ChatGPT desktop app, use the model and reasoning control
beneath the composer to choose an available model and adjust its reasoning effort.
If you see the Power slider, open **Advanced** to choose a specific model,
such as GPT-6.2 Astra.

**Reasoning effort** guides how much work the model puts into thinking through
your request. Higher effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  <CodexModelSwitcher client:visible surface="work" className="lg:mt-7" />

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

## Choose a model

These recommendations apply to **ChatGPT Work** on the web. Use the
model and reasoning control beneath the composer to choose an available model
and adjust its reasoning effort.

**Reasoning effort** guides how much work the model puts into thinking through
your request. Higher effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  <CodexModelSwitcher client:visible surface="work" className="lg:mt-7" />

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

## Choose a model

GPT-6.1 Terra requires Codex CLI 0.159.0 or later. To use it, run
`codex -m gpt-6.1-terra`.

In an interactive CLI session, use `/model` to switch models or adjust
reasoning effort. To start Codex with Sol, use `--model` or its `-m` alias:

```bash
codex --model gpt-6.2-sol
```

The same option works with non-interactive runs. For example:

```bash
codex exec -m gpt-6.2-sol "Review the current changes"
```

**Reasoning effort** guides how much work the model puts into thinking through
your request. Higher effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

## Choose a model

Use the model switcher below the composer to choose an available model and
reasoning effort.

**Reasoning effort** guides how much work the model puts into thinking through
your request. Higher effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  <CodexModelSwitcher client:visible forceDark className="lg:mt-7" />

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,web">

This example shows the Power slider for a ChatGPT Work account with access to
  both GPT-6.2 models. New Work chats start with GPT-6.2 Sol at **Light** on
  supported consumer plans or **Medium** in Enterprise workspaces with the model
  enabled. Move the Power slider toward **Smarter** for deeper reasoning or
  **Faster** for faster, lower-cost work. Open **Advanced** to choose a specific
  model or reasoning effort from the options available to your account.

</ContentModeSwitch>

<a id="recommended-models"></a>
<a id="other-models"></a>
<a id="deprecated-codex-models"></a>
<a id="configure-your-default-local-model"></a>
<a id="choose-a-model-for-cloud-tasks"></a>

<ContentModeSwitch group="codex-surface" ids="app,web,cli,ide">

## Recommended models

GPT-6.2 Astra and GPT-6.2 Sol are now available in ChatGPT Work and Codex on
[supported plans and clients](https://learn.chatgpt.com/docs/pricing#feature-availability). For demanding
work across code, apps, or research, choose GPT-6.2 Astra. In Codex, try Astra to
trace a bug across services, fix it, and test the change. See
[Prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra).

Choose GPT-6.2 Sol for
everyday coding, writing, and work across several sources. It costs fewer credits
per token than GPT-6.2 Astra at [Standard speed](https://learn.chatgpt.com/docs/pricing#token-rates).
GPT-6.1 Terra is a fast, efficient choice for writing, visual understanding, and
computer use. Luna suits focused, repeatable tasks.

These recommendations apply to ChatGPT Work and Codex. For Chat availability, see [models in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt) in the Help Center.

<a id="app-compare-models"></a>

<ModelDetails
  client:load
  name="GPT-6.2 Astra"
  slug="gpt-6.2-astra"
  imageLabel="6.2 Astra"
  wallpaperUrl="/images/api/models/gpt-6.2-astra-block.webp"
  description="Choose GPT-6.2 Astra for demanding projects, such as diagnosing a bug across services or turning research into a presentation that follows your template."
  data={{
    features: [
      { title: "ChatGPT Work", value: "Web, mobile, and desktop" },
      { title: "Codex", value: "App and CLI" },
      { title: "Default context in Codex", value: "272,000 tokens" },
    ],
  }}
/>

<ModelDetails
  client:load
  name="GPT-6.2 Sol"
  slug="gpt-6.2-sol"
  imageLabel="6.2 Sol"
  wallpaperUrl="/images/api/models/gpt-6.2-sol-block.webp"
  description="Use GPT-6.2 Sol for everyday tasks like editing code, drafting a report, or turning project notes into a plan."
  data={{
    features: [
      { title: "ChatGPT Work", value: "Web, mobile, and desktop" },
      { title: "Codex", value: "App and CLI" },
      { title: "Default context in Codex", value: "500,000 tokens" },
    ],
  }}
/>

<ModelDetails
  client:load
  name="gpt-6-astra"
  slug="gpt-6-astra"
  imageLabel="Astra"
  wallpaperUrl="/images/api/models/gpt-6-astra-texture.webp"
  description="Combine reasoning and computer use to tackle complex work across code, apps, and research."
  data={{
    features: [
      {
        title: "Capability",
        value: "",
        icons: [
          "openai.SparklesFilled",
        ],
      },
      {
        title: "Speed",
        value: "",
        icons: ["openai.Flash", "openai.Flash"],
      },
      { title: "ChatGPT desktop app", value: true },
      { title: "ChatGPT web", value: true },
      { title: "Codex CLI", value: true },
      { title: "Codex IDE extension", value: true },
      { title: "ChatGPT Credits", value: true },
      { title: "API Access", value: true },
    ],
  }}
/>

<ModelDetails
  client:load
  name="gpt-6.1-sol"
  slug="gpt-6.1-sol"
  imageLabel="6.1 Sol"
  wallpaperUrl="/images/api/models/gpt-6.1-sol-texture.webp"
  description="Performance close to GPT-6 Astra for complex work at a lower cost. Consider it for repeated, long-running work across code, apps, and documents."
  data={{
    features: [
      {
        title: "Capability",
        value: "",
        icons: [
          "openai.SparklesFilled",
        ],
      },
      {
        title: "Speed",
        value: "",
        icons: ["openai.Flash", "openai.Flash", "openai.Flash"],
      },
      { title: "Work and Codex in the desktop app", value: true },
      { title: "ChatGPT Work on the web", value: true },
      { title: "Codex CLI", value: true },
      { title: "Codex IDE extension", value: true },
      { title: "ChatGPT Credits", value: true },
      { title: "API Access", value: true },
    ],
  }}
/>

<a
  id="gpt-61-terra"
  data-codex-legacy-anchor
  className="block scroll-mt-24"
></a>

<ModelDetails
  client:load
  name="gpt-6.1-terra"
  slug="gpt-6.1-terra"
  imageLabel="6.1 Terra"
  wallpaperUrl="/images/api/models/gpt-6.1-terra-block.webp"
  description="A fast, efficient model for clear writing, visual understanding, and computer use. Try it for drafting proposals, interpreting charts, or working with information in an app."
  data={{
    features: [
      {
        title: "Capability",
        value: "",
        icons: [
          "openai.SparklesFilled",
        ],
      },
      {
        title: "Speed",
        value: "",
        icons: ["openai.Flash", "openai.Flash", "openai.Flash", "openai.Flash"],
      },
      { title: "Work and Codex in the desktop app", value: true },
      { title: "ChatGPT Work on the web", value: true },
      { title: "Codex CLI", value: true },
      { title: "ChatGPT Credits", value: true },
      { title: "API Access", value: true },
    ],
  }}
/>

<ModelDetails
  client:load
  name="gpt-6-luna"
  slug="gpt-6-luna"
  imageLabel="6 Luna"
  wallpaperUrl="/images/api/models/gpt-5.6-luna.webp"
  description="Our most efficient model for focused, high-volume tasks, including summarization, extraction, and focused coding."
  data={{
    features: [
      {
        title: "Capability",
        value: "",
        icons: [
          "openai.SparklesFilled",
        ],
      },
      {
        title: "Speed",
        value: "",
        icons: ["openai.Flash", "openai.Flash", "openai.Flash", "openai.Flash"],
      },
      { title: "Work and Codex in the desktop app", value: true },
      { title: "ChatGPT Work on the web", value: true },
      { title: "Codex CLI", value: true },
      { title: "Codex IDE extension", value: true },
      { title: "ChatGPT Credits", value: true },
      { title: "API Access", value: true },
    ],
  }}
/>

</ContentModeSwitch>

To use a longer context window in Codex, set `model_context_window` in
[`config.toml`](https://learn.chatgpt.com/docs/config-file/config-advanced#model-reasoning-verbosity-and-limits).
GPT-6.2 Astra and GPT-6.2 Sol each support a context window of up to 1 million tokens.

<a id="gpt-61-sol"></a>
<a id="gpt-6.1-sol"></a>

GPT-6.1 Sol uses a default context window of 500,000 tokens in Codex and
ChatGPT Work. See [pricing](https://learn.chatgpt.com/docs/pricing) for subscription usage and credit rates.

For model availability, pricing, and usage limits, see [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) in the Help Center.

<ContentModeSwitch group="codex-surface" ids="app,web,cli,ide">

<a id="choosing-sol-terra-and-luna"></a>

<a id="choosing-astra-sol-and-luna"></a>
<a id="app-choosing-astra-sol-and-luna"></a>
<a id="web-choosing-astra-sol-and-luna"></a>
<a id="cli-choosing-astra-sol-and-luna"></a>
<a id="ide-choosing-astra-sol-and-luna"></a>

## Choosing a model

Start with a task you know well and compare the result with what you need.
Consider how long you're willing to wait, how much usage the task requires,
and the level of detail or judgment involved. You can change models as your
work changes.

### Where each model shines

- **GPT-6.2 Astra or GPT-6 Astra, for the hardest end-to-end work.** Choose an
  available Astra model for tasks that need sustained reasoning across code,
  apps, or research. Give it the sources, constraints, and checks that define a
  useful result.
- **GPT-6.2 Sol, for everyday work.** Choose Sol to edit code, draft documents,
  or turn several sources into a plan.
- **GPT-6.1 Terra, for everyday writing and visual work.** Choose Terra for clear
  communication, interpreting images and screens, and completing tasks across
  supported apps. Try it for drafting proposals, reviewing visual materials,
  or filling out forms from source documents.
- **Luna, for clear, repeatable tasks.** Choose Luna for specific, high-volume
  tasks when you know what a good result looks like, such as extraction,
  classification, transformation, and structured summaries.

### Try an example

Use your own materials with these prompts, and tell ChatGPT what a useful
result should include.

| Model                        | Task                                           | Example prompt                                                                                                                                                                        |
| ---------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT-6.2 Astra or GPT-6 Astra | Work through a complex decision.               | "Compare these three vendor proposals against our requirements. Explain the tradeoffs, recommend an option, and list the questions we should resolve before deciding."                |
| GPT-6.2 Sol                  | Bring several sources into a working document. | "Use this project brief, meeting notes, and timeline to draft an implementation plan. Identify dependencies, flag conflicting details, and list the decisions we still need to make." |
| GPT-6.1 Terra                | Make sense of visual information.              | "Review these dashboard screenshots and summarize the main changes. Refer to the chart labels and values, and flag anything you can't read confidently."                              |
| Luna                         | Organize information into a consistent format. | "Turn these meeting notes into a table of action items, owners, and due dates. Mark any missing owner or date as unspecified."                                                        |

Review the result against your source materials, especially names, numbers,
and details taken from images. For tasks on websites or in desktop apps, check
the [browser use](https://learn.chatgpt.com/docs/browser) and [computer use](https://learn.chatgpt.com/docs/computer-use) setup
requirements first.

### Pick a reasoning effort

For example, you might use a lower effort to rewrite a short email and a higher
effort to compare several proposals with competing requirements.

For GPT-6.2 Astra or GPT-6.2 Sol, start with the effort your client selects
and adjust it based on the task. For Luna, start with **High**. For GPT-6
Astra, start with **Light** (`low` in configuration). Increase the effort for
tasks that need more planning, analysis, or checking.

- **Light** in the ChatGPT desktop app, ChatGPT Work on the web, and IDE extension, or **Low** in the
  CLI, suits quick, well-scoped tasks.
- **Medium** balances speed and depth for tasks that need more planning.
- **High** and **Extra High** suit difficult work with multiple steps, sources,
  or tradeoffs.

  [Learn more in our Model selection guide](https://learn.chatgpt.com/docs/model-selection#how-to-think-about-models-and-reasoning-effort)

### Know when to use Max or Ultra

**Max** gives the selected model more time to reason about a single task. Use it
for the hardest problems, when depth matters more than speed or usage. If you
don't see Max in the ChatGPT desktop app, check your app settings.

**Ultra** uses [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to handle
separate parts of a complex task in parallel. Choose it when you can divide the
work into meaningful parts. Most tasks do not need Max or Ultra.

GPT-6 Luna supports reasoning efforts up to **Max**, but not **Ultra**.

In the CLI, use `/model`, choose a model, then select **More reasoning…**
to see its supported Max or Ultra options.

If your model supports Ultra but it doesn't appear in the desktop app's model
slider, go to **Settings** > **Configuration**, then turn on
**Ultra in model picker slider**.

</ContentModeSwitch>

## GPT-5.5 retirement

Effective October 14, 2026, at noon PDT (19:00 UTC), GPT-5.5 retires from
Codex for users signed in with ChatGPT. The OpenAI API and Codex sessions
authenticated with an API key aren't affected.

For Codex with ChatGPT sign-in, choose an available replacement:

- On Plus, Pro, Business, Enterprise, and Edu plans, choose **GPT-6.1 Sol**
  (`gpt-6.1-sol`) when available.
- On Free and Go plans, choose **GPT-6 Luna** (`gpt-6-luna`) in the desktop app
  when available.

Replace `gpt-5.5` in workspace defaults, saved model settings, managed
configurations, custom agents, scheduled tasks, and scripts that select a model.

See [workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability#prepare-for-the-gpt-55-retirement)
for administrator guidance.

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

## Other models

With API-key authentication, model availability follows your API organization
and project. GPT-5.5 remains available through the OpenAI API and in Codex
sessions authenticated with an API key. See the [API model catalog](https://developers.openai.com/api/docs/models).

For a custom model provider or gateway, use a compatible Responses API endpoint.
See [Custom model providers](https://learn.chatgpt.com/docs/config-file/config-advanced#custom-model-providers)
for configuration and [Gateway compatibility](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility)
for streaming, tool, and conversation requirements. Current Codex releases don't
support `wire_api = "chat"` or a Chat Completions-only endpoint.

## Deprecated Codex models

GPT-5.3-Codex-Spark retired on September 14, 2026, and is no longer available
in the ChatGPT desktop app, Codex CLI, or IDE extension. Update saved
configurations, custom agents, and scripts that select `gpt-5.3-codex-spark`
to use an [available model](https://learn.chatgpt.com/docs/models#recommended-models). See the
[Spark retirement notice](https://learn.chatgpt.com/docs/changelog#codex-2026-09-14-codex-spark-deprecation).

GPT-5.5 retires from Codex with ChatGPT sign-in on October 14, 2026, at noon
PDT (19:00 UTC). Replace `gpt-5.5` with a model available to your account and
client. API-key sessions aren't affected. See
[GPT-5.5 retirement](https://learn.chatgpt.com/docs/models#gpt-55-retirement) for plan-specific
replacements and the migration checklist.

The `gpt-5.4` and `gpt-5.4-mini` models retired from Codex with ChatGPT sign-in
on August 31, 2026. Replace `gpt-5.4` with `gpt-6-sol` and
`gpt-5.4-mini` with `gpt-6-luna` when available to your plan and client.
In Enterprise and Edu, an administrator must enable Luna first. Update workspace
defaults, saved model settings, managed configurations, custom agents, and
scheduled tasks with an available replacement.

The `gpt-5.2` and `gpt-5.3-codex` models are already deprecated in Codex when
you sign in with ChatGPT. Update scripts, configuration files, and
`codex exec --model` commands that still reference those models.

The OpenAI API and Codex authenticated with your own API key aren't affected
by the GPT-5.4 retirement. For current API model availability, see the
[API models page](https://developers.openai.com/api/docs/models).

## Configure your default local model

The ChatGPT desktop app, Codex CLI, and IDE extension use the same `config.toml`
[configuration file](https://learn.chatgpt.com/docs/config-file/config-basic). To specify a model, add a
`model` entry to your configuration file. If you don't specify a model, the
ChatGPT desktop app, Codex CLI, or IDE extension uses a recommended model.
This example selects Sol in the app or CLI. When sharing a configuration with
the IDE extension, pick a model available in every client you use,
such as `gpt-6.1-sol`.

```toml
model = "gpt-6.2-sol"
```

</ContentModeSwitch>
