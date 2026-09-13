---
source_type: 'learn'
source_area: 'learn_pets'
source_url: 'https://learn.chatgpt.com/docs/pets'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Pets

Source: https://learn.chatgpt.com/docs/pets

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Pets are optional animated companions for following work. Where a pet appears
and what it shows depend on the interface you use. Choosing a pet changes its
appearance, not how ChatGPT completes tasks.

<ContentModeSwitch group="codex-surface" id="app">

## Use a floating pet

In the ChatGPT desktop app on macOS and Windows, a pet can float above other
app windows. Use the controls below it to start a chat by typing or speaking,
and follow activity while you work in other apps.

### Choose and wake a pet

1. Open the profile menu at the bottom of the app and select **Pets**. You can
   also open [**Settings**](codex://settings) and go to **Pets**.
2. Choose a built-in or custom pet, or select **Mini** to show the chat controls
   without a pet. If you haven't created a custom pet yet, select **Create pet**
   first.
3. Enter `/pet`, or open the command menu and select **Show pet**.
   You can also right-click the pet and select **Hide** to hide it.

To change your pet's size, select **Customize** in **Settings > Pets** and adjust
**Pet size**. Select **Reset** to restore the default size.

When you select a custom pet, it also appears in your **Profile** view.

> Illustration: A pet above floating chat controls. A cursor types and sends a request, then selects the bell to open the thread activity.

### Show or hide the floating controls

With the desktop app running, use the global shortcut to show the controls and
focus Quick Chat:

| Platform | Default shortcut  |
| -------- | ----------------- |
| macOS    | **Option+Space**  |
| Windows  | **Windows+Alt+P** |

You can change **Show pet** in **Settings > Keyboard shortcuts**. Pressing the
shortcut again keeps the controls open and focuses Quick Chat.

To hide the controls, right-click the pet and select **Hide**, select **Hide pet**
in the command menu or **Settings > Pets**, or enter `/pet` again. Your pet
selection and position persist when you reopen the app.
If the controls aren't available, update the app and check whether your
workspace allows pets.

### Start a chat

1. Move the pointer over the controls below your pet and select the pencil icon.
2. Enter your request and press **Enter** to send it. Use `@` to add context
   and `$` to choose a skill.
3. Select the bell icon to follow progress in your threads. Select a thread to
   open the full conversation in ChatGPT, or select the chevron to collapse
   your threads.

A chat started from these controls is outside a project. To use a project's
context, start the chat from that project in the main app.

To speak instead, select the voice icon. See
[ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) for voice availability and controls.

### Understand pet status

| Status          | Meaning                                                  |
| --------------- | -------------------------------------------------------- |
| **Running**     | A chat is actively working.                              |
| **Needs input** | A chat needs your approval, answer, or another decision. |
| **Ready**       | A chat has completed and has unread activity.            |
| **Blocked**     | A chat failed or encountered a system error.             |

When more than one chat has activity, the pet prioritizes chats that need
input, followed by blocked, ready, and running chats. Select the bell icon to
show your threads, then choose a thread to open its conversation. Select the
chevron to collapse your threads.

The activity tray is separate from [system
notifications](https://learn.chatgpt.com/docs/notifications?surface=app#app-configure-desktop-notifications).

### Send Appshots to your pet

On macOS, press both **Command** keys at the same time while using an app to
take an [Appshot](https://learn.chatgpt.com/docs/appshots). If your pet is visible and the main ChatGPT
window is in the background, the appshot goes to your pet and starts a new chat.
This also works when **Mini** is selected.

Set **Appshot destination** to **Automatic** in settings and authorize Appshots
permissions in the main app before using this shortcut.

On Windows, Appshots open in the main ChatGPT app.

### Follow Computer Use

On macOS, the [Computer Use](https://learn.chatgpt.com/docs/computer-use) picture-in-picture window can
attach to your pet. Move the pet, and the window follows. If your pet is hidden,
sending the picture-in-picture window to it shows the pet automatically.

### Create a custom pet

1. Open **Settings > Pets** and select **Create pet**.
2. The app installs the bundled `hatch-pet` skill, reloads skills, and opens a
   new chat.
3. Describe the pet you want and send the prompt.
4. When the task finishes, return to **Settings > Pets**, select **Refresh**,
   and choose your new pet.

Custom pets created in the desktop app are stored locally on your computer.
They don't automatically sync to ChatGPT web.

### Reduce animation

Pets respect your operating system's reduced motion setting. When reduced
motion is enabled, the pet uses a still frame instead of sprite animation.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

## Choose a pet on the web

If Pets are available for your account and workspace, open **Settings >
Personalization > Pet > Select pet**. Choose a built-in pet, or choose
**Default** to use ChatGPT without a pet.

A web pet appears inside supported ChatGPT Work chats. It doesn't provide the
desktop app's floating overlay, activity tray, or `/pet` command.

### Upload a custom pet

Select **Upload pet** to add a custom sprite sheet. The file must be a
transparent PNG or WebP, exactly 1536 × 1872 pixels, and no larger than 20 MiB.
You can edit, download, refresh, or delete uploaded pets from the same setting.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

## Choose a terminal pet

In an interactive Codex CLI session:

- Enter `/pets` or `/pet` to open the pet picker.
- Enter `/pets <name>` to choose a pet directly.
- Enter `/pets off` to disable terminal pets.

The picker includes built-in pets and compatible custom pets installed on your
computer. A terminal pet reports activity for the current CLI session. It uses
**Running**, **Needs input**, **Ready**, and **Blocked** states, but it doesn't
provide the desktop app's multiple-chat activity tray.

Terminal pets require iTerm2 3.6 or later, or a terminal with Kitty graphics or
Sixel support. They are unavailable inside tmux and Zellij.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

## Pets in the IDE extension

The Codex IDE extension doesn't provide a pet picker or floating pet overlay.
Use the ChatGPT desktop app or Codex CLI when you want to use your own pet.

</ContentModeSwitch>

## Related docs

- [Notifications](https://learn.chatgpt.com/docs/notifications)
- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [ChatGPT desktop app settings](https://learn.chatgpt.com/docs/reference/settings#pets)
