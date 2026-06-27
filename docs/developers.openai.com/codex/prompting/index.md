---
source_type: 'developers'
source_area: 'codex_cli_docs'
source_url: 'https://developers.openai.com/codex/prompting'
source_last_modified: '2026-05-21T23:45:36Z'
source_etag: 'W/"ec35bd1a6fcc5870768459df017c5fd3"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3"]
---

# Prompting – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/prompting

## Prompts

You interact with Codex by sending prompts (user messages) that describe what you want it to do.

Example prompts:

```
Explain how the transform module works and how other modules use it.
```

```
Add a new command-line option `--json` that outputs JSON.
```

When you submit a prompt, Codex works in a loop: it calls the model and then performs the actions indicated by the model output, such as file reads, file edits, and tool calls. This process ends when the task is complete or you cancel it.

As with ChatGPT, Codex is only as effective as the instructions you give it. Here are some tips we find helpful when prompting Codex:

- Codex produces higher-quality outputs when it can verify its work. Include steps to reproduce an issue, validate a feature, and run linting and pre-commit checks.
- Codex handles complex work better when you break it into smaller, focused steps. Smaller tasks are easier for Codex to test and for you to review. If you’re not sure how to split a task up, ask Codex to propose a plan.

For more ideas about prompting Codex, refer to [workflows](/codex/workflows).

## Threads

A thread is a single session: your prompt plus the model outputs and tool calls that follow. A thread can include multiple prompts. For example, your first prompt might ask Codex to implement a feature, and a follow-up prompt might ask it to add tests.

A thread is said to be “running” when Codex is actively working on it. You can run multiple threads at once, but avoid having two threads modify the same files. You can also resume a thread later by continuing it with another prompt.

Threads can run either locally or in the cloud:

- **Local threads** run on your machine. Codex can read and edit your files and run commands, so you can see what changes and use your existing tools. To reduce the risk of unwanted changes outside your workspace, local threads run in a [sandbox](/codex/agent-approvals-security).
- **Cloud threads** run in an isolated [environment](/codex/cloud/environments). Codex clones your repository and checks out the branch it’s working on. Cloud threads are useful when you want to run work in parallel or delegate tasks from another device. To use cloud threads with your repo, push your code to GitHub first. You can also [delegate tasks from your local machine](/codex/ide/cloud-tasks), which includes your current working state.

In the Codex app, you can also start a chat without choosing a project. Chats
aren’t tied to a saved repository or project folder. Use them for research,
planning, connected-tool workflows, or other work where Codex shouldn’t start
from a codebase. Chats use a Codex-managed `threads` directory under your Codex
home as their working location. By default, that location is `~/.codex/threads`.
To change the base location for this state, set `CODEX_HOME`; see
[Config and state locations](/codex/config-advanced#config-and-state-locations).

## Context

When you submit a prompt, include context that Codex can use, such as references to relevant files and images. The Codex IDE extension automatically includes the list of open files and the selected text range as context.

As the agent works, it also gathers context from file contents, tool output, and an ongoing record of what it has done and what it still needs to do.

All information in a thread must fit within the model’s **context window**, which varies by model. Codex monitors and reports the remaining space. For longer tasks, Codex may automatically **compact** the context by summarizing relevant information and discarding less relevant details. With repeated compaction, Codex can continue working on complex tasks over many steps.

## Goal mode

Goal mode gives Codex a persistent objective to work toward across a longer
task. Use it when the work may take many steps, or when Codex needs a clear
definition of done that it can keep checking as it works.

![Codex app goal progress controls above the composer](/images/codex/app/goal-dialog-light.webp)

When you set a goal, the goal text acts as both the starting prompt and the
completion criteria. Codex uses it to decide what to do next and whether the
task is complete. Start Goal mode with `/goal` in the [Codex
app](/codex/app/commands#set-or-manage-a-goal-with-goal), [IDE
extension](/codex/ide/slash-commands), or [CLI](/codex/cli/slash-commands#set-or-view-a-task-goal-with-goal).

If `/goal` doesn’t appear in the slash command list, enable `features.goals`
in `config.toml`:

```
[features]
goals = true
```

You can also run `codex features enable goals` from the CLI or ask Codex to run it.
In the Codex app, progress appears above the composer with controls to pause,
resume, edit, or clear the goal.

Write goals so Codex can tell whether it has succeeded. Good goals include a
specific outcome, measurable target, or test criteria. For example:

```
Migrate this codebase from JavaScript to TypeScript. The app should compile in
strict mode without explicit `any` type definitions.
```

```
Reduce the time to interactive of the home page to below 1 second.
```

If the goal is hard to define up front, start with `/plan` and ask Codex to
shape it before implementation. You can also ask Codex to interview you and
draft a goal with clear success criteria.

You can continue steering Codex after the goal starts. Send follow-up messages
to adjust constraints, such as asking Codex to use a particular library or
avoid a specific approach. Use side chats when you want a status recap or
explanation without interrupting the main task. For long-running work, pause
the goal before you lose connectivity, then resume or edit it when you are
ready to continue.

