# Review pull requests faster | Codex use cases

Source: https://developers.openai.com/codex/use-cases/github-code-reviews

[← All use cases](/codex/use-cases)

Use Codex in GitHub to automatically surface regressions, missing tests, and documentation issues directly on a pull request.

Easy

5s

Related links

[Use Codex in GitHub](/codex/integrations/github)  [Custom instructions with AGENTS.md](/codex/guides/agents-md)

## Best for

- Teams that want another review signal before human merge approval
- Large codebases for projects in production

## Skills & Plugins

- [Security Best Practices](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices)

  Focus the review on risky surfaces such as secrets, auth, and dependency changes.

## Starter prompt

@codex review for security regressions, missing tests, and risky behavior changes.

## How to use

Start by adding Codex code review to your GitHub organization or repository. See [Use Codex in GitHub](/codex/integrations/github) for more details.

You can set up Codex to automatically review every pull request, or you can request a review with `@codex review` in a pull request comment.

If Codex flags a regression or potential issue, you can ask it to fix it by commenting on the pull request with a follow-up prompt like `@codex fix it`.

This will start a new cloud task that will fix the issue and update the pull request.

## Define additional guidance

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

[![](/images/codex/codex-wallpaper-1.webp)

### Bring your app to ChatGPT

Build one narrow ChatGPT app outcome end to end: define the tools, scaffold the MCP server...

Integrations  Code](/codex/use-cases/chatgpt-apps)[![](/images/codex/codex-wallpaper-2.webp)

### Coordinate new-hire onboarding

Use Codex to gather approved new-hire context, stage tracker updates, draft team-by-team...

Integrations  Data](/codex/use-cases/new-hire-onboarding)[![](/images/codex/codex-wallpaper-2.webp)

### Create a CLI Codex can use

Ask Codex to create a composable CLI it can run from any folder, combine with repo scripts...

Engineering  Code](/codex/use-cases/agent-friendly-clis)

