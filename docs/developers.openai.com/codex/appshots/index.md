---
source_type: 'developers'
source_area: 'codex_appshots'
source_url: 'https://developers.openai.com/codex/appshots'
source_last_modified: '2026-05-21T18:05:21Z'
source_etag: 'W/"cf9b698680521e3d0f810ba442e9079d"'
codex_cli_versions: ["0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0"]
codex_cli_versions_raw: ["codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0"]
---

# Appshots – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/appshots

Appshots let you send the frontmost app window to a Codex thread. Use them when
you’re actively working in another app on your computer and want to provide
Codex with your current context so it can help you with the task.

Appshots are available in the Codex app on macOS. Press both Command keys, or
your custom Appshots hotkey, to take one.

## What appshots capture

An appshot captures the frontmost window only. It can include:

- An image of the visible window.
- Available text from that window, including visible text and text the app makes
  available outside the visible scroll area.

After you add an appshot to a thread, it behaves like a Codex attachment. Codex
stores appshots locally in the session file, like files or images you attach
manually.

## When to use appshots

Use appshots when Codex needs context from a Mac app before it can act.

Examples:

- Share an API reference page and ask Codex to write a script that uses it.
- Share an email or calendar view and ask Codex to draft the next step.
- Share an image editor, design, or preview window and ask Codex to revise the
  related assets or code.
- Share an error, settings panel, or app state that’s easier to show than
  describe.

## Take an appshot

1. Open the Codex app on your Mac.
2. Open the app and window you want to share.
3. Press both Command keys, or the custom hotkey you configured in Codex
   settings.
4. Allow macOS permissions if Codex asks.
5. Ask Codex to perform a task with the appshot.

By default, Codex starts a new thread for the appshot. If you interacted with a
Codex thread in the last 60 seconds, Codex adds the appshot to that recent
thread instead. Taking consecutive appshots adds them to the same thread.

You can change the Appshots hotkey in Codex settings.

## Permissions and safety

Codex may ask for permissions before it can take appshots:

- **Screen & System Audio Recording** lets Codex capture an image of the
  frontmost window.
- **Accessibility** lets Codex read available text from the frontmost window.

Taking an appshot shares the captured image and available text with Codex.
Avoid taking appshots of sensitive content unless the task requires that
content.

Review appshots the same way you would review sharing screenshots and documents
with Codex.

## Limits and troubleshooting

Appshots are a Codex app feature. Create them from the Codex app on macOS. If
you resume a thread in the CLI that already contains an appshot, the attachment
is part of the thread history, but the CLI can’t create a new appshot.

For some apps and websites, including Google Docs, Gmail, Google Sheets, and
Google Slides, Codex may receive only the visible screenshot and may not receive
the full document or off-screen text. If you have the matching plugin installed,
Codex can use that plugin to access the relevant app content and help with your
request.

If appshots don’t work:

1. Open **System Settings > Privacy & Security**.
2. Check **Screen & System Audio Recording** and **Accessibility** for Codex
   Computer Use.
3. Restart Codex and try again.

