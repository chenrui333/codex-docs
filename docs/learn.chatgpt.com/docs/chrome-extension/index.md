---
source_type: 'learn'
source_area: 'learn_chrome_extension'
source_url: 'https://learn.chatgpt.com/docs/chrome-extension'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1"]
---

# Browser extension

Source: https://learn.chatgpt.com/docs/chrome-extension

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use the ChatGPT browser extension to work in Google Chrome, Microsoft Edge,
Brave, Opera, or Vivaldi from the ChatGPT desktop app. ChatGPT can read or act
on sites where you're already signed in, such as LinkedIn, Salesforce, Gmail,
or internal tools.

All five browsers support tab mentions and browser control from the desktop
app. Chrome, Edge, Brave, and Vivaldi also support side chat. **Opera doesn't
support side chat**; start its tasks in the desktop app instead.

Update the ChatGPT desktop app before setting up another browser. Browser
availability can depend on rollout and your workspace settings.

To let ChatGPT control its built-in browser instead, use `@Browser`. The
[built-in browser](https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app)
supports sign-in and keeps browsing work inside ChatGPT without using your
regular browser profile.

ChatGPT can also switch between tools as a task requires, using plugins when a
dedicated integration is available, your browser when it needs signed-in browser
context, and the built-in browser for localhost.

  <Alert
    client:load
    color="warning"
    variant="soft"
    description="Treat page content as untrusted context, and review the website before allowing ChatGPT to continue."
  />

<a id="use-chatgpt-from-chrome"></a>

## Use side chat in your browser

Side chat is available in Chrome, Edge, Brave, and Vivaldi.

Open ChatGPT beside the page you're viewing to ask about the page or continue
into tasks that can use its context alongside local files and connected apps.
ChatGPT can use context from your open tabs when a task needs it.

1. Open the page you want to work with.
2. Select ChatGPT from the browser toolbar or **Extensions** menu. On macOS, you
   can also press <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd>.
3. Ask a question about the page or give ChatGPT a task.

The panel stays with the tab where you opened it. Chats you start in side chat
are available in the ChatGPT app, and you can open recent ChatGPT chats in
the side chat, so you can continue work in either place.

> Illustration: ChatGPT open beside the current Chrome tab.

## Bring tabs and selected text into a chat

Mention an open browser tab in the desktop app when you want ChatGPT to use
that page as context. In browsers with side chat, you can also mention tabs
there, or highlight text on a page and bring the selection into your chat to
ask about a specific passage without copying the whole page.

In browsers with side chat, you can also right-click the page and select
**Ask ChatGPT**. The side chat opens with the relevant page context so you can
continue the request in your browser.

### Ask about a YouTube video

Open a YouTube video, then ask a question about it in a supported side chat.
When captions are available, ChatGPT can use the video's timestamped transcript
to explain, summarize, or answer questions about the content.

Treat webpage content, selected text, and video transcripts as untrusted
context. Review the page and any requested permissions before asking ChatGPT to
use or act on that information.

<a id="set-up-the-chrome-extension"></a>

## Set up your browser

Install the browser on your computer, then open **Settings > Computer Use** in
the ChatGPT desktop app. Expand **More browsers** if your browser isn't shown
in the main list.

1. Select your browser and follow any prompt to install the required plugin.
2. Select **Install** beside the browser to open its extension store page.
   Install the ChatGPT extension and review the browser's permission prompts.
3. Return to **Computer Use** and confirm that the browser shows **Manage**.
4. Start a ChatGPT Work or Codex chat and select your browser with an
   `@`-mention. Use the browser profile where you installed the extension.

The browser's toggle in **Computer Use** controls whether it appears in the
`@`-mention menu. Select **Manage** to change website permissions instead.

> Illustration: Computer Use settings showing Google Chrome connected through the Chrome extension.

<a id="start-a-chrome-task-from-chatgpt"></a>

## Start a browser task from ChatGPT

After setup, start a new ChatGPT Work or Codex chat. Select **Chrome**, **Edge**,
**Brave Browser**, **Opera**, or **Vivaldi** from the `@`-mention menu to choose
which browser ChatGPT uses. For example:

```text
@Edge open Salesforce and update the account from these call notes.
```

You can also mention an open tab to give ChatGPT context from that page.
Opera supports these desktop workflows even though it doesn't have side chat.

## Control website access

By default, ChatGPT asks before it interacts with each new website. ChatGPT bases
the prompt on the website host, such as `example.com`.

When ChatGPT asks to use a website, you can choose the option that matches the
task and your risk tolerance:

- **Allow once** to let ChatGPT use the website one time.
- **Allow for this site** so ChatGPT can use the website again without asking.
- **Allow for all sites** so ChatGPT can use websites without asking.
- **Decline** to prevent ChatGPT from using the website.

### Manage allowed and blocked websites

In the ChatGPT desktop app, go to **Settings** > **Computer Use**, then select
**Manage** next to your browser to manage an allowlist and blocklist for
domains. The allowlist contains domains ChatGPT can use without asking again.
The blocklist contains domains ChatGPT shouldn't use. The supported browsers
share these website permissions.

Removing a domain from the allowlist means ChatGPT asks again before using it.
Removing a domain from the blocklist means ChatGPT can ask again instead of
treating the domain as blocked.

#### Allow for all sites <ElevatedRiskBadge class="ml-2" />

If you select **Allow for all sites**, ChatGPT no longer asks for confirmation
before using websites. Only choose this option if you trust ChatGPT to use any
website open in the browser.

#### Browser history <ElevatedRiskBadge class="ml-2" />

Browser history can include sensitive telemetry, internal URLs, search terms,
and activity from browser sessions on signed-in devices. If you allow ChatGPT to
access browser history, relevant history entries can become part of the context
ChatGPT uses for the task. Malicious or misleading page content can increase the
risk that ChatGPT copies this data somewhere unintended.

ChatGPT asks when it wants to use browser history. ChatGPT scopes history access to
the request, and history doesn't have an always-allow option.

## Data and security

<a id="chrome-extension-permissions"></a>

### Browser extension permissions

Your browser asks you to accept permissions when you install the extension.
For example, Chrome's permission prompt may include:

- Access the page debugger
- Read and change all your data on all websites
- Read and change your browsing history on all your signed-in devices
- Display notifications
- Read and change your bookmarks
- Manage your downloads
- Communicate with cooperating native applications
- View and manage your tab groups

These extension permissions make it capable of operating browser
workflows. ChatGPT still uses its own confirmations, settings, allowlists, and
blocklists before using websites or browser history during a task.

### Memories

Computer Use follows your Memories setting. If Memories is on, ChatGPT can
use relevant saved memories while working in your browser. If Memories is off,
browser control doesn't use memories.

### What OpenAI stores from browsing

OpenAI doesn't store a separate complete record of your browser actions from the
extension. OpenAI stores browser activity only when it becomes part of the ChatGPT
context, such as text ChatGPT reads from a page, screenshots, tool calls,
summaries, messages, or other content included in the chat.

Your ChatGPT data controls apply to content processed in context.
Avoid sending secrets or highly sensitive data through browser tasks unless
they're required and you are present to review each prompt.

## Troubleshooting

If ChatGPT can't connect to your browser, first confirm the website ChatGPT is trying to
access isn't in the blocklist in Settings. If the website isn't blocked, work
through these checks:

1. Update the ChatGPT desktop app. If you have more than one ChatGPT or Codex
   desktop app installed, update each one or remove copies you no longer use.
2. Restart your browser. In Chrome, Edge, Brave, or Vivaldi, reopen ChatGPT from
   the toolbar or **Extensions** menu and confirm the side chat loads. Opera
   doesn't have side chat; check its connection from the desktop app.
3. In **Settings > Computer Use**, confirm that your browser appears and shows
   **Manage**. If it still shows **Install**, follow the setup flow again.
   Turn on its toggle if the browser is missing from the `@`-mention menu.
4. Make sure you are using the browser profile where the extension is
   installed. If you use more than one profile, install and enable the
   extension in the active profile.
5. Start a new ChatGPT Work or Codex chat and try the browser task again. This can
   clear chat-specific connection state.
6. Restart the ChatGPT desktop app, then try again. If the extension still
   doesn't connect, reinstall it through **Settings > Computer Use**.
7. If ChatGPT still can't use the browser, run `/feedback`
   in the app and include the chat ID when you contact support.

### Upload files

If a Chrome task needs to upload a file from your computer, allow the Chrome
extension to access file URLs in Chrome:

1. In Chrome, open the extensions icon in the toolbar, then click **Manage
   Extensions**.
2. On the extension card, click **Details**.
3. Turn on **Allow access to file URLs**.

After you change the setting, start the Chrome task again.
