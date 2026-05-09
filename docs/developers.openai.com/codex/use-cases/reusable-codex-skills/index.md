---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/reusable-codex-skills'
source_last_modified: '2026-05-08T00:47:36Z'
source_etag: 'W/"f17c8c949220c101509162262bec7c07"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0"]
---

# Save workflows as skills | Codex use cases

Source: https://developers.openai.com/codex/use-cases/reusable-codex-skills

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Save workflows as skills

Create a skill Codex can keep on hand for work you repeat.

Difficulty **Easy**

Time horizon **5m**

Turn a working Codex thread, review rules, test commands, release checklists, design conventions, writing examples, or repo-specific scripts into a skill Codex can use in future threads.

## Best for

- Codified workflows you want Codex to use again.
- Teams that want a reusable skill instead of a long prompt pasted into every thread.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/reusable-codex-skills/?export=pdf)

Turn a working Codex thread, review rules, test commands, release checklists, design conventions, writing examples, or repo-specific scripts into a skill Codex can use in future threads.

Easy

5m

Related links

[Agent skills](/codex/skills)

## Best for

- Codified workflows you want Codex to use again.
- Teams that want a reusable skill instead of a long prompt pasted into every thread.

## Skills & Plugins

- [Skill Creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)

  Gather information about the workflow, scaffold a skill, keep the main instructions short, and validate the result.

| Skill | Why use it |
| --- | --- |
| [Skill Creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | Gather information about the workflow, scaffold a skill, keep the main instructions short, and validate the result. |

## Starter prompt

Use $skill-creator to create a Codex skill that [fixes failing Buildkite checks on a GitHub PR / turns PR notes into inline review comments / writes our release notes from merged PRs]
Use these sources when creating the skill:
- Working example: [say "use this thread," link a merged PR, or paste a good Codex answer]
- Source: [paste a Slack thread, PR review link, runbook URL, docs URL, or ticket]
- Repo: [repo path, if this skill depends on one repo]
- Scripts or commands to reuse: [test command], [preview command], [log-fetch script], [release command]
- Good output: [paste the Slack update, changelog entry, review comment, ticket, or final answer you want future threads to match]

[Open in the Codex app](codex://new?prompt=Use+%24skill-creator+to+create+a+Codex+skill+that+%5Bfixes+failing+Buildkite+checks+on+a+GitHub+PR+%2F+turns+PR+notes+into+inline+review+comments+%2F+writes+our+release+notes+from+merged+PRs%5D%0A%0AUse+these+sources+when+creating+the+skill%3A%0A-+Working+example%3A+%5Bsay+%22use+this+thread%2C%22+link+a+merged+PR%2C+or+paste+a+good+Codex+answer%5D%0A-+Source%3A+%5Bpaste+a+Slack+thread%2C+PR+review+link%2C+runbook+URL%2C+docs+URL%2C+or+ticket%5D%0A-+Repo%3A+%5Brepo+path%2C+if+this+skill+depends+on+one+repo%5D%0A-+Scripts+or+commands+to+reuse%3A+%5Btest+command%5D%2C+%5Bpreview+command%5D%2C+%5Blog-fetch+script%5D%2C+%5Brelease+command%5D%0A-+Good+output%3A+%5Bpaste+the+Slack+update%2C+changelog+entry%2C+review+comment%2C+ticket%2C+or+final+answer+you+want+future+threads+to+match%5D "Open in the Codex app")

Use $skill-creator to create a Codex skill that [fixes failing Buildkite checks on a GitHub PR / turns PR notes into inline review comments / writes our release notes from merged PRs]
Use these sources when creating the skill:
- Working example: [say "use this thread," link a merged PR, or paste a good Codex answer]
- Source: [paste a Slack thread, PR review link, runbook URL, docs URL, or ticket]
- Repo: [repo path, if this skill depends on one repo]
- Scripts or commands to reuse: [test command], [preview command], [log-fetch script], [release command]
- Good output: [paste the Slack update, changelog entry, review comment, ticket, or final answer you want future threads to match]

## Create a skill Codex can keep on hand

Use skills to give Codex reusable instructions, resources, and scripts for work you repeat. A [skill](/codex/skills) can preserve the thread, doc, command, or example that made Codex useful the first time.

Start with one working example: a Codex thread that cherry-picked a PR, a release checklist from Notion, a set of useful PR comments, or a Slack thread explaining a launch process.

## How to use

1. Add the context you want Codex to use.

   Stay in the Codex thread you want to preserve, paste the Slack thread or docs link, and add the rule, command, or example Codex should remember.
2. Run the starter prompt.

   The prompt names the skill you want, then gives `$skill-creator` the thread, doc, PR, command, or output to preserve.
3. Let Codex create and validate the skill.

   The result should define the `$skill-name`, describe when it should trigger, and keep reusable instructions in the right place.

   Skills in `~/.codex/skills` are available from any repo. Skills in the current repo can be committed so teammates can use them too.
4. Use the skill, then update it from the thread.

   Invoke the new `$skill-name` on the next PR, alert, review, release note, or design task. If it uses the wrong test command, misses a review rule, skips a runbook step, or writes a draft you would not send, ask Codex to add that correction to the skill.

## Provide source material

Give `$skill-creator` the material that explains how the skill should work.

| What you have | What to add |
| --- | --- |
| **A workflow from a Codex thread that you want to preserve** | Stay in that thread and say `use this thread`. Codex can use the conversation, commands, edits, and feedback from that thread as the starting point. |
| **Docs or a runbook** | Paste the release checklist, link the incident-response runbook, attach the API PDF, or point Codex at the markdown guide in your repo. |
| **Team conversation** | Paste the Slack thread where someone explained an alert, link the PR review with frontend rules, or attach the support conversation that explains the customer problem. |
| **Scripts or commands the skill should reuse** | Add the test command, preview command, release script, log-fetch script, or local helper command you want future Codex threads to run. |
| **A good result** | Add the merged PR, final changelog entry, accepted launch note, resolved ticket, before/after screenshot, or final Codex answer you want future threads to match. |

If the source is in Slack, Linear, GitHub, Notion, or Sentry, connect that tool in Codex with a [plugin](/codex/plugins), mention it in the starter prompt, or paste the relevant part into the thread.

## What Codex creates

Most skills start as a `SKILL.md` file. `$skill-creator` can add longer references, scripts, or assets when the workflow needs them.

- my-skill/

  - SKILL.md    Required: instructions and metadata
  - references/    Optional: longer docs
  - scripts/    Optional: repeatable commands
  - assets/    Optional: templates and starter files

## Skills you could create

Use the same pattern when future threads should read the same runbook, run the same CLI, follow the same review rubric, write the same team update, or QA the same browser flow. For example:

- **`$buildkite-fix-ci`** downloads failed job logs, diagnoses the error, and proposes the smallest code fix.
- **`$fix-merge-conflicts`** checks out a GitHub PR, updates it against the base branch, resolves conflicts, and returns the exact push command.
- **`$frontend-skill`** keeps Codex close to your UI taste, existing components, screenshot QA loop, asset choices, and browser polish pass.
- **`$pr-review-comments`** turns review notes into concise inline comments with the right tone and GitHub links.
- **`$web-game-prototyper`** scopes the first playable loop, chooses assets, tunes game feel, captures screenshots, and polishes in the browser.

## Related use cases

[![](/images/codex/codex-wallpaper-3.webp)

### Follow a goal

Use `/goal` when a task needs Codex to keep working across turns toward a verifiable...

Engineering  Automation](/codex/use-cases/follow-goals)[![](/images/codex/codex-wallpaper-3.webp)

### Add evals to your AI application

Ask Codex to inspect your AI application, identify the behavior you want to evaluate, and...

Evaluation  Quality](/codex/use-cases/ai-app-evals)[![](/images/codex/codex-wallpaper-1.webp)

### Build React Native apps with Expo

Use Codex with the Expo plugin to scaffold React Native apps, stay inside Expo Router and...

Mobile  Engineering](/codex/use-cases/react-native-expo-apps)

