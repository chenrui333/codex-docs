---
source_type: 'developers'
source_area: 'codex_reference'
source_url: 'https://developers.openai.com/codex/speed'
source_last_modified: '2026-04-25T06:36:12Z'
source_etag: 'W/"7519f69d0295f8db589cbd228c494e83"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Speed – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/speed

## Fast mode

Codex offers the ability to increase the speed of the model for increased
credit consumption.

Fast mode increases supported model speed by 1.5x and consumes credits at a
higher rate than Standard mode. It currently supports GPT-5.5 and GPT-5.4,
consuming credits at 2.5x the Standard rate for GPT-5.5 and 2x the Standard
rate for GPT-5.4.

Use `/fast on`, `/fast off`, or `/fast status` in the CLI to change or inspect
the current setting. You can also persist the default with `service_tier = "fast"` plus `[features].fast_mode = true` in `config.toml`. Fast mode is
available in the Codex IDE extension, Codex CLI, and the Codex app when you
sign in with ChatGPT. With an API key, Codex uses standard API pricing instead
and you can’t use Fast mode credits.

[
Your browser does not support the video tag.
](/videos/codex/fast-mode-demo.mp4)

## Codex-Spark

GPT-5.3-Codex-Spark is a separate fast, less-capable Codex model optimized for
near-instant, real-time coding iteration. Unlike fast mode, which speeds up a
supported model at a higher credit rate, Codex-Spark is its own model choice
and has its own usage limits.

During research preview Codex-Spark is only available for ChatGPT Pro subscribers.

