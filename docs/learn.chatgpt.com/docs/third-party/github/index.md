---
source_type: 'learn'
source_area: 'learn_third_party'
source_url: 'https://learn.chatgpt.com/docs/third-party/github'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
---

# Codex code review in GitHub

Source: https://learn.chatgpt.com/docs/third-party/github

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use Codex code review to get another high-signal review pass on GitHub pull
requests. Codex reviews the pull request diff, follows your repository guidance,
and posts a standard GitHub code review focused on serious issues.

<YouTubeEmbed
  title="Codex code review walkthrough"
  videoId="HwbSWVg5Ln4"
  class="max-w-md mr-auto"
/>

## Before you start

Make sure you have:

- [Codex cloud](https://learn.chatgpt.com/docs/cloud) set up for the repository you want to review.
- Access to [Codex code review settings](https://chatgpt.com/codex/settings/code-review).
- An `AGENTS.md` file if you want Codex to follow repository-specific review guidance.

## Set up Codex code review

1. Set up [Codex cloud](https://learn.chatgpt.com/docs/cloud).
2. Go to [Codex settings](https://chatgpt.com/codex/settings/code-review).
3. Turn on **Code review** for your repository.

  <img src="https://developers.openai.com/images/codex/code-review/code-review-settings.png"
    alt="Codex settings showing the Code review toggle"
    class="block h-auto w-full mx-0!"
  />

## Request a Codex review

1. In a pull request comment, mention `@codex review`.
2. Wait for Codex to react (👀) and post a review.

  <img src="https://developers.openai.com/images/codex/code-review/review-trigger.png"
    alt="A pull request comment with @codex review"
    class="block h-auto w-full mx-0!"
  />

Codex posts a review on the pull request, just like a teammate would. In
GitHub, Codex flags only P0 and P1 issues so review comments stay focused on
high-priority risks.

  <img src="https://developers.openai.com/images/codex/code-review/review-example.png"
    alt="Example Codex code review on a pull request"
    class="block h-auto w-full mx-0!"
  />

## Enable automatic reviews

If you want Codex to review every pull request automatically, turn on
**Automatic reviews** in [Codex settings](https://chatgpt.com/codex/settings/code-review).
Codex will post a review whenever someone opens a new PR for review, without
needing an `@codex review` comment.

## Customize what Codex reviews

Codex searches your repository for `AGENTS.md` files and follows the applicable
code review rules. Add a `## Code Review Rules` section to the file closest to
the code the rules govern. Use `###` headings to group related checks when
helpful.

For example, an experiment-reporting service can keep post-exposure behavior
from changing a comparison cohort:

```md
## Code Review Rules

### Experiment cohorts

- Do not filter treatment comparisons on post-exposure behavior, including conversion or retention.
  Safe path: build cohorts from assignment or exposure; report conversion as an outcome.
```

Put repository-wide rules in the root `AGENTS.md` and service-specific rules
in a nested file, such as `services/experiment_reporting/AGENTS.md`. Codex
applies the root and more-specific guidance that covers each changed file, so
unrelated changes don't have to carry service-specific context.

Start with two or three concise rules that encode checks reviewers often explain. Useful rules:

- **Focus on consequential, repository-specific behavior.** Describe the
  compatibility constraint, data boundary, or unsafe side effect to flag and
  why it matters.
- **State the safe path or exception.** Give Codex enough context to distinguish
  a real issue from expected behavior.
- **Keep rules scoped and durable.** Prefer outcomes over function names that
  can change, and place guidance near the code it governs.
- **Leave mechanical checks in CI.** Keep formatting, lint, and other
  deterministic checks out of review rules.

Open a representative pull request and request a review with `@codex review`.
Refine the rules based on the findings and feedback you see, and narrow or
remove guidance that produces noise.

Code review rules guide Codex; they don't replace tests, branch protections, or
required approvals.

For a one-off focus, add it to your pull request comment:

`@codex review for security regressions`

## Act on review findings

After Codex posts a review, you can ask it to fix issues in the same pull
request by leaving another comment:

```md
@codex fix the P1 issue
```

Codex starts a cloud chat with the pull request as context and can push a fix
back to the branch when it has permission to do so.

## Give Codex other tasks

If you mention `@codex` in a comment with anything other than `review`, Codex starts a [cloud chat](https://learn.chatgpt.com/docs/cloud) using your pull request as context.

```md
@codex fix the CI failures
```

## Troubleshoot code review

If Codex doesn't react or post a review:

- Confirm you turned on **Code review** for the repository in [Codex settings](https://chatgpt.com/codex/settings/code-review).
- Confirm the pull request belongs to a repository with [Codex cloud](https://learn.chatgpt.com/docs/cloud) set up.
- Use the exact trigger `@codex review` in a pull request comment.
- For automatic reviews, check that you turned on **Automatic reviews** and that
  the pull request event matches your review trigger settings.
