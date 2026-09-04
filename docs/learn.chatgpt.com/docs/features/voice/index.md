---
source_type: 'learn'
source_area: 'learn_features'
source_url: 'https://learn.chatgpt.com/docs/features/voice'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# ChatGPT Voice

Source: https://learn.chatgpt.com/docs/features/voice

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Powered by GPT-Live, ChatGPT Voice lets you talk through ideas and coordinate
tasks in Chat, Work, and Codex in the ChatGPT desktop app. Start work, check
progress, or change direction without switching back to typing.

ChatGPT Voice is available in the ChatGPT desktop app with ChatGPT Plus,
Pro, Business, Edu, and Enterprise plans. Enterprise and Edu availability
begins with a two-week early-access period before the feature becomes available
by default. You can also use ChatGPT Voice through
[Remote on iOS](https://learn.chatgpt.com/docs/remote-connections#set-up-mobile-access) after pairing
your phone with a desktop host. Availability also depends on rollout status and
workspace settings. See [feature availability](https://learn.chatgpt.com/docs/pricing#feature-availability).

> Illustration: Interactive ChatGPT Voice conversation with microphone and speaker controls.

## Start talking

1. Open the Codex task you want to discuss in the ChatGPT desktop app, or start
   a new chat or task.
2. Select **Start voice chat** in an existing task, or **Start new voice chat**
   in a new chat or task.
3. The first time you start a voice chat, allow microphone access, choose a
   voice, and review screen context on macOS.
4. Start talking. Select **Stop voice chat** when you finish.

Voice in existing Codex tasks is rolling out. When available, you can start
talking in a task that began with typed messages. Voice uses that task's
conversation and selected model to carry out your requests, so you can discuss
its progress or change direction without starting another task.

If **Start voice chat** isn't available in an existing task, update the desktop
app and the Codex host running the task. Availability also depends on your
account and workspace. You can still start a new voice chat where supported,
or use [voice dictation](https://learn.chatgpt.com/docs/prompting#use-voice-dictation) to enter prompt
text. To resume an earlier voice chat, open it and select **Start voice chat**.

You can set a shortcut in **Settings > Voice > Voice chat hotkey**.

## Have a conversation

ChatGPT Voice supports natural turn-taking. You can interrupt ChatGPT
during a response, ask a follow-up, or change direction. If ChatGPT starts work,
keep talking to check progress or steer the task.

## Delegate and coordinate work

ChatGPT Voice can start separate tasks for longer work, check existing tasks,
and send follow-up instructions. It brings progress, blockers, and results back
to your voice conversation so you can keep talking while work continues.

For example:

- “Review today's launch brief and summarize decisions that need approval.”
- “Start a Codex task to run the tests and investigate anything that doesn't pass.”
- “Check active tasks and summarize anything blocking progress.”

You can also ask to speak to another Codex task, then ask to return to the
previous one. For example, say, “Let me talk to the task reviewing the tests,”
then, “Take me back to the previous task.” The destination task must support
voice and be available on a connected host.

ChatGPT Voice follows the same [permissions](https://learn.chatgpt.com/docs/permission-modes) as
the tasks it directs in Chat, Work, and Codex in the ChatGPT desktop app.

## Show ChatGPT what you see

On macOS, turn on **Screen context** in **Settings > Voice**, then say, “Take a
look at this.” ChatGPT can take an
[appshot](https://learn.chatgpt.com/docs/appshots#permissions-and-safety) of your frontmost window and
use it as context. Your organization can disable this capability.

An appshot can include the window's image and accessible text, including content
outside the visible scroll area. macOS may request **Screen & System Audio
Recording** and **Accessibility** permissions. Avoid sharing windows that
contain sensitive information, including text outside the visible scroll area.

## ChatGPT Voice and voice dictation

Use ChatGPT Voice for a live conversation with ChatGPT. Use [voice
dictation](https://learn.chatgpt.com/docs/prompting#use-voice-dictation) when you only want to turn
speech into prompt text before sending it.

## Limits and troubleshooting

Only one voice chat can be active across the ChatGPT desktop app at a time.
Voice conversations use a separate, plan-dependent allowance measured in rolling
five-hour windows. Tasks started through Voice continue to use your Codex usage
budget. ChatGPT notifies you when you reach either limit. See [Voice pricing and
limits](https://learn.chatgpt.com/docs/pricing#chatgpt-voice-in-desktop).

If you can't start a voice chat, confirm that ChatGPT Voice is available for your
plan, rollout, and workspace. Then check microphone permissions and whether a
voice chat is already active in another app window. If screen context isn't
available, check **Settings > Voice**, Appshots permissions, and your
organization's restrictions.
