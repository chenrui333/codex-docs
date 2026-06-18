---
source_type: 'developers'
source_area: 'codex_changelog'
source_url: 'https://developers.openai.com/codex/changelog'
source_last_modified: '2026-06-18T18:36:04Z'
source_etag: 'W/"14bb3eafd3bb2dcfadc479f1c1bd03f5"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Changelog – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/changelog

### New features

- Added rate-limit reset banking for Plus and Pro users, including one free
  reset at launch and
  [referral invitations](/codex/pricing#invite-friends-and-coworkers) for
  earning more during the current promotion. Eligible Business members can
  invite coworkers to earn shared workspace credits through a separate
  referral program.
- Added [Developer mode](/codex/app/browser#developer-mode) for Browser use in
  Chrome and the Codex in-app browser. It gives Codex controlled Chrome
  DevTools Protocol (CDP) access for performance profiling and deeper debugging
  of network traffic, console output, runtime errors, and page state.
- Added the `/init` command to the app composer for creating project
  instructions with the same initialization workflow as the Codex CLI.
- Added customizable macOS Dock icons with light and dark Codex variants.
- Added Computer Use for Enterprise users outside the European Economic Area,
  the United Kingdom, and Switzerland.
- Added support for configuring per-app access controls for Computer Use on
  Windows.
- Added an **Unread chats** section to the command menu, with the most recently
  updated unread chat selected by default.

### Performance improvements and bug fixes

- Made Browser use up to 2x faster through CDP and DOM snapshot optimizations
  that reduce browser round trips.
- Made command, browser, integration, and source activity summaries easier to
  understand, and improved how completed chats present files, automations, and
  other durable output.
- Improved plugin management by including workspace plugins, refreshing plugin
  state more reliably after installation or removal, and letting you upload a
  new version of an already-shared plugin without changing its access.
- Improved usage-limit errors with inline plan and workspace guidance,
  including reset timing when available.
- Added `Cmd`+`Enter` and `Ctrl`+`Enter` as
  shortcuts for submitting custom approval feedback.
- Fixed Browser use download handling and improved Developer mode recovery and
  diagnostics.
- Fixed scheduled automations so they honor the selected approval mode, and
  fixed manual project ordering, Browser tab dragging, MCP app sizing after
  right-pane transitions, and clickable ChatGPT thread mentions.
- Fixed issues affecting background agent tab restoration, commit and pull
  request message generation, sidebar pull request status updates, Codex Mobile
  QR pairing, remote-control MFA, remote SSH installation and connection,
  updater prompts, and overlay positioning at non-default zoom levels.
- Additional performance improvements and bug fixes.

