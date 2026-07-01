---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/complete-tasks-from-messages'
source_last_modified: '2026-06-05T16:40:45Z'
source_etag: 'W/"675cb9817e38b5cac1632e0e23a70345"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5"]
---

# Complete tasks from messages | Codex use cases

Source: https://developers.openai.com/codex/use-cases/complete-tasks-from-messages

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Complete tasks from messages

Turn iMessage threads into completed work across the apps involved.

Difficulty **Easy**

Time horizon **5m**

Use Computer Use to read one Messages thread, complete the task, and draft a reply.

## Best for

- Message threads that contain a concrete request, follow-up, or booking task
- Work that needs a quick check across Messages plus a few related apps

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/complete-tasks-from-messages/?export=pdf)

Use Computer Use to read one Messages thread, complete the task, and draft a reply.

Easy

5m

Related links

[Computer Use](/codex/app/computer-use)  [Customize Codex](/codex/concepts/customization)

## Best for

- Message threads that contain a concrete request, follow-up, or booking task
- Work that needs a quick check across Messages plus a few related apps

## Starter prompt

@Computer Look at my messages from [person].
Then:
- understand the request
- complete the task across the apps involved
- draft a reply in the same thread
Pause before anything irreversible, such as placing an order or confirming a booking.

Open in the Codex app

@Computer Look at my messages from [person].
Then:
- understand the request
- complete the task across the apps involved
- draft a reply in the same thread
Pause before anything irreversible, such as placing an order or confirming a booking.

## Introduction

Many message threads contain hidden to-dos: book dinner, schedule a follow-up, research options, submit a receipt, or pull together information for a reply. Computer Use can help by reading the thread, identifying the task, and completing the work across the apps involved.

This is a good fit when the message contains a concrete request and you want Codex to handle the follow-through, not just summarize the thread.

## How to use

1. Install the [Computer Use plugin](/codex/app/computer-use).
2. Ask Codex to review a specific message thread or sender.
3. Tell it what action to take and whether it should pause before completing anything.
4. Specify whether it should draft a reply in the original thread.

For example:

- `@Computer Look at my messages from [person]. Check my availability, find 2 dinner options in Hayes Valley, and draft a reply in the same thread. Check in with me before completing booking.`

## Practical tips

### Ask for a pause before irreversible actions

If the task might send money, submit an order, confirm a booking, or finalize a schedule, tell Codex to stop and ask before taking that last step.

### Make sure the supporting apps are ready

This works best when the related apps are already signed in and available. If the task depends on Maps, Calendar, Notes, a reservation site, or a browser session, prepare those ahead of time.

### Expect the thread to be marked as read

When Codex opens the thread in Messages, it will behave like a normal user viewing the conversation. Treat that as a read.

## Good follow-ups

This same pattern can work for other inbox-style surfaces too, such as Slack or email, when the work starts from a message and finishes somewhere else. If the workflow becomes common, add a reusable preference or instruction in [customization](/codex/concepts/customization) so Codex handles those requests the same way every time.

### Suggested prompt

**Finish One Task From a Message Thread**

@Computer Look at my messages from [person].
Then:
- understand the request
- complete the task across the apps involved
- draft a reply in the same thread
Pause before anything irreversible, such as placing an order or confirming a booking.

## Related use cases

[![](/codex/use-cases/learn-a-new-concept.webp)

### Learn a new concept

Use Codex to study material such as research papers or courses, split the reading across...

Knowledge Work  Data](/codex/use-cases/learn-a-new-concept)[![](/codex/use-cases/use-your-computer-with-codex.webp)

### Use your computer with Codex

Use Computer Use to hand off multi-step tasks across Mac apps, windows, and files.

Knowledge Work  Workflow](/codex/use-cases/use-your-computer-with-codex)[![](/codex/use-cases/new-hire-onboarding.webp)

### Coordinate new-hire onboarding

Use Codex to gather approved new-hire context, stage tracker updates, draft team-by-team...

Integrations  Data](/codex/use-cases/new-hire-onboarding)

