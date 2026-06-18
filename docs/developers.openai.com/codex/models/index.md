---
source_type: 'developers'
source_area: 'codex_reference'
source_url: 'https://developers.openai.com/codex/models'
source_last_modified: '2026-06-05T00:32:22Z'
source_etag: 'W/"02ef280774bbd158a0a5566084f1303b"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Models – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/models

## Recommended models

![gpt-5.5](/images/api/models/gpt-5.5.jpg)

gpt-5.5

OpenAI's newest frontier model for complex coding, computer use, knowledge work, and research workflows in Codex.

codex -m gpt-5.5

Copy command

Capability

Speed

Codex CLI & SDK

Codex app & IDE extension

Codex Cloud

ChatGPT Credits

API Access

![gpt-5.4](/images/api/models/gpt-5.4.jpg)

gpt-5.4

Flagship frontier model for professional work with strong coding, reasoning, tool use, and agentic workflow capabilities.

codex -m gpt-5.4

Copy command

Capability

Speed

Codex CLI & SDK

Codex app & IDE extension

Codex Cloud

ChatGPT Credits

API Access

![gpt-5.4-mini](/images/api/models/gpt-5-mini.jpg)

gpt-5.4-mini

Fast, efficient mini model for responsive coding tasks and subagents.

codex -m gpt-5.4-mini

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

For most tasks in Codex, start with
`gpt-5.5`. It is
strongest for complex coding, computer use, knowledge work, and research
workflows. GPT-5.5 is currently available in Codex when you sign in with
ChatGPT or API-key authentication. Use

`gpt-5.4-mini`

when you want a faster, lower-cost option for lighter coding tasks or
subagents. The `gpt-5.3-codex-spark` model is available in research preview
for ChatGPT Pro subscribers and is optimized for near-instant, real-time
coding iteration.

## Other models

When you sign in with ChatGPT, Codex works best with the recommended models listed above.

You can also point Codex at any model and provider that supports either the [Chat Completions](https://platform.openai.com/docs/api-reference/chat) or [Responses APIs](https://platform.openai.com/docs/api-reference/responses) to fit your specific use case.

Support for the Chat Completions API is deprecated and will be removed in
future releases of Codex.

## Deprecated Codex models

The `gpt-5.2` and `gpt-5.3-codex` models are deprecated in Codex when you sign in with ChatGPT. If your scripts, configuration files, or `codex exec --model` commands still reference deprecated models, update them to the latest model listed above.

Some models that are deprecated for ChatGPT sign-in may still be available in the API. If your workflow depends on one of those models, use API-key authentication and check the [API models page](/api/docs/models) for current availability.

## Configuring models

### Configure your default local model

The Codex CLI and IDE extension use the same `config.toml` [configuration file](/codex/config-basic). To specify a model, add a `model` entry to your configuration file. If you don’t specify a model, the Codex app, CLI, or IDE Extension defaults to a recommended model.

```
model = "gpt-5.5"
```

### Choosing a different local model temporarily

In the Codex CLI, you can use the `/model` command during an active thread to change the model. In the IDE extension, you can use the model selector below the input box to choose your model.

To start a new Codex CLI thread with a specific model or to specify the model for `codex exec` you can use the `--model`/`-m` flag:

```
codex -m gpt-5.5
```

### Choosing your model for cloud tasks

Currently, you can’t change the default model for Codex cloud tasks.

