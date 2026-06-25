---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/manage-your-inbox'
source_last_modified: '2026-06-05T16:52:48Z'
source_etag: 'W/"17607cd2d64b72c26fc665b69fb91c3a"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2"]
---

# Manage your inbox | Codex use cases

Source: https://developers.openai.com/codex/use-cases/manage-your-inbox

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Manage your inbox

Have Codex find the emails that matter and write the replies in your voice.

Difficulty **Easy**

Time horizon **5m**

Use Codex with Gmail to find emails that need attention, draft responses in your voice, pull context from the tools where your work happens, and keep watching for new replies on a schedule.

## Best for

- People who want Codex to find emails that need attention instead of manually sorting them.
- Recurring inbox checks where Codex can create reviewable drafts in the background.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/manage-your-inbox/?export=pdf)

Use Codex with Gmail to find emails that need attention, draft responses in your voice, pull context from the tools where your work happens, and keep watching for new replies on a schedule.

Easy

5m

Related links

[Codex plugins](/codex/plugins)  [Codex automations](/codex/app/automations)

## Best for

- People who want Codex to find emails that need attention instead of manually sorting them.
- Recurring inbox checks where Codex can create reviewable drafts in the background.

## Skills & Plugins

- [Gmail](https://github.com/openai/plugins/tree/main/plugins/gmail)

  Search and triage Gmail threads, read the surrounding conversation, create reply drafts, and organize messages when you explicitly ask.
- [Slack](https://github.com/openai/plugins/tree/main/plugins/slack)

  Check team-message context when an email needs the latest decision, owner, asset, or blocker.
- [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive)

  Read source docs, FAQs, notes, or approved writing examples that should shape the draft.

| Skill | Why use it |
| --- | --- |
| [Gmail](https://github.com/openai/plugins/tree/main/plugins/gmail) | Search and triage Gmail threads, read the surrounding conversation, create reply drafts, and organize messages when you explicitly ask. |
| [Slack](https://github.com/openai/plugins/tree/main/plugins/slack) | Check team-message context when an email needs the latest decision, owner, asset, or blocker. |
| [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive) | Read source docs, FAQs, notes, or approved writing examples that should shape the draft. |

## Starter prompt

Can you check my @gmail, figure out what I need to respond to, and write drafts in my voice.
Use my recent sent replies or @google-drive [writing examples] for tone.
Use @slack, @google-drive, or other sources where my work happens when the email is missing the latest decision, owner, file, or blocker.

Open in the Codex app

Can you check my @gmail, figure out what I need to respond to, and write drafts in my voice.
Use my recent sent replies or @google-drive [writing examples] for tone.
Use @slack, @google-drive, or other sources where my work happens when the email is missing the latest decision, owner, file, or blocker.

## Review your inbox

Ask Codex to check Gmail, find the messages that deserve a reply, and write drafts in your voice. It can use recent sent mail or approved writing examples for style, then search Slack, docs, project notes, or other tools when the email lacks context on its own.

Use Codex for the first pass over your inbox: find the emails that need your attention, draft the replies, and bring in the work context that explains the bigger picture.

1. Ask Codex to review Gmail for emails that need your attention.
2. Ask it to use Slack, docs, or project notes for context that explains the bigger picture.
3. Tell Codex which drafts were useful and which emails it should ignore next time.
4. Add an automation when the thread is useful, and pin it if you want fast access later.

Use the Gmail plugin directly. You can give Codex a broad inbox request, a time window, or a label if you already know the scope. If tone matters, ask Codex to look at recent sent replies or a doc with examples before drafting.

Use the starter prompt on this page for the first inbox pass. Codex should return a short queue: drafts for emails that need attention, messages that can wait, and the context it used when the answer depended on more than the email thread.

## Let the thread learn your taste

Treat the first pass like calibration. If Codex drafts too many replies, tell it which emails were noise. If it misses something important, tell it why that thread mattered. If the tone is off, correct the draft directly.

Good start. For future passes:
- draft replies for [the kinds of emails that matter]
- ignore [newsletters, FYIs, calendar churn, or other noise]
- sound more like [shorter, warmer, more direct, or less formal]
- use @slack for context when a thread mentions [project, account, or team]

Over time, the thread should get better at deciding what needs a draft and what can stay out of your way.

## Automate email triage on a schedule

You can create automations to run a scheduled check-in on the same thread. Codex wakes up, checks Gmail and the context sources you named, and posts only when there are emails that need your attention or drafts worth reviewing.

Once the drafts look useful, ask Codex to keep an eye on Gmail. Email triage is a good job to automate: the drafts are reviewable, and you still decide what gets sent.

Can you keep an eye on my @gmail and create drafts for emails that need my attention?
Check [hourly, every weekday morning, or at 4 PM].
Use @slack or @google-drive for context when needed. Skip obvious noise. Do not send anything.

Use this with Codex [automations](/codex/app/automations) after the thread has a good sense of your reply patterns. If Codex finds an email that needs a decision it cannot make, it should flag the question instead of guessing.

## Organize your inbox

The Gmail plugin can also help organize your inbox. Keep that as a separate command after you trust the triage.

Archive or label the low-priority emails from this pass.
Only touch the messages you listed as [can wait, newsletter, or already handled].
Do not delete or send anything.

For deletion, make the instruction explicit and narrow. Drafting replies is safe to automate for review; destructive cleanup should stay deliberate.

## Related use cases

[![](/codex/use-cases/slack-action-triage.webp)

### Prioritize Slack action items

Use Codex with Slack and the tools where work happens to find direct asks, implicit...

Automation  Integrations](/codex/use-cases/slack-action-triage)[![](/codex/use-cases/proactive-teammate.webp)

### Set up a teammate

Connect the tools where work happens, teach one thread what matters, then add an automation...

Automation  Integrations](/codex/use-cases/proactive-teammate)[![](/codex/use-cases/zoom-meeting-follow-ups.webp)

### Turn meetings into follow-ups

Use Codex with Zoom transcripts and AI Companion summaries to draft customer follow-up...

Automation  Integrations](/codex/use-cases/zoom-meeting-follow-ups)

