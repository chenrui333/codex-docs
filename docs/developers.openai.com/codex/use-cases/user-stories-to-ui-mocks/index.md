---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/user-stories-to-ui-mocks'
source_last_modified: '2026-06-03T19:26:53Z'
source_etag: 'W/"9eb9fb927c05352893468b9894dcd6ce"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0"]
---

# Turn user stories into UI mocks | Codex use cases

Source: https://developers.openai.com/codex/use-cases/user-stories-to-ui-mocks

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Turn user stories into UI mocks

Convert product feedback, issue threads, and design context into mockups your team can react to and implement.

Difficulty **Easy**

Time horizon **30m**

Use Codex to gather product feedback from Slack, Linear, Google Drive, normalize it into user stories and constraints, then generate UI mockups with ImageGen. When the direction is chosen, turn the mock into a working prototype.

## Best for

- Product teams turning scattered feedback into a visual direction for a feature.
- Design and engineering teams that want mockups grounded in source material before building.
- Teams who want to iterate fast based on user feedback.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/user-stories-to-ui-mocks/?export=pdf)

Use Codex to gather product feedback from Slack, Linear, Google Drive, normalize it into user stories and constraints, then generate UI mockups with ImageGen. When the direction is chosen, turn the mock into a working prototype.

Easy

30m

Related links

[Codex plugins](/codex/plugins)

## Best for

- Product teams turning scattered feedback into a visual direction for a feature.
- Design and engineering teams that want mockups grounded in source material before building.
- Teams who want to iterate fast based on user feedback.

## Skills & Plugins

- [Slack](https://github.com/openai/plugins/tree/main/plugins/slack)

  Search approved feedback channels and threads for user stories, pain points, quotes, and open questions.
- [Linear](https://github.com/openai/plugins/tree/main/plugins/linear)

  Pull feature requests, bug reports, labels, priorities, and project context into the mock brief.
- [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive)

  Read research notes, call summaries, docs, sheets, and slides that contain product feedback or design requirements.
- [Figma](https://github.com/openai/plugins/tree/main/plugins/figma)

  Fetch design context, screenshots, and design-system references so mocks do not drift away from the product's visual language.
- ImageGen

  Generate UI mockups, variations, and visual truth from the synthesized stories and design constraints.
- [Build Web Apps](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)

  Turn the selected mock into a working web prototype and verify the implementation against the mock.

| Skill | Why use it |
| --- | --- |
| [Slack](https://github.com/openai/plugins/tree/main/plugins/slack) | Search approved feedback channels and threads for user stories, pain points, quotes, and open questions. |
| [Linear](https://github.com/openai/plugins/tree/main/plugins/linear) | Pull feature requests, bug reports, labels, priorities, and project context into the mock brief. |
| [Google Drive](https://github.com/openai/plugins/tree/main/plugins/google-drive) | Read research notes, call summaries, docs, sheets, and slides that contain product feedback or design requirements. |
| [Figma](https://github.com/openai/plugins/tree/main/plugins/figma) | Fetch design context, screenshots, and design-system references so mocks do not drift away from the product's visual language. |
| ImageGen | Generate UI mockups, variations, and visual truth from the synthesized stories and design constraints. |
| [Build Web Apps](https://github.com/openai/plugins/tree/main/plugins/build-web-apps) | Turn the selected mock into a working web prototype and verify the implementation against the mock. |

## Starter prompt

Turn this [user story/set of user feedbacks] into a UI mock for a feature that would solve the problem, using these sources as context:
- @slack [channels or thread links]
- @linear [issue links, project, team, or view]
- @google-drive [research notes, survey export, doc, sheet, or slide deck]
Do that while respecting the current design system and existing UI [provide Figma file or screenshot as reference].

[Open in the Codex app](codex://threads/new?prompt=Turn+this+%5Buser+story%2Fset+of+user+feedbacks%5D+into+a+UI+mock+for+a+feature+that+would+solve+the+problem%2C+using+these+sources+as+context%3A%0A-+%40slack+%5Bchannels+or+thread+links%5D%0A-+%40linear+%5Bissue+links%2C+project%2C+team%2C+or+view%5D%0A-+%40google-drive+%5Bresearch+notes%2C+survey+export%2C+doc%2C+sheet%2C+or+slide+deck%5D%0A%0ADo+that+while+respecting+the+current+design+system+and+existing+UI+%5Bprovide+Figma+file+or+screenshot+as+reference%5D. "Open in the Codex app")

Turn this [user story/set of user feedbacks] into a UI mock for a feature that would solve the problem, using these sources as context:
- @slack [channels or thread links]
- @linear [issue links, project, team, or view]
- @google-drive [research notes, survey export, doc, sheet, or slide deck]
Do that while respecting the current design system and existing UI [provide Figma file or screenshot as reference].

## Introduction

Product teams often collect feedback from various sources, such as Slack threads, Linear issues, Google Drive docs or sheets, or customer-call notes. Sometimes, they have clear user stories illustrating a problem they want to solve, and sometimes, the context lives in those sources.

Codex can gather this context and turn it into a UI mock for a feature that would solve the problem, and once validated, can be implemented into the product.

## Generate visual truth

If you have a clear user story, you can start with that. If not, you can have a discussion with Codex first, gathering context from different sources and synthesizing it into a user story.

Then, you can ask Codex to use ImageGen to create a few mock directions. The mocks should preserve the product’s information architecture and design-system constraints.

If helpful, you can provide screenshots of the current UI or a Figma file as reference.

Do this until you are satisfied with the mock. The more scoped the changes are, the more likely Codex is to generate a mock that can be implemented directly.

## Move from mock to prototype

Use the final mock image that you want Codex to implement. Re-attach this image in a new turn rather than continuing the conversation directly.
You can then ask Codex to implement the mock – optionally using the [Build Web Apps plugin](/codex/plugins/build-web-apps) if you’re building a web app – to turn it into a working prototype:

Use this image as a reference and implement in this repository this feature. Use this conversation as context to help you implement it with the right constraints. Minimize the creation of new components: explore the codebase and reuse existing components and design system when possible.

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

