---
source_type: 'learn'
source_area: 'learn_features'
source_url: 'https://learn.chatgpt.com/docs/features/codex-micro'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Codex Micro

Source: https://learn.chatgpt.com/docs/features/codex-micro

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Micro is a limited-run collaboration between Codex and Work Louder. It
works with the ChatGPT desktop app, giving you a quick way to check on chats,
jump between them, use push-to-talk, and trigger common actions or skills
without leaving the keyboard.

    <Illustration description="Interactive Codex Micro keyboard with illuminated Agent Keys, customizable Command Keys, a dial, and an analog stick">
      <CodexMicroKeyboardIllustration
        ariaLabel="Interactive Codex Micro keyboard with illuminated Agent Keys, customizable Command Keys, a dial, and an analog stick"
      />
    </Illustration>

## Set up Codex Micro

1. Open the ChatGPT desktop app.
2. Connect Codex Micro to your computer with a USB-C cable or Bluetooth, then
   follow the setup that appears when ChatGPT detects it.
3. On macOS, allow **Input Monitoring** when prompted so ChatGPT can respond to
   key presses.
4. Open **Settings > Codex Micro** to choose which chats the Agent Keys follow,
   assign actions to the Command Keys and analog directions, and adjust the
   lighting.

To open these settings again, press and hold the dial for 500 milliseconds or
select the Codex Micro icon beside your account name at the bottom of ChatGPT.

You'll see **Codex Micro** in Settings after ChatGPT detects the device for the
first time. If you want to use the device outside ChatGPT, customize those
controls with [Work Louder Input](https://worklouder.cc/micro-setup).

<a id="read-and-switch-tasks-with-agent-keys"></a>

## Read and switch chats with Agent Keys

Each of the six frosted Agent Keys can follow a chat and light up to show its
current status. Press an Agent Key once to switch to that chat without bringing
ChatGPT forward. Press it twice within 350 milliseconds to switch chats and
bring the ChatGPT window forward.

| Light | Status           | Meaning                                   |
| ----- | ---------------- | ----------------------------------------- |
| White | Idle             | The chat is idle.                         |
| Blue  | Thinking         | ChatGPT is working.                       |
| Green | Complete         | The chat completed with an unread update. |
| Amber | Requires input   | ChatGPT needs your approval or response.  |
| Red   | Error            | Something went wrong.                     |
| Off   | No assigned chat | The key doesn't follow a chat.            |

The selected chat's key pulses with its status light.

Out of the box, the keys follow your six most recently updated chats, whether
or not they're pinned. You can change **Agent source** in **Settings > Codex
Micro** to use a different arrangement:

- **Most recent chats**: Follow the six most recently updated chats, pinned or
  unpinned.
- **Pinned chats**: Follow the first six chats in **Pinned**.
- **Priority chats**: Put chats waiting for input, unread chats, and active
  chats first.
- **Custom assignments**: Choose the chat assigned to each Agent Key. Press an
  unassigned Agent Key to open a new chat. When you start the chat, ChatGPT
  assigns it to that key.

The status colors stay the same. You can decide which chats the Agent Keys
follow, but you can't turn them into extra Command Keys.

## Use and customize Command Keys

Codex Micro comes with six actions in its default layout:

|                            Key                            | Default action                           |
| :-------------------------------------------------------: | ---------------------------------------- |
|  <CodexMicroTableKeycap keycapId="FAST" label="Fast" />   | Turn Fast mode on or off.                |
| <CodexMicroTableKeycap keycapId="APPR" label="Approve" /> | Approve the current request.             |
| <CodexMicroTableKeycap keycapId="REJ" label="Decline" />  | Decline the current request.             |
|  <CodexMicroTableKeycap keycapId="SPLIT" label="Fork" />  | Continue the current chat in a new chat. |
|   <CodexMicroTableKeycap keycapId="MIC" label="Mic" />    | Start push-to-talk.                      |
| <CodexMicroTableKeycap keycapId="CODEX" label="Codex" />  | Send the message in the composer.        |

The Mic key uses your computer's microphone. Codex Micro doesn't have a
microphone of its own. Hold the key while you speak, then release it to stop.
For hands-free recording, press it twice within 350 milliseconds to keep
recording. Press it again to stop.

A sea-green light moves around the keyboard while you record. It changes to a
moving white light while ChatGPT processes your speech, then turns solid white
when the prompt is ready. Press the Codex key to send it.

In **Settings > Codex Micro**, select a Command Key, then choose its keycap and
action. You can open the browser or terminal, review changes, commit with Git,
create a pull request, attach files or photos, manage scheduled tasks, change
reasoning effort, or open **Skills**. If you choose a keycap that's already used
somewhere else, ChatGPT swaps the two instead of using one keycap twice.

After you remap a key, swap the physical keycap to match its new action.

## Use the analog stick and dial

The analog stick moves freely in any direction. When you push it far enough
from the center, ChatGPT turns the movement into one of four directional
actions. Codex Micro starts with the mappings shown here.

Choose any available ChatGPT desktop command or enabled skill for each
direction in **Settings > Codex Micro**.

| Direction | Default action             |
| --------- | -------------------------- |
| Up        | Turn Plan mode on or off.  |
| Right     | Go forward in app history. |
| Down      | Show or hide the sidebar.  |
| Left      | Go back in app history.    |

The dial moves through the composer controls and options, with **Reasoning**
selected by default. Turn the dial to change the selection, then press it to
open or select the focused control. When a composer control or menu is open,
the Agent Key immediately to the right of the dial lights red. Press that key
to cancel.

In **Settings > Codex Micro**, choose whether the dial uses **Composer
navigation** or **Reasoning only**. In **Reasoning only** mode, turning the dial
opens and adjusts reasoning effort. Press the dial to open the slider or its
advanced options.

## Adjust lighting

In **Settings > Codex Micro**, adjust the brightness and choose how long the
lights stay on when you're not using Codex Micro. They come back on when you
use the keyboard or an Agent Key changes status. By default, the lights turn
off after three minutes.

When the keyboard reports its battery status, you can see it in **Settings >
Codex Micro** and in the Codex Micro icon's sidebar tooltip.

## Add more layers

Codex uses layer 1. Use [Work Louder
Input](https://worklouder.cc/micro-setup) to configure up to five more layers
with shortcuts and actions for other apps.

## Troubleshoot Codex Micro

### Pair the keyboard again

Use the bottom-left touch control to start pairing again. The rear button
controls power and doesn't start pairing.

1. Hold the bottom-left touch control for three seconds to enter communication
   mode.
2. Tap the control to choose Bluetooth channel 1, 2, or 3.
3. Hold the control for three seconds on that channel. The channel light flashes
   while pairing and turns solid when paired.

### Fix Input Monitoring on macOS

If **Settings > Codex Micro** shows that Input Monitoring isn't set up, select
**Open System Settings**, then follow these steps:

1. Open **System Settings > Privacy & Security > Input Monitoring**.
2. Turn on access for ChatGPT if it's already listed. If it's missing, drag
   **ChatGPT** from Applications into the list, or select **Add (+)** and choose
   **ChatGPT**.
3. Quit and reopen ChatGPT, then confirm ChatGPT detects Codex Micro on layer 1.

For more about this macOS permission, see [Apple's Input Monitoring
guide](https://support.apple.com/guide/mac-help/mchl4cedafb6/mac).

### Get more Work Louder help

For help with Bluetooth, cables, power, or resetting the keyboard, see
the [Creator Micro 2 setup guide from Work Louder](https://worklouder.cc/micro-setup).
For direct support, email [hello@worklouder.cc](mailto:hello@worklouder.cc).

## Get Codex Micro

You can buy Codex Micro through [OpenAI Supply
Co](https://openai.com/supply/co-lab/work-louder/) while supplies last.

{/* vale Microsoft.We = NO */}
{/* vale write-good.TooWordy = NO */}

We expect orders to begin shipping shortly after purchase.

{/* vale Microsoft.We = YES */}
{/* vale write-good.TooWordy = YES */}
