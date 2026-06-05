---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/slack-action-triage'
source_last_modified: '2026-06-05T16:54:10Z'
source_etag: 'W/"c852315a9b3bfe03b55abe5b1943f9d8"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0"]
---

# Prioritize Slack action items | Codex use cases

Source: https://developers.openai.com/codex/use-cases/slack-action-triage

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Prioritize Slack action items

Turn Slack threads and DMs into a ranked queue of next steps.

Difficulty **Easy**

Time horizon **30m**

Use Codex with Slack and the tools where work happens to find direct asks, implicit follow-ups, resolved items, and the highest-impact next actions before drafting replies or handoffs.

## Best for

- People who get work through Slack and need Codex to separate live asks from already-handled chatter.
- Launch, community, support, product, and operations workstreams where context is split across DMs, channels, and threads.
- Teams that want a ranked action queue before drafting replies, handoffs, docs changes, or follow-up tasks.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/slack-action-triage/?export=pdf)

Use Codex with Slack and the tools where work happens to find direct asks, implicit follow-ups, resolved items, and the highest-impact next actions before drafting replies or handoffs.

Easy

30m

Related links

[Codex plugins](/codex/plugins)  [Use Codex in Slack](/codex/integrations/slack)  [Codex automations](/codex/app/automations)

## Best for

- People who get work through Slack and need Codex to separate live asks from already-handled chatter.
- Launch, community, support, product, and operations workstreams where context is split across DMs, channels, and threads.
- Teams that want a ranked action queue before drafting replies, handoffs, docs changes, or follow-up tasks.

## Skills & Plugins

- [Slack](https://github.com/openai/plugins/tree/main/plugins/slack)

  Search DMs, channels, thread replies, mentions, and shared context before deciding what still needs attention.
- [Gmail](https://github.com/openai/plugins/tree/main/plugins/gmail)

  Cross-check email when a Slack thread refers to an outreach, intro, or sent follow-up.
- [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive)

  Read linked docs, decks, sheets, or source material when the Slack thread depends on an artifact.
- [Google Calendar](https://github.com/openai/plugins/tree/main/plugins/google-calendar)

  Check event timing when a thread depends on a meeting, launch, webinar, or deadline.

| Skill | Why use it |
| --- | --- |
| [Slack](https://github.com/openai/plugins/tree/main/plugins/slack) | Search DMs, channels, thread replies, mentions, and shared context before deciding what still needs attention. |
| [Gmail](https://github.com/openai/plugins/tree/main/plugins/gmail) | Cross-check email when a Slack thread refers to an outreach, intro, or sent follow-up. |
| [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive) | Read linked docs, decks, sheets, or source material when the Slack thread depends on an artifact. |
| [Google Calendar](https://github.com/openai/plugins/tree/main/plugins/google-calendar) | Check event timing when a thread depends on a meeting, launch, webinar, or deadline. |

## Starter prompt

Can you check @slack for messages to me about [workstream] from [time window] and return a ranked action queue?
Look across DMs, group DMs, channel mentions, and threads.
For each item, include:
- source link or thread
- what is being asked
- whether it needs my reply, a person or lead, a docs or code change, or just a decision
- why it matters
- the recommended next step
Before calling anything unresolved, read the latest thread replies and skip items that were already handled.
Do not post messages directly but suggest drafts for my review.

Open in the Codex app

Can you check @slack for messages to me about [workstream] from [time window] and return a ranked action queue?
Look across DMs, group DMs, channel mentions, and threads.
For each item, include:
- source link or thread
- what is being asked
- whether it needs my reply, a person or lead, a docs or code change, or just a decision
- why it matters
- the recommended next step
Before calling anything unresolved, read the latest thread replies and skip items that were already handled.
Do not post messages directly but suggest drafts for my review.

## Find the work hidden in Slack

Slack is often where a request starts, but not where the full context lives. A teammate might ask for a reply in a DM, clarify the real action in a thread, link a doc in a channel, and resolve the issue later without mentioning you again.

Use this workflow when you want Codex to read the Slack context, check whether the ask is still live, and return the few items that actually need your attention. The goal is to get a ranked action queue: what needs a reply, a decision, a person to contact, a doc update, or a handoff.

## Run the triage pass

1. Give Codex a time window, workstream, person, channel, or topic.
2. Ask it to search DMs, group DMs, channel mentions, and relevant thread replies.
3. Have Codex read the latest thread tail before calling an item unresolved.
4. Ask for a ranked queue sorted by urgency and impact.
5. Ask Codex to draft the reply, handoff, or follow-up task.

After trying this and tweaking the flow to match your needs, you can turn it into a [thread automation](/codex/app/automations#thread-automations) by asking Codex to do the same thing on a schedule.

## Ask for the right output

A useful triage result should explain why each item is still live. It should also skip old asks that someone answered later in the thread.

You should expect to see something like this:

![](/assets/OAI_Codex-Blossom_Fallback_Black.svg)
Codex

**Top action item:** Priya is asking for concrete customer
examples, not just more ideas.

**Why it matters:** the launch update needs real people the
team can contact this week.

**Evidence:** the original channel message asked for use cases,
but the thread later says “please DM me if you have leads.”

**Next step:** reply with two named leads, or say you can be
the example if that is more useful.

Good output makes the distinction explicit: an idea is different from a lead, a live ask is different from an FYI, and a request you already answered shouldn’t stay in the queue.

If you get too much noise or too few actionable items, tweak the prompt and if needed, mention specific slack channels you want Codex to pay attention to.

## Draft the follow-up

Once the queue is right, keep the action in the same thread. Ask Codex to draft a reply or handoff from the evidence it already gathered:

Draft the Slack reply for each of these action items, using evidence from the triage pass.
Do not post it directly, but suggest drafts for my review.

## Related use cases

[![](/codex/use-cases/proactive-teammate.webp)

### Set up a teammate

Connect the tools where work happens, teach one thread what matters, then add an automation...

Automation  Integrations](/codex/use-cases/proactive-teammate)[![](/codex/use-cases/zoom-meeting-follow-ups.webp)

### Turn meetings into follow-ups

Use Codex with Zoom transcripts and AI Companion summaries to draft customer follow-up...

Automation  Integrations](/codex/use-cases/zoom-meeting-follow-ups)[![](/codex/use-cases/manage-your-inbox.webp)

### Manage your inbox

Use Codex with Gmail to find emails that need attention, draft responses in your voice, pull...

Automation  Integrations](/codex/use-cases/manage-your-inbox)

