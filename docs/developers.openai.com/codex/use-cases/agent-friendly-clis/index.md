---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/agent-friendly-clis'
source_last_modified: '2026-05-22T16:22:17Z'
source_etag: 'W/"006917c64502b8148ddfb98b4df6b9da"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0"]
---

# Create a CLI Codex can use | Codex use cases

Source: https://developers.openai.com/codex/use-cases/agent-friendly-clis

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Create a CLI Codex can use

Give Codex a composable command for an API, log source, export, or team script.

Difficulty **Intermediate**

Time horizon **1h**

Ask Codex to create a composable CLI it can run from any folder, combine with repo scripts, use to download files, and remember through a companion skill.

## Best for

- Repeated work where Codex needs to search, read, download from, or safely write to the same service, export, local archive, or repo script.
- Agent tools that need paged search, exact reads by ID, predictable JSON, downloaded files, local indexes, or draft-before-write commands.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/agent-friendly-clis/?export=pdf)

Ask Codex to create a composable CLI it can run from any folder, combine with repo scripts, use to download files, and remember through a companion skill.

Intermediate

1h

Related links

[Codex skills](/codex/skills)  [Create custom skills](/codex/skills/create-skill)

## Best for

- Repeated work where Codex needs to search, read, download from, or safely write to the same service, export, local archive, or repo script.
- Agent tools that need paged search, exact reads by ID, predictable JSON, downloaded files, local indexes, or draft-before-write commands.

## Skills & Plugins

- [Cli Creator](https://github.com/openai/skills/tree/main/skills/.curated/cli-creator)

  Design the command surface, build the CLI, add setup and auth checks, install the command on PATH, and verify it from another folder.
- [Skill Creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)

  Create the companion skill that teaches later Codex tasks which CLI commands to run first and which write actions require approval.

| Skill | Why use it |
| --- | --- |
| [Cli Creator](https://github.com/openai/skills/tree/main/skills/.curated/cli-creator) | Design the command surface, build the CLI, add setup and auth checks, install the command on PATH, and verify it from another folder. |
| [Skill Creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | Create the companion skill that teaches later Codex tasks which CLI commands to run first and which write actions require approval. |

## Starter prompt

Use $cli-creator to create a CLI you can use, and use $skill-creator to create the companion skill in this same thread.
Source to learn from: [docs URL, OpenAPI spec, redacted curl command, existing script path, log folder, CSV or JSON export, SQLite database path, or pasted --help output].
First job the CLI should support: [download failed CI logs from a build URL, search support tickets and read one by ID, query an admin API, read a local database, or run one step from an existing script].
Optional write job: [create a draft comment, upload media, retry a failed job, or read-only for now].
Command name: [cli-name, or recommend one].
Before coding, show me the proposed command surface and ask only for missing details that would block the build.

[Open in the Codex app](codex://threads/new?prompt=Use+%24cli-creator+to+create+a+CLI+you+can+use%2C+and+use+%24skill-creator+to+create+the+companion+skill+in+this+same+thread.%0A%0ASource+to+learn+from%3A+%5Bdocs+URL%2C+OpenAPI+spec%2C+redacted+curl+command%2C+existing+script+path%2C+log+folder%2C+CSV+or+JSON+export%2C+SQLite+database+path%2C+or+pasted+--help+output%5D.%0A%0AFirst+job+the+CLI+should+support%3A+%5Bdownload+failed+CI+logs+from+a+build+URL%2C+search+support+tickets+and+read+one+by+ID%2C+query+an+admin+API%2C+read+a+local+database%2C+or+run+one+step+from+an+existing+script%5D.%0A%0AOptional+write+job%3A+%5Bcreate+a+draft+comment%2C+upload+media%2C+retry+a+failed+job%2C+or+read-only+for+now%5D.%0A%0ACommand+name%3A+%5Bcli-name%2C+or+recommend+one%5D.%0A%0ABefore+coding%2C+show+me+the+proposed+command+surface+and+ask+only+for+missing+details+that+would+block+the+build. "Open in the Codex app")

Use $cli-creator to create a CLI you can use, and use $skill-creator to create the companion skill in this same thread.
Source to learn from: [docs URL, OpenAPI spec, redacted curl command, existing script path, log folder, CSV or JSON export, SQLite database path, or pasted --help output].
First job the CLI should support: [download failed CI logs from a build URL, search support tickets and read one by ID, query an admin API, read a local database, or run one step from an existing script].
Optional write job: [create a draft comment, upload media, retry a failed job, or read-only for now].
Command name: [cli-name, or recommend one].
Before coding, show me the proposed command surface and ask only for missing details that would block the build.

## Introduction

When Codex keeps using the same API, log source, exported inbox, local database, or team script, give that work a composable interface: a command it can run from any folder, inspect, narrow, and combine with `git`, `gh`, `rg`, tests, and repo scripts.

Add a companion skill that records when Codex should use the CLI, what to run first, how to keep output small, where downloaded files land, and which write commands need approval.

In this workflow, `$cli-creator` helps Codex build the command. `$skill-creator` helps Codex save a reusable skill such as `$ci-logs`, which future tasks can invoke by name.

## How to use

1. [Decide whether the job needs a CLI](#choose-what-the-cli-should-do)
2. [Share the source Codex should learn from](#share-the-docs-files-or-commands)
3. [Run `$cli-creator`](#ask-codex-to-build-the-cli-and-skill)
4. [Test the installed command](#verify-the-command-works-from-any-folder)
5. [Invoke the saved skill later](#use-the-skill-later)

## Choose what the CLI should do

Start with the thing you want Codex to do, not the technology you want it to write. A good CLI turns a repeated read, search, download, export, draft, upload, poll, or safe write into a command Codex can run from any repo.

| Situation | What Codex can do with the CLI |
| --- | --- |
| **CI logs live behind a build page.** | Take a build URL, download failed job logs to `./logs`, and return file paths plus short snippets. |
| **Support tickets arrive as a weekly export.** | Index the newest CSV or JSON export, search by customer or phrase, and read one ticket by stable ID. |
| **An API response is too large for context.** | List only the fields it needs, read the full object by ID, and export the complete response to a file. |
| **A Slack export has long threads.** | Search with `--limit`, read one thread, and return nearby context instead of the whole archive. |
| **A team script runs four different steps.** | Split setup, discovery, download, draft, upload, poll, and live write into separate commands. |
| **A plugin finds the record, but Codex needs a file.** | Keep the plugin in the thread; use a CLI to download the attachment, trace, report, video, or log bundle and return the path. |

## Share the docs, files, or commands

Codex needs something concrete to learn from: docs or OpenAPI, a redacted curl command, an export or database path, a log folder, or an existing script. If you want the CLI to follow a familiar style, paste a short `--help` output from `gh`, `kubectl`, or your team’s own tool.

If the command needs auth, tell Codex the environment variable name, config file path, or login flow it should support. Set the secret yourself in your shell or config file. Do not paste secrets into the thread. Ask Codex to make the CLI’s setup check fail clearly when auth is missing.

## Ask Codex to build the CLI and skill

Use the starter prompt on this page. Fill in the source Codex should learn from and the first job the CLI should support.

Before Codex writes code, it should show the proposed command surface and ask only for missing details that would block the build.

## Verify the command works from any folder

Codex should not stop after `cargo run`, `python path/to/script.py`, or an uninstalled package command. Ask it to test the installed command from another repo or a temporary folder, the way a later task will use it.

**Test the CLI like a future agent**

Test [cli-name] the way you would use it in a future task.
Please show proof that:
- command -v [cli-name] succeeds from outside the CLI source folder
- [cli-name] --help explains the main commands
- the setup/auth check runs
- one safe discovery, list, or search command works
- one exact read command works with an ID from the discovery result
- any large log, export, trace, or payload writes to a file and returns the path
- live write commands are not run unless I explicitly approved them
Then read the companion skill and tell me the shortest prompt I should use when I need this CLI again.

If Codex returns a giant JSON blob, ask it to narrow the default response and add a file export for full payloads. If it forgets the approval boundary, ask it to update the companion skill before you use it in another thread.

## Use the skill later

When you need the CLI again, invoke the skill instead of pasting the docs again:

Use $ci-logs to download the failed logs for this build URL and tell me the first failing step.

Use $support-export to search this week's refund complaints and read the three highest-value tickets.

Use $admin-api to find this user's workspace, read the billing record, and draft a safe account note.

For recurring work, test the skill once in a normal thread, then ask Codex to turn that same invocation into an automation.

## Related use cases

[![](/codex/use-cases/ai-app-evals.webp)

### Add evals to your AI application

Ask Codex to inspect your AI application, identify the behavior you want to evaluate, and...

Evaluation  Quality](/codex/use-cases/ai-app-evals)[![](/codex/use-cases/follow-goals.webp)

### Follow a goal

Use `/goal` when a task needs Codex to keep working across turns toward a verifiable...

Engineering  Automation](/codex/use-cases/follow-goals)[![](/codex/use-cases/dependency-incident-audits.webp)

### Audit dependency incidents

Use Codex to turn a public package or supply chain advisory into a read-only audit, then...

Engineering  Quality](/codex/use-cases/dependency-incident-audits)

