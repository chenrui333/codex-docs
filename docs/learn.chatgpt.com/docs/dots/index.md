---
source_type: 'learn'
source_area: 'learn_dots'
source_url: 'https://learn.chatgpt.com/docs/dots'
source_kind: 'learn_markdown'
---

# Meet dots

Source: https://learn.chatgpt.com/docs/dots

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<OFeatureCanvas>

<a id="introducing-o"></a>
<a id="what-is-o"></a>

Your dot is an always-on agent that keeps work moving across your tools and projects. You can keep talking to it while it works, and it reaches out with results or decisions that need you.

Powered by GPT-6 Astra, your dot lives in the cloud and has its own computer and browser. You can reach it and it can keep working even when your computer is off. It can research, analyze data, prepare documents, and build software, using relevant context from past conversations and your preferences.

<a id="access-to-dots"></a>

**Dots are rolling out gradually to eligible accounts.** See [availability and access](#access) for plan, region, and workspace requirements.

<a id="meet-your-o"></a>

## Make it your own

Create your dot in the ChatGPT desktop app or a desktop browser. Setup offers app connections and, in the desktop app, access to your computer. Your dot introduces itself and uses the context available to it to suggest ways it can help. You can start talking to it while it gets to know your work.

Give your dot a name and choose its shape, color, eyes, glasses, and accessories. You can change these anytime.

Your dot starts with a handle such as @yourname-dot. Naming it updates the handle, for example, @tibo-alfred for a dot named Alfred.

<a id="make-it-yours"></a>

<a id="stay-connected"></a>

<a id="your-dot-wherever-you-are"></a>

## Message or call your dot

Continue talking to your dot in ChatGPT on desktop or in the mobile app when the supporting update is available. Create your dot on desktop first; mobile web is not supported.

> Illustration: An illustrative ChatGPT conversation starts on desktop and continues with the same dot in the mobile app: a venue comparison gains a budget constraint. Mobile use requires the supporting app update.

You can message your dot or call it to discuss work, change priorities, or make a decision. In ChatGPT, select the phone button in your dot’s conversation to start a call. You can also type messages while you’re talking. Work you’ve assigned can continue after the call ends.

You reach the same dot in ChatGPT, Slack, Teams, or a call. Changing where you talk to it doesn’t start a new dot or reset its memory. Messages stay in their respective channels, while your dot can use relevant context across them. Before sharing information from a private conversation with other people, your dot checks that you’ve allowed it.

Tell your dot where to send different kinds of updates. For example, ask it to keep routine progress in ChatGPT and bring decisions to you in Slack. Explain which changes need your attention, such as a deadline at risk.

<a id="choose-where-o-can-reach-you"></a>
<a id="where-to-use-o"></a>

Open your dot's profile and select **Add** to connect an available contact method. See [Message your dot](https://learn.chatgpt.com/docs/dots/channels) for channel details.

In Slack, you can DM your dot or mention it in a channel you’ve added it to. By default, it responds to you; you can instruct it to engage with others. Existing permissions and safeguards still apply to what it shares and does. Tell it which channels and events to watch for. Adding it to a channel alone doesn’t start monitoring. You can also message your dot in Microsoft Teams. See [Slack and Teams](https://learn.chatgpt.com/docs/dots/channels#slack-and-teams).

<a id="how-o-works"></a>
<a id="how-your-dot-works"></a>

## How dots work

Your dot works between conversations. It tracks progress, works out what needs to happen next, and follows through as things change. Once you’ve asked it to handle something, you can return with new information or priorities without restarting the work. Your dot brings back results and turns to you for decisions that need your judgment.

> Illustration: A dot explains how it follows up between conversations and asks for decisions.

Your dot can decide when to pause and wake up to continue work; you don’t need a fixed schedule for every follow-up. It can use background agents to work on several things in parallel while you keep talking to it. It also researches connected information to suggest useful next steps.

For example, if your dot is helping organize an offsite, it can update the headcount as people confirm and ask before sending a request for revised pricing.

<a id="context-that-carries-forward"></a>

### Memory and context

Your dot draws on the conversation, relevant ChatGPT memory, and its own saved notes about your preferences, decisions, and ongoing work. These notes carry forward across conversations and contact methods, so it can build on what you’ve discussed as your work changes.

It can also research connected information and keep private notes to identify useful next steps. That research is read-only; follow-up actions require the applicable permissions. See [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory).

<a id="where-the-work-happens"></a>

### Its computer and yours

Your dot has its own computer and browser in the cloud for research, files, and running software. Cloud work can continue while your devices are off. When you need to inspect the browser or do a step yourself, open its computer and select **Take over**. Select **Return control** when you’re ready for your dot to continue. See [computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps) for connection details.

<DotProductPreview
  client:visible
  variant="computer"
  copy={{
    label:
      "Example of a dot's cloud browser displaying the California DMV vehicle registration renewal page, with the Take over control.",
    title: "{name}'s computer",
    domain:
      "dmv.ca.gov/portal/vehicle-registration/vehicle-registration-renewal/",
    websiteUrl:
      "https://www.dmv.ca.gov/portal/vehicle-registration/vehicle-registration-renewal/",
    websiteImageSrc: "/images/codex/dots/california-dmv-registration.jpg",
    websiteImageAlt:
      "California DMV website showing Vehicle Registration Online Renewal and the Before You Begin checklist.",
    status: "{name} has control",
    actions: ["Take over"],
  }}
/>

Connect your computer once through your dot’s profile to make its local files, code, and apps available for your dot’s work. You can connect only one personal computer at a time. The connection stays in place between tasks. Your computer must be online with the ChatGPT app open for your dot to use it. This permission is separate from connecting your computer to Codex or enabling Work Sync.

Your dot can use supported [plugins](https://learn.chatgpt.com/docs/plugins) installed and enabled for your account, with their connected accounts and existing permissions. For example, use Gmail to find relevant email, Google Drive to work with documents, and GitHub to investigate code and prepare changes. Each plugin must be connected and permitted to perform the actions you request. Local skills require a connected computer. Connecting a messaging channel doesn’t automatically grant access to your apps or computer.

<a id="connections"></a>

Each connection serves a different purpose:

| Connection              | What it enables                                                        |
| ----------------------- | ---------------------------------------------------------------------- |
| Messaging channel       | Talk to your dot and receive updates there.                            |
| Connected app or plugin | Use that service's information and tools within its permissions.       |
| Local computer          | Work with that computer's files, apps, and tasks while it's available. |

Connecting a messaging channel doesn't also connect your inbox, other apps,
or local computer. Your dot's cloud computer is separate from your devices
and their signed-in browser sessions.

### Signing in to websites

Your dot uses the same private browser sign-in flow as ChatGPT Work. When a website needs a login, it can send you a sign-in request. Open the request to enter your credentials and any requested verification in a private form. Your credentials go to the browser outside the conversation. You can also select **Take over to sign in** to complete the steps on the website yourself, then select **Done** when you’ve finished.

<DotWebsiteSignIn
  copy={{
    label:
      "Two illustrative views of website sign-in: Alfred requests access to a saved venue proposal, then a private sign-in form offers optional saving and browser takeover.",
    requestStep: "1. Open the sign-in request",
    formStep: "2. Sign in privately",
    name: "Alfred",
    request:
      "Sign in to your venue account so I can review the saved proposal.",
    domain: "venues.example.com",
    title: "Sign in to venues.example.com",
    description: "Enter your login details to continue.",
    help: "Learn more",
    fields: [{ label: "Email address" }, { label: "Password", password: true }],
    saveLabel: "Save to Passwords",
    takeoverLabel: "Take over to sign in",
    skipLabel: "Not now",
    submitLabel: "Sign in",
  }}
/>

The cloud browser has its own sessions, separate from the browser on your computer. Once you sign in, your dot can use that session for later work until you sign out or the website requires another login. When available, **Save to Passwords** lets you optionally save the login. Using a saved login for a new sign-in requires your confirmation. See [website sign-in](https://learn.chatgpt.com/docs/dots/computers-and-apps#sign-in-to-a-website).

Some websites block cloud browsers or require extra verification. You can ask your dot to try a connected computer instead. This may create a separate task on that computer; it doesn’t transfer the cloud browser’s session.

### Tasks and conversations

Your dot can use background agents, start new cloud threads, and create Work or Codex tasks on a connected computer. It can also continue existing local Codex tasks. For cloud coding work that needs your repository and setup, it can use a Codex cloud environment you’ve created.

Cloud threads appear as separate conversations in the desktop, web, and mobile apps, where you can review results and give further instructions. Local Codex tasks appear on the connected computer. You can keep talking to your dot while these tasks run.

In the desktop app, open your dot’s profile and select **Activity**, then open a task to inspect its progress, results, or requests for input. Your dot can check results and send follow-up instructions to tasks it created. See [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory#assigned-work) for where tasks run and how to continue them.

Connecting your computer lets your dot work with its tasks and files. It doesn't give your dot access to every conversation in every app.

### Permissions and approvals

Built-in safeguards, your existing ChatGPT app permissions, and automatic approval checks apply from the start. Before an action affects your accounts or shares information, review determines whether your dot can proceed, needs your approval, or must hand a step over to you.

You can add instructions for how you want your dot to work, such as asking it to show you drafts before sending them. Custom rules are optional controls for more specific ongoing boundaries. Neither instructions nor custom rules override built-in safety requirements. See [Control your dot](https://learn.chatgpt.com/docs/dots/controls).

<a id="what-o-can-do"></a>
<a id="things-to-try-with-o"></a>
<a id="try-more-with-o"></a>
<a id="what-could-you-do-with-yours"></a>

## Work with your dot

Start with work you regularly need to check or update. Describe the responsibility and share the source material it needs, then review its work and explain what needs to change.

<a id="work-with-o"></a>
<a id="start-working-together"></a>
<a id="give-o-your-first-task"></a>
<a id="an-event-youre-organizing"></a>
<a id="a-project-youre-working-on"></a>

### Give it a responsibility

For an offsite, share the plan and venue emails, then ask your dot to identify upcoming decisions and deadlines.

**An offsite to organize:**

```text
Help me keep our offsite on track. Read the plan and venue emails I shared, and make a list of decisions, deadlines, and things we're waiting on. Focus on anything that affects the budget or needs an answer this week. Draft suggested replies for my review, but don't send them.
```

Review the first result and correct any missing details before expanding the responsibility.

<a id="keep-working-together"></a>
<a id="things-you-want-to-follow-through-on"></a>

### Choose when and where to hear from it

Tell your dot what to keep current and which changes deserve your attention. It can decide when to follow up. If you want an update at a specific time, include a time zone and a duration or end date, and ask it to confirm the schedule.

**A scheduled check-in:**

```text
Check the connected planning channel each weekday at 9 AM Central for the next four weeks. Update our offsite list when something changes. Message me in ChatGPT if a deadline is at risk or you need a decision from me. Keep routine updates in the checklist. Confirm the schedule.
```

### Review and redirect

When priorities change, tell your dot what to change in the work already underway.

Ask your dot what it's working on and what needs your input. In the desktop app, open its profile and use **Activity** to review delegated tasks. Ask it to list recurring work and confirm what's scheduled.

Use **Pause** to stop your dot’s current main task. Stop delegated tasks in **Activity** and cancel recurring tasks in **Scheduled** separately. Ending a voice call doesn’t necessarily stop assigned work. See [Stop work](https://learn.chatgpt.com/docs/dots/controls#stop-work).

Review important results and their sources. Your dot can make mistakes, and stopping a task doesn't undo actions it has already completed.

### Ways to work with your dot

Give your dot access to the relevant sources and tell it what to keep track of. For example:

- **Keep a sales proposal current.** Share the proposal and customer requirements. As the requested seat count or terms change, have your dot update the figures, track outstanding security and technical reviews, and bring you the next decisions.
- **Prepare content from each interview.** Share the interview material and photos. Ask your dot to draft a caption, show notes, and clip ideas for review. You can refine the title or tone from your phone before publishing.
- **Keep launch materials aligned with the product.** Connect the launch channel and share the brief, deck, and approved visuals. Have your dot flag product changes that affect the campaign and prepare revised copy, slides, and speaker notes for your review.
- **Update a study as results arrive.** Share the study and new measurements. Have your dot update the comparison chart, explain where repeat results differ from the first batch, and draft a findings summary and proposed next tests for review.
- **Follow up on software feedback.** Connect the feedback source and code project. Ask your dot to investigate reported problems, such as a missing item in a sidebar, and prepare a fix for code review before merging.

## Access

**For workspace admins:** See [Set up dots for work](https://learn.chatgpt.com/docs/enterprise/dots-admin-guide) for workspace setup, permissions, and security and governance guidance.

Dots are rolling out gradually. You may not see dots immediately, even if your plan is eligible.

- **Pro 100, Pro 200, and Pro 500:** For users over 18 outside the European Economic Area, United Kingdom, and Switzerland.
- **Business Premium:** Rolling out worldwide.
- **Enterprise:** Rolling out worldwide. Dots are off by default and must be enabled by a workspace administrator.

Conversations with your dot don’t count toward your ChatGPT usage limits. Tasks your dot starts or manages in Work or Codex count toward those products’ usage limits as usual. Your plan includes an allowance for deeper work, with extended limits for the first month after launch.

Create your dot in the desktop app or in ChatGPT on a desktop browser. After setup, use the same dot in the mobile app when the supporting update is available. Mobile web is not supported.

## Reference

| Guide                                                | Covers                                                           |
| ---------------------------------------------------- | ---------------------------------------------------------------- |
| [Getting started](https://learn.chatgpt.com/docs/dots/getting-started)       | Setup, your first conversation, and assigning work.              |
| [Messaging](https://learn.chatgpt.com/docs/dots/channels)                    | ChatGPT, calls, Slack, and Teams.                                |
| [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory)     | Assigned work, recurring tasks, context, and proactive research. |
| [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps) | Cloud work, local access, plugins, and website sign-in.          |
| [Controls](https://learn.chatgpt.com/docs/dots/controls)                     | Review activity, manage permissions, and stop work.              |

</OFeatureCanvas>
