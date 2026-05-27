---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/event-launch-playbooks'
source_last_modified: '2026-05-22T16:26:28Z'
source_etag: 'W/"eda411c5c4b239940f633c1ee1956a3b"'
codex_cli_versions: ["0.131.0", "0.132.0", "0.133.0", "0.134.0"]
codex_cli_versions_raw: ["codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0"]
---

# Run event playbooks | Codex use cases

Source: https://developers.openai.com/codex/use-cases/event-launch-playbooks

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Run event playbooks

Create repeatable workflows for event program management.

Difficulty **Intermediate**

Time horizon **1h**

Use Codex with Slack, Google Drive, and Calendar to gather planning context, draft attendee-facing copy, and prepare a private checklist with owners, approvals, and open questions.

## Best for

- Community, developer relations, marketing, and operations teams running events.
- Event pages, handoffs, and launch checklists where public copy and private operations need to stay separate.
- Recurring event programs that need source-backed templates, owners, approvals, and open questions.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/event-launch-playbooks/?export=pdf)

Use Codex with Slack, Google Drive, and Calendar to gather planning context, draft attendee-facing copy, and prepare a private checklist with owners, approvals, and open questions.

Intermediate

1h

Related links

[Codex plugins](/codex/plugins)  [Codex automations](/codex/app/automations)  [Use Codex in Slack](/codex/integrations/slack)

## Best for

- Community, developer relations, marketing, and operations teams running events.
- Event pages, handoffs, and launch checklists where public copy and private operations need to stay separate.
- Recurring event programs that need source-backed templates, owners, approvals, and open questions.

## Skills & Plugins

- [Slack](https://github.com/openai/plugins/tree/main/plugins/slack)

  Read planning channels, threads, canvases, and decisions that define the current event scope.
- [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive)

  Gather approved templates, event docs, decks, recap notes, and launch assets.
- [Google Calendar](https://github.com/openai/plugins/tree/main/plugins/google-calendar)

  Check event timing, deadlines, and meeting context while building the playbook.
- Sheets

  Track tasks, owners, and deadlines in a structured format.

| Skill | Why use it |
| --- | --- |
| [Slack](https://github.com/openai/plugins/tree/main/plugins/slack) | Read planning channels, threads, canvases, and decisions that define the current event scope. |
| [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive) | Gather approved templates, event docs, decks, recap notes, and launch assets. |
| [Google Calendar](https://github.com/openai/plugins/tree/main/plugins/google-calendar) | Check event timing, deadlines, and meeting context while building the playbook. |
| Sheets | Track tasks, owners, and deadlines in a structured format. |

## Starter prompt

Create a source-backed playbook for [event].
Sources to use:
- planning channels or threads: [links or names]
- approved docs, decks, sheets, or templates: [links or names]
- calendar events or deadlines: [links or dates]
Split the output into:
- attendee-facing copy
- private operating checklist
- owner map
- support plan or resources
- approvals still needed
- open questions
- source appendix
Do not publish anything or assume missing details. Put unknowns in open questions and keep private operations out of the public copy.

[Open in the Codex app](codex://threads/new?prompt=Create+a+source-backed+playbook+for+%5Bevent%5D.%0A%0ASources+to+use%3A%0A-+planning+channels+or+threads%3A+%5Blinks+or+names%5D%0A-+approved+docs%2C+decks%2C+sheets%2C+or+templates%3A+%5Blinks+or+names%5D%0A-+calendar+events+or+deadlines%3A+%5Blinks+or+dates%5D%0A%0ASplit+the+output+into%3A%0A-+attendee-facing+copy%0A-+private+operating+checklist%0A-+owner+map%0A-+support+plan+or+resources%0A-+approvals+still+needed%0A-+open+questions%0A-+source+appendix%0A%0ADo+not+publish+anything+or+assume+missing+details.+Put+unknowns+in+open+questions+and+keep+private+operations+out+of+the+public+copy. "Open in the Codex app")

Create a source-backed playbook for [event].
Sources to use:
- planning channels or threads: [links or names]
- approved docs, decks, sheets, or templates: [links or names]
- calendar events or deadlines: [links or dates]
Split the output into:
- attendee-facing copy
- private operating checklist
- owner map
- support plan or resources
- approvals still needed
- open questions
- source appendix
Do not publish anything or assume missing details. Put unknowns in open questions and keep private operations out of the public copy.

## Introduction

When you have event programs to manage, for example our [Codex community meetups](/community/meetups), you often have context scattered across multiple sources:

- The public event page
- The program support plan
- Slack messages
- Sheets or documents
- etc.

You can use Codex to gather the approved planning sources and turn them into a playbook that separates attendee-facing copy from private operating details.

## Create your first playbook

Use the starter prompt to ask Codex to generate an event playbook for you. It should:

- Name planning sources (these could be links, internal tools, etc.)
- List required information
- Define rules for attendee-facing copy (keeping internal logistics out of it)

You should get a list of things to check and run every time a new event is planned.

## Run the playbook as an automation

After the first run of your new playbook works, keep the same thread open and ask Codex to run it as a scheduled automation.

Review the new event requests.
Check:
- attendee-facing copy has no private logistics, budget notes, or internal-only partner context
- asks are in line with the event program
And give me a draft for follow up questions/checks I could send.

## Related use cases

[![](/codex/use-cases/new-hire-onboarding.webp)

### Coordinate new-hire onboarding

Use Codex to gather approved new-hire context, stage tracker updates, draft team-by-team...

Integrations  Data](/codex/use-cases/new-hire-onboarding)[![](/codex/use-cases/draft-prds-from-sources.webp)

### Draft PRDs from internal context

Use Codex with the $documents skill and connected apps such as Linear, Slack, Notion or...

Integrations  Knowledge Work](/codex/use-cases/draft-prds-from-sources)[![](/codex/use-cases/meeting-prep-briefs.webp)

### Prepare meeting briefs

Use Codex with Calendar, Drive, Slack, and Gmail to gather approved sources before a...

Integrations  Knowledge Work](/codex/use-cases/meeting-prep-briefs)

