---
source_type: 'developers'
source_area: 'codex_concept'
source_url: 'https://developers.openai.com/codex/concepts/sandboxing'
source_last_modified: '2026-05-20T00:54:21Z'
source_etag: 'W/"525233ccfcca2141b594eb6814566647"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0"]
---

# Sandbox – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/concepts/sandboxing

The sandbox is the boundary that lets Codex act autonomously without giving it
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
between macOS, Linux, WSL2, and native Windows, but the idea is the same across
surfaces: give the agent a bounded place to work so routine tasks can run
autonomously inside clear limits.

## Why it matters

The sandbox reduces approval fatigue. Instead of asking you to confirm every
low-risk command, Codex can read files, make edits, and run routine project
commands within the boundary you already approved.

It also gives you a clearer trust model for agentic work. You aren’t just
trusting the agent’s intentions; you are trusting that the agent is operating
inside enforced limits. That makes it easier to let Codex work independently
while still knowing when it will stop and ask for help.

## Getting started

Codex applies sandboxing automatically when you use the default permissions
mode.

### Prerequisites

On **macOS**, sandboxing works out of the box using the built-in Seatbelt
framework.

On **Windows**, Codex uses the native [Windows
sandbox](/codex/windows#windows-sandbox) when you run in PowerShell and the
Linux sandbox implementation when you run in WSL2.

On **Linux and WSL2**, install `bubblewrap` with your package manager first:

```
sudo apt install bubblewrap
```

```
sudo dnf install bubblewrap
```

Codex uses the first `bwrap` executable it finds on `PATH`. If no `bwrap`
executable is available, Codex falls back to a bundled helper, but that helper
requires support for unprivileged user namespace creation. Installing the
distribution package that provides `bwrap` keeps this setup reliable.

Codex surfaces a startup warning when `bwrap` is missing or when the helper
can’t create the needed user namespace. On distributions that restrict this
AppArmor setting, prefer loading the `bwrap` AppArmor profile so `bwrap` can
keep working without disabling the restriction globally.

**Ubuntu AppArmor note:** On Ubuntu 25.04, installing `bubblewrap` from
Ubuntu’s package repository should work without extra AppArmor setup. The
`bwrap-userns-restrict` profile ships in the `apparmor` package at
`/etc/apparmor.d/bwrap-userns-restrict`.

On Ubuntu 24.04, Codex may still warn that it can’t create the needed user
namespace after `bubblewrap` is installed. Copy and load the extra profile:

```
sudo apt update
sudo apt install apparmor-profiles apparmor-utils
sudo install -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
```

`apparmor_parser -r` loads the profile into the kernel without a reboot. You
can also reload all AppArmor profiles:

```
sudo systemctl reload apparmor.service
```

If that profile is unavailable or does not resolve the issue, you can disable
the AppArmor unprivileged user namespace restriction with:

```
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

## How you control it

Most people start with the permissions controls in the product.

In the Codex app and IDE, you choose a mode from the permissions selector under
the composer or chat input. That selector lets you rely on Codex’s default
permissions, switch to full access, or use your custom configuration.

Ask Codex anything.

Default permissions

5.5High

#### Default permissions

Codex can read and edit files in the current workspace and run routine local commands. It asks before using the internet or going beyond the workspace boundary.

Sandbox
:   `workspace-write`

Approvals policy
:   `on-request`

Reviewer
:   `user`

In the CLI, use [`/permissions`](/codex/cli/slash-commands#update-permissions-with-permissions)
to switch modes during a session.

## Configure defaults

If you want Codex to start with the same behavior every time, use a custom
configuration. Codex stores those defaults in `config.toml`, its local settings
file. [Config basics](/codex/config-basic) explains how it works, and the
[Configuration reference](/codex/config-reference) documents the exact keys for
`sandbox_mode`, `approval_policy`, `approvals_reviewer`, and
`sandbox_workspace_write.writable_roots`. Use those settings to decide how much
autonomy Codex gets by default, which directories it can write to, when it
should pause for approval, and who reviews eligible approval requests.

At a high level, the common sandbox modes are:

- `read-only`: Codex can inspect files, but it can’t edit files or run
  commands without approval.
- `workspace-write`: Codex can read files, edit within the workspace, and run
  routine local commands inside that boundary. This is the default low-friction
  mode for local work.
- `danger-full-access`: Codex runs without sandbox restrictions. This removes
  the filesystem and network boundaries and should be used only when you want
  Codex to act with full access.

The common approval policies are:

- `untrusted`: Codex asks before running commands that aren’t in its trusted
  set.
- `on-request`: Codex works inside the sandbox by default and asks when it
  needs to go beyond that boundary.
- `never`: Codex doesn’t stop for approval prompts.

When approvals are interactive, you can also choose who reviews them with
`approvals_reviewer`:

- `user`: approval prompts surface to the user. This is the default.
- `auto_review`: eligible approval prompts go to a reviewer agent (see
  [Auto-review](/codex/concepts/sandboxing/auto-review)).

Full access means using `sandbox_mode = "danger-full-access"` together with
`approval_policy = "never"`. By contrast, the lower-risk local automation
preset is `sandbox_mode = "workspace-write"` together with
`approval_policy = "on-request"`, or the matching CLI flags
`--sandbox workspace-write --ask-for-approval on-request`. You can then keep
`approvals_reviewer = "user"` for manual approvals or set
`approvals_reviewer = "auto_review"` for automatic approval review.

If you need Codex to work across more than one directory, writable roots let
you extend the places it can modify without removing the sandbox entirely. If
you need a broader or narrower trust boundary, adjust the default sandbox mode
and approval policy instead of relying on one-off exceptions.

When a workflow needs a specific exception, use [rules](/codex/rules). Rules
let you allow, prompt, or forbid command prefixes outside the sandbox, which is
often a better fit than broadly expanding access. For a higher-level overview
of approvals and sandbox behavior in the app, see
[Codex app features](/codex/app/features#approvals-and-sandboxing), and for the
IDE-specific settings entry points, see [Codex IDE extension settings](/codex/ide/settings).

Automatic review, when available, does not change the sandbox boundary. It is
one possible `approvals_reviewer` for approval requests at that boundary, such
as sandbox escalations, blocked network access, or side-effecting tool calls
that still need approval. Actions already allowed inside the sandbox run
without extra review. For the reviewer lifecycle, trigger types, denial
semantics, and configuration details, see
[Auto-review](/codex/concepts/sandboxing/auto-review).

Platform details live in the platform-specific docs. For native Windows setup,
behavior, and troubleshooting, see [Windows](/codex/windows). For admin
requirements and organization-level constraints on sandboxing and approvals, see
[Agent approvals & security](/codex/agent-approvals-security).

