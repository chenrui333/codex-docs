---
source_type: 'learn'
source_area: 'learn_appshots'
source_url: 'https://learn.chatgpt.com/docs/appshots'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Appshots

Source: https://learn.chatgpt.com/docs/appshots

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Appshots let you send the frontmost app window to a chat in ChatGPT. Use them when
you're actively working in another app on your computer and want to provide
ChatGPT with your current context so it can help you with the task.

Appshots are available in the ChatGPT desktop app on macOS and Windows. Press
  both Command keys on macOS or both Alt keys on Windows to take one. You can
  also configure a custom Appshots hotkey.

## What appshots capture

An appshot captures the frontmost window only. It can include:

- An image of the visible window.
- Available text from that window, including visible text and text the app makes
  available outside the visible scroll area.

After you add an appshot to a chat, it behaves like an attachment. ChatGPT
stores appshots locally in the session file, like files or images you attach
manually.

## When to use appshots

Use appshots when ChatGPT needs context from another app before it can act.

Examples:

- Share an API reference page and ask ChatGPT to write a script that uses it.
- Share an email or calendar view and ask ChatGPT to draft the next step.
- Share an image editor, design, or preview window and ask ChatGPT to revise the
  related assets or code.
- Share an error, settings panel, or app state that's easier to show than
  describe.

## Take an appshot

1. Bring the app window you want to share to the front.
2. Press both Command keys on macOS or both Alt keys on Windows, or use the
   custom hotkey you configured in ChatGPT settings.
3. Complete the permission setup if ChatGPT asks.
4. Ask ChatGPT to perform a task with the appshot.

> Illustration: ChatGPT chat composer with an Appshot attachment and follow-up prompt

By default, ChatGPT starts a new chat for the appshot. If you interacted with a
chat in the last 60 seconds, ChatGPT adds the appshot to that recent
chat instead. Taking consecutive appshots adds them to the same chat.

You can change the hotkey and **Appshot destination** in the app settings.
Choose **Current chat** or **New chat** to set a destination, or keep
**Automatic** for the behavior described here.

<a id="use-appshots-with-mini"></a>

### Use appshots from the floating controls

On macOS, when the [floating pet controls](https://learn.chatgpt.com/docs/pets?surface=app#app-send-appshots-to-your-pet)
are open and the main ChatGPT window is in the background, **Automatic** starts
a new chat from those controls with the appshot. This also works when you select
**Mini** as your pet. Complete Appshots permission setup in the main app
first. On Windows, Appshots open in the main app.

## Permissions and safety

On macOS, ChatGPT may ask for these permissions before it can take appshots:

- **Screen & System Audio Recording** lets ChatGPT capture an image of the
  frontmost window.
- **Accessibility** lets ChatGPT read available text from the frontmost window.

Taking an appshot shares the captured image and available text with ChatGPT.
Avoid taking appshots of sensitive content unless the task requires that
content.

Review appshots the same way you would review sharing screenshots and documents
with ChatGPT.

## Limits and troubleshooting

Appshots require the ChatGPT desktop app on macOS or Windows. If you resume a
chat in the CLI that already contains an appshot, the attachment is part of
the chat history, but the CLI can't create a new appshot.

For some apps and websites, including Google Docs, Gmail, Google Sheets, and
Google Slides, ChatGPT may receive only the visible screenshot and may not receive
the full document or off-screen text. In ChatGPT Work or Codex, ChatGPT can use a
matching installed plugin to access the relevant app content and help with your
request.

If appshots don't work, update the desktop app, check the configured hotkey,
and confirm that your organization allows Appshots. On macOS, also check
permissions:

1. Open **System Settings > Privacy & Security**.
2. Check **Screen & System Audio Recording** and **Accessibility** for Codex
   Computer Use.
3. Restart the app and try again.
