---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/update-documentation'
source_last_modified: '2026-06-05T18:37:22Z'
source_etag: 'W/"4656d2dac964add0470235c4869fc614"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2"]
---

# Keep documentation up-to-date | Codex use cases

Source: https://developers.openai.com/codex/use-cases/update-documentation

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Keep documentation up-to-date

Use code and other sources to automate docs updates.

Difficulty **Easy**

Time horizon **30m**

Use Codex to compare source code changes, public docs, release notes, and PR context, then draft focused documentation updates with verification steps before publishing.

## Best for

- Developer docs, READMEs, runbooks, examples, and migration notes that need to track behavior that changes frequently.
- Teams that maintain documentation for a technical product.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/update-documentation/?export=pdf)

Use Codex to compare source code changes, public docs, release notes, and PR context, then draft focused documentation updates with verification steps before publishing.

Easy

30m

Related links

[Workflows](/codex/workflows)

## Best for

- Developer docs, READMEs, runbooks, examples, and migration notes that need to track behavior that changes frequently.
- Teams that maintain documentation for a technical product.

## Skills & Plugins

- [GitHub](https://github.com/openai/plugins/tree/main/plugins/github)

  Read issues, pull requests, comments, review threads, and failed checks when GitHub is part of your bug intake.

| Skill | Why use it |
| --- | --- |
| [GitHub](https://github.com/openai/plugins/tree/main/plugins/github) | Read issues, pull requests, comments, review threads, and failed checks when GitHub is part of your bug intake. |

## Starter prompt

Update the [product/feature] documentation based on the following sources:
- the changed source files in [this repo/source linked repo]
- the existing docs pages that mention a new behavior
- any linked issue, PR, release note, or public reference I provide below
Then:
- identify what is user-facing
- update only the docs that need to change
- keep unpublished roadmap, private customer details, and internal-only context out of public docs
- preserve the existing docs structure, terminology, and cross-links
- run the docs checks that fit the change
Before finalizing, summarize what changed, what you verified, and any claims you could not prove from trusted sources.
[link release notes or other references here]

Open in the Codex app

Update the [product/feature] documentation based on the following sources:
- the changed source files in [this repo/source linked repo]
- the existing docs pages that mention a new behavior
- any linked issue, PR, release note, or public reference I provide below
Then:
- identify what is user-facing
- update only the docs that need to change
- keep unpublished roadmap, private customer details, and internal-only context out of public docs
- preserve the existing docs structure, terminology, and cross-links
- run the docs checks that fit the change
Before finalizing, summarize what changed, what you verified, and any claims you could not prove from trusted sources.
[link release notes or other references here]

## Introduction

Documentation is easiest to keep current when it is updated alongside source changes, not weeks later. Codex can inspect changed code, tests, release notes, linked issues, and pull request context, then draft a scoped docs update that matches the existing structure.

Use this workflow for developer docs, README updates, changelog drafts, migration notes, runbooks, or anything else that needs to track behavior that changes frequently.

## How to use

1. Start from the change you need to document.

   Share the branch, pull request, commit, issue, or files. If the docs are public, say explicitly that unpublished roadmap, private customer details, and internal-only context should stay out.
2. Ask Codex to map the affected docs.

   Have it search existing docs for feature names, config keys, commands, examples, and related terms before drafting.
3. Update the smallest useful docs surface.

   Codex should preserve the current page structure, terminology, cross-links, and frontmatter. It should avoid broad rewrites when a precise note, example, or section update is enough.
4. Verify the changes.

   Ask Codex to run formatting and docs checks that fit the repo, then summarize the evidence behind each user-facing claim.

## What to give Codex

| Source | Why it helps |
| --- | --- |
| Changed code and tests | Lets Codex analyze actual behavior to draft focused documentation updates. |
| Public release notes or product docs | Helps Codex match public terminology, availability, and feature status. |
| Pull request or issue context | Explains why the change happened and which user-facing behavior matters. |
| Local docs checks | Gives Codex a concrete definition of done before the docs are published. |

Adding more context such as public release notes lets Codex avoid including private context or updates that are not yet public.

## Make the workflow repeatable

For a repo-wide convention, add documentation expectations to [AGENTS.md](/codex/guides/agents-md). For example:

```
## Documentation

- When user-facing behavior changes, check whether docs, examples, or changelogs need updates.
- Public docs must only include public information or behavior visible in this repo.
- Preserve existing terminology and frontmatter.
- Run the docs formatting and build checks before final handoff.
```

If the process has more steps, turn it into a [skill](/codex/skills) so future Codex threads can follow the same source-checking, drafting, and verification loop. See [Save workflows as skills](/codex/use-cases/reusable-codex-skills) that shares more details on this pattern.

You can also turn this workflow into a [thread automation](/codex/app/automations#thread-automations) by asking Codex to run it on a schedule, asking to fetch all the recent PRs from GitHub to automatically keep docs up-to-date, for example on a weekly basis:

Create an automation that does the same as the workflow above, fetching all the recent PRs in [this repo/linked repo] and update docs based on the changes.

## Related use cases

[![](/codex/use-cases/agent-friendly-clis.webp)

### Create a CLI Codex can use

Ask Codex to create a composable CLI it can run from any folder, combine with repo scripts...

Engineering  Code](/codex/use-cases/agent-friendly-clis)[![](/codex/use-cases/browser-games.webp)

### Create browser-based games

Use Codex to turn a game brief into first a well-defined plan, and then a real browser-based...

Engineering  Code](/codex/use-cases/browser-games)[![](/codex/use-cases/follow-goals.webp)

### Follow a goal

Use `/goal` when a task needs Codex to keep working across turns toward a verifiable...

Engineering  Automation](/codex/use-cases/follow-goals)

