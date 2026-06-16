---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/draft-prds-from-sources'
source_last_modified: '2026-06-05T16:59:08Z'
source_etag: 'W/"21cb53f838433e5cf3a536a36cf8b11e"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0"]
---

# Draft PRDs from internal context | Codex use cases

Source: https://developers.openai.com/codex/use-cases/draft-prds-from-sources

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Draft PRDs from internal context

Create product requirements documents from Linear, Slack, source documents, and meeting notes.

Difficulty **Easy**

Time horizon **30m**

Use Codex with the $documents skill and connected apps such as Linear, Slack, Notion or Google Drive to create a reviewable PRD with the expected sections, a timeline, decisions, open questions, and a source appendix.

## Best for

- Product teams turning planning context into a PRD, proposal, launch brief, or decision memo.
- PMs who need to draft a PRD quickly after aligning with the team in internal discussions.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/draft-prds-from-sources/?export=pdf)

Use Codex with the $documents skill and connected apps such as Linear, Slack, Notion or Google Drive to create a reviewable PRD with the expected sections, a timeline, decisions, open questions, and a source appendix.

Easy

30m

Related links

[Codex plugins](/codex/plugins)  [Agent skills](/codex/skills)  [Codex app](/codex/app)

## Best for

- Product teams turning planning context into a PRD, proposal, launch brief, or decision memo.
- PMs who need to draft a PRD quickly after aligning with the team in internal discussions.

## Skills & Plugins

- Documents

  Create, edit, and verify a DOCX when the PRD should become a polished file instead of chat text.
- [Slack](https://github.com/openai/plugins/tree/main/plugins/slack)

  Read product discussions, launch threads, decision notes, and follow-up questions from approved channels or thread links.
- [Linear](https://github.com/openai/plugins/tree/main/plugins/linear)

  Read projects, issues, priorities, acceptance criteria, and open work that should shape the PRD.
- [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive)

  Read planning docs, research notes, specs, exported meeting notes, and source folders.
- [Notion](https://github.com/openai/plugins/tree/main/plugins/notion)

  Read roadmap pages, project notes, meeting notes, and team wikis that should shape the PRD.

| Skill | Why use it |
| --- | --- |
| Documents | Create, edit, and verify a DOCX when the PRD should become a polished file instead of chat text. |
| [Slack](https://github.com/openai/plugins/tree/main/plugins/slack) | Read product discussions, launch threads, decision notes, and follow-up questions from approved channels or thread links. |
| [Linear](https://github.com/openai/plugins/tree/main/plugins/linear) | Read projects, issues, priorities, acceptance criteria, and open work that should shape the PRD. |
| [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive) | Read planning docs, research notes, specs, exported meeting notes, and source folders. |
| [Notion](https://github.com/openai/plugins/tree/main/plugins/notion) | Read roadmap pages, project notes, meeting notes, and team wikis that should shape the PRD. |

## Starter prompt

Use $documents to create a PRD for [feature or product area] from @linear [project or milestone], @slack [channel or thread], and @google-drive or @notion [planning docs, research notes, meeting notes, or source folder].
Include the problem, users, goals/non-goals, requirements, UX, technical considerations, metrics, launch plan, risks, open questions, decisions, timeline, and source appendix.
Cite the sources behind requirement-level claims. If sources disagree, call out the conflict instead of choosing silently. Draft only. Do not post, update Linear, or share the document until I approve it.

Open in the Codex app

Use $documents to create a PRD for [feature or product area] from @linear [project or milestone], @slack [channel or thread], and @google-drive or @notion [planning docs, research notes, meeting notes, or source folder].
Include the problem, users, goals/non-goals, requirements, UX, technical considerations, metrics, launch plan, risks, open questions, decisions, timeline, and source appendix.
Cite the sources behind requirement-level claims. If sources disagree, call out the conflict instead of choosing silently. Draft only. Do not post, update Linear, or share the document until I approve it.

## Introduction

Before working on a new product or feature, it’s common to draft a product requirements document (PRD) to align on the scope and requirements. Most often than not, the context needed to write that PRD is already available in the team’s internal systems: tickets on Linear, discussions on Slack, drafts in Notion or Google Drive, etc. Codex can gather this context and draft a PRD that you can review and iterate on, while keeping the source trail visible.

[
Your browser does not support the video tag.
](https://cdn.openai.com/codex/docs/developers-website/use-cases/draft-prds-from-slack-linear-docs.mp4)

## Choose the sources

Start with the sources you want Codex to use: the Linear project, the Slack planning channel or thread, and any Drive docs, Notion pages, meeting notes, or local files that should be cited in the PRD.
You should also clearly outline the PRD sections you expect, such as the problem, users, requirements, UX, tech, launch plan, timeline, or decisions.

1. Start with `$documents` when the output should be a real DOCX.
2. Name the sources directly: the Linear project or milestone, the Slack channel or thread, and the docs or notes Codex should cite.
3. Give Codex the PRD section contract.
4. Review the source appendix first, then the requirements and open questions.
5. Use the same thread to resolve gaps, tighten scope, and prepare the handoff.

## Refine in the same thread

Use the starter prompt on this page for the first draft. If something is missing, point Codex at the missing source instead of starting over.

## Check the source trail

Before sharing the PRD, ask Codex to list the claims with weak or missing support, the unresolved questions, and the decisions it treated as confirmed. If the source appendix does not make those easy to audit, keep refining the same thread before exporting or posting anything.

### Suggested prompt

**Check the Source Trail**

Before I share this PRD, check the source trail.
List:
- requirements with weak or missing source support
- open questions that still need an owner or decision
- decisions you treated as confirmed
- any claims that should move out of the PRD and into open questions
Keep the source appendix linked and easy to audit.

## Related use cases

[![](/codex/use-cases/new-hire-onboarding.webp)

### Coordinate new-hire onboarding

Use Codex to gather approved new-hire context, stage tracker updates, draft team-by-team...

Integrations  Data](/codex/use-cases/new-hire-onboarding)[![](/codex/use-cases/meeting-prep-briefs.webp)

### Prepare meeting briefs

Use Codex with Calendar, Drive, Slack, and Gmail to gather approved sources before a...

Integrations  Knowledge Work](/codex/use-cases/meeting-prep-briefs)[![](/codex/use-cases/event-launch-playbooks.webp)

### Run event playbooks

Use Codex with Slack, Google Drive, and Calendar to gather planning context, draft...

Integrations  Knowledge Work](/codex/use-cases/event-launch-playbooks)

