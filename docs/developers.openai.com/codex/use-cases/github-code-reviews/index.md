---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/github-code-reviews'
source_last_modified: '2026-06-02T19:22:02Z'
source_etag: 'W/"8260163f5bff0c5848bdc4a705329f28"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0"]
---

# Review GitHub pull requests | Codex use cases

Source: https://developers.openai.com/codex/use-cases/github-code-reviews

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Review GitHub pull requests

Catch regressions and potential issues before human review.

Difficulty **Easy**

Time horizon **5s**

Use Codex code review in GitHub to automatically surface regressions, missing tests, and documentation issues directly on a pull request.

## Best for

- Teams that want another review signal before human merge approval
- Large codebases for projects in production

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/github-code-reviews/?export=pdf)

Use Codex code review in GitHub to automatically surface regressions, missing tests, and documentation issues directly on a pull request.

Easy

5s

Related links

[Codex code review in GitHub](/codex/integrations/github)  [Custom instructions with AGENTS.md](/codex/guides/agents-md)

## Best for

- Teams that want another review signal before human merge approval
- Large codebases for projects in production

## Skills & Plugins

- [Security Best Practices](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices)

  Focus the review on risky surfaces such as secrets, auth, and dependency changes.

| Skill | Why use it |
| --- | --- |
| [Security Best Practices](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) | Focus the review on risky surfaces such as secrets, auth, and dependency changes. |

## Starter prompt

@codex review for security regressions, missing tests, and risky behavior changes.

@codex review for security regressions, missing tests, and risky behavior changes.

## How to use

Start by adding Codex code review to your GitHub organization or repository.
See [Codex code review in GitHub](/codex/integrations/github) for more details.

You can set up Codex to automatically review every pull request, or you can request a review with `@codex review` in a pull request comment.

If Codex flags a regression or potential issue, you can ask it to fix it by commenting on the pull request with a follow-up prompt like `@codex fix it`.

This will start a new cloud task that will fix the issue and update the pull request.

## Define review guidance

To customize what Codex reviews, add or update a top-level `AGENTS.md` with a section like this:

```
## Review guidelines

- Flag typos and grammar issues as P0 issues.
- Flag potential missing documentation as P1 issues.
- Flag missing tests as P1 issues.
  ...
```

Codex applies guidance from the closest `AGENTS.md` to each changed file. You can place more specific instructions deeper in the tree when particular packages need extra scrutiny.

## Related use cases

[![](/codex/use-cases/build-and-deploy-internal-apps.webp)

### Build and deploy internal apps

Use Codex with Sites to build, test, and deploy internal apps, with built-in storage and...

Front-end  Integrations](/codex/use-cases/build-and-deploy-internal-apps)[![](/codex/use-cases/deploy-app-or-website.webp)

### Deploy an app or website

Use Codex with Build Web Apps and Vercel to turn a repo, screenshot, design, or rough app...

Front-end  Integrations](/codex/use-cases/deploy-app-or-website)[![](/codex/use-cases/verified-operations-workflows.webp)

### Run verified operations

Use Codex to normalize inputs, run approved scripts or APIs, retry bounded failures, and...

Automation  Integrations](/codex/use-cases/verified-operations-workflows)

