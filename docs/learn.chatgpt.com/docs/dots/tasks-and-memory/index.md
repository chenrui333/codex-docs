---
source_type: 'learn'
source_area: 'learn_dots'
source_url: 'https://learn.chatgpt.com/docs/dots/tasks-and-memory'
source_kind: 'learn_markdown'
---

# Tasks and memory

Source: https://learn.chatgpt.com/docs/dots/tasks-and-memory

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Your dot can keep track of more than one responsibility at a time. You can switch
tasks, add a detail, or change priorities in the same conversation. Describe
the result you need and the sources it should use. Built-in safeguards and app
permissions apply automatically; you can add more specific instructions.

> Illustration: A dot conversation shows two task links, a follow-up instruction, and a tested draft pull request ready for review. Activity and Outputs appear alongside the conversation.

## Assigned work

Your dot keeps working between conversations and follows through as things change. It can decide when to pause and wake up to continue, so you don’t need to put every follow-up on a fixed schedule. You can also specify a time or a supported event that should trigger work. Tell it which results deserve an update and which decisions need your input.

Your dot can divide work among background agents that run in parallel and report back to it. You can keep talking to your dot while they work. It can also create separate, visible threads and send follow-up instructions.

New cloud threads appear in your desktop, web, and mobile apps, where you can open them and continue steering the work. Local Codex threads are available on the connected computer. For coding work that needs a particular repository and setup, your dot can use a Codex cloud environment you’ve created.

| Task                         | How your dot can work with it                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------- |
| New local Work or Codex task | Create a task on a computer connected to your dot. Keep that computer online with the ChatGPT app open. |
| Existing local Codex task    | Continue the task on a connected computer. Identify the task and what you want to change.               |
| New cloud coding task        | Create a task in a Codex cloud environment you have already set up. Your computer can be offline.       |
| Task your dot created        | Check results and send follow-up instructions using the task's original computer or cloud environment.  |

For cloud coding work, create the environment in Codex first, including its
repository and setup configuration. Changing your dot's selected computer
doesn't move an existing task to that computer.

In the desktop app, open your dot's profile, select **Activity**, and open a
task to inspect its progress, files, results, or requests for input. You can
also give instructions directly. Your dot can continue coordinating the task
when you step away.

A new task receives instructions and context from your dot for that work. It
has its own conversation; it doesn't automatically receive every conversation
you've had with your dot. Connecting a computer doesn't grant access to every
existing ChatGPT or Codex conversation.

Review the output and any reported errors even after a run completes. A
completed run doesn't by itself confirm that the requested result was achieved
or delivered. See [Review work](https://learn.chatgpt.com/docs/dots/controls#review-work).

## Recurring tasks

Work that repeats at fixed times needs a saved schedule. Specify:

- What your dot should check or update.
- When it should run, including the time zone and any end date.
- Which changes deserve a notification.
- Where to deliver results.

For example:

> Check the connected planning channel each weekday at 9 AM Pacific for the
> next four weeks. Update the project checklist when a deadline changes.
> Message me in ChatGPT only if a deadline is at risk or you need a decision.
> Confirm the schedule.

Ask your dot to confirm what it saved. Use **Scheduled** to review recurring
work, or ask your dot to list, change, or cancel its scheduled tasks.

Stopping active work and canceling a schedule are separate actions. See
[Controls](https://learn.chatgpt.com/docs/dots/controls#stop-work).

### Event monitoring

When a connected service supports event monitoring, you can instead ask your
dot to respond to a specific event. For example, ask it to investigate new
bug reports in a connected Slack channel and prepare fixes for your review.
Tell it which events to watch for and when to notify you. Ask it to confirm
which events it can follow. Connecting Slack or another source alone doesn't
create a monitoring task.

## Context and memory

Your dot uses the conversation it is working in, relevant ChatGPT memory, and
its own saved notes to keep track of your preferences and ongoing responsibilities.
These serve different purposes.

### Conversation context

Context is the information available to your dot while it responds or works:
messages, instructions, relevant source material, and results from its tools
or delegated work. It can use this information to connect a new request to work
already underway.

The context available for an interaction is a selection of this information.
Calls use selected conversation context, which can differ from the information
available to a task working in the background.

### Persistent memory

Your dot starts with relevant context from ChatGPT memory. It also keeps its own
notes about preferences, decisions, and ongoing work so it can use them in later
conversations. These notes are separate from ChatGPT's saved memory and are not
a complete transcript of everything you've said.

As you work together, your dot can update these notes to reflect new decisions
and changing priorities. Changing a ChatGPT saved-memory setting doesn't
necessarily change the notes your dot has already made.

### Across messaging channels

ChatGPT, Slack, and Teams are ways to reach the same dot. Switching
between them doesn't create a separate dot or reset its saved notes. Information
you share through one contact method can inform its work and replies through
another.

The visible conversations remain distinct. A message in ChatGPT isn't automatically
copied into your Slack conversation. Your dot's ability to use information also
doesn't grant permission to disclose it to another audience. For example, it can
use a deadline you shared privately to help you prepare an update, but sharing
private details in a team channel still requires permission.

This continuity applies to conversations with your dot. Connecting a computer
doesn't make every conversation in every app available to it. See
[Message your dot](https://learn.chatgpt.com/docs/dots/channels) for contact methods and availability.

## Proactive research

Alongside assigned work, your dot can research information it has permission
to read and keep private notes about useful findings. This background research
can connect new information to earlier work. For example, your dot might flag
that a release decision conflicts with a draft you shared last week.

Proactive research itself doesn't send messages, change connected apps, or
control a browser or computer. The background agents report their findings to
your dot, which can bring you a suggestion or question. Any follow-up action
is subject to the permissions and approvals that apply to that work.

Assigned recurring tasks can include actions you've authorized. Their
permissions and schedule are separate from proactive research.
