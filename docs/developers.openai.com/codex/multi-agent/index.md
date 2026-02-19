# Multi-agents

Source: https://developers.openai.com/codex/multi-agent

Use experimental multi-agent collaboration in Codex CLI

Codex can run multi-agent workflows by spawning specialized agents in parallel and then collecting their results in one response. This can be particularly helpful for complex tasks that are highly parallel, such as codebase exploration or implementing a multi-step feature plan.

With multi-agent workflows you can also define your own set of agents with different model configurations and instructions depending on the agent.

## Enable multi-agent

Multi-agent workflows are currently experimental and need to be explicitly enabled.

You can enable this feature from the CLI with `/experimental`. Enable
**Multi-agents**, then restart Codex.

Multi-agent activity is currently surfaced in the CLI. Visibility in other
surfaces (the Codex app and IDE Extension) is coming soon.

You can also add the [`multi_agent` feature flag](/codex/config-basic#feature-flags) directly to your configuration file (`~/.codex/config.toml`):

```
[features]
multi_agent = true
```

## Typical workflow

Codex handles orchestration across agents, including spawning new sub-agents, routing follow-up instructions, waiting for results, and closing agent threads.

When many agents are running, Codex waits until all requested results are available, then returns a consolidated response.

Codex will automatically decide when to spawn a new agent or you can explicitly ask it to do so.

To see it in action, try the following prompt on your project:

```
I would like to review the following points on the current PR (this branch vs main). Spawn one agent per point, wait for all of them, and summarize the result for each point.
1. Security issue
2. Code quality
3. Bugs
4. Race
5. Test flakiness
6. Maintainability of the code
```

## Managing sub-agents

- Use `/agent` in the CLI to switch between active agent threads and inspect the ongoing thread.
- Ask Codex directly to steer a running sub-agent, stop it, or close completed agent threads.

## Approvals and sandbox controls

Sub-agents inherit your current sandbox policy, but they run with
non-interactive approvals. If a sub-agent attempts an action that would require
a new approval, that action fails and the error is surfaced in the parent
workflow.

You can also override the sandbox configuration for individual [agent roles](#agent-roles) such as explicitly marking an agent to work in read-only mode.

## Agent roles

You configure agent roles in the `[agents]` section of your [configuration](/codex/config-basic#configuration-precedence).

Agent roles can be defined either in your local configuration (typically `~/.codex/config.toml`) or shared in a project-specific `.codex/config.toml`.

Each role can provide guidance (`description`) for when Codex should use this agent, and optionally load a
role-specific config file (`config_file`) when Codex spawns an agent with that role.

Codex ships with built-in roles:

- `default`
- `worker`
- `explorer`

Each agent role can override your default configuration. Common settings to override for an agent role are:

- `model` and `model_reasoning_effort` to select a specific model for your agent role
- `sandbox_mode` to mark an agent as `read-only`
- `developer_instructions` to give the agent role additional instructions without relying on the parent agent for passing them

### Schema

| Field | Type | Required | Purpose |
| --- | --- | --- | --- |
| `agents.max_threads` | number | No | Maximum number of concurrently open agent threads. |
| `[agents.<name>]` | table | No | Declares a role. `<name>` is used as the `agent_type` when spawning an agent. |
| `agents.<name>.description` | string | No | Human-facing role guidance shown to Codex when it decides which role to use. |
| `agents.<name>.config_file` | string (path) | No | Path to a TOML config layer applied to spawned agents for that role. |

**Notes:**

- Unknown fields in `[agents.<name>]` are rejected.
- Relative `config_file` paths are resolved relative to the `config.toml` file that defines the role.
- If a role name matches a built-in role (for example, `explorer`), your user-defined role takes precedence.
- If Codex can’t load a role config file, agent spawns can fail until you fix the file.
- Any configuration not set by the agent role will be inherited from the parent session.

### Example agent roles

Below is an example that overrides the definitions for the built-in `default` and `explorer` agent roles and defines a new `reviewer` role.

Example `~/.codex/config.toml`:

```
[agents.default]
description = "General-purpose helper."

[agents.reviewer]
description = "Find security, correctness, and test risks in code."
config_file = "agents/reviewer.toml"

[agents.explorer]
description = "Fast codebase explorer for read-heavy tasks."
config_file = "agents/custom-explorer.toml"
```

Example config file for the `reviewer` role (`~/.codex/agents/reviewer.toml`):

```
model = "gpt-5.3-codex"
model_reasoning_effort = "high"
developer_instructions = "Focus on high priority issues, write tests to validate hypothesis before flagging an issue. When finding security issues give concrete steps on how to reproduce the vulnerability."
```

Example config file for the `explorer` role (`~/.codex/agents/custom-explorer.toml`):

```
model = "gpt-5.3-codex-spark"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
```

