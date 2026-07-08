---
source_type: 'developers'
source_area: 'codex_glossary'
source_url: 'https://developers.openai.com/codex/glossary'
source_last_modified: '2026-06-05T16:39:02Z'
source_etag: 'W/"471e05deb837536bdaadef64e5be6172"'
codex_cli_versions: ["0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0"]
codex_cli_versions_raw: ["codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0"]
---

# Glossary – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/glossary

Use this glossary as a quick reference for Codex terms across the app, CLI, IDE extension, cloud, SDK, and related integrations.

| Term | Definition | Applies to |
| --- | --- | --- |
| [Agent](/codex) | The Codex worker that reasons over context, uses tools, and completes a task. | App, CLI, IDE extension, Cloud |
| [AGENTS.md](/codex/guides/agents-md) | Repository or user guidance file that gives Codex persistent instructions. | App, CLI, IDE extension, Cloud |
| [Analytics dashboard](/codex/enterprise/governance#analytics-dashboard) | Admin view for Codex usage, adoption, and code review metrics. | Enterprise |
| [API key sign-in](/codex/auth#sign-in-with-an-api-key) | Authentication using an OpenAI API key. | App, CLI, IDE extension |
| [Approval policy](/codex/agent-approvals-security#sandbox-and-approvals) | Rules for when Codex must ask before taking an action. | App, CLI, IDE extension |
| [Approval request](/codex/agent-approvals-security#automatic-approval-reviews) | Codex asking to allow a restricted action. | App, CLI, IDE extension |
| [Apps (connectors)](/codex/plugins) | Integration that lets Codex access external services. Available through plugins; also called connectors. | App, CLI, IDE extension |
| [Appshot](/codex/appshots) | Snapshot of the frontmost app window sent to a Codex thread. | App |
| [Auth cache](/codex/auth#login-caching) | Locally stored login credentials reused by Codex. | App, CLI, IDE extension |
| [Automatic approval review](/codex/agent-approvals-security#automatic-approval-reviews) | Model-based review of eligible approval requests before they proceed. | App, CLI, IDE extension |
| [Automation](/codex/app/automations) | A scheduled or recurring Codex task. | App |
| [Automation run](/codex/app/automations#managing-tasks) | One execution of a scheduled automation that may report findings or archive itself. | App |
| [Browser use](/codex/app/browser#browser-use) | App capability that lets Codex operate the in-app browser directly. | App |
| [Chat](/codex/app/features#chats) | A Codex conversation not tied to a project. | App |
| [ChatGPT sign-in](/codex/auth#sign-in-with-chatgpt) | Authentication using a ChatGPT account and workspace permissions. | App, CLI, IDE extension, Cloud |
| [Chronicle](/codex/memories/chronicle) | Opt-in feature that builds memories from recent screen context. | App |
| [Cloud](/codex/cloud) | Mode where Codex works remotely in an OpenAI-managed environment. | App, IDE extension, Web |
| [Cloud environment](/codex/cloud/environments) | Configured container setup used for Codex cloud tasks. | Cloud |
| [Cloud task](/codex/cloud/environments#how-codex-cloud-tasks-run) | A remotely executed Codex task that runs in a cloud environment. | Cloud |
| [Cloud thread](/codex/prompting#threads) | A thread that runs in a Codex cloud environment. | Cloud |
| [Codex](/codex) | OpenAI's coding agent for software development tasks. | App, CLI, IDE extension, Web, Cloud, SDK |
| [Codex app](/codex/app) | Desktop app for running Codex threads in parallel, with built-in worktree support, automations, and Git functionality. | Desktop |
| [Codex app-server](/codex/app-server) | Local JSON-RPC server for embedding Codex threads, turns, approvals, history, and streamed events in custom clients. | App, IDE extension, SDK |
| [Codex CLI](/codex/cli) | Terminal client for running Codex interactively or in scripts. | Terminal |
| [Codex cloud](/codex/cloud) | OpenAI-managed execution environment where Codex can work on repository tasks remotely. | Web, App, IDE extension |
| [codex exec](/codex/noninteractive) | CLI command for running Codex non-interactively from scripts or CI. | CLI |
| [Codex IDE extension](/codex/ide) | Editor integration for using Codex inside IDEs like VS Code, JetBrains IDEs, Cursor, and Windsurf. | IDE |
| [Codex SDK](/codex/sdk) | Programmatic interface for building Codex-powered workflows or integrations. | SDK |
| [Codex web](/codex/cloud) | Browser-based Codex surface for delegating cloud tasks. | Browser |
| [Codex-managed worktree](/codex/app/worktrees#codex-managed-and-permanent-worktrees) | A temporary worktree Codex creates and manages for a thread. | App |
| [Compaction](/codex/prompting#context) | Summarizing older context so long-running work can continue. | App, CLI, IDE extension, Cloud |
| [Compliance API](/codex/enterprise/governance#compliance-api) | API for exporting Codex activity and audit metadata. | Enterprise |
| [Computer use](/codex/app/computer-use) | App capability that lets Codex interact with desktop applications through the UI. | App |
| [config.toml](/codex/config-reference#configtoml) | Local Codex configuration files. | App, CLI, IDE extension |
| [Connected host](/codex/remote-connections#what-comes-from-the-connected-host) | Computer or development environment that provides files, tools, and shell access for remote Codex work. | App, Mobile |
| [Connector](/codex/plugins) | App integration that lets Codex access external services. Available through plugins; also called apps. | App, Cloud |
| [Container cache](/codex/cloud/environments#container-caching) | Saved cloud container state reused to speed up future tasks. | Cloud |
| [Context](/codex/prompting#context) | Information Codex can use while working, such as files, prior messages, tool output, and instructions. | App, CLI, IDE extension, Cloud, SDK |
| [Context window](/api/docs/guides/conversation-state#managing-the-context-window) | The maximum amount of information the model can consider at once. | App, CLI, IDE extension, Cloud, SDK |
| [Custom agent](/codex/subagents#custom-agents) | User-defined agent role with its own instructions and settings. | App, CLI |
| [Deny-read rule](/codex/permissions#deny-reads-with-exact-paths-or-globs) | Filesystem permission rule that prevents Codex from reading sensitive paths or glob matches. | App, CLI, IDE extension, Enterprise |
| [Diff](/codex/app/review#what-changes-it-shows) | Set of Git file changes shown for inspection, comments, staging, or reverting. | App, Git, Review |
| [Domain allowlist](/codex/cloud/internet-access#domain-allowlist) | Set of domains Codex cloud can reach when agent internet access is enabled. | Cloud |
| [Environment (local)](/codex/app/local-environments) | App configuration to tell Codex how to set up worktrees for a project. | App, Worktree |
| [Environment variable](/codex/cloud/environments#environment-variables-and-secrets) | Runtime configuration value available during task execution. | Cloud, CLI, IDE extension |
| [Ephemeral session](/codex/noninteractive#basic-usage) | Non-interactive run that skips saving session state after it completes. | CLI |
| [Fast mode](/codex/speed#fast-mode) | Speed setting that makes supported models respond faster at a higher credit cost. | CLI, IDE extension |
| [Filesystem permission](/codex/permissions#filesystem-permissions) | Permission profile rule that grants or denies read and write access to paths. | App, CLI, IDE extension |
| [Finding](/codex/app/automations#managing-tasks) | A notable result or issue surfaced by an automation. | App |
| [Full access](/codex/concepts/sandboxing#configure-defaults) | Mode where Codex runs without normal sandbox restrictions. | App, CLI, IDE extension |
| [Git worktree](/codex/app/worktrees#whats-a-worktree) | A second checkout of the same repository for parallel branch work. | App, Git |
| [Handoff](/codex/app/worktrees#working-between-local-and-worktree) | Moving a thread and its work between Local and Worktree. | App |
| [Heartbeat](/codex/app/automations#thread-automations) | A recurring thread wake-up that returns Codex to the same conversation on a schedule. Also called a thread automation. | App |
| [Hook](/codex/hooks) | A lifecycle handler that runs when a Codex event matches, such as tool use, permission requests, or when a turn stops. | App, CLI, IDE extension |
| [Hook event](/codex/hooks#config-shape) | Lifecycle point where configured hook handlers can run. | App, CLI, IDE extension |
| [Hunk](/codex/app/review#staging-and-reverting-files) | Contiguous section of a diff that can be staged, unstaged, or reverted independently. | App, Git, Review |
| [Inline comment](/codex/app/review#inline-comments-for-feedback) | Line-specific feedback attached to a diff. | App |
| [Live web search](/codex/config-basic#web-search-mode) | Real-time web lookup for current information. | App, CLI, IDE extension |
| [Local](/codex/app/worktrees#working-between-local-and-worktree) | Mode where Codex works on the user's computer. | App, CLI, IDE extension |
| [Local thread](/codex/prompting#threads) | A thread that runs on the user's machine. | App, CLI, IDE extension |
| [Maintenance script](/codex/cloud/environments#container-caching) | Optional script run when a cached cloud container resumes. | Cloud |
| [Managed configuration](/codex/enterprise/managed-configuration) | Organization-controlled Codex defaults and restrictions. | Enterprise |
| [MCP](/codex/mcp) | Model Context Protocol, a standard for connecting Codex to external tools and context. | App, CLI, IDE extension |
| [MCP resource](/codex/mcp#supported-mcp-features) | Readable context exposed by an MCP server for Codex to inspect. | App, CLI, IDE extension |
| [MCP server](/codex/mcp#supported-mcp-features) | External tool or context provider exposed through MCP. | App, CLI, IDE extension |
| [MCP tool](/codex/mcp#supported-mcp-features) | Action exposed by an MCP server that Codex can call during a task. | App, CLI, IDE extension |
| [MDM](/codex/enterprise/managed-configuration#macos-managed-preferences-mdm) | Mobile device management tooling for distributing device profiles and managed Codex settings. | Enterprise |
| [Memories](/codex/memories) | Locally stored context Codex can reuse across sessions. | App, CLI, IDE extension |
| [Model](/codex/models) | The AI model Codex uses for reasoning and tool work. | App, CLI, IDE extension, Cloud, SDK |
| [Network access](/codex/agent-approvals-security#network-access-) | Permission for commands or environments to reach the internet. | App, CLI, IDE extension, Cloud |
| [Network policy](/codex/agent-approvals-security#network-policy) | Domain-based allow and deny rules that constrain sandboxed outbound network traffic. | App, CLI, IDE extension |
| [Non-interactive mode](/codex/noninteractive) | CLI mode for running Codex from scripts or CI. | CLI |
| [Output schema](/codex/noninteractive#create-structured-outputs-with-a-schema) | JSON Schema passed to `codex exec` to constrain the final response. | CLI |
| [Permanent worktree](/codex/app/worktrees#codex-managed-and-permanent-worktrees) | A long-lived worktree kept as its own project. | App |
| [Permission profile](/codex/permissions#define-and-select-a-profile) | Named least-privilege policy that combines filesystem and network rules for local command execution. | App, CLI, IDE extension |
| [Plan](/codex/learn/best-practices#plan-first-for-difficult-tasks) | Codex's proposed or tracked steps for completing a task. | App, CLI, IDE extension, Cloud |
| [Plugin](/codex/plugins) | Installable bundle that can distribute skills, tools, and integrations. | App, CLI, IDE extension |
| [Plugin manifest](/codex/plugins/build#plugin-structure) | Plugin metadata file that identifies a plugin and points to bundled skills, apps, MCP servers, hooks, and metadata. | App, CLI, IDE extension, Plugins |
| [Prefix rule](/codex/rules#understand-the-rules-language) | Command-rule pattern that allows, prompts for, or forbids matching command prefixes. | App, CLI, IDE extension, Enterprise |
| [Profile](/codex/config-advanced#profiles) | Named configuration preset for Codex. | CLI, IDE extension |
| [Progressive disclosure](/codex/skills) | Loading skill details only when needed to preserve context. | App, CLI, IDE extension |
| [Project](/codex/app/features#multitask-across-projects) | A selected codebase or folder Codex works in. | App |
| [Prompt](/codex/prompting) | The user instruction or request sent to Codex. | App, CLI, IDE extension, Cloud, SDK |
| [Pull request review](/codex/app/review#pull-request-reviews) | Codex review of changes or feedback on a pull request. | App, CLI, GitHub |
| [RBAC](/codex/enterprise/admin-setup#step-2-set-up-custom-roles-rbac) | Role-based access control for workspace permissions. | Enterprise |
| [Read-only mode](/codex/concepts/sandboxing) | Mode where Codex can inspect but not modify without approval. | App, CLI, IDE extension |
| [Reasoning effort](/codex/config-basic#reasoning-effort) | Setting that controls how much reasoning budget a model uses. | App, CLI, IDE extension, SDK |
| [Remote connection](/codex/remote-connections) | Connection that lets Codex work from another device using a connected host. | App, Mobile |
| [requirements.toml](/codex/config-reference#requirementstoml) | Admin-enforced requirements file for managed Codex setups. | Enterprise |
| [Review pane](/codex/app/review) | App view for inspecting diffs, comments, and Git changes. | App |
| [Rules](/codex/rules) | Policies that allow, prompt for, or deny command prefixes or permission exceptions. | App, CLI, IDE extension |
| [Sandbox](/codex/concepts/sandboxing) | Enforced boundary limiting what Codex commands can access or modify. | App, CLI, IDE extension |
| [Sandbox mode](/codex/config-basic#sandbox-level) | Configuration that defines Codex's filesystem and network limits. | App, CLI, IDE extension |
| [Sandbox preset](/codex/sdk#sandbox-presets) | SDK shorthand for common sandbox policies such as read-only, workspace-write, or full access. | SDK |
| [Schedule](/codex/app/automations) | The timing rule for an automation. | App |
| [Secret](/codex/cloud/environments#environment-variables-and-secrets) | Encrypted value available to setup scripts but removed before the agent phase. | Cloud |
| [Setup script](/codex/app/local-environments#setup-scripts) | Script run before the agent starts to install dependencies or prepare tools. | App worktrees |
| [Skill](/codex/skills) | Reusable workflow package with instructions and optional scripts or references. | App, CLI, IDE extension |
| [Skill invocation](/codex/skills#how-codex-uses-skills) | Explicit or implicit activation of a skill. | App, CLI, IDE extension |
| [Slash command](/codex/cli/slash-commands) | Command entered with a leading slash to control or inspect a Codex CLI session. | CLI |
| [Standalone automation](/codex/app/automations) | Independent scheduled run that reports separate findings. | App |
| [STDIO MCP server](/codex/mcp#stdio-servers) | MCP server launched as a local process by a configured command and arguments. | CLI, IDE extension |
| [Streamable HTTP MCP server](/codex/mcp#streamable-http-servers) | MCP server reached over HTTP, optionally with bearer token or OAuth authentication. | CLI, IDE extension |
| [Subagent](/codex/concepts/subagents) | Specialized child agent spawned to work on part of a task. | App, CLI |
| [Subagent workflow](/codex/concepts/subagents#core-terms) | Workflow where Codex runs delegated agents in parallel and combines their results. | App, CLI |
| [Task](/codex/app/automations#managing-tasks) | The unit of work Codex is asked to complete. | App, CLI, IDE extension, Cloud, SDK |
| [Thread](/codex/prompting#threads) | A single Codex session containing prompts, model output, and tool activity. | App, CLI, IDE extension, Cloud, SDK |
| [Thread automation](/codex/app/automations#thread-automations) | Recurring wake-up attached to an existing thread. Also called a heartbeat. | App |
| [Thread fork](/codex/app-server#start-or-resume-a-thread) | New thread branched from the stored history of an existing thread. | App-server, SDK |
| [Turn](/codex/app-server#core-primitives) | One exchange in a thread, usually a user prompt plus Codex's response and actions. | App, CLI, IDE extension, Cloud, SDK |
| [Universal image](/codex/cloud/environments#default-universal-image) | Default Codex cloud container image with common tools preinstalled. | Cloud |
| [Web search cache](/codex/config-basic#web-search-mode) | Pre-indexed search results Codex can use without live browsing. | App, CLI, IDE extension |
| [Worktree](/codex/app/worktrees) | Mode where Codex isolates changes in a separate Git worktree. | App |
| [Writable roots](/codex/agent-approvals-security#protected-paths-in-writable-roots) | Directories Codex is allowed to modify. | App, CLI, IDE extension |

Term

[Agent](/codex)

Definition

The Codex worker that reasons over context, uses tools, and completes a task.

Applies to

App, CLI, IDE extension, Cloud

Term

[AGENTS.md](/codex/guides/agents-md)

Definition

Repository or user guidance file that gives Codex persistent instructions.

Applies to

App, CLI, IDE extension, Cloud

Term

[Analytics dashboard](/codex/enterprise/governance#analytics-dashboard)

Definition

Admin view for Codex usage, adoption, and code review metrics.

Applies to

Enterprise

Term

[API key sign-in](/codex/auth#sign-in-with-an-api-key)

Definition

Authentication using an OpenAI API key.

Applies to

App, CLI, IDE extension

Term

[Approval policy](/codex/agent-approvals-security#sandbox-and-approvals)

Definition

Rules for when Codex must ask before taking an action.

Applies to

App, CLI, IDE extension

Term

[Approval request](/codex/agent-approvals-security#automatic-approval-reviews)

Definition

Codex asking to allow a restricted action.

Applies to

App, CLI, IDE extension

Term

[Apps (connectors)](/codex/plugins)

Definition

Integration that lets Codex access external services. Available through plugins; also called connectors.

Applies to

App, CLI, IDE extension

Term

[Appshot](/codex/appshots)

Definition

Snapshot of the frontmost app window sent to a Codex thread.

Applies to

App

Term

[Auth cache](/codex/auth#login-caching)

Definition

Locally stored login credentials reused by Codex.

Applies to

App, CLI, IDE extension

Term

[Automatic approval review](/codex/agent-approvals-security#automatic-approval-reviews)

Definition

Model-based review of eligible approval requests before they proceed.

Applies to

App, CLI, IDE extension

Term

[Automation](/codex/app/automations)

Definition

A scheduled or recurring Codex task.

Applies to

App

Term

[Automation run](/codex/app/automations#managing-tasks)

Definition

One execution of a scheduled automation that may report findings or archive itself.

Applies to

App

Term

[Browser use](/codex/app/browser#browser-use)

Definition

App capability that lets Codex operate the in-app browser directly.

Applies to

App

Term

[Chat](/codex/app/features#chats)

Definition

A Codex conversation not tied to a project.

Applies to

App

Term

[ChatGPT sign-in](/codex/auth#sign-in-with-chatgpt)

Definition

Authentication using a ChatGPT account and workspace permissions.

Applies to

App, CLI, IDE extension, Cloud

Term

[Chronicle](/codex/memories/chronicle)

Definition

Opt-in feature that builds memories from recent screen context.

Applies to

App

Term

[Cloud](/codex/cloud)

Definition

Mode where Codex works remotely in an OpenAI-managed environment.

Applies to

App, IDE extension, Web

Term

[Cloud environment](/codex/cloud/environments)

Definition

Configured container setup used for Codex cloud tasks.

Applies to

Cloud

Term

[Cloud task](/codex/cloud/environments#how-codex-cloud-tasks-run)

Definition

A remotely executed Codex task that runs in a cloud environment.

Applies to

Cloud

Term

[Cloud thread](/codex/prompting#threads)

Definition

A thread that runs in a Codex cloud environment.

Applies to

Cloud

Term

[Codex](/codex)

Definition

OpenAI's coding agent for software development tasks.

Applies to

App, CLI, IDE extension, Web, Cloud, SDK

Term

[Codex app](/codex/app)

Definition

Desktop app for running Codex threads in parallel, with built-in worktree support, automations, and Git functionality.

Applies to

Desktop

Term

[Codex app-server](/codex/app-server)

Definition

Local JSON-RPC server for embedding Codex threads, turns, approvals, history, and streamed events in custom clients.

Applies to

App, IDE extension, SDK

Term

[Codex CLI](/codex/cli)

Definition

Terminal client for running Codex interactively or in scripts.

Applies to

Terminal

Term

[Codex cloud](/codex/cloud)

Definition

OpenAI-managed execution environment where Codex can work on repository tasks remotely.

Applies to

Web, App, IDE extension

Term

[codex exec](/codex/noninteractive)

Definition

CLI command for running Codex non-interactively from scripts or CI.

Applies to

CLI

Term

[Codex IDE extension](/codex/ide)

Definition

Editor integration for using Codex inside IDEs like VS Code, JetBrains IDEs, Cursor, and Windsurf.

Applies to

IDE

Term

[Codex SDK](/codex/sdk)

Definition

Programmatic interface for building Codex-powered workflows or integrations.

Applies to

SDK

Term

[Codex web](/codex/cloud)

Definition

Browser-based Codex surface for delegating cloud tasks.

Applies to

Browser

Term

[Codex-managed worktree](/codex/app/worktrees#codex-managed-and-permanent-worktrees)

Definition

A temporary worktree Codex creates and manages for a thread.

Applies to

App

Term

[Compaction](/codex/prompting#context)

Definition

Summarizing older context so long-running work can continue.

Applies to

App, CLI, IDE extension, Cloud

Term

[Compliance API](/codex/enterprise/governance#compliance-api)

Definition

API for exporting Codex activity and audit metadata.

Applies to

Enterprise

Term

[Computer use](/codex/app/computer-use)

Definition

App capability that lets Codex interact with desktop applications through the UI.

Applies to

App

Term

[config.toml](/codex/config-reference#configtoml)

Definition

Local Codex configuration files.

Applies to

App, CLI, IDE extension

Term

[Connected host](/codex/remote-connections#what-comes-from-the-connected-host)

Definition

Computer or development environment that provides files, tools, and shell access for remote Codex work.

Applies to

App, Mobile

Term

[Connector](/codex/plugins)

Definition

App integration that lets Codex access external services. Available through plugins; also called apps.

Applies to

App, Cloud

Term

[Container cache](/codex/cloud/environments#container-caching)

Definition

Saved cloud container state reused to speed up future tasks.

Applies to

Cloud

Term

[Context](/codex/prompting#context)

Definition

Information Codex can use while working, such as files, prior messages, tool output, and instructions.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Context window](/api/docs/guides/conversation-state#managing-the-context-window)

Definition

The maximum amount of information the model can consider at once.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Custom agent](/codex/subagents#custom-agents)

Definition

User-defined agent role with its own instructions and settings.

Applies to

App, CLI

Term

[Deny-read rule](/codex/permissions#deny-reads-with-exact-paths-or-globs)

Definition

Filesystem permission rule that prevents Codex from reading sensitive paths or glob matches.

Applies to

App, CLI, IDE extension, Enterprise

Term

[Diff](/codex/app/review#what-changes-it-shows)

Definition

Set of Git file changes shown for inspection, comments, staging, or reverting.

Applies to

App, Git, Review

Term

[Domain allowlist](/codex/cloud/internet-access#domain-allowlist)

Definition

Set of domains Codex cloud can reach when agent internet access is enabled.

Applies to

Cloud

Term

[Environment (local)](/codex/app/local-environments)

Definition

App configuration to tell Codex how to set up worktrees for a project.

Applies to

App, Worktree

Term

[Environment variable](/codex/cloud/environments#environment-variables-and-secrets)

Definition

Runtime configuration value available during task execution.

Applies to

Cloud, CLI, IDE extension

Term

[Ephemeral session](/codex/noninteractive#basic-usage)

Definition

Non-interactive run that skips saving session state after it completes.

Applies to

CLI

Term

[Fast mode](/codex/speed#fast-mode)

Definition

Speed setting that makes supported models respond faster at a higher credit cost.

Applies to

CLI, IDE extension

Term

[Filesystem permission](/codex/permissions#filesystem-permissions)

Definition

Permission profile rule that grants or denies read and write access to paths.

Applies to

App, CLI, IDE extension

Term

[Finding](/codex/app/automations#managing-tasks)

Definition

A notable result or issue surfaced by an automation.

Applies to

App

Term

[Full access](/codex/concepts/sandboxing#configure-defaults)

Definition

Mode where Codex runs without normal sandbox restrictions.

Applies to

App, CLI, IDE extension

Term

[Git worktree](/codex/app/worktrees#whats-a-worktree)

Definition

A second checkout of the same repository for parallel branch work.

Applies to

App, Git

Term

[Handoff](/codex/app/worktrees#working-between-local-and-worktree)

Definition

Moving a thread and its work between Local and Worktree.

Applies to

App

Term

[Heartbeat](/codex/app/automations#thread-automations)

Definition

A recurring thread wake-up that returns Codex to the same conversation on a schedule. Also called a thread automation.

Applies to

App

Term

[Hook](/codex/hooks)

Definition

A lifecycle handler that runs when a Codex event matches, such as tool use, permission requests, or when a turn stops.

Applies to

App, CLI, IDE extension

Term

[Hook event](/codex/hooks#config-shape)

Definition

Lifecycle point where configured hook handlers can run.

Applies to

App, CLI, IDE extension

Term

[Hunk](/codex/app/review#staging-and-reverting-files)

Definition

Contiguous section of a diff that can be staged, unstaged, or reverted independently.

Applies to

App, Git, Review

Term

[Inline comment](/codex/app/review#inline-comments-for-feedback)

Definition

Line-specific feedback attached to a diff.

Applies to

App

Term

[Live web search](/codex/config-basic#web-search-mode)

Definition

Real-time web lookup for current information.

Applies to

App, CLI, IDE extension

Term

[Local](/codex/app/worktrees#working-between-local-and-worktree)

Definition

Mode where Codex works on the user's computer.

Applies to

App, CLI, IDE extension

Term

[Local thread](/codex/prompting#threads)

Definition

A thread that runs on the user's machine.

Applies to

App, CLI, IDE extension

Term

[Maintenance script](/codex/cloud/environments#container-caching)

Definition

Optional script run when a cached cloud container resumes.

Applies to

Cloud

Term

[Managed configuration](/codex/enterprise/managed-configuration)

Definition

Organization-controlled Codex defaults and restrictions.

Applies to

Enterprise

Term

[MCP](/codex/mcp)

Definition

Model Context Protocol, a standard for connecting Codex to external tools and context.

Applies to

App, CLI, IDE extension

Term

[MCP resource](/codex/mcp#supported-mcp-features)

Definition

Readable context exposed by an MCP server for Codex to inspect.

Applies to

App, CLI, IDE extension

Term

[MCP server](/codex/mcp#supported-mcp-features)

Definition

External tool or context provider exposed through MCP.

Applies to

App, CLI, IDE extension

Term

[MCP tool](/codex/mcp#supported-mcp-features)

Definition

Action exposed by an MCP server that Codex can call during a task.

Applies to

App, CLI, IDE extension

Term

[MDM](/codex/enterprise/managed-configuration#macos-managed-preferences-mdm)

Definition

Mobile device management tooling for distributing device profiles and managed Codex settings.

Applies to

Enterprise

Term

[Memories](/codex/memories)

Definition

Locally stored context Codex can reuse across sessions.

Applies to

App, CLI, IDE extension

Term

[Model](/codex/models)

Definition

The AI model Codex uses for reasoning and tool work.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Network access](/codex/agent-approvals-security#network-access-)

Definition

Permission for commands or environments to reach the internet.

Applies to

App, CLI, IDE extension, Cloud

Term

[Network policy](/codex/agent-approvals-security#network-policy)

Definition

Domain-based allow and deny rules that constrain sandboxed outbound network traffic.

Applies to

App, CLI, IDE extension

Term

[Non-interactive mode](/codex/noninteractive)

Definition

CLI mode for running Codex from scripts or CI.

Applies to

CLI

Term

[Output schema](/codex/noninteractive#create-structured-outputs-with-a-schema)

Definition

JSON Schema passed to `codex exec` to constrain the final response.

Applies to

CLI

Term

[Permanent worktree](/codex/app/worktrees#codex-managed-and-permanent-worktrees)

Definition

A long-lived worktree kept as its own project.

Applies to

App

Term

[Permission profile](/codex/permissions#define-and-select-a-profile)

Definition

Named least-privilege policy that combines filesystem and network rules for local command execution.

Applies to

App, CLI, IDE extension

Term

[Plan](/codex/learn/best-practices#plan-first-for-difficult-tasks)

Definition

Codex's proposed or tracked steps for completing a task.

Applies to

App, CLI, IDE extension, Cloud

Term

[Plugin](/codex/plugins)

Definition

Installable bundle that can distribute skills, tools, and integrations.

Applies to

App, CLI, IDE extension

Term

[Plugin manifest](/codex/plugins/build#plugin-structure)

Definition

Plugin metadata file that identifies a plugin and points to bundled skills, apps, MCP servers, hooks, and metadata.

Applies to

App, CLI, IDE extension, Plugins

Term

[Prefix rule](/codex/rules#understand-the-rules-language)

Definition

Command-rule pattern that allows, prompts for, or forbids matching command prefixes.

Applies to

App, CLI, IDE extension, Enterprise

Term

[Profile](/codex/config-advanced#profiles)

Definition

Named configuration preset for Codex.

Applies to

CLI, IDE extension

Term

[Progressive disclosure](/codex/skills)

Definition

Loading skill details only when needed to preserve context.

Applies to

App, CLI, IDE extension

Term

[Project](/codex/app/features#multitask-across-projects)

Definition

A selected codebase or folder Codex works in.

Applies to

App

Term

[Prompt](/codex/prompting)

Definition

The user instruction or request sent to Codex.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Pull request review](/codex/app/review#pull-request-reviews)

Definition

Codex review of changes or feedback on a pull request.

Applies to

App, CLI, GitHub

Term

[RBAC](/codex/enterprise/admin-setup#step-2-set-up-custom-roles-rbac)

Definition

Role-based access control for workspace permissions.

Applies to

Enterprise

Term

[Read-only mode](/codex/concepts/sandboxing)

Definition

Mode where Codex can inspect but not modify without approval.

Applies to

App, CLI, IDE extension

Term

[Reasoning effort](/codex/config-basic#reasoning-effort)

Definition

Setting that controls how much reasoning budget a model uses.

Applies to

App, CLI, IDE extension, SDK

Term

[Remote connection](/codex/remote-connections)

Definition

Connection that lets Codex work from another device using a connected host.

Applies to

App, Mobile

Term

[requirements.toml](/codex/config-reference#requirementstoml)

Definition

Admin-enforced requirements file for managed Codex setups.

Applies to

Enterprise

Term

[Review pane](/codex/app/review)

Definition

App view for inspecting diffs, comments, and Git changes.

Applies to

App

Term

[Rules](/codex/rules)

Definition

Policies that allow, prompt for, or deny command prefixes or permission exceptions.

Applies to

App, CLI, IDE extension

Term

[Sandbox](/codex/concepts/sandboxing)

Definition

Enforced boundary limiting what Codex commands can access or modify.

Applies to

App, CLI, IDE extension

Term

[Sandbox mode](/codex/config-basic#sandbox-level)

Definition

Configuration that defines Codex's filesystem and network limits.

Applies to

App, CLI, IDE extension

Term

[Sandbox preset](/codex/sdk#sandbox-presets)

Definition

SDK shorthand for common sandbox policies such as read-only, workspace-write, or full access.

Applies to

SDK

Term

[Schedule](/codex/app/automations)

Definition

The timing rule for an automation.

Applies to

App

Term

[Secret](/codex/cloud/environments#environment-variables-and-secrets)

Definition

Encrypted value available to setup scripts but removed before the agent phase.

Applies to

Cloud

Term

[Setup script](/codex/app/local-environments#setup-scripts)

Definition

Script run before the agent starts to install dependencies or prepare tools.

Applies to

App worktrees

Term

[Skill](/codex/skills)

Definition

Reusable workflow package with instructions and optional scripts or references.

Applies to

App, CLI, IDE extension

Term

[Skill invocation](/codex/skills#how-codex-uses-skills)

Definition

Explicit or implicit activation of a skill.

Applies to

App, CLI, IDE extension

Term

[Slash command](/codex/cli/slash-commands)

Definition

Command entered with a leading slash to control or inspect a Codex CLI session.

Applies to

CLI

Term

[Standalone automation](/codex/app/automations)

Definition

Independent scheduled run that reports separate findings.

Applies to

App

Term

[STDIO MCP server](/codex/mcp#stdio-servers)

Definition

MCP server launched as a local process by a configured command and arguments.

Applies to

CLI, IDE extension

Term

[Streamable HTTP MCP server](/codex/mcp#streamable-http-servers)

Definition

MCP server reached over HTTP, optionally with bearer token or OAuth authentication.

Applies to

CLI, IDE extension

Term

[Subagent](/codex/concepts/subagents)

Definition

Specialized child agent spawned to work on part of a task.

Applies to

App, CLI

Term

[Subagent workflow](/codex/concepts/subagents#core-terms)

Definition

Workflow where Codex runs delegated agents in parallel and combines their results.

Applies to

App, CLI

Term

[Task](/codex/app/automations#managing-tasks)

Definition

The unit of work Codex is asked to complete.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Thread](/codex/prompting#threads)

Definition

A single Codex session containing prompts, model output, and tool activity.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Thread automation](/codex/app/automations#thread-automations)

Definition

Recurring wake-up attached to an existing thread. Also called a heartbeat.

Applies to

App

Term

[Thread fork](/codex/app-server#start-or-resume-a-thread)

Definition

New thread branched from the stored history of an existing thread.

Applies to

App-server, SDK

Term

[Turn](/codex/app-server#core-primitives)

Definition

One exchange in a thread, usually a user prompt plus Codex's response and actions.

Applies to

App, CLI, IDE extension, Cloud, SDK

Term

[Universal image](/codex/cloud/environments#default-universal-image)

Definition

Default Codex cloud container image with common tools preinstalled.

Applies to

Cloud

Term

[Web search cache](/codex/config-basic#web-search-mode)

Definition

Pre-indexed search results Codex can use without live browsing.

Applies to

App, CLI, IDE extension

Term

[Worktree](/codex/app/worktrees)

Definition

Mode where Codex isolates changes in a separate Git worktree.

Applies to

App

Term

[Writable roots](/codex/agent-approvals-security#protected-paths-in-writable-roots)

Definition

Directories Codex is allowed to modify.

Applies to

App, CLI, IDE extension

Expand to view all

