---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/meeting-prep-briefs'
source_last_modified: '2026-05-20T00:58:28Z'
source_etag: 'W/"925523f2900baec4ecc93d8578954748"'
codex_cli_versions: ["0.131.0", "0.132.0", "0.133.0"]
codex_cli_versions_raw: ["codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0"]
---

# Prepare meeting briefs | Codex use cases

Source: https://developers.openai.com/codex/use-cases/meeting-prep-briefs

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Prepare meeting briefs

Turn calendar context into an agenda and notes plan.

Difficulty **Easy**

Time horizon **30m**

Use Codex with Calendar, Drive, Slack, and Gmail to gather approved sources before a meeting, then draft objectives, agenda, questions, and a notes template.

## Best for

- Meetings where context is split across calendar invites, docs, Slack threads, email, and notes.
- Managers, product teams, operators, and interviewers who want a source-backed prep packet.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/meeting-prep-briefs/?export=pdf)

Use Codex with Calendar, Drive, Slack, and Gmail to gather approved sources before a meeting, then draft objectives, agenda, questions, and a notes template.

Easy

30m

Related links

[Codex plugins](/codex/plugins)  [Use Codex with Google Calendar](/codex/plugins)  [Codex app](/codex/app)

## Best for

- Meetings where context is split across calendar invites, docs, Slack threads, email, and notes.
- Managers, product teams, operators, and interviewers who want a source-backed prep packet.

## Skills & Plugins

- [Google Calendar](https://github.com/openai/plugins/tree/main/plugins/google-calendar)

  Find the meeting, attendees, timing, and attached material that should shape the brief.
- [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive)

  Read linked docs, interview notes, pre-reads, trackers, and source artifacts.
- [Slack](https://github.com/openai/plugins/tree/main/plugins/slack)

  Pull the latest planning thread, decision context, or collaborator updates when the meeting depends on them.
- [Gmail](https://github.com/openai/plugins/tree/main/plugins/gmail)

  Check related email threads for scheduling changes, attachments, or external context.

| Skill | Why use it |
| --- | --- |
| [Google Calendar](https://github.com/openai/plugins/tree/main/plugins/google-calendar) | Find the meeting, attendees, timing, and attached material that should shape the brief. |
| [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive) | Read linked docs, interview notes, pre-reads, trackers, and source artifacts. |
| [Slack](https://github.com/openai/plugins/tree/main/plugins/slack) | Pull the latest planning thread, decision context, or collaborator updates when the meeting depends on them. |
| [Gmail](https://github.com/openai/plugins/tree/main/plugins/gmail) | Check related email threads for scheduling changes, attachments, or external context. |

## Starter prompt

Help me prepare for [meeting] on [date].
Use only these sources:
- calendar event: [event name or date range]
- docs or notes: [links or names]
- Slack channels or threads: [optional]
- Gmail thread or sender: [optional]
First, inventory the sources you can access and name any source gaps.
Return:
- meeting objective
- attendee context
- key source-backed facts
- likely agenda
- open questions
- decisions or follow-ups I may owe
- suggested notes template for the meeting
Keep unsupported claims in a separate source gaps section. Do not update docs, send messages, or share the brief until I approve it.

[Open in the Codex app](codex://new?prompt=Help+me+prepare+for+%5Bmeeting%5D+on+%5Bdate%5D.%0A%0AUse+only+these+sources%3A%0A-+calendar+event%3A+%5Bevent+name+or+date+range%5D%0A-+docs+or+notes%3A+%5Blinks+or+names%5D%0A-+Slack+channels+or+threads%3A+%5Boptional%5D%0A-+Gmail+thread+or+sender%3A+%5Boptional%5D%0A%0AFirst%2C+inventory+the+sources+you+can+access+and+name+any+source+gaps.%0A%0AReturn%3A%0A-+meeting+objective%0A-+attendee+context%0A-+key+source-backed+facts%0A-+likely+agenda%0A-+open+questions%0A-+decisions+or+follow-ups+I+may+owe%0A-+suggested+notes+template+for+the+meeting%0A%0AKeep+unsupported+claims+in+a+separate+source+gaps+section.+Do+not+update+docs%2C+send+messages%2C+or+share+the+brief+until+I+approve+it. "Open in the Codex app")

Help me prepare for [meeting] on [date].
Use only these sources:
- calendar event: [event name or date range]
- docs or notes: [links or names]
- Slack channels or threads: [optional]
- Gmail thread or sender: [optional]
First, inventory the sources you can access and name any source gaps.
Return:
- meeting objective
- attendee context
- key source-backed facts
- likely agenda
- open questions
- decisions or follow-ups I may owe
- suggested notes template for the meeting
Keep unsupported claims in a separate source gaps section. Do not update docs, send messages, or share the brief until I approve it.

## Prepare from the sources you already have

Meeting context often lives outside the calendar invite. There may be a pre-read in Drive, a decision in Slack, an email thread, or notes from an earlier conversation.

Use Codex to gather the approved sources and draft a short prep brief with the objective, agenda, open questions, and a notes template.

## Gather the right context

1. Name the meeting, date, or calendar event.
2. Point Codex at the docs, notes, Slack threads, email threads, or folders it can use.
3. Ask Codex to inventory the sources before writing the brief.
4. Have it separate confirmed context, source gaps, and open questions.
5. Ask for a notes template or scorecard if you need to capture decisions during the meeting.

For interview loops, ask Codex to read the approved notes or question bank, then produce a structured scorecard. For recurring planning meetings, ask it to compare the last notes with the latest source updates so the agenda starts from what changed.

## Keep the brief scannable

Ask for the smallest output that will help. You should get something like this:

![](/assets/OAI_Codex-Blossom_Fallback_Black.svg)
Codex

**Objective:** decide whether the launch plan has enough owner
coverage for the next two weeks.

**Context:** the pre-read has a draft owner map, but two
follow-up items in Slack still need dates.

**Questions:** who owns partner review, and what is the latest
date for the public copy freeze?

**Notes template:** decisions, owners, dates, risks, and
follow-ups.

If the brief includes private or sensitive information, keep the output local to the thread and ask Codex to flag anything that doesn’t belong in a shared doc.

Turn this prep brief into a live notes template.
Keep the source-backed context short, then add sections for:
- decisions
- owners and dates
- risks
- unanswered questions
- follow-ups I owe
- follow-ups other people own
Flag anything private that doesn't belong in a shared meeting doc.

## Related use cases

[![](/codex/use-cases/new-hire-onboarding.webp)

### Coordinate new-hire onboarding

Use Codex to gather approved new-hire context, stage tracker updates, draft team-by-team...

Integrations  Data](/codex/use-cases/new-hire-onboarding)[![](/codex/use-cases/draft-prds-from-sources.webp)

### Draft PRDs from internal context

Use Codex with the $documents skill and connected apps such as Linear, Slack, Notion or...

Integrations  Knowledge Work](/codex/use-cases/draft-prds-from-sources)[![](/codex/use-cases/event-launch-playbooks.webp)

### Run event playbooks

Use Codex with Slack, Google Drive, and Calendar to gather planning context, draft...

Integrations  Knowledge Work](/codex/use-cases/event-launch-playbooks)

