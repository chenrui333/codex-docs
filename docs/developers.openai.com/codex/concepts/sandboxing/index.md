# Sandboxing

Source: https://developers.openai.com/codex/concepts/sandboxing

Sandboxing is the boundary that lets Codex act autonomously without giving it
unrestricted access to your machine. When Codex runs local commands in the
**Codex app**, **IDE extension**, or **CLI**, those commands run inside a
constrained environment instead of running with full access by default.

That environment defines what Codex can do on its own, such as which files it
can modify and whether commands can use the network. When a task stays inside
those boundaries, Codex can keep moving without stopping for confirmation. When
it needs to go beyond them, Codex falls back to the approval flow.

Sandboxing and approvals are different controls that work together. The
sandbox defines technical boundaries. The approval policy decides when Codex
must stop and ask before crossing them.

## What the sandbox does

The sandbox applies to spawned commands, not just to Codex’s built-in file
operations. If Codex runs tools like `git`, package managers, or test runners,
those commands inherit the same sandbox boundaries.

Codex uses platform-native enforcement on each OS. The implementation differs
between macOS, Linux, WSL, and native Windows, but the idea is the same across
surfaces: give the agent a bounded place to work so routine tasks can run
autonomously inside clear limits.

## Why it matters

Sandboxing reduces approval fatigue. Instead of asking you to confirm every
low-risk command, Codex can read files, make edits, and run routine project
commands within the boundary you already approved.

It also gives you a clearer trust model for agentic work. You are not just
trusting the agent’s intentions; you are trusting that the agent is operating
inside enforced limits. That makes it easier to let Codex work independently
while still knowing when it will stop and ask for help.

## How you control it

Most people start with the permissions controls in the product.

In the Codex app and IDE, you choose a mode from the permissions selector under
the composer or chat input. That selector lets you rely on Codex’s default
permissions, switch to full access, or use your custom configuration.

![Codex app permissions selector showing Default permissions, Full access, and Custom (config.toml)](/images/codex/app/permissions-selector-light.webp)

In the CLI, use [`/permissions`](/codex/cli/slash-commands#update-permissions-with-permissions)
to switch modes during a session.

## Configure defaults

If you want Codex to start with the same behavior every time, use a custom
configuration. Codex stores those defaults in `config.toml`, its local settings
file. [Config basics](/codex/config-basic) explains how it works, and the
[Configuration reference](/codex/config-reference) documents the exact keys for
`sandbox_mode`, `approval_policy`, and
`sandbox_workspace_write.writable_roots`. Use those settings to decide how much
autonomy Codex gets by default, which directories it can write to, and when it
should pause for approval.

At a high level, the common sandbox modes are:

- `read-only`: Codex can inspect files, but it cannot edit files or run
  commands without approval.
- `workspace-write`: Codex can read files, edit within the workspace, and run
  routine local commands inside that boundary. This is the default low-friction
  mode for local work.
- `danger-full-access`: Codex runs without sandbox restrictions. This removes
  the filesystem and network boundaries and should be used only when you want
  Codex to act with full access.

The common approval policies are:

- `untrusted`: Codex asks before running commands that are not in its trusted
  set.
- `on-request`: Codex works inside the sandbox by default and asks when it
  needs to go beyond that boundary.
- `never`: Codex does not stop for approval prompts.

Full access means using `sandbox_mode = "danger-full-access"` together with
`approval_policy = "never"`. By contrast, `--full-auto` is the lower-risk local
automation preset: `sandbox_mode = "workspace-write"` and
`approval_policy = "on-request"`.

If you need Codex to work across more than one directory, writable roots let
you extend the places it can modify without removing the sandbox entirely. If
you need a broader or narrower trust boundary, adjust the default sandbox mode
and approval policy instead of relying on ad hoc exceptions.

When a workflow needs a specific exception, use [rules](/codex/rules). Rules
let you allow, prompt, or forbid command prefixes outside the sandbox, which is
often a better fit than broadly expanding access. For a higher-level overview
of approvals and sandbox behavior in the app, see
[Codex app features](/codex/app/features#approvals-and-sandboxing), and for the
IDE-specific settings entry points, see [Codex IDE extension settings](/codex/ide/settings).

Platform details live in the platform-specific docs. For native Windows setup,
behavior, and troubleshooting, see [Windows](/codex/windows). For admin
requirements and organization-level constraints on sandboxing and approvals, see
[Agent approvals & security](/codex/agent-approvals-security).

