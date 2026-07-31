---
source_type: 'learn'
source_area: 'learn_changelog'
source_url: 'https://learn.chatgpt.com/docs/changelog'
source_kind: 'learn_html_fallback'
source_last_modified: '2026-07-31T06:46:04Z'
source_etag: 'W/"7cf5a0496e2368d4ece094fdfbfc8310"'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# ChatGPT & Codex changelog | ChatGPT Learn

Source: https://learn.chatgpt.com/docs/changelog

### New features

- Added rate-limit reset banking for Plus and Pro users, including one free
  reset at launch and
  [referral invitations](/codex/pricing#invite-friends-and-coworkers) for
  earning more during the current promotion. Eligible Business members can
  invite coworkers to earn shared workspace credits through a separate
  referral program.
- Added [Developer mode](/codex/browser?surface=app#app-developer-mode) for Browser use in
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

