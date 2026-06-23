---
source_type: 'developers'
source_area: 'codex_memory'
source_url: 'https://developers.openai.com/codex/memories/chronicle'
source_last_modified: '2026-06-16T15:42:29Z'
source_etag: 'W/"bd38761b7c59a3470c24f8fe7f4be649"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0"]
---

# Chronicle – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/memories/chronicle

Chronicle is in an **opt-in research preview**. It is only available for
ChatGPT Pro subscribers on macOS. Please review the [Privacy and
Security](#privacy-and-security) section for details and to understand the
current risks before enabling.

Chronicle augments Codex memories with context from your screen. When you prompt
Codex, those memories can help it understand what you’ve been working on with
less need for you to restate context.

Chronicle is available as an opt-in research preview in the Codex app on macOS.
It requires macOS Screen Recording and Accessibility permissions. Before
enabling, be aware that Chronicle uses rate limits quickly, increases risk of
prompt injection, and stores memories unencrypted on your device.

## How Chronicle helps

We’ve designed Chronicle to reduce the amount of context you have to restate
when you work with Codex. By using recent screen context to improve memory
building, Chronicle can help Codex understand what you’re referring to, identify
the right source to use, and pick up on the tools and workflows you rely on.

### Use what’s on screen

With Chronicle Codex can understand what you are currently looking at, saving
you time and context switching.

### Fill in missing context

No need to carefully craft your context and start from zero. Chronicle lets
Codex fill in the gaps in your context.

### Remember tools and workflows

No need to explain to Codex which tools to use to perform your work. Codex
learns as you work to save you time in the long run.

In these cases, Codex uses Chronicle to provide additional context. When another
source is better for the job, such as reading the specific file, Slack thread,
Google Doc, dashboard, or pull request, Codex uses Chronicle to identify the
source and then use that source directly.

## Enable Chronicle

1. Open Settings in the Codex app.
2. Go to **Personalization** and make sure **Memories** is enabled.
3. Turn on **Chronicle** below the Memories setting.
4. Review the consent dialog and choose **Continue**.
5. Grant macOS Screen Recording and Accessibility permissions when prompted.
6. When setup completes, choose **Try it out** or start a new thread.

If macOS reports that Screen Recording or Accessibility permission is denied,
open System Settings > Privacy & Security > Screen Recording or
Accessibility and enable Codex. If a permission is restricted by macOS or your
organization, Chronicle will start after the restriction is removed and Codex
receives the required permission.

## Pause or disable Chronicle at any time

You control when Chronicle generates memories using screen context. Use the
Codex menu bar icon to choose **Pause Chronicle** or **Resume Chronicle**. Pause
Chronicle before meetings or when viewing sensitive content that you do not want
Codex to use as context. To disable Chronicle, return to **Settings >
Personalization > Memories** and turn off **Chronicle**.

You can also control whether memories are used in a given thread. [Learn
more](/codex/memories#control-memories-per-thread).

## Rate limits

Chronicle works by running sandboxed agents in the background to generate
memories from captured screen images. These agents currently consume rate limits
quickly.

## Privacy and security

Chronicle uses screen captures, which can include sensitive information visible
on your screen. It does not have access to your microphone or system audio.
Don’t use Chronicle to record meetings or communications with others without
their consent. Pause Chronicle when viewing content you do not want remembered
in memories.

### Where does Chronicle store my data?

Screen captures are ephemeral and will only be saved temporarily on your
computer. Temporary screen capture files may appear under
`$TMPDIR/chronicle/screen_recording/` while Chronicle is running. Screen captures
that are older than 6 hours will be deleted while Chronicle is running.

The memories that Chronicle generates are just like other Codex memories:
unencrypted markdown files that you can read and modify if needed. You can also
ask Codex to search them. If you want to have Codex forget something you can
delete the respective file inside the folder or selectively edit the markdown
files to remove the information you’d like to remove. You should not manually
add new information. The generated Chronicle memories are stored locally on your
computer under `$CODEX_HOME/memories_extensions/chronicle/` (typically
`~/.codex/memories_extensions/chronicle`).

Both directories for your screen captures and memories might contain sensitive information. Make sure you do not share content with others, and be aware that other programs on your computer can also access these files.

### What data gets shared with OpenAI?

Chronicle captures screen context locally, then periodically uses Codex to
summarize recent activity into memories. To generate those memories, Chronicle
starts an ephemeral Codex session with access to this screen context. That
session may process selected screenshot frames, OCR text extracted from
screenshots, timing information, and local file paths for the relevant time
window.

Screen captures used for memory generation are stored temporarily on your device. They are processed on our
servers to generate memories, which are then stored locally on device. We do not
store the screenshots on our servers after processing unless required by law,
and do not use them for training.

The generated memories are Markdown files stored locally under
`$CODEX_HOME/memories_extensions/chronicle/`. When Codex uses memories in a
future session, relevant memory contents may be included as context for that
session, and may be used to improve our models if allowed in your ChatGPT
settings. [Learn more](https://help.openai.com/en/articles/7730893-data-controls-faq).

## Prompt injection risk

Using Chronicle increases risk to prompt injection attacks from screen content.
For instance, if you browse a site with malicious agent instructions, Codex may
follow those instructions.

## Troubleshooting

### How do I enable Chronicle?

If you do not see the Chronicle setting, make sure you are using a Codex app
build that includes Chronicle and that you have Memories enabled inside Settings
> Personalization.

Chronicle is currently only available for ChatGPT Pro subscribers on macOS.

If setup does not complete:

1. Confirm that Codex has Screen Recording and Accessibility permissions.
2. Quit and reopen the Codex app.
3. Open **Settings > Personalization** and check the Chronicle status.

### Which model is used for generating the Chronicle memories?

Chronicle uses the same model as your other [Memories](/codex/memories). If you
did not configure a specific model it uses your default Codex model. To choose a
specific model, update the `consolidation_model` in your
[configuration](/codex/config-basic).

```
[memories]
consolidation_model = "gpt-5.4-mini"
```

