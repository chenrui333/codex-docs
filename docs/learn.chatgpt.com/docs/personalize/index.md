---
source_type: 'learn'
source_area: 'learn_personalize'
source_url: 'https://learn.chatgpt.com/docs/personalize'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Personalize ChatGPT

Source: https://learn.chatgpt.com/docs/personalize

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Personalize ChatGPT so its responses and working style better match your
preferences. You control which personalization features are enabled and can
change them in settings. Available controls vary between web and desktop.

## Choose a personality

Choose **Friendly**, **Pragmatic**, or **None** as the default personality in
**Settings > Personalization**. A personality changes how ChatGPT communicates;
it doesn't change what the model can do.

## Add custom instructions

Use custom instructions for preferences you want ChatGPT to follow across
chats, such as your preferred response style. In Codex, these personal
instructions are stored in your global `AGENTS.md` file. Projects and
repositories can also provide their own instructions.

[Learn how `AGENTS.md` instructions work](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Match your writing style in Work

In ChatGPT Work on the web, writing style uses your own writing from connected
apps to help drafts sound like you.

1. Open [Set up writing style](https://chatgpt.com/?surface=work&writing_style=setup).
2. Connect the available email, messaging, or document apps you want ChatGPT
   to use. Available apps depend on your account and workspace.
3. Select **Use writing style** to enable it. Connecting an app alone doesn't
   complete setup.
4. Ask Work to draft an email, message, or document.

To turn it off, open **Settings > Personalization > Writing** on the web and
disable **Reference my writing style**. You can return to setup from the same
section.

## Carry context forward with memories

[Memories](https://learn.chatgpt.com/docs/customization/memories) let ChatGPT carry useful context from earlier chats
into future work. They can include stable preferences, recurring workflows,
project conventions, and other context you would otherwise need to repeat.

Memories are separate from required project guidance. Keep instructions that
must always apply in `AGENTS.md` or checked-in project documentation.

## Add recent activity with Computer History

[Computer History](https://learn.chatgpt.com/docs/customization/computer-history) is an opt-in macOS
desktop feature that can turn activity across allowed apps and websites into
memories and a timeline. It uses interaction events, along with text and other
context available through macOS accessibility features. It does not include
screenshots in your history or record audio.

Review what Computer History includes before enabling it. You can pause it,
exclude apps and websites, inspect or delete individual timeline items, and
clear recent or all history at any time.

## Manage personalization

Open [**Settings**](codex://settings) to update your personality, custom
instructions, memories, and other available personalization controls. See
[ChatGPT desktop app settings](https://learn.chatgpt.com/docs/reference/settings) for an overview of
everyday preferences.
