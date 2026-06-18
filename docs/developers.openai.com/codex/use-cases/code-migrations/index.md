---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/code-migrations'
source_last_modified: '2026-06-05T17:28:33Z'
source_etag: 'W/"084baf0b5173fb4836129aa3d1cd473f"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Run code migrations | Codex use cases

Source: https://developers.openai.com/codex/use-cases/code-migrations

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Run code migrations

Migrate legacy stacks in controlled checkpoints.

Difficulty **Advanced**

Time horizon **1h**

Use Codex to map a legacy system to a new stack, land the move in milestones, and validate parity before each transition.

## Best for

- Legacy-to-modern stack moves where frameworks, runtimes, build systems, or platform conventions need to change.
- Teams that need compatibility layers, phased transitions, and explicit validation at each migration checkpoint.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/code-migrations/?export=pdf)

Use Codex to map a legacy system to a new stack, land the move in milestones, and validate parity before each transition.

Advanced

1h

Related links

[Modernizing your Codebase with Codex](/cookbook/examples/codex/code_modernization)  [Follow a goal](/codex/use-cases/follow-goals)  [Worktrees in the Codex app](/codex/app/worktrees)

## Best for

- Legacy-to-modern stack moves where frameworks, runtimes, build systems, or platform conventions need to change.
- Teams that need compatibility layers, phased transitions, and explicit validation at each migration checkpoint.

## Skills & Plugins

- [Security Best Practices](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices)

  Check risky migrations, dependency changes, and exposed surfaces before you merge.
- [Gh Fix Ci](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci)

  Work through failing CI after each migration milestone instead of leaving cleanup until the end.
- [Aspnet Core](https://github.com/openai/skills/tree/main/skills/.curated/aspnet-core)

  Use framework-specific guidance when a migration touches ASP.NET Core app models, `Program.cs`, middleware, testing, performance, or version upgrades.

| Skill | Why use it |
| --- | --- |
| [Security Best Practices](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) | Check risky migrations, dependency changes, and exposed surfaces before you merge. |
| [Gh Fix Ci](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci) | Work through failing CI after each migration milestone instead of leaving cleanup until the end. |
| [Aspnet Core](https://github.com/openai/skills/tree/main/skills/.curated/aspnet-core) | Use framework-specific guidance when a migration touches ASP.NET Core app models, `Program.cs`, middleware, testing, performance, or version upgrades. |

## Starter prompt

Migrate this codebase from [legacy stack or system] to [target stack or system].
Requirements:
- Start by inventorying the legacy assumptions: routing, data models, auth, configuration, build tooling, tests, deployment, and external contracts.
- Map the old stack to the new one and call out anything that has no direct equivalent.
- Propose an incremental migration plan with compatibility layers or checkpoints instead of one big rewrite.
- Keep behavior unchanged unless the migration explicitly requires a user-visible change.
- Work in milestones and run lint, type-check, and focused tests after each milestone.
- Keep rollback or fallback options visible until the transition is complete.
- If validation fails, fix it before continuing.
- Start by mapping the migration surface and proposing the checkpoint plan.

Open in the Codex app

Migrate this codebase from [legacy stack or system] to [target stack or system].
Requirements:
- Start by inventorying the legacy assumptions: routing, data models, auth, configuration, build tooling, tests, deployment, and external contracts.
- Map the old stack to the new one and call out anything that has no direct equivalent.
- Propose an incremental migration plan with compatibility layers or checkpoints instead of one big rewrite.
- Keep behavior unchanged unless the migration explicitly requires a user-visible change.
- Work in milestones and run lint, type-check, and focused tests after each milestone.
- Keep rollback or fallback options visible until the transition is complete.
- If validation fails, fix it before continuing.
- Start by mapping the migration surface and proposing the checkpoint plan.

## Introduction

When you are moving from one stack to another, you can leverage Codex to map and execute a controlled migration: routing, data models, configuration, auth, background jobs, build tooling, deployment, tests, or even the language and framework conventions themselves.

Codex is useful here because it can inventory the legacy system, map old concepts to new ones, and land the change in checkpoints instead of one giant rewrite. That matters when you are moving off a legacy framework, porting to a new runtime, or incrementally replacing one stack with another while the product still has to keep working.

## How to use

1. Start by inventorying the migration surface: legacy packages, framework conventions, routing, data access, auth, configuration, build tooling, tests, deployment assumptions, and any external contracts that must survive the move.
2. Ask Codex to map the legacy concepts to the target stack and call out what has no direct match.
3. Choose an incremental strategy: compatibility layer, module-by-module port, branch-by-abstraction, or a strangler-style replacement around one boundary at a time.
4. Keep behavior stable until the migration itself forces a visible change, and name those exceptions explicitly.
5. After each milestone, run the smallest validation that proves parity: lint, type-check, focused tests, contract tests, smoke tests, or a side-by-side check against the legacy path.
6. Review the diff and the remaining transition risk after each checkpoint instead of waiting for the full rewrite.

## Leverage ExecPlans

In our [code modernization cookbook](/cookbook/examples/codex/code_modernization), we introduce ExecPlans: documents that let Codex keep an overview of the cleanup, spell out the intended end state, and log validation after each pass.
When you ask Codex to run a complex migration, ask it to create an ExecPlan for each part of the system to make sure every decision and tech stack choice is recorded and can be reviewed later.

## Combine with a goal

For long-running migration slices, use a [goal](/codex/use-cases/follow-goals) to guide Codex through the work. Set the goal with a clear end state, parity checks, rollback expectations, and a stopping condition.

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

