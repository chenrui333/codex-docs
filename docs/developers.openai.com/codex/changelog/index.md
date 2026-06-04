---
source_type: 'developers'
source_area: 'codex_changelog'
source_url: 'https://developers.openai.com/codex/changelog'
source_last_modified: '2026-06-04T14:54:09Z'
source_etag: 'W/"8643f77c7ff47779a23ddfc9352c9fa4"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0"]
---

# Changelog – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/changelog

Codex is becoming a broader workspace for getting work done with AI. This
update makes it easier to start work with less setup, verify what Codex is
building, create richer outputs, and keep momentum across longer-running tasks.

#### Verify more of your work

The Codex app now includes an early [**in-app browser**](/codex/app/browser). You
can open local or public pages that don’t require sign-in, comment directly on
the rendered page, and ask Codex to address page-level feedback.

![Codex app showing a browser comment on a local web app preview](/images/codex/app/in-app-browser-light.webp)

[**Computer use**](/codex/app/computer-use) lets Codex operate macOS apps by seeing,
clicking, and typing, which helps with native app testing, simulator flows,
low-risk app settings, and GUI-only bugs.

The feature isn’t available in the European Economic Area, the United Kingdom, or
Switzerland at launch.

#### Start, follow, and steer work

[**Chats**](/codex/app/features#projectless-threads) are threads you can start
without choosing a project folder first. They’re useful for research, writing,
planning, analysis, source gathering, and tool-driven work that doesn’t begin in
a codebase.

For work that needs a later check-in,
[**thread automations**](/codex/app/automations#thread-automations) can wake up
the same thread on a schedule while preserving the conversation context. Use
them to check a long-running process, watch for updates, or continue a
follow-up loop without starting from scratch.

[**The task sidebar**](/codex/app/features#task-sidebar) makes plans, sources,
generated artifacts, and summaries easier to follow while Codex works.
[**Context-aware suggestions**](/codex/app/settings#context-aware-suggestions)
can also help you pick up relevant follow-ups when you start or return to Codex.

#### Stronger for software development

Codex now brings more of the **pull request workflow** into the app. You can
inspect [**GitHub pull requests**](/codex/app/review#pull-request-reviews) in the
sidebar, review comments in the diff, review changed files, then ask Codex to
explain feedback, make changes, check them, and keep the review moving.

#### Review richer outputs

The [**artifact viewer**](/codex/app/features#artifact-viewer) can preview
generated files such as PDF files, spreadsheets, documents, and presentations in
the sidebar before you commit or share them. [**Memories**](/codex/memories),
where available, can also carry useful context from past tasks into future
threads, including stable preferences, project conventions, and recurring work
patterns.

#### Other features

- [Remote connections](/codex/remote-connections) - We are gradually rolling out SSH remote connections in alpha
- Support for [multiple terminals](/codex/app/features#integrated-terminal)
- macOS menu bar and [Windows system tray](/codex/app/windows) support
- [Multi-window support](/codex/app/features#floating-pop-out-window)
- [Intel Mac support](/codex/app)
- [New plugins](/codex/plugins)
- Improved thread and tool rendering

