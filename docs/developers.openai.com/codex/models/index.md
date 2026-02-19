# Codex Models

Source: https://developers.openai.com/codex/models

Meet the AI models that power Codex

## Recommended models

![gpt-5.3-codex](/images/codex/codex-wallpaper-1.webp)

gpt-5.3-codex

Most capable agentic coding model to date, combining frontier coding performance with stronger reasoning and professional knowledge capabilities.

codex -m gpt-5.3-codex

Copy command

Capability

Speed

Codex CLI & SDK

Codex app & IDE extension

Codex Cloud

ChatGPT Credits

API Access

![gpt-5.3-codex-spark](/images/codex/codex-wallpaper-2.webp)

gpt-5.3-codex-spark

Text-only research preview model optimized for near-instant, real-time coding iteration. Available to ChatGPT Pro users.

codex -m gpt-5.3-codex-spark

Copy command

Capability

Speed

Codex CLI & SDK

Codex app & IDE extension

Codex Cloud

ChatGPT Credits

API Access

![gpt-5.2-codex](/images/codex/gpt-5.2-codex.png)

gpt-5.2-codex

Advanced coding model for real-world engineering. Succeeded by GPT-5.3-Codex.

codex -m gpt-5.2-codex

Copy command

Capability

Speed

Codex CLI & SDK

Codex app & IDE extension

Codex Cloud

ChatGPT Credits

API Access

For most coding tasks in Codex, start with gpt-5.3-codex. It is available for
ChatGPT-authenticated Codex sessions in the Codex app, CLI, IDE extension, and
Codex Cloud. API access for GPT-5.3-Codex will come soon. The
gpt-5.3-codex-spark model is available in research preview for ChatGPT Pro
subscribers.

## Alternative models

![gpt-5.2](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5.2.jpg)

gpt-5.2

Our best general agentic model for tasks across industries and domains.

codex -m gpt-5.2

Copy command

Show details

![gpt-5.1-codex-max](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5.1-codex-max.jpg)

gpt-5.1-codex-max

Optimized for long-horizon, agentic coding tasks in Codex.

codex -m gpt-5.1-codex-max

Copy command

Show details

![gpt-5.1](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5.1.jpg)

gpt-5.1

Great for coding and agentic tasks across domains. Succeeded by GPT-5.2.

codex -m gpt-5.1

Copy command

Show details

![gpt-5.1-codex](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5.1-codex.jpg)

gpt-5.1-codex

Optimized for long-running, agentic coding tasks in Codex. Succeeded by GPT-5.1-Codex-Max.

codex -m gpt-5.1-codex

Copy command

Show details

![gpt-5-codex](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5-codex.jpg)

gpt-5-codex

Version of GPT-5 tuned for long-running, agentic coding tasks. Succeeded by GPT-5.1-Codex.

codex -m gpt-5-codex

Copy command

Show details

![gpt-5-codex-mini](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5-codex.jpg)

gpt-5-codex-mini

Smaller, more cost-effective version of GPT-5-Codex. Succeeded by GPT-5.1-Codex-Mini.

codex -m gpt-5-codex

Copy command

Show details

![gpt-5](https://cdn.openai.com/API/docs/images/model-page/model-art/gpt-5.jpg)

gpt-5

Reasoning model for coding and agentic tasks across domains. Succeeded by GPT-5.1.

codex -m gpt-5

Copy command

Show details

## Other models

Codex works best with the models listed above.

You can also point Codex at any model and provider that supports either the [Chat Completions](https://platform.openai.com/docs/api-reference/chat) or [Responses APIs](https://platform.openai.com/docs/api-reference/responses) to fit your specific use case.

Support for the Chat Completions API is deprecated and will be removed in
future releases of Codex.

## Configuring models

### Configure your default local model

The Codex CLI and IDE extension use the same `config.toml` [configuration file](/codex/config-basic). To specify a model, add a `model` entry to your configuration file. If you don’t specify a model, the Codex app, CLI, or IDE Extension defaults to a recommended model.

```
model = "gpt-5.2"
```

### Choosing a different local model temporarily

In the Codex CLI, you can use the `/model` command during an active thread to change the model. In the IDE extension, you can use the model selector below the input box to choose your model.

To start a new Codex CLI thread with a specific model or to specify the model for `codex exec` you can use the `--model`/`-m` flag:

```
codex -m gpt-5.3-codex
```

### Choosing your model for cloud tasks

Currently, you can’t change the default model for Codex cloud tasks.

