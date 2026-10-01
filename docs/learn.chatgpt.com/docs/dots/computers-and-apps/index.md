---
source_type: 'learn'
source_area: 'learn_dots'
source_url: 'https://learn.chatgpt.com/docs/dots/computers-and-apps'
source_kind: 'learn_markdown'
---

# Connect computers and apps to your dot

Source: https://learn.chatgpt.com/docs/dots/computers-and-apps

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Your dot lives in the cloud and has its own computer and browser. It stays
available when your computer is off. Connecting your own computer and apps
gives it access to more of your work. These connections are separate from
the [channels you use to message your dot](https://learn.chatgpt.com/docs/dots/channels). You can send
a request from your phone while your dot works in the cloud or coordinates
work on a connected computer.

## Use the cloud computer

Open your dot's profile and look under **Computers** to inspect its cloud
computer. You can also select **Open computer** when your dot offers a browser
handoff.

Opening the computer doesn't give you control. Select **Take over** to use its
mouse and keyboard, then **Return control** when your dot can continue.

Use the cloud computer for research, documents, data analysis, or software
work. Cloud work can continue while your devices are off, and the computer can
keep its state between periods of use. It has its own files, software, and
browser sessions. Signing in to a website on your computer doesn't sign your
dot in to that website.

## Cloud threads

Your dot can start separate threads for cloud work. These appear in your desktop, web, and mobile apps, where you can review results and give further instructions while your dot continues coordinating. For coding work, it can use a Codex cloud environment you’ve set up with the repository and configuration it needs.

Your dot can work on several things in parallel, and you can keep talking to it while those threads run. See [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory#assigned-work).

## Sign in to a website

Your dot uses the same private sign-in flow as ChatGPT Work. When a website
needs a login, your dot can send a request with a private form. Enter your
credentials there and complete any verification the website requires, such as
a verification code. The form sends this information to the remote browser
outside your conversation.

You can also choose to sign in on the website instead. This opens your dot's
browser in takeover mode so you can complete the steps yourself. Return control
when you're ready for your dot to continue.

### Staying signed in

A website session can remain available for later work until you sign out or
the website expires it. Your dot's cloud browser has its own sessions; it doesn't
inherit logins from your personal browser. Some websites block cloud browsers
or require further verification.

### Saving and reusing a login

When offered, **Save to Passwords** lets you save a login for future
sign-ins. Saving is optional. If a matching saved login is available for a new
sign-in request, you can confirm that you want to use it or enter another account.

A saved login and an active website session are different. Your dot can continue
using a valid session without signing in again. Reusing a saved login to sign in
requires your confirmation.

## Connect your computer

Connect your computer once to make its local files, code, and apps available
for your dot’s work:

1. Open your dot's profile in the ChatGPT app on that computer.
2. Under **Computers**, find **Your computer** and select **Allow access**.
3. Review the confirmation and select **Allow access** to connect it.

You can connect only one personal computer at a time. Your dot’s cloud computer stays connected. Access to your computer applies
wherever you message the same dot, including from your phone.

Your dot can create local Work or Codex tasks and continue existing local Codex
tasks. A task can be managed
in the cloud while using files and tools on your connected computer. Open the
task to inspect where the work is happening or give instructions directly. See
[Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory#assigned-work) for task types
and connection requirements.

If a website blocks the cloud browser, ask your dot to try your connected
computer. This may create a separate local task. It doesn't transfer the cloud
browser's session or guarantee that a particular local browser is supported.

The connection persists between tasks. Keep your computer online and the
ChatGPT app open while your dot uses it.
An **Offline** status means the computer is unavailable; it doesn't revoke
the connection. Select **Revoke access** to remove access. Your dot's
local-computer permission is separate from connecting a computer to Codex or
enabling Work Sync. Neither connection alone gives your dot access.

## Connect apps

Your dot can use supported [plugins](https://learn.chatgpt.com/docs/plugins) installed and enabled for your account. Access depends on the plugin’s connected account, permissions, and the environment where the work runs. Local skills require a connected computer.

For example, connect Gmail to find relevant email, Google Drive to read and update documents, or GitHub to investigate an issue and prepare a pull request. Install and connect each plugin you want your dot to use.

Review
the connected account and its allowed actions. Your existing ChatGPT app
permissions apply to your dot. For example, you can allow it to read email
without allowing it to send email. If a connection expires, open the request
to reconnect it before continuing.

Adding a contact method doesn't grant access to your apps or computer. For
example, messaging your dot in Slack doesn't connect your inbox.
