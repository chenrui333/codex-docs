---
source_type: 'learn'
source_area: 'learn_dots'
source_url: 'https://learn.chatgpt.com/docs/dots/getting-started'
source_kind: 'learn_markdown'
---

# Get started with your dot

Source: https://learn.chatgpt.com/docs/dots/getting-started

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Create your dot in the ChatGPT mobile app, desktop app, or a desktop browser. You can give it more than one ongoing responsibility.

## Create your dot

<WorkflowSteps>

1. Open dots in the ChatGPT mobile app, desktop app, or a desktop browser, and follow the introduction.
2. Give your dot a name and customize its appearance. You can keep the defaults and change them later.
3. Connect plugins for the apps you want your dot to use, such as email, calendar, and files. You can skip this step and add them later.

</WorkflowSteps>

### Set up on mobile or desktop

Choose whichever device works best for you: the ChatGPT mobile app, desktop app, or a desktop browser. After setup, you can continue with the same dot across devices.

If you prefer to set up on your phone, use the latest version of the ChatGPT mobile app. You can name your dot, customize its appearance, and connect plugins there. You can also choose to have ChatGPT open directly to your dot’s conversation. Mobile web is not supported. See [access and preview limits](https://learn.chatgpt.com/docs/dots#access) if dots is not available to your account.

### Connect your computer

Connecting your own computer lets your dot work there when it’s helpful: using files on your computer, working with the context of your signed-in browser, or starting and managing your local Codex tasks. Keep your computer online with the ChatGPT app open while your dot uses it.

This connection is optional. Your dot has its own cloud computer and can work without access to your device. You can [connect your computer](https://learn.chatgpt.com/docs/dots/computers-and-apps#connect-your-computer) from the desktop app during setup or later, whether you created your dot on mobile or desktop.

## Connect tools and contact methods

Connect what your dot needs:

- **Apps:** Connect services through [plugins](https://learn.chatgpt.com/docs/plugins) so your dot can use their information and tools.
- **Messaging:** Open your dot's profile and select **Add** to connect a contact method, such as Slack. See [Message your dot](https://learn.chatgpt.com/docs/dots/channels).
- **Your computer:** Connect it once from your dot’s profile to make local files, code, and apps available for future work. Keep it online with the ChatGPT app open while your dot uses it.

These connections are separate. Connecting a messaging channel doesn't automatically grant access to an inbox, other apps, or your computer. Your dot lives in the cloud and has its own computer and browser for work that doesn't need your device.

## Your first conversation

Your dot introduces itself and uses the context and connected apps available
to it to learn about your work and suggest where it can help. You can start
talking to it while it gathers that context. If it needs more information or
access, it can ask. Its suggestions depend on the information available to it.

It starts with relevant ChatGPT memory and keeps notes as you work together.
See [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory#context-and-memory).

<a id="give-it-a-first-task"></a>

## Start working together

Start with work you want your dot to keep track of, rather than treating each conversation as a fresh request. Describe what matters, share the relevant sources, and explain which decisions need your input. Built-in safeguards and approval checks apply alongside your existing app permissions. For example:

<DotPrompt
  client:load
  label="An offsite to organize"
  prompt="Help me keep our offsite on track. Use the plan and venue emails I shared to keep track of decisions, deadlines, and unanswered questions. Let me know when something needs my attention, and draft suggested replies for my review."
/>

Review the result and correct missing details. Your dot can delegate parts of a request to ChatGPT Work or Codex. In the desktop app, open your dot’s profile and select [Activity](https://learn.chatgpt.com/docs/dots/controls#review-work) to inspect delegated work and requests for input.

<a id="set-up-a-follow-up"></a>

## Keep the work moving

Your dot can decide when to follow up and use background agents to work on several things at once. Keep talking to it to add context, change priorities, or make a decision. You don’t need to restart the work in a new conversation.

Tell it where to send updates and when to interrupt you. You can also request a fixed schedule when the timing matters. Include the time zone and duration:

<DotPrompt
  client:load
  label="A scheduled check-in"
  prompt="Check the connected planning channel each weekday at 9 AM Central for the next four weeks. Update my checklist when a deadline changes. If a deadline is at risk, message me in ChatGPT and draft a reminder for my review. Confirm the schedule."
/>

Where a connected source supports it, you can also ask your dot to act when a specified event occurs, such as when a new bug report appears in a Slack channel. Ask it to confirm what it set up. You can revise a responsibility or cancel a recurring task later. Ending a conversation or voice call doesn't necessarily stop assigned work.
