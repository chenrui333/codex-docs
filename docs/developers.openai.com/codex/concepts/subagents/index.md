# Subagents – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/concepts/subagents

Codex can run subagent workflows by spawning specialized agents in parallel so
they can explore, tackle, or analyze work concurrently.

This page explains the core concepts and tradeoffs. For setup, agent configuration, and examples, see [Subagents](/codex/subagents).

## Why subagent workflows help

Even with large context windows, models have limits. If you flood the main conversation (where you’re defining requirements, constraints, and decisions) with noisy intermediate output such as exploration notes, test logs, stack traces, and command output, the session can become less reliable over time.

This is often described as:

- **Context pollution**: useful information gets buried under noisy intermediate output.
- **Context rot**: performance degrades as the conversation fills up with less relevant details.

For background, see the Chroma writeup on [context rot](https://research.trychroma.com/context-rot).

Subagent workflows help by moving noisy work off the main thread:

- Keep the **main agent** focused on requirements, decisions, and final outputs.
- Run specialized **subagents** in parallel for exploration, tests, or log analysis.
- Return **summaries** from subagents instead of raw intermediate output.

They can also save time when the work can run independently in parallel, and
they make larger-shaped tasks more tractable by breaking them into bounded
pieces. For example, Codex can split analysis of a multi-million-token
document into smaller problems and return distilled takeaways to the main
thread.

As a starting point, use parallel agents for read-heavy tasks such as
exploration, tests, triage, and summarization. Be more careful with parallel
write-heavy workflows, because agents editing code at once can create
conflicts and increase coordination overhead.

## Core terms

Codex uses a few related terms in subagent workflows:

- **Subagent workflow**: A workflow where Codex runs parallel agents and combines their results.
- **Subagent**: A delegated agent that Codex starts to handle a specific task.
- **Agent thread**: The CLI thread for an agent, which you can inspect and switch between with `/agent`.

## Triggering subagent workflows

Codex doesn’t spawn subagents automatically, and it should only use subagents when you
explicitly ask for subagents or parallel agent work.

In practice, manual triggering means using direct instructions such as
“spawn two agents,” “delegate this work in parallel,” or “use one agent per
point.” Subagent workflows consume more tokens than comparable single-agent runs
because each subagent does its own model and tool work.

A good subagent prompt should explain how to divide the work, whether Codex
should wait for all agents before continuing, and what summary or output to
return.

```
Review this branch with parallel subagents. Spawn one subagent for security risks, one for test gaps, and one for maintainability. Wait for all three, then summarize the findings by category with file references.
```

## Choosing models and reasoning

Different agents need different model and reasoning settings.

If you don’t pin a model or `model_reasoning_effort`, Codex can choose a setup
that balances intelligence, speed, and price for the task. It may favor
`gpt-5.4-mini` for fast scans or a higher-effort `gpt-5.4`
configuration for more demanding reasoning. When you want finer control, steer that
choice in your prompt or set `model` and `model_reasoning_effort` directly in
the agent file.

For most tasks in Codex, start with `gpt-5.4`. Use `gpt-5.4-mini` when you
want a faster, lower-cost option for lighter subagent work. If you have
ChatGPT Pro and want near-instant text-only iteration, `gpt-5.3-codex-spark`
remains available in research preview.

### Model choice

- **`gpt-5.4`**: Start here for most agents. It combines strong coding, reasoning, tool use, and broader workflows. The main agent and agents that coordinate ambiguous or multi-step work fit here.
- **`gpt-5.4-mini`**: Use for agents that favor speed and efficiency over depth, such as exploration, read-heavy scans, large-file review, or processing supporting documents. It works well for parallel workers that return distilled results to the main agent.
- **`gpt-5.3-codex-spark`**: If you have ChatGPT Pro, use this research preview model for near-instant, text-only iteration when latency matters more than broader capability.

### Reasoning effort (`model_reasoning_effort`)

- **`high`**: Use when an agent needs to trace complex logic, check assumptions, or work through edge cases (for example, reviewer or security-focused agents).
- **`medium`**: A balanced default for most agents.
- **`low`**: Use when the task is straightforward and speed matters most.

Higher reasoning effort increases response time and token usage, but it can improve quality for complex work. For details, see [Models](/codex/models), [Config basics](/codex/config-basic), and [Configuration Reference](/codex/config-reference).

