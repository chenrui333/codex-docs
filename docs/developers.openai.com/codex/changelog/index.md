# Codex changelog

Source: https://developers.openai.com/codex/changelog

Latest updates to Codex, OpenAI’s coding agent

[All updates](/codex/changelog)  [General](/codex/changelog?type=general)  [Codex app](/codex/changelog?type=codex-app)  [Codex CLI](/codex/changelog?type=codex-cli)

[February 2026](#month-2026-02)  [January 2026](#month-2026-01)  [December 2025](#month-2025-12)  [November 2025](#month-2025-11)  [October 2025](#month-2025-10)  [September 2025](#month-2025-09)  [August 2025](#month-2025-08)  [June 2025](#month-2025-06)  [May 2025](#month-2025-05)

## February 2026

- 2026-02-18

  ### Codex CLI 0.104.0

  ```
  $ npm install -g @openai/codex@0.104.0
  ```

    View details

  ## New Features

  - Added `WS_PROXY`/`WSS_PROXY` environment support (including lowercase variants) for websocket proxying in the network proxy. ([#11784](https://github.com/openai/codex/pull/11784))
  - App-server v2 now emits notifications when threads are archived or unarchived, enabling clients to react without polling. ([#12030](https://github.com/openai/codex/pull/12030))
  - Protocol/core now carry distinct approval IDs for command approvals to support multiple approvals within a single shell command execution flow. ([#12051](https://github.com/openai/codex/pull/12051))

  ## Bug Fixes

  - `Ctrl+C`/`Ctrl+D` now cleanly exits the cwd-change prompt during resume/fork flows instead of implicitly selecting an option. ([#12040](https://github.com/openai/codex/pull/12040))
  - Reduced false-positive safety-check downgrade behavior by relying on the response header model (and websocket top-level events) rather than the response body model slug. ([#12061](https://github.com/openai/codex/pull/12061))

  ## Documentation

  - Updated docs and schemas to cover websocket proxy configuration, new thread archive/unarchive notifications, and the command approval ID plumbing. ([#11784](https://github.com/openai/codex/pull/11784), [#12030](https://github.com/openai/codex/pull/12030), [#12051](https://github.com/openai/codex/pull/12051))

  ## Chores

  - Made the Rust release workflow resilient to `npm publish` attempts for an already-published version. ([#12044](https://github.com/openai/codex/pull/12044))
  - Standardized remote compaction test mocking and refreshed related snapshots to align with the default production-shaped behavior. ([#12050](https://github.com/openai/codex/pull/12050))

  ## Changelog

  Full Changelog: [rust-v0.103.0...rust-v0.104.0](https://github.com/openai/codex/compare/rust-v0.103.0...rust-v0.104.0)

  - [#11784](https://github.com/openai/codex/pull/11784) feat(network-proxy): add websocket proxy env support [@viyatb-oai](https://github.com/viyatb-oai)
  - [#12044](https://github.com/openai/codex/pull/12044) don't fail if an npm publish attempt is for an existing version. [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#12040](https://github.com/openai/codex/pull/12040) tui: exit session on Ctrl+C in cwd change prompt [@charley-oai](https://github.com/charley-oai)
  - [#12030](https://github.com/openai/codex/pull/12030) app-server: Emit thread archive/unarchive notifications [@euroelessar](https://github.com/euroelessar)
  - [#12061](https://github.com/openai/codex/pull/12061) Chore: remove response model check and rely on header model for downgrade [@shijie-oai](https://github.com/shijie-oai)
  - [#12051](https://github.com/openai/codex/pull/12051) feat(core): plumb distinct approval ids for command approvals [@owenlin0](https://github.com/owenlin0)
  - [#12050](https://github.com/openai/codex/pull/12050) Unify remote compaction snapshot mocks around default endpoint behavior [@charley-oai](https://github.com/charley-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.104.0)
- 2026-02-17

  ### Codex CLI 0.103.0

  ```
  $ npm install -g @openai/codex@0.103.0
  ```

    View details

  ## New Features

  - App listing responses now include richer app details (`app_metadata`, branding, and labels), so clients can render more complete app cards without extra requests. ([#11706](https://github.com/openai/codex/pull/11706))
  - Commit co-author attribution now uses a Codex-managed `prepare-commit-msg` hook, with `command_attribution` override support (default label, custom label, or disable). ([#11617](https://github.com/openai/codex/pull/11617))

  ## Bug Fixes

  - Removed the `remote_models` feature flag to prevent fallback model metadata when it was disabled, improving model selection reliability and performance. ([#11699](https://github.com/openai/codex/pull/11699))

  ## Chores

  - Updated Rust dependencies (`clap`, `env_logger`, `arc-swap`) and refreshed Bazel lock state as routine maintenance. ([#11888](https://github.com/openai/codex/pull/11888), [#11889](https://github.com/openai/codex/pull/11889), [#11890](https://github.com/openai/codex/pull/11890), [#12032](https://github.com/openai/codex/pull/12032))
  - Reverted the Rust toolchain bump to `1.93.1` after CI breakage. ([#11886](https://github.com/openai/codex/pull/11886), [#12035](https://github.com/openai/codex/pull/12035))

  ## Changelog

  Full Changelog: [rust-v0.102.0...rust-v0.103.0](https://github.com/openai/codex/compare/rust-v0.102.0...rust-v0.103.0)

  - [#11699](https://github.com/openai/codex/pull/11699) chore: rm remote models fflag [@sayan-oai](https://github.com/sayan-oai)
  - [#11706](https://github.com/openai/codex/pull/11706) [apps] Expose more fields from apps listing endpoints. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11890](https://github.com/openai/codex/pull/11890) chore(deps): bump arc-swap from 1.8.0 to 1.8.2 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#11886](https://github.com/openai/codex/pull/11886) chore(deps): bump rust-toolchain from 1.93.0 to 1.93.1 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#12032](https://github.com/openai/codex/pull/12032) chore: just bazel-lock-update [@bolinfest](https://github.com/bolinfest)
  - [#11888](https://github.com/openai/codex/pull/11888) chore(deps): bump clap from 4.5.56 to 4.5.58 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#11889](https://github.com/openai/codex/pull/11889) chore(deps): bump env\_logger from 0.11.8 to 0.11.9 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#11617](https://github.com/openai/codex/pull/11617) Use prompt-based co-author attribution with config override [@gabec-openai](https://github.com/gabec-openai)
  - [#12035](https://github.com/openai/codex/pull/12035) Revert "chore(deps): bump rust-toolchain from 1.93.0 to 1.93.1 in /co…dex-rs ([#11886](https://github.com/openai/codex/pull/11886))" [@etraut-openai](https://github.com/etraut-openai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.103.0)
- 2026-02-17

  ### Codex CLI 0.102.0

  ```
  $ npm install -g @openai/codex@0.102.0
  ```

    View details

  ## New Features

  - Added a more unified permissions flow, including clearer permissions history in the TUI and a slash command to grant sandbox read access when directories are blocked. ([#11633](https://github.com/openai/codex/pull/11633), [#11512](https://github.com/openai/codex/pull/11512), [#11550](https://github.com/openai/codex/pull/11550), [#11639](https://github.com/openai/codex/pull/11639))
  - Introduced structured network approval handling, with richer host/protocol context shown directly in approval prompts. ([#11672](https://github.com/openai/codex/pull/11672), [#11674](https://github.com/openai/codex/pull/11674))
  - Expanded app-server fuzzy file search with explicit session-complete signaling so clients can stop loading indicators reliably. ([#10268](https://github.com/openai/codex/pull/10268), [#11773](https://github.com/openai/codex/pull/11773))
  - Added customizable multi-agent roles via config, including migration toward the new multi-agent naming/config surface. ([#11917](https://github.com/openai/codex/pull/11917), [#11982](https://github.com/openai/codex/pull/11982), [#11939](https://github.com/openai/codex/pull/11939), [#11918](https://github.com/openai/codex/pull/11918))
  - Added a `model/rerouted` notification so clients can detect and render model reroute events explicitly. ([#12001](https://github.com/openai/codex/pull/12001))

  ## Bug Fixes

  - Fixed remote image attachments so they persist correctly across resume/backtrack and history replay in the TUI. ([#10590](https://github.com/openai/codex/pull/10590))
  - Fixed a TUI accessibility regression where animation gating for screen reader users was not consistently respected. ([#11860](https://github.com/openai/codex/pull/11860))
  - Fixed app-server thread resume behavior to correctly rejoin active in-memory threads and tighten invalid resume cases. ([#11756](https://github.com/openai/codex/pull/11756))
  - Fixed `model/list` output to return full model data plus visibility metadata, avoiding unintended server-side filtering. ([#11793](https://github.com/openai/codex/pull/11793))
  - Fixed several `js_repl` stability issues, including reset hangs, in-flight tool-call races, and a `view_image` panic path. ([#11932](https://github.com/openai/codex/pull/11932), [#11922](https://github.com/openai/codex/pull/11922), [#11800](https://github.com/openai/codex/pull/11800), [#11796](https://github.com/openai/codex/pull/11796))
  - Fixed app integration edge cases in mention parsing and app list loading/filtering behavior. ([#11894](https://github.com/openai/codex/pull/11894), [#11518](https://github.com/openai/codex/pull/11518), [#11697](https://github.com/openai/codex/pull/11697))

  ## Documentation

  - Updated contributor guidance to require snapshot coverage for user-visible TUI changes. ([#10669](https://github.com/openai/codex/pull/10669))
  - Updated docs/help text around Codex app and MCP command usage. ([#11926](https://github.com/openai/codex/pull/11926), [#11813](https://github.com/openai/codex/pull/11813))

  ## Chores

  - Improved developer log tooling with new `just log --search` and `just log --compact` modes. ([#11995](https://github.com/openai/codex/pull/11995), [#11994](https://github.com/openai/codex/pull/11994))
  - Updated vendored `rg` and tightened Bazel/Cargo lockfile sync checks to reduce dependency drift. ([#12007](https://github.com/openai/codex/pull/12007), [#11790](https://github.com/openai/codex/pull/11790))

  ## Changelog

  Full Changelog: [rust-v0.101.0...rust-v0.102.0](https://github.com/openai/codex/compare/rust-v0.101.0...rust-v0.102.0)

  - [#10268](https://github.com/openai/codex/pull/10268) app-server: add fuzzy search sessions for streaming file search [@nornagon-openai](https://github.com/nornagon-openai)
  - [#11547](https://github.com/openai/codex/pull/11547) Parse first order skill/connector mentions [@canvrno-oai](https://github.com/canvrno-oai)
  - [#11227](https://github.com/openai/codex/pull/11227) feat(app-server): experimental flag to persist extended history [@owenlin0](https://github.com/owenlin0)
  - [#10672](https://github.com/openai/codex/pull/10672) Add js\_repl host helpers and exec end events [@fjord-oai](https://github.com/fjord-oai)
  - [#11512](https://github.com/openai/codex/pull/11512) add a slash command to grant sandbox read access to inaccessible directories [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#11631](https://github.com/openai/codex/pull/11631) chore(core) Deprecate approval\_policy: on-failure [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11636](https://github.com/openai/codex/pull/11636) Better error message for model limit hit. [@xl-openai](https://github.com/xl-openai)
  - [#11633](https://github.com/openai/codex/pull/11633) feat: introduce Permissions [@bolinfest](https://github.com/bolinfest)
  - [#10669](https://github.com/openai/codex/pull/10669) docs: require insta snapshot coverage for UI changes [@joshka-oai](https://github.com/joshka-oai)
  - [#11645](https://github.com/openai/codex/pull/11645) fix: skip review\_start\_with\_detached\_delivery\_returns\_new\_thread\_id o… [@owenlin0](https://github.com/owenlin0)
  - [#11639](https://github.com/openai/codex/pull/11639) [feat] add seatbelt permission files [@celia-oai](https://github.com/celia-oai)
  - [#11622](https://github.com/openai/codex/pull/11622) Remove absolute path in rollout\_summary [@wendyjiao-openai](https://github.com/wendyjiao-openai)
  - [#10671](https://github.com/openai/codex/pull/10671) Add js\_repl\_tools\_only model and routing restrictions [@fjord-oai](https://github.com/fjord-oai)
  - [#11657](https://github.com/openai/codex/pull/11657) app-server tests: disable shell\_snapshot for review suite [@bolinfest](https://github.com/bolinfest)
  - [#11646](https://github.com/openai/codex/pull/11646) app-server: stabilize detached review start on Windows [@bolinfest](https://github.com/bolinfest)
  - [#11638](https://github.com/openai/codex/pull/11638) fix(app-server): surface more helpful errors for json-rpc [@owenlin0](https://github.com/owenlin0)
  - [#11417](https://github.com/openai/codex/pull/11417) [apps] Add is\_enabled to app info. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11630](https://github.com/openai/codex/pull/11630) Add new apps\_mcp\_gateway [@canvrno-oai](https://github.com/canvrno-oai)
  - [#11656](https://github.com/openai/codex/pull/11656) Persist complete TurnContextItem state via canonical conversion [@charley-oai](https://github.com/charley-oai)
  - [#11510](https://github.com/openai/codex/pull/11510) Remove git commands from dangerous command checks [@joshka-oai](https://github.com/joshka-oai)
  - [#11668](https://github.com/openai/codex/pull/11668) feat(shell-tool-mcp): add patched zsh build pipeline [@nornagon-openai](https://github.com/nornagon-openai)
  - [#11275](https://github.com/openai/codex/pull/11275) Added a test to verify that feature flags that are enabled by default are stable [@etraut-openai](https://github.com/etraut-openai)
  - [#11651](https://github.com/openai/codex/pull/11651) Add cwd as an optional field to thread/list [@acrognale-oai](https://github.com/acrognale-oai)
  - [#11660](https://github.com/openai/codex/pull/11660) chore(approvals) More approvals scenarios [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11518](https://github.com/openai/codex/pull/11518) [apps] Fix app loading logic. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11679](https://github.com/openai/codex/pull/11679) fix: dont show NUX for upgrade-target models that are hidden [@sayan-oai](https://github.com/sayan-oai)
  - [#11515](https://github.com/openai/codex/pull/11515) Point Codex App tooltip links to app landing page [@joshka-oai](https://github.com/joshka-oai)
  - [#11671](https://github.com/openai/codex/pull/11671) chore(core) Restrict model-suggested rules [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11703](https://github.com/openai/codex/pull/11703) fix(ci) lock rust toolchain at 1.93.0 to unblock [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11662](https://github.com/openai/codex/pull/11662) feat(network-proxy): structured policy signaling and attempt correlation to core [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11709](https://github.com/openai/codex/pull/11709) fix(shell-tool-mcp) build dependencies [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11618](https://github.com/openai/codex/pull/11618) feat: add token usage on memories [@jif-oai](https://github.com/jif-oai)
  - [#11722](https://github.com/openai/codex/pull/11722) Lower missing rollout log level [@jif-oai](https://github.com/jif-oai)
  - [#11712](https://github.com/openai/codex/pull/11712) chore: streamline phase 2 [@jif-oai](https://github.com/jif-oai)
  - [#11731](https://github.com/openai/codex/pull/11731) feat: memories config [@jif-oai](https://github.com/jif-oai)
  - [#11736](https://github.com/openai/codex/pull/11736) feat: increase windows workers stack [@jif-oai](https://github.com/jif-oai)
  - [#11739](https://github.com/openai/codex/pull/11739) feat: add slug in name [@jif-oai](https://github.com/jif-oai)
  - [#11745](https://github.com/openai/codex/pull/11745) chore: move explorer to spark [@jif-oai](https://github.com/jif-oai)
  - [#11748](https://github.com/openai/codex/pull/11748) Fix memories output schema requirements [@jif-oai](https://github.com/jif-oai)
  - [#11669](https://github.com/openai/codex/pull/11669) core: limit search\_tool\_bm25 to Apps and clarify discovery guidance [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#11755](https://github.com/openai/codex/pull/11755) app-server-test-client websocket client and thread tools [@maxj-oai](https://github.com/maxj-oai)
  - [#11663](https://github.com/openai/codex/pull/11663) fix: reduce flakiness of compact\_resume\_after\_second\_compaction\_preserves\_history [@bolinfest](https://github.com/bolinfest)
  - [#11667](https://github.com/openai/codex/pull/11667) sandbox NUX metrics update [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#11695](https://github.com/openai/codex/pull/11695) Updated app bug report template [@etraut-openai](https://github.com/etraut-openai)
  - [#11477](https://github.com/openai/codex/pull/11477) feat: switch on dying sub-agents [@jif-oai](https://github.com/jif-oai)
  - [#11711](https://github.com/openai/codex/pull/11711) feat(tui): prevent macOS idle sleep while turns run [@yvolovich-cyber](https://github.com/yvolovich-cyber)
  - [#11686](https://github.com/openai/codex/pull/11686) Report syntax errors in rules file [@etraut-openai](https://github.com/etraut-openai)
  - [#11763](https://github.com/openai/codex/pull/11763) Update read\_path prompt [@zuxin-oai](https://github.com/zuxin-oai)
  - [#11772](https://github.com/openai/codex/pull/11772) chore: mini [@jif-oai](https://github.com/jif-oai)
  - [#11697](https://github.com/openai/codex/pull/11697) [apps] Improve app listing filtering. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11666](https://github.com/openai/codex/pull/11666) Add js\_repl kernel crash diagnostics [@fjord-oai](https://github.com/fjord-oai)
  - [#11687](https://github.com/openai/codex/pull/11687) support app usage analytics [@alexsong-oai](https://github.com/alexsong-oai)
  - [#11769](https://github.com/openai/codex/pull/11769) Improve GitHub issue deduplication reliability by introducing a stage… [@etraut-openai](https://github.com/etraut-openai)
  - [#11770](https://github.com/openai/codex/pull/11770) fix(nix): use correct version from Cargo.toml in flake build [@rupurt](https://github.com/rupurt)
  - [#11677](https://github.com/openai/codex/pull/11677) turn metadata: per-turn non-blocking [@pash-openai](https://github.com/pash-openai)
  - [#11692](https://github.com/openai/codex/pull/11692) rmcp-client: fix auth crash [@maxj-oai](https://github.com/maxj-oai)
  - [#10590](https://github.com/openai/codex/pull/10590) tui: preserve remote image attachments across resume/backtrack [@charley-oai](https://github.com/charley-oai)
  - [#11782](https://github.com/openai/codex/pull/11782) turn metadata followups [@pash-openai](https://github.com/pash-openai)
  - [#11773](https://github.com/openai/codex/pull/11773) [app-server] add fuzzyFileSearch/sessionCompleted [@nornagon-openai](https://github.com/nornagon-openai)
  - [#11756](https://github.com/openai/codex/pull/11756) codex-rs: fix thread resume rejoin semantics [@maxj-oai](https://github.com/maxj-oai)
  - [#11793](https://github.com/openai/codex/pull/11793) fix: send unfiltered models over model/list [@sayan-oai](https://github.com/sayan-oai)
  - [#11799](https://github.com/openai/codex/pull/11799) fix(protocol): make local image test Bazel-friendly [@joshka-oai](https://github.com/joshka-oai)
  - [#11796](https://github.com/openai/codex/pull/11796) Fix js\_repl view\_image test runtime panic [@fjord-oai](https://github.com/fjord-oai)
  - [#11800](https://github.com/openai/codex/pull/11800) Fix js\_repl in-flight tool-call waiter race [@fjord-oai](https://github.com/fjord-oai)
  - [#11658](https://github.com/openai/codex/pull/11658) feat(skills): add permission profiles from openai.yaml metadata [@celia-oai](https://github.com/celia-oai)
  - [#11790](https://github.com/openai/codex/pull/11790) bazel: enforce MODULE.bazel.lock sync with Cargo.lock [@joshka-oai](https://github.com/joshka-oai)
  - [#11803](https://github.com/openai/codex/pull/11803) add perf metrics for connectors load [@alexsong-oai](https://github.com/alexsong-oai)
  - [#11659](https://github.com/openai/codex/pull/11659) Handle model-switch base instructions after compaction [@charley-oai](https://github.com/charley-oai)
  - [#11813](https://github.com/openai/codex/pull/11813) Fixed help text for `mcp` and `mcp-server` CLI commands [@etraut-openai](https://github.com/etraut-openai)
  - [#11672](https://github.com/openai/codex/pull/11672) feat(core): add structured network approval plumbing and policy decision model [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11674](https://github.com/openai/codex/pull/11674) feat(tui): render structured network approval prompts in approval overlay [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11550](https://github.com/openai/codex/pull/11550) feat(tui) Permissions update history item [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11767](https://github.com/openai/codex/pull/11767) fix(core): add linux bubblewrap sandbox tag [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11534](https://github.com/openai/codex/pull/11534) Add process\_uuid to sqlite logs [@charley-oai](https://github.com/charley-oai)
  - [#11487](https://github.com/openai/codex/pull/11487) core: snapshot tests for compaction requests, post-compaction layout, some additional compaction tests [@charley-oai](https://github.com/charley-oai)
  - [#11690](https://github.com/openai/codex/pull/11690) fix: show user warning when using default fallback metadata [@sayan-oai](https://github.com/sayan-oai)
  - [#11780](https://github.com/openai/codex/pull/11780) chore(tui): reduce noisy key logging [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#11884](https://github.com/openai/codex/pull/11884) fix: only emit unknown model warning on user turns [@sayan-oai](https://github.com/sayan-oai)
  - [#11893](https://github.com/openai/codex/pull/11893) bazel: fix snapshot parity for tests/\*.rs rust\_test targets [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#11759](https://github.com/openai/codex/pull/11759) feat: use shell policy in shell snapshot [@jif-oai](https://github.com/jif-oai)
  - [#11615](https://github.com/openai/codex/pull/11615) Allow hooks to error [@gt-oai](https://github.com/gt-oai)
  - [#11918](https://github.com/openai/codex/pull/11918) chore: rename collab feature flag key to multi\_agent [@jif-oai](https://github.com/jif-oai)
  - [#11924](https://github.com/openai/codex/pull/11924) nit: memory storage [@jif-oai](https://github.com/jif-oai)
  - [#11917](https://github.com/openai/codex/pull/11917) feat: add customizable roles for multi-agents [@jif-oai](https://github.com/jif-oai)
  - [#11926](https://github.com/openai/codex/pull/11926) docs: mention Codex app in README intro [@vb-openai](https://github.com/vb-openai)
  - [#11900](https://github.com/openai/codex/pull/11900) feat: drop MCP managing tools if no MCP servers [@jif-oai](https://github.com/jif-oai)
  - [#11939](https://github.com/openai/codex/pull/11939) Rename collab modules to multi agents [@jif-oai](https://github.com/jif-oai)
  - [#11894](https://github.com/openai/codex/pull/11894) [apps] Fix app mention syntax. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11866](https://github.com/openai/codex/pull/11866) chore(core) rm Feature::RequestRule [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11948](https://github.com/openai/codex/pull/11948) add(feedback): over-refusal / safety check [@fouad-openai](https://github.com/fouad-openai)
  - [#11860](https://github.com/openai/codex/pull/11860) Fixed screen reader regression in CLI [@etraut-openai](https://github.com/etraut-openai)
  - [#11964](https://github.com/openai/codex/pull/11964) add(core): safety check downgrade warning [@fouad-openai](https://github.com/fouad-openai)
  - [#11951](https://github.com/openai/codex/pull/11951) fix(core) exec\_policy parsing fixes [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11932](https://github.com/openai/codex/pull/11932) fix: js\_repl reset hang by clearing exec tool calls without waiting [@jif-oai](https://github.com/jif-oai)
  - [#11974](https://github.com/openai/codex/pull/11974) Hide /debug slash commands from popup menu [@jif-oai](https://github.com/jif-oai)
  - [#11922](https://github.com/openai/codex/pull/11922) fix: race in js repl [@jif-oai](https://github.com/jif-oai)
  - [#11969](https://github.com/openai/codex/pull/11969) fix(ci) Fix shell-tool-mcp.yml [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11908](https://github.com/openai/codex/pull/11908) Exit early when session initialization fails [@jif-oai](https://github.com/jif-oai)
  - [#11986](https://github.com/openai/codex/pull/11986) nit: wording multi-agent [@jif-oai](https://github.com/jif-oai)
  - [#11995](https://github.com/openai/codex/pull/11995) feat: add `--search` to `just log` [@jif-oai](https://github.com/jif-oai)
  - [#11994](https://github.com/openai/codex/pull/11994) feat: add `--compact` mode to `just log` [@jif-oai](https://github.com/jif-oai)
  - [#11833](https://github.com/openai/codex/pull/11833) Don't allow model\_supports\_reasoning\_summaries to disable reasoning [@etraut-openai](https://github.com/etraut-openai)
  - [#11807](https://github.com/openai/codex/pull/11807) Centralize context update diffing logic [@charley-oai](https://github.com/charley-oai)
  - [#12007](https://github.com/openai/codex/pull/12007) Update vendored rg to the latest stable version (15.1) [@etraut-openai](https://github.com/etraut-openai)
  - [#11970](https://github.com/openai/codex/pull/11970) Protect workspace .agents directory in Windows sandbox [@etraut-openai](https://github.com/etraut-openai)
  - [#12005](https://github.com/openai/codex/pull/12005) Add /statusline tooltip entry [@jif-oai](https://github.com/jif-oai)
  - [#11982](https://github.com/openai/codex/pull/11982) feat: move agents config to main config [@jif-oai](https://github.com/jif-oai)
  - [#11224](https://github.com/openai/codex/pull/11224) chore: clarify web\_search deprecation notices and consolidate tests [@sayan-oai](https://github.com/sayan-oai)
  - [#12001](https://github.com/openai/codex/pull/12001) Feat: add model reroute notification [@shijie-oai](https://github.com/shijie-oai)
  - [#11801](https://github.com/openai/codex/pull/11801) Add remote skill scope/product\_surface/enabled params and cleanup [@xl-openai](https://github.com/xl-openai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.102.0)
- 2026-02-12

  ### Codex app v260212

  ### New features

  - Support for GPT-5.3-Codex-Spark
  - Added conversation forking
  - Added [floating pop-out window](/codex/app/features#floating-pop-out-window) to take a conversation with you

  ### Bug fixes

  - Improved performance and bug fixes

  Alpha testing for the Codex app on Windows is also starting. [Sign up here](https://openai.com/form/codex-app/) to be a potential alpha tester.
- 2026-02-12

  ### Introducing GPT-5.3-Codex-Spark

  [Today, we’re releasing a research preview of GPT-5.3-Codex-Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/),
  a smaller version of GPT-5.3-Codex and our first model designed for real-time
  coding. Codex-Spark is optimized to feel near-instant, delivering more than 1000 tokens per second while remaining highly capable for real-world coding tasks.

  Codex-Spark is available in research preview for ChatGPT Pro users in
  the latest Codex app, CLI, and IDE extension. This release also marks the first
  milestone in our partnership with Cerebras.

  At launch, Codex-Spark is text-only with a 128k context window. During
  the research preview, usage has separate model-specific limits and doesn’t
  count against standard Codex limits. During high demand, access may slow down
  or queue while we balance reliability across users.

  To switch to GPT-5.3-Codex-Spark:

  - In the CLI, start a new thread with:

    ```
    codex --model gpt-5.3-codex-spark
    ```

    Or use `/model` during a session.
  - In the IDE extension, choose GPT-5.3-Codex-Spark from the model selector in
    the composer.
  - In the Codex app, choose GPT-5.3-Codex-Spark from the model selector in the
    composer.

  If you don’t see GPT-5.3-Codex-Spark yet, update the CLI, IDE extension, or
  Codex app to the latest version.

  GPT-5.3-Codex-Spark isn’t available in the API at launch.
  For API-key workflows, continue using `gpt-5.2-codex`.
- 2026-02-12

  ### Codex CLI 0.101.0

  ```
  $ npm install -g @openai/codex@0.101.0
  ```

    View details

  ## Bug Fixes

  - Model resolution now preserves the requested model slug when selecting by prefix, so model references stay stable instead of being rewritten. ([#11602](https://github.com/openai/codex/pull/11602))
  - Developer messages are now excluded from phase-1 memory input, reducing noisy or irrelevant content entering memory. ([#11608](https://github.com/openai/codex/pull/11608))
  - Memory phase processing concurrency was reduced to make consolidation/staging more stable under load. ([#11614](https://github.com/openai/codex/pull/11614))

  ## Chores

  - Cleaned and simplified the phase-1 memory pipeline code paths. ([#11605](https://github.com/openai/codex/pull/11605))
  - Minor repository maintenance: formatting and test-suite hygiene updates in remote model tests. ([#11619](https://github.com/openai/codex/pull/11619))

  ## Changelog

  Full Changelog: [rust-v0.100.0...rust-v0.101.0](https://github.com/openai/codex/compare/rust-v0.100.0...rust-v0.101.0)

  - [#11605](https://github.com/openai/codex/pull/11605) chore: drop and clean from phase 1 [@jif-oai](https://github.com/jif-oai)
  - [#11602](https://github.com/openai/codex/pull/11602) fix(core) model\_info preserves slug [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11608](https://github.com/openai/codex/pull/11608) exclude developer messages from phase-1 memory input [@wendyjiao-openai](https://github.com/wendyjiao-openai)
  - [#11591](https://github.com/openai/codex/pull/11591) Add cwd to memory files [@wendyjiao-openai](https://github.com/wendyjiao-openai)
  - [#11614](https://github.com/openai/codex/pull/11614) chore: reduce concurrency of memories [@jif-oai](https://github.com/jif-oai)
  - [#11619](https://github.com/openai/codex/pull/11619) fix: fmt [@jif-oai](https://github.com/jif-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.101.0)
- 2026-02-12

  ### Codex CLI 0.100.0

  ```
  $ npm install -g @openai/codex@0.100.0
  ```

    View details

  ## New Features

  - Added an experimental, feature-gated JavaScript REPL runtime (`js_repl`) that can persist state across tool calls, with optional runtime path overrides. ([#10674](https://github.com/openai/codex/pull/10674))
  - Added support for multiple simultaneous rate limits across the protocol, backend client, and TUI status surfaces. ([#11260](https://github.com/openai/codex/pull/11260))
  - Reintroduced app-server websocket transport with a split inbound/outbound architecture, plus connection-aware thread resume subscriptions. ([#11370](https://github.com/openai/codex/pull/11370), [#11474](https://github.com/openai/codex/pull/11474))
  - Added memory management slash commands in the TUI (`/m_update`, `/m_drop`) and expanded memory-read/metrics plumbing. ([#11569](https://github.com/openai/codex/pull/11569), [#11459](https://github.com/openai/codex/pull/11459), [#11593](https://github.com/openai/codex/pull/11593))
  - Enabled Apps SDK apps in ChatGPT connector handling. ([#11486](https://github.com/openai/codex/pull/11486))
  - Promoted sandbox capabilities on both Linux and Windows, and introduced a new `ReadOnlyAccess` policy shape for configurable read access. ([#11381](https://github.com/openai/codex/pull/11381), [#11341](https://github.com/openai/codex/pull/11341), [#11387](https://github.com/openai/codex/pull/11387))

  ## Bug Fixes

  - Fixed websocket incremental output duplication, prevented appends after `response.completed`, and treated `response.incomplete` as an error path. ([#11383](https://github.com/openai/codex/pull/11383), [#11402](https://github.com/openai/codex/pull/11402), [#11558](https://github.com/openai/codex/pull/11558))
  - Improved websocket session stability by continuing ping handling when idle and suppressing noisy first-retry errors during quick reconnects. ([#11413](https://github.com/openai/codex/pull/11413), [#11548](https://github.com/openai/codex/pull/11548))
  - Fixed stale thread entries by dropping missing rollout files and cleaning stale DB metadata during thread listing. ([#11572](https://github.com/openai/codex/pull/11572))
  - Fixed Windows multi-line paste reliability in terminals (especially VS Code integrated terminal) by increasing paste burst timing tolerance. ([#9348](https://github.com/openai/codex/pull/9348))
  - Fixed incorrect inheritance of `limit_name` when merging partial rate-limit updates. ([#11557](https://github.com/openai/codex/pull/11557))
  - Reduced repeated skill parse-error spam during active edits by increasing file-watcher debounce from 1s to 10s. ([#11494](https://github.com/openai/codex/pull/11494))

  ## Documentation

  - Added JS REPL documentation and config/schema guidance for enabling and configuring the feature. ([#10674](https://github.com/openai/codex/pull/10674))
  - Updated app-server websocket transport documentation in the app-server README. ([#11370](https://github.com/openai/codex/pull/11370))

  ## Chores

  - Split `codex-common` into focused `codex-utils-*` crates to simplify dependency boundaries across Rust workspace components. ([#11422](https://github.com/openai/codex/pull/11422))
  - Improved Rust release pipeline throughput and reliability for Windows and musl targets, including parallel Windows builds and musl link fixes. ([#11488](https://github.com/openai/codex/pull/11488), [#11500](https://github.com/openai/codex/pull/11500), [#11556](https://github.com/openai/codex/pull/11556))
  - Prevented GitHub release asset upload collisions by excluding duplicate `cargo-timing.html` artifacts. ([#11564](https://github.com/openai/codex/pull/11564))

  ## Changelog

  Full Changelog: [rust-v0.99.0...rust-v0.100.0](https://github.com/openai/codex/compare/rust-v0.99.0...rust-v0.100.0)

  - [#11383](https://github.com/openai/codex/pull/11383) Do not resend output items in incremental websockets connections [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11246](https://github.com/openai/codex/pull/11246) chore: persist turn\_id in rollout session and make turn\_id uuid based [@celia-oai](https://github.com/celia-oai)
  - [#11260](https://github.com/openai/codex/pull/11260) feat: support multiple rate limits [@xl-openai](https://github.com/xl-openai)
  - [#11412](https://github.com/openai/codex/pull/11412) tui: show non-file layer content in /debug-config [@bolinfest](https://github.com/bolinfest)
  - [#11405](https://github.com/openai/codex/pull/11405) Remove `test-support` feature from `codex-core` and replace it with explicit test toggles [@bolinfest](https://github.com/bolinfest)
  - [#11428](https://github.com/openai/codex/pull/11428) fix: flaky test [@jif-oai](https://github.com/jif-oai)
  - [#11429](https://github.com/openai/codex/pull/11429) feat: improve thread listing [@jif-oai](https://github.com/jif-oai)
  - [#11422](https://github.com/openai/codex/pull/11422) feat: split codex-common into smaller utils crates [@bolinfest](https://github.com/bolinfest)
  - [#11439](https://github.com/openai/codex/pull/11439) feat: new memory prompts [@jif-oai](https://github.com/jif-oai)
  - [#11305](https://github.com/openai/codex/pull/11305) Cache cloud requirements [@gt-oai](https://github.com/gt-oai)
  - [#11452](https://github.com/openai/codex/pull/11452) nit: increase max raw memories [@jif-oai](https://github.com/jif-oai)
  - [#11455](https://github.com/openai/codex/pull/11455) feat: close mem agent after consolidation [@jif-oai](https://github.com/jif-oai)
  - [#11454](https://github.com/openai/codex/pull/11454) fix: optional schema of memories [@jif-oai](https://github.com/jif-oai)
  - [#11449](https://github.com/openai/codex/pull/11449) feat: set policy for phase 2 memory [@jif-oai](https://github.com/jif-oai)
  - [#11420](https://github.com/openai/codex/pull/11420) chore: rename disable\_websockets -> websockets\_disabled [@sayan-oai](https://github.com/sayan-oai)
  - [#11402](https://github.com/openai/codex/pull/11402) Do not attempt to append after response.completed [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11462](https://github.com/openai/codex/pull/11462) clean: memory rollout recorder [@jif-oai](https://github.com/jif-oai)
  - [#11381](https://github.com/openai/codex/pull/11381) feat(core): promote Linux bubblewrap sandbox to Experimental [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11389](https://github.com/openai/codex/pull/11389) Extract `codex-config` from `codex-core` [@bolinfest](https://github.com/bolinfest)
  - [#11370](https://github.com/openai/codex/pull/11370) Reapply "Add app-server transport layer with websocket support" [@maxj-oai](https://github.com/maxj-oai)
  - [#11470](https://github.com/openai/codex/pull/11470) feat: panic if Constrained does not support Disabled [@bolinfest](https://github.com/bolinfest)
  - [#11475](https://github.com/openai/codex/pull/11475) feat: remove "cargo check individual crates" from CI [@bolinfest](https://github.com/bolinfest)
  - [#11459](https://github.com/openai/codex/pull/11459) feat: memory read path [@jif-oai](https://github.com/jif-oai)
  - [#11471](https://github.com/openai/codex/pull/11471) chore: clean rollout extraction in memories [@jif-oai](https://github.com/jif-oai)
  - [#9348](https://github.com/openai/codex/pull/9348) fix(tui): increase paste burst char interval on Windows to 30ms [@yuvrajangadsingh](https://github.com/yuvrajangadsingh)
  - [#11464](https://github.com/openai/codex/pull/11464) chore: sub-agent never ask for approval [@jif-oai](https://github.com/jif-oai)
  - [#11414](https://github.com/openai/codex/pull/11414) Linkify feedback link [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11480](https://github.com/openai/codex/pull/11480) chore: update mem prompt [@jif-oai](https://github.com/jif-oai)
  - [#11485](https://github.com/openai/codex/pull/11485) fix: Constrained import [@owenlin0](https://github.com/owenlin0)
  - [#11341](https://github.com/openai/codex/pull/11341) Promote Windows Sandbox [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10674](https://github.com/openai/codex/pull/10674) Add feature-gated freeform js\_repl core runtime [@fjord-oai](https://github.com/fjord-oai)
  - [#11419](https://github.com/openai/codex/pull/11419) refactor: codex app-server ThreadState [@maxj-oai](https://github.com/maxj-oai)
  - [#11413](https://github.com/openai/codex/pull/11413) Pump pings [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11488](https://github.com/openai/codex/pull/11488) feat: use more powerful machines for building Windows releases [@bolinfest](https://github.com/bolinfest)
  - [#11479](https://github.com/openai/codex/pull/11479) nit: memory truncation [@jif-oai](https://github.com/jif-oai)
  - [#11494](https://github.com/openai/codex/pull/11494) Increased file watcher debounce duration from 1s to 10s [@etraut-openai](https://github.com/etraut-openai)
  - [#11335](https://github.com/openai/codex/pull/11335) Add AfterToolUse hook [@gt-oai](https://github.com/gt-oai)
  - [#11500](https://github.com/openai/codex/pull/11500) feat: build windows support binaries in parallel [@bolinfest](https://github.com/bolinfest)
  - [#11290](https://github.com/openai/codex/pull/11290) chore(tui) Simplify /status Permissions [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11503](https://github.com/openai/codex/pull/11503) Make codex-sdk depend on openai/codex [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11474](https://github.com/openai/codex/pull/11474) app-server: thread resume subscriptions [@maxj-oai](https://github.com/maxj-oai)
  - [#11277](https://github.com/openai/codex/pull/11277) Added seatbelt policy rule to allow os.cpus [@etraut-openai](https://github.com/etraut-openai)
  - [#11506](https://github.com/openai/codex/pull/11506) chore: inject originator/residency headers to ws client [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#11497](https://github.com/openai/codex/pull/11497) Hydrate previous model across resume/fork/rollback/task start [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11513](https://github.com/openai/codex/pull/11513) feat: try to fix bugs I saw in the wild in the resource parsing logic [@bolinfest](https://github.com/bolinfest)
  - [#11509](https://github.com/openai/codex/pull/11509) Consolidate search\_tool feature into apps [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#11388](https://github.com/openai/codex/pull/11388) change model cap to server overload [@willwang-openai](https://github.com/willwang-openai)
  - [#11504](https://github.com/openai/codex/pull/11504) Pre-sampling compact with previous model context [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11516](https://github.com/openai/codex/pull/11516) Clamp auto-compact limit to context window [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11520](https://github.com/openai/codex/pull/11520) Update context window after model switch [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11519](https://github.com/openai/codex/pull/11519) Use slug in tui [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11522](https://github.com/openai/codex/pull/11522) fix: add --test\_verbose\_timeout\_warnings to bazel.yml [@bolinfest](https://github.com/bolinfest)
  - [#11526](https://github.com/openai/codex/pull/11526) fix: remove errant Cargo.lock files [@bolinfest](https://github.com/bolinfest)
  - [#11521](https://github.com/openai/codex/pull/11521) test(app-server): stabilize app/list thread feature-flag test by using file-backed MCP OAuth creds [@bolinfest](https://github.com/bolinfest)
  - [#11387](https://github.com/openai/codex/pull/11387) feat: make sandbox read access configurable with `ReadOnlyAccess` [@bolinfest](https://github.com/bolinfest)
  - [#11486](https://github.com/openai/codex/pull/11486) [apps] Allow Apps SDK apps. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11532](https://github.com/openai/codex/pull/11532) fix compilation [@sayan-oai](https://github.com/sayan-oai)
  - [#11531](https://github.com/openai/codex/pull/11531) Teach codex to test itself [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11540](https://github.com/openai/codex/pull/11540) ci: remove actions/cache from rust release workflows [@bolinfest](https://github.com/bolinfest)
  - [#11542](https://github.com/openai/codex/pull/11542) ci(windows): use DotSlash for zstd in rust-release-windows [@bolinfest](https://github.com/bolinfest)
  - [#11498](https://github.com/openai/codex/pull/11498) build(linux-sandbox): always compile vendored bubblewrap on Linux; remove CODEX\_BWRAP\_ENABLE\_FFI [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11545](https://github.com/openai/codex/pull/11545) fix: make project\_doc skill-render tests deterministic [@bolinfest](https://github.com/bolinfest)
  - [#11543](https://github.com/openai/codex/pull/11543) ci: capture cargo timings in Rust CI and release workflows [@bolinfest](https://github.com/bolinfest)
  - [#11539](https://github.com/openai/codex/pull/11539) Bump rmcp to 0.15 [@gpeal](https://github.com/gpeal)
  - [#11548](https://github.com/openai/codex/pull/11548) Hide the first websocket retry [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11551](https://github.com/openai/codex/pull/11551) Add logs to model cache [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11556](https://github.com/openai/codex/pull/11556) Fix rust-release failures in musl linking and release asset upload [@bolinfest](https://github.com/bolinfest)
  - [#11558](https://github.com/openai/codex/pull/11558) Handle response.incomplete [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11557](https://github.com/openai/codex/pull/11557) fix: stop inheriting rate-limit limit\_name [@xl-openai](https://github.com/xl-openai)
  - [#11564](https://github.com/openai/codex/pull/11564) rust-release: exclude cargo-timing.html from release assets [@bolinfest](https://github.com/bolinfest)
  - [#11546](https://github.com/openai/codex/pull/11546) fix: update memory writing prompt [@zuxin-oai](https://github.com/zuxin-oai)
  - [#11448](https://github.com/openai/codex/pull/11448) Fix test flake [@gt-oai](https://github.com/gt-oai)
  - [#11569](https://github.com/openai/codex/pull/11569) feat: mem slash commands [@jif-oai](https://github.com/jif-oai)
  - [#11573](https://github.com/openai/codex/pull/11573) Fix flaky pre\_sampling\_compact switch test [@jif-oai](https://github.com/jif-oai)
  - [#11571](https://github.com/openai/codex/pull/11571) feat: mem drop cot [@jif-oai](https://github.com/jif-oai)
  - [#11572](https://github.com/openai/codex/pull/11572) Ensure list\_threads drops stale rollout files [@jif-oai](https://github.com/jif-oai)
  - [#11575](https://github.com/openai/codex/pull/11575) fix: db stuff mem [@jif-oai](https://github.com/jif-oai)
  - [#11581](https://github.com/openai/codex/pull/11581) nit: upgrade DB version [@jif-oai](https://github.com/jif-oai)
  - [#11577](https://github.com/openai/codex/pull/11577) feat: truncate with model infos [@jif-oai](https://github.com/jif-oai)
  - [#11590](https://github.com/openai/codex/pull/11590) chore: clean consts [@jif-oai](https://github.com/jif-oai)
  - [#11593](https://github.com/openai/codex/pull/11593) feat: metrics to memories [@jif-oai](https://github.com/jif-oai)
  - [#11579](https://github.com/openai/codex/pull/11579) Fix config test on macOS [@gt-oai](https://github.com/gt-oai)
  - [#11600](https://github.com/openai/codex/pull/11600) feat: add sanitizer to redact secrets [@jif-oai](https://github.com/jif-oai)
  - [#11609](https://github.com/openai/codex/pull/11609) chore: drop mcp validation of dynamic tools [@jif-oai](https://github.com/jif-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.100.0)
- 2026-02-11

  ### Codex CLI 0.99.0

  ```
  $ npm install -g @openai/codex@0.99.0
  ```

    View details

  ## New Features

  - Running direct shell commands no longer interrupts an in-flight turn; commands can execute concurrently when a turn is active. ([#10513](https://github.com/openai/codex/pull/10513))
  - Added `/statusline` to configure which metadata appears in the TUI footer interactively. ([#10546](https://github.com/openai/codex/pull/10546))
  - The TUI resume picker can now toggle sort order between creation time and last-updated time with an in-picker mode indicator. ([#10752](https://github.com/openai/codex/pull/10752))
  - App-server clients now get dedicated APIs for steering active turns, listing experimental features, resuming agents, and opting out of specific notifications. ([#10721](https://github.com/openai/codex/pull/10721), [#10821](https://github.com/openai/codex/pull/10821), [#10903](https://github.com/openai/codex/pull/10903), [#11319](https://github.com/openai/codex/pull/11319))
  - Enterprise/admin requirements can now restrict web search modes and define network constraints through `requirements.toml`. ([#10964](https://github.com/openai/codex/pull/10964), [#10958](https://github.com/openai/codex/pull/10958))
  - Image attachments now accept GIF and WebP inputs in addition to existing formats. ([#11237](https://github.com/openai/codex/pull/11237))
  - Enable snapshotting of the shell environment and `rc` files ([#11172](https://github.com/openai/codex/pull/11172))

  ## Bug Fixes

  - Fixed a Windows startup issue where buffered keypresses could cause the TUI sign-in flow to exit immediately. ([#10729](https://github.com/openai/codex/pull/10729))
  - Required MCP servers now fail fast during start/resume flows instead of continuing in a broken state. ([#10902](https://github.com/openai/codex/pull/10902))
  - Fixed a file-watcher bug that emitted spurious skills reload events and could generate very large log files. ([#11217](https://github.com/openai/codex/pull/11217))
  - Improved TUI input reliability: long option labels wrap correctly, Tab submits in steer mode when idle, history recall keeps cursor placement consistent, and stashed drafts restore image placeholders correctly. ([#11123](https://github.com/openai/codex/pull/11123), [#10035](https://github.com/openai/codex/pull/10035), [#11295](https://github.com/openai/codex/pull/11295), [#9040](https://github.com/openai/codex/pull/9040))
  - Fixed model-modality edge cases by surfacing clearer `view_image` errors on text-only models and stripping unsupported image history during model switches. ([#11336](https://github.com/openai/codex/pull/11336), [#11349](https://github.com/openai/codex/pull/11349))
  - Reduced false approval mismatches for wrapped/heredoc shell commands and guarded against empty command lists in exec policy evaluation. ([#10941](https://github.com/openai/codex/pull/10941), [#11397](https://github.com/openai/codex/pull/11397))

  ## Documentation

  - Expanded app-server docs and protocol references for `turn/steer`, experimental-feature discovery, `resume_agent`, notification opt-outs, and null `developer_instructions` normalization. ([#10721](https://github.com/openai/codex/pull/10721), [#10821](https://github.com/openai/codex/pull/10821), [#10903](https://github.com/openai/codex/pull/10903), [#10983](https://github.com/openai/codex/pull/10983), [#11319](https://github.com/openai/codex/pull/11319))
  - Updated TUI composer docs to reflect draft/image restoration, steer-mode Tab submit behavior, and history-navigation cursor semantics. ([#9040](https://github.com/openai/codex/pull/9040), [#10035](https://github.com/openai/codex/pull/10035), [#11295](https://github.com/openai/codex/pull/11295))

  ## Chores

  - Reworked npm release packaging so platform-specific binaries are distributed via `@openai/codex` dist-tags, reducing package-size pressure while preserving platform-specific installs (including `@alpha`). ([#11318](https://github.com/openai/codex/pull/11318), [#11339](https://github.com/openai/codex/pull/11339))
  - Pulled in a security-driven dependency update for `time` (RUSTSEC-2026-0009). ([#10876](https://github.com/openai/codex/pull/10876))

  ## Changelog

  Full Changelog: [rust-v0.98.0...rust-v0.99.0](https://github.com/openai/codex/compare/rust-v0.98.0...rust-v0.99.0)

  - [#10729](https://github.com/openai/codex/pull/10729) fix(tui): flush input buffer on init to prevent early exit on Windows [@Ashutosh0x](https://github.com/Ashutosh0x)
  - [#10689](https://github.com/openai/codex/pull/10689) fix: flaky landlock [@jif-oai](https://github.com/jif-oai)
  - [#10513](https://github.com/openai/codex/pull/10513) Allow user shell commands to run alongside active turns [@jif-oai](https://github.com/jif-oai)
  - [#10738](https://github.com/openai/codex/pull/10738) nit: backfill stronger [@jif-oai](https://github.com/jif-oai)
  - [#10246](https://github.com/openai/codex/pull/10246) adding fork information (UI) when forking [@pap-openai](https://github.com/pap-openai)
  - [#10748](https://github.com/openai/codex/pull/10748) Update explorer role default model [@jif-oai](https://github.com/jif-oai)
  - [#10425](https://github.com/openai/codex/pull/10425) Include real OS info in metrics. [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10745](https://github.com/openai/codex/pull/10745) feat: resumable backfill [@jif-oai](https://github.com/jif-oai)
  - [#10758](https://github.com/openai/codex/pull/10758) feat: wire ephemeral in `codex exec` [@jif-oai](https://github.com/jif-oai)
  - [#10756](https://github.com/openai/codex/pull/10756) chore: handle shutdown correctly in tui [@jif-oai](https://github.com/jif-oai)
  - [#10637](https://github.com/openai/codex/pull/10637) feat: add memory tool [@jif-oai](https://github.com/jif-oai)
  - [#10751](https://github.com/openai/codex/pull/10751) feat: repair DB in case of missing lines [@jif-oai](https://github.com/jif-oai)
  - [#10762](https://github.com/openai/codex/pull/10762) nit: add DB version in discrepancy recording [@jif-oai](https://github.com/jif-oai)
  - [#10621](https://github.com/openai/codex/pull/10621) Leverage state DB metadata for thread summaries [@jif-oai](https://github.com/jif-oai)
  - [#9691](https://github.com/openai/codex/pull/9691) Add hooks implementation and wire up to `notify` [@gt-oai](https://github.com/gt-oai)
  - [#10546](https://github.com/openai/codex/pull/10546) feat(tui): add /statusline command for interactive status line configuration [@fcoury](https://github.com/fcoury)
  - [#10752](https://github.com/openai/codex/pull/10752) feat(tui): add sortable resume picker with created/updated timestamp toggle [@fcoury](https://github.com/fcoury)
  - [#10769](https://github.com/openai/codex/pull/10769) fix(tui): fix resume\_picker\_orders\_by\_updated\_at test [@owenlin0](https://github.com/owenlin0)
  - [#10423](https://github.com/openai/codex/pull/10423) fix(auth): isolate chatgptAuthTokens concept to auth manager and app-server [@owenlin0](https://github.com/owenlin0)
  - [#10775](https://github.com/openai/codex/pull/10775) nit: gpt-5.3-codex announcement [@jif-oai](https://github.com/jif-oai)
  - [#10782](https://github.com/openai/codex/pull/10782) nit: gpt-5.3-codex announcement 2 [@jif-oai](https://github.com/jif-oai)
  - [#10711](https://github.com/openai/codex/pull/10711) add sandbox policy and sandbox name to codex.tool.call metrics [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10660](https://github.com/openai/codex/pull/10660) chore: rm web-search-eligible header [@sayan-oai](https://github.com/sayan-oai)
  - [#10783](https://github.com/openai/codex/pull/10783) fix: announcement in prio [@jif-oai](https://github.com/jif-oai)
  - [#10721](https://github.com/openai/codex/pull/10721) [app-server] Add a method to list experimental features. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#10787](https://github.com/openai/codex/pull/10787) chore: limit update to 0.98.0 NUX to < 0.98.0 ver [@sayan-oai](https://github.com/sayan-oai)
  - [#10655](https://github.com/openai/codex/pull/10655) Add analytics for /rename and /fork [@pap-openai](https://github.com/pap-openai)
  - [#10790](https://github.com/openai/codex/pull/10790) feat: wait for backfill to be ready [@jif-oai](https://github.com/jif-oai)
  - [#10693](https://github.com/openai/codex/pull/10693) Add app-server transport layer with websocket support [@maxj-oai](https://github.com/maxj-oai)
  - [#10818](https://github.com/openai/codex/pull/10818) other announcement [@jif-oai](https://github.com/jif-oai)
  - [#10815](https://github.com/openai/codex/pull/10815) Sync app-server requirements API with refreshed cloud loader [@xl-openai](https://github.com/xl-openai)
  - [#10820](https://github.com/openai/codex/pull/10820) go back to auto-enabling web\_search for azure [@sayan-oai](https://github.com/sayan-oai)
  - [#10727](https://github.com/openai/codex/pull/10727) Send beta header with websocket connects [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10809](https://github.com/openai/codex/pull/10809) updates: use brew api for version check [@magus](https://github.com/magus)
  - [#10793](https://github.com/openai/codex/pull/10793) Add stage field for experimental flags. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#10821](https://github.com/openai/codex/pull/10821) feat(app-server): turn/steer API [@owenlin0](https://github.com/owenlin0)
  - [#10792](https://github.com/openai/codex/pull/10792) Print warning when config does not meet requirements [@gt-oai](https://github.com/gt-oai)
  - [#10699](https://github.com/openai/codex/pull/10699) feat: expose detailed metrics to runtime metrics [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#10784](https://github.com/openai/codex/pull/10784) Gate app tooltips to macOS [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10843](https://github.com/openai/codex/pull/10843) Log an event (info only) when we receive a file watcher event [@etraut-openai](https://github.com/etraut-openai)
  - [#10852](https://github.com/openai/codex/pull/10852) Personality setting is no longer available in experimental menu [@etraut-openai](https://github.com/etraut-openai)
  - [#10840](https://github.com/openai/codex/pull/10840) Removed the "remote\_compaction" feature flag [@etraut-openai](https://github.com/etraut-openai)
  - [#10876](https://github.com/openai/codex/pull/10876) sec: fix version of `time` to prevent vulnerability [@jif-oai](https://github.com/jif-oai)
  - [#10892](https://github.com/openai/codex/pull/10892) nit: test an [@jif-oai](https://github.com/jif-oai)
  - [#10894](https://github.com/openai/codex/pull/10894) feat: backfill async again [@jif-oai](https://github.com/jif-oai)
  - [#10902](https://github.com/openai/codex/pull/10902) Handle required MCP startup failures across components [@jif-oai](https://github.com/jif-oai)
  - [#10851](https://github.com/openai/codex/pull/10851) Removed "exec\_policy" feature flag [@etraut-openai](https://github.com/etraut-openai)
  - [#10457](https://github.com/openai/codex/pull/10457) Queue nudges while plan generating [@charley-oai](https://github.com/charley-oai)
  - [#10822](https://github.com/openai/codex/pull/10822) Add app configs to config.toml [@canvrno-oai](https://github.com/canvrno-oai)
  - [#10420](https://github.com/openai/codex/pull/10420) feat(network-proxy): add structured policy decision to blocked errors [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10814](https://github.com/openai/codex/pull/10814) fix(linux-sandbox): block io\_uring syscalls in no-network seccomp policy [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10698](https://github.com/openai/codex/pull/10698) core: preconnect Responses websocket for first turn [@joshka-oai](https://github.com/joshka-oai)
  - [#10574](https://github.com/openai/codex/pull/10574) core: refresh developer instructions after compaction replacement history [@charley-oai](https://github.com/charley-oai)
  - [#10914](https://github.com/openai/codex/pull/10914) chore(app-server): update AGENTS.md for config + optional collection guidance [@owenlin0](https://github.com/owenlin0)
  - [#10928](https://github.com/openai/codex/pull/10928) chore(app-server): add experimental annotation to relevant fields [@owenlin0](https://github.com/owenlin0)
  - [#10927](https://github.com/openai/codex/pull/10927) Treat compaction failure as failure state [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10861](https://github.com/openai/codex/pull/10861) Support alternative websocket API [@by-openai](https://github.com/by-openai)
  - [#10826](https://github.com/openai/codex/pull/10826) add originator to otel [@alexsong-oai](https://github.com/alexsong-oai)
  - [#10855](https://github.com/openai/codex/pull/10855) TUI/Core: preserve duplicate skill/app mention selection across submit + resume [@daniel-oai](https://github.com/daniel-oai)
  - [#10943](https://github.com/openai/codex/pull/10943) app-server: print help message to console when starting websockets server [@JaviSoto](https://github.com/JaviSoto)
  - [#10938](https://github.com/openai/codex/pull/10938) Mark Config.apps as experimental, correct schema generation issue [@canvrno-oai](https://github.com/canvrno-oai)
  - [#10947](https://github.com/openai/codex/pull/10947) fix(tui): conditionally restore status indicator using message phase [@sayan-oai](https://github.com/sayan-oai)
  - [#10965](https://github.com/openai/codex/pull/10965) refactor(network-proxy): flatten network config under [network] [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10970](https://github.com/openai/codex/pull/10970) Fixed a flaky test [@etraut-openai](https://github.com/etraut-openai)
  - [#10710](https://github.com/openai/codex/pull/10710) Process-group cleanup for stdio MCP servers to prevent orphan process storms [@etraut-openai](https://github.com/etraut-openai)
  - [#10964](https://github.com/openai/codex/pull/10964) feat: add support for allowed\_web\_search\_modes in requirements.toml [@bolinfest](https://github.com/bolinfest)
  - [#10977](https://github.com/openai/codex/pull/10977) fix: use expected line ending in codex-rs/core/config.schema.json [@bolinfest](https://github.com/bolinfest)
  - [#10973](https://github.com/openai/codex/pull/10973) Do not poll for usage when using API Key auth [@etraut-openai](https://github.com/etraut-openai)
  - [#10921](https://github.com/openai/codex/pull/10921) Show left/right arrows to navigate in tui request\_user\_input [@charley-oai](https://github.com/charley-oai)
  - [#10988](https://github.com/openai/codex/pull/10988) fix: normalize line endings when reading file on Windows [@bolinfest](https://github.com/bolinfest)
  - [#10903](https://github.com/openai/codex/pull/10903) Add resume\_agent collab tool [@jif-oai](https://github.com/jif-oai)
  - [#10909](https://github.com/openai/codex/pull/10909) Bootstrap shell commands via user shell snapshot [@jif-oai](https://github.com/jif-oai)
  - [#10993](https://github.com/openai/codex/pull/10993) Fix flaky windows CI test [@etraut-openai](https://github.com/etraut-openai)
  - [#10987](https://github.com/openai/codex/pull/10987) Fixed a flaky Windows test that is consistently causing a CI failure [@etraut-openai](https://github.com/etraut-openai)
  - [#10958](https://github.com/openai/codex/pull/10958) feat(core): add network constraints schema to requirements.toml [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10983](https://github.com/openai/codex/pull/10983) app-server: treat null mode developer instructions as built-in defaults [@charley-oai](https://github.com/charley-oai)
  - [#11039](https://github.com/openai/codex/pull/11039) feat: include state of [experimental\_network] in /debug-config output [@bolinfest](https://github.com/bolinfest)
  - [#11040](https://github.com/openai/codex/pull/11040) Simplify pre-connect [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10966](https://github.com/openai/codex/pull/10966) feat: enable premessage-deflate for websockets [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#9040](https://github.com/openai/codex/pull/9040) fix(tui): rehydrate drafts and restore image placeholders [@Chriss4123](https://github.com/Chriss4123)
  - [#10824](https://github.com/openai/codex/pull/10824) Fallback to HTTP on UPGRADE\_REQUIRED [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11028](https://github.com/openai/codex/pull/11028) Defer persistence of rollout file [@etraut-openai](https://github.com/etraut-openai)
  - [#10980](https://github.com/openai/codex/pull/10980) fix: remove config.schema.json from tag check [@bolinfest](https://github.com/bolinfest)
  - [#11051](https://github.com/openai/codex/pull/11051) Gate view\_image tool by model input\_modalities [@wiltzius-openai](https://github.com/wiltzius-openai)
  - [#11109](https://github.com/openai/codex/pull/11109) [bazel] Upgrade some rulesets in preparation for enabling windows [@zbarsky-openai](https://github.com/zbarsky-openai)
  - [#11114](https://github.com/openai/codex/pull/11114) chore: refactor network-proxy so that ConfigReloader is injectable behavior [@bolinfest](https://github.com/bolinfest)
  - [#10718](https://github.com/openai/codex/pull/10718) Upgrade rmcp to 0.14 [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11044](https://github.com/openai/codex/pull/11044) feat: include [experimental\_network] in <environment\_context> [@bolinfest](https://github.com/bolinfest)
  - [#10994](https://github.com/openai/codex/pull/10994) [apps] Improve app loading. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11121](https://github.com/openai/codex/pull/11121) chore: reverse the codex-network-proxy -> codex-core dependency [@bolinfest](https://github.com/bolinfest)
  - [#11105](https://github.com/openai/codex/pull/11105) feat: include NetworkConfig through ExecParams [@bolinfest](https://github.com/bolinfest)
  - [#11155](https://github.com/openai/codex/pull/11155) tui: avoid no-op status-line redraws [@rakan-oai](https://github.com/rakan-oai)
  - [#10799](https://github.com/openai/codex/pull/10799) feat: do not close unified exec processes across turns [@jif-oai](https://github.com/jif-oai)
  - [#11172](https://github.com/openai/codex/pull/11172) chore: enable shell snapshot [@jif-oai](https://github.com/jif-oai)
  - [#11175](https://github.com/openai/codex/pull/11175) fix: do not show closed agents in `/agent` [@jif-oai](https://github.com/jif-oai)
  - [#11173](https://github.com/openai/codex/pull/11173) chore: enable sub agents [@jif-oai](https://github.com/jif-oai)
  - [#11193](https://github.com/openai/codex/pull/11193) Deflake mixed parallel tools timing test [@gt-oai](https://github.com/gt-oai)
  - [#10770](https://github.com/openai/codex/pull/10770) Load requirements on windows [@gt-oai](https://github.com/gt-oai)
  - [#11132](https://github.com/openai/codex/pull/11132) core: account for all post-response items in auto-compact token checks [@charley-oai](https://github.com/charley-oai)
  - [#11198](https://github.com/openai/codex/pull/11198) tools: remove get\_memory tool and tests [@jif-oai](https://github.com/jif-oai)
  - [#10937](https://github.com/openai/codex/pull/10937) Translate websocket errors [@rasmusrygaard](https://github.com/rasmusrygaard)
  - [#11217](https://github.com/openai/codex/pull/11217) Fixed bug in file watcher that results in spurious skills update events and large log files [@etraut-openai](https://github.com/etraut-openai)
  - [#11216](https://github.com/openai/codex/pull/11216) Move warmup to the task level [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11203](https://github.com/openai/codex/pull/11203) Try to stop small helper methods [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11197](https://github.com/openai/codex/pull/11197) [bazel] Upgrade some rulesets in preparation for enabling windows, part 2 [@zbarsky-openai](https://github.com/zbarsky-openai)
  - [#11158](https://github.com/openai/codex/pull/11158) chore: remove network-proxy-cli crate [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11230](https://github.com/openai/codex/pull/11230) Revert "chore: enable sub agents" [@jif-oai](https://github.com/jif-oai)
  - [#11123](https://github.com/openai/codex/pull/11123) TUI: fix request\_user\_input wrapping for long option labels [@charley-oai](https://github.com/charley-oai)
  - [#11133](https://github.com/openai/codex/pull/11133) core: add focused diagnostics for remote compaction overflows [@charley-oai](https://github.com/charley-oai)
  - [#10657](https://github.com/openai/codex/pull/10657) feat: search\_tool [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#11199](https://github.com/openai/codex/pull/11199) state: add memory consolidation lock primitives [@jif-oai](https://github.com/jif-oai)
  - [#10835](https://github.com/openai/codex/pull/10835) feat: extend skills/list to support additional roots. [@xl-openai](https://github.com/xl-openai)
  - [#10960](https://github.com/openai/codex/pull/10960) skill-creator: Remove invalid reference. [@xl-openai](https://github.com/xl-openai)
  - [#11219](https://github.com/openai/codex/pull/11219) feat: use a notify instead of grace to close ue process [@jif-oai](https://github.com/jif-oai)
  - [#11231](https://github.com/openai/codex/pull/11231) feat: tie shell snapshot to cwd [@jif-oai](https://github.com/jif-oai)
  - [#10962](https://github.com/openai/codex/pull/10962) fix(tui): keep unified exec summary on working line [@joshka-oai](https://github.com/joshka-oai)
  - [#11232](https://github.com/openai/codex/pull/11232) Add originator to otel metadata tags [@alexsong-oai](https://github.com/alexsong-oai)
  - [#11237](https://github.com/openai/codex/pull/11237) adding image support for gif and webp [@natea-oai](https://github.com/natea-oai)
  - [#10924](https://github.com/openai/codex/pull/10924) [apps] Add gated instructions for Apps. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11228](https://github.com/openai/codex/pull/11228) Use longest remote model prefix matching [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11242](https://github.com/openai/codex/pull/11242) fix(feature) UnderDevelopment feature must be off [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11185](https://github.com/openai/codex/pull/11185) fix: nix build by adding missing dependencies and fix outputHashes [@Philipp-M](https://github.com/Philipp-M)
  - [#10035](https://github.com/openai/codex/pull/10035) fix(tui): tab submits when no task running in steer mode [@joshka-oai](https://github.com/joshka-oai)
  - [#11238](https://github.com/openai/codex/pull/11238) Remove offline fallback for models [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9739](https://github.com/openai/codex/pull/9739) Update models.json @github-actions
  - [#11255](https://github.com/openai/codex/pull/11255) Revert "Update models.json" [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11245](https://github.com/openai/codex/pull/11245) deflake linux-sandbox NoNewPrivs timeout [@joshka-oai](https://github.com/joshka-oai)
  - [#11256](https://github.com/openai/codex/pull/11256) Revert "Revert "Update models.json"" [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11262](https://github.com/openai/codex/pull/11262) chore: change ConfigState so it no longer depends on a single config.toml file for reloading [@bolinfest](https://github.com/bolinfest)
  - [#11263](https://github.com/openai/codex/pull/11263) test: deflake nextest child-process leak in MCP harnesses [@joshka-oai](https://github.com/joshka-oai)
  - [#11247](https://github.com/openai/codex/pull/11247) Adjust shell command timeouts for Windows [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11240](https://github.com/openai/codex/pull/11240) fix(app-server): for external auth, replace id\_token with chatgpt\_acc… [@owenlin0](https://github.com/owenlin0)
  - [#11140](https://github.com/openai/codex/pull/11140) chore(deps): bump insta from 1.46.2 to 1.46.3 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#11139](https://github.com/openai/codex/pull/11139) chore(deps): bump anyhow from 1.0.100 to 1.0.101 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#11138](https://github.com/openai/codex/pull/11138) chore(deps): bump regex from 1.12.2 to 1.12.3 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#11239](https://github.com/openai/codex/pull/11239) Disable dynamic model refresh for custom model providers [@etraut-openai](https://github.com/etraut-openai)
  - [#11269](https://github.com/openai/codex/pull/11269) feat: reserve loopback ephemeral listeners for managed proxy [@bolinfest](https://github.com/bolinfest)
  - [#11279](https://github.com/openai/codex/pull/11279) [apps] Add thread\_id param to optionally load thread config for apps feature check. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11244](https://github.com/openai/codex/pull/11244) feat: add SkillPolicy to skill metadata and support allow\_implicit\_invocation [@alexsong-oai](https://github.com/alexsong-oai)
  - [#10215](https://github.com/openai/codex/pull/10215) chore(tui) cleanup /approvals [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11113](https://github.com/openai/codex/pull/11113) feat(sandbox): enforce proxy-aware network routing in sandbox [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10940](https://github.com/openai/codex/pull/10940) feat: support configurable metric\_exporter [@alexsong-oai](https://github.com/alexsong-oai)
  - [#11294](https://github.com/openai/codex/pull/11294) chore: put crypto provider logic in a shared crate [@bolinfest](https://github.com/bolinfest)
  - [#11207](https://github.com/openai/codex/pull/11207) feat: retain NetworkProxy, when appropriate [@bolinfest](https://github.com/bolinfest)
  - [#11200](https://github.com/openai/codex/pull/11200) memories: add extraction and prompt module foundation [@jif-oai](https://github.com/jif-oai)
  - [#11191](https://github.com/openai/codex/pull/11191) feat: add connector capabilities to sub-agents [@jif-oai](https://github.com/jif-oai)
  - [#11304](https://github.com/openai/codex/pull/11304) Fix spawn\_agent input type [@jif-oai](https://github.com/jif-oai)
  - [#11300](https://github.com/openai/codex/pull/11300) feat: align memory phase 1 and make it stronger [@jif-oai](https://github.com/jif-oai)
  - [#11311](https://github.com/openai/codex/pull/11311) Extract hooks into dedicated crate [@jif-oai](https://github.com/jif-oai)
  - [#11306](https://github.com/openai/codex/pull/11306) feat: phase 2 consolidation [@jif-oai](https://github.com/jif-oai)
  - [#11318](https://github.com/openai/codex/pull/11318) chore: split NPM packages [@jif-oai](https://github.com/jif-oai)
  - [#11322](https://github.com/openai/codex/pull/11322) Fix pending input test waiting logic [@jif-oai](https://github.com/jif-oai)
  - [#11265](https://github.com/openai/codex/pull/11265) Remove ApiPrompt [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11295](https://github.com/openai/codex/pull/11295) tui: keep history recall cursor at line end [@joshka-oai](https://github.com/joshka-oai)
  - [#11288](https://github.com/openai/codex/pull/11288) fix(protocol): approval policy never prompt [@fouad-openai](https://github.com/fouad-openai)
  - [#11323](https://github.com/openai/codex/pull/11323) Revert "Add app-server transport layer with websocket support ([#10693](https://github.com/openai/codex/pull/10693))" [@maxj-oai](https://github.com/maxj-oai)
  - [#11162](https://github.com/openai/codex/pull/11162) Fix: update parallel tool call exec approval to approve on request id [@shijie-oai](https://github.com/shijie-oai)
  - [#11249](https://github.com/openai/codex/pull/11249) [apps] Improve app installation flow. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#11319](https://github.com/openai/codex/pull/11319) feat: opt-out of events in the app-server [@jif-oai](https://github.com/jif-oai)
  - [#11241](https://github.com/openai/codex/pull/11241) Treat first rollout session\_meta as canonical thread identity [@guinness-oai](https://github.com/guinness-oai)
  - [#11339](https://github.com/openai/codex/pull/11339) # Use `@openai/codex` dist-tags for platform binaries instead of separate package names [@bolinfest](https://github.com/bolinfest)
  - [#11330](https://github.com/openai/codex/pull/11330) test(core): stabilize ARM bazel remote-model and parallelism tests [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#11345](https://github.com/openai/codex/pull/11345) core: remove stale apply\_patch SandboxPolicy TODO in seatbelt [@bolinfest](https://github.com/bolinfest)
  - [#11343](https://github.com/openai/codex/pull/11343) Compare full request for websockets incrementality [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11344](https://github.com/openai/codex/pull/11344) fix: reduce usage of `open_if_present` [@jif-oai](https://github.com/jif-oai)
  - [#11336](https://github.com/openai/codex/pull/11336) Always expose view\_image and return unsupported image-input error [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11346](https://github.com/openai/codex/pull/11346) Sanitize MCP image output for text-only models [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11337](https://github.com/openai/codex/pull/11337) Extract tool building [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10941](https://github.com/openai/codex/pull/10941) fix(core): canonicalize wrapper approvals and support heredoc prefix … [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10946](https://github.com/openai/codex/pull/10946) include sandbox (seatbelt, elevated, etc.) as in turn metadata header [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#11349](https://github.com/openai/codex/pull/11349) Strip unsupported images from prompt history to guard against model switch [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#11348](https://github.com/openai/codex/pull/11348) Use thin LTO for alpha Rust release builds [@bolinfest](https://github.com/bolinfest)
  - [#11334](https://github.com/openai/codex/pull/11334) chore: unify memory job flow [@jif-oai](https://github.com/jif-oai)
  - [#11364](https://github.com/openai/codex/pull/11364) feat: mem v2 - PR1 [@jif-oai](https://github.com/jif-oai)
  - [#11365](https://github.com/openai/codex/pull/11365) feat: mem v2 - PR2 [@jif-oai](https://github.com/jif-oai)
  - [#11366](https://github.com/openai/codex/pull/11366) feat: mem v2 - PR3 [@jif-oai](https://github.com/jif-oai)
  - [#11274](https://github.com/openai/codex/pull/11274) Update models.json @github-actions
  - [#11361](https://github.com/openai/codex/pull/11361) # Split command parsing/safety out of `codex-core` into new `codex-command` [@bolinfest](https://github.com/bolinfest)
  - [#11369](https://github.com/openai/codex/pull/11369) feat: mem v2 - PR4 [@jif-oai](https://github.com/jif-oai)
  - [#11362](https://github.com/openai/codex/pull/11362) Enable SOCKS defaults for common local network proxy use cases [@viyatb-oai](https://github.com/viyatb-oai)
  - [#11359](https://github.com/openai/codex/pull/11359) ci: fall back to local Bazel on forks without BuildBuddy key [@joshka-oai](https://github.com/joshka-oai)
  - [#11372](https://github.com/openai/codex/pull/11372) feat: mem v2 - PR5 [@jif-oai](https://github.com/jif-oai)
  - [#11374](https://github.com/openai/codex/pull/11374) feat: mem v2 - PR6 (consolidation) [@jif-oai](https://github.com/jif-oai)
  - [#11377](https://github.com/openai/codex/pull/11377) feat: prevent double backfill [@jif-oai](https://github.com/jif-oai)
  - [#11378](https://github.com/openai/codex/pull/11378) chore: rename codex-command to codex-shell-command [@bolinfest](https://github.com/bolinfest)
  - [#11376](https://github.com/openai/codex/pull/11376) Update models.json @github-actions
  - [#11394](https://github.com/openai/codex/pull/11394) Disable very flaky tests [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11386](https://github.com/openai/codex/pull/11386) Prefer websocket transport when model opts in [@pakrym-oai](https://github.com/pakrym-oai)
  - [#11373](https://github.com/openai/codex/pull/11373) tui: queue non-pending rollback trims in app-event order [@charley-oai](https://github.com/charley-oai)
  - [#11393](https://github.com/openai/codex/pull/11393) Remove `deterministic_process_ids` feature to avoid duplicate `codex-core` builds [@bolinfest](https://github.com/bolinfest)
  - [#11397](https://github.com/openai/codex/pull/11397) fix(exec-policy) No empty command lists [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.99.0)
- 2026-02-09

  ### GPT-5.3-Codex in Cursor and VS Code

  Starting today, GPT-5.3-Codex is available natively in Cursor and VS Code.

  API access is starting with a small set of customers as part of a phased
  release.

  This is the first model treated as a high security capability under the
  Preparedness Framework.

  Safety controls will continue to scale, and API access will expand over the
  next few weeks.
- 2026-02-05

  ### Codex app v260205

  ### New features

  - Support for **[GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)**.
  - Added mid-turn steering. Submit a message while Codex is working to direct its behavior.
  - Attach or drop any file type.

  ### Bug fixes

  - Fix flickering of the app.
- 2026-02-05

  ### Introducing GPT-5.3-Codex

  [Today we’re releasing GPT-5.3-Codex](http://openai.com/index/introducing-gpt-5-3-codex/),
  the most capable agentic coding model to date for complex, real-world software
  engineering.

  GPT-5.3-Codex combines the frontier coding performance of GPT-5.2-Codex with
  stronger reasoning and professional knowledge capabilities, and runs 25% faster
  for Codex users. It’s also better at collaboration while the agent is
  working—delivering more frequent progress updates and responding to steering in
  real time.

  GPT-5.3-Codex is available with paid ChatGPT plans everywhere you can use
  Codex: the Codex app, the CLI, the IDE extension, and Codex Cloud on the web.
  API access for the model will come soon.

  To switch to GPT-5.3-Codex:

  - In the CLI, start a new thread with:

    ```
    codex --model gpt-5.3-codex
    ```

    Or use `/model` during a session.
  - In the IDE extension, make sure you are signed in with ChatGPT, then choose
    GPT-5.3-Codex from the model selector in the composer.
  - In the Codex app, make sure you are signed in with ChatGPT, then choose
    GPT-5.3-Codex from the model selector in the composer.
  - If you don’t see GPT-5.3-Codex, update the CLI, IDE extension, or Codex app
    to the latest version.

  For API-key workflows, continue using `gpt-5.2-codex` while API support rolls
  out.
- 2026-02-05

  ### Codex CLI 0.98.0

  ```
  $ npm install -g @openai/codex@0.98.0
  ```

    View details

  ## New Features

  - Introducing GPT-5.3-Codex. [Learn More](https://openai.com/index/introducing-gpt-5-3-codex/)
  - Steer mode is now stable and enabled by default, so `Enter` sends immediately during running tasks while `Tab` explicitly queues follow-up input. ([#10690](https://github.com/openai/codex/pull/10690))

  ## Bug Fixes

  - Fixed `resumeThread()` argument ordering in the TypeScript SDK so resuming with local images no longer starts an unintended new session. ([#10709](https://github.com/openai/codex/pull/10709))
  - Fixed model-instruction handling when changing models mid-conversation or resuming with a different model, ensuring the correct developer instructions are applied. ([#10651](https://github.com/openai/codex/pull/10651), [#10719](https://github.com/openai/codex/pull/10719))
  - Fixed a remote compaction mismatch where token pre-estimation and compact payload generation could use different base instructions, improving trim accuracy and avoiding context overflows. ([#10692](https://github.com/openai/codex/pull/10692))
  - Cloud requirements now reload immediately after login instead of requiring a later refresh path to take effect. ([#10725](https://github.com/openai/codex/pull/10725))

  ## Chores

  - Restored the default assistant personality to Pragmatic across config and related tests/UI snapshots. ([#10705](https://github.com/openai/codex/pull/10705))
  - Unified collaboration mode naming and metadata across prompts, tools, protocol types, and TUI labels for more consistent mode behavior and messaging. ([#10666](https://github.com/openai/codex/pull/10666))

  ## Changelog

  Full Changelog: [rust-v0.97.0...rust-v0.98.0](https://github.com/openai/codex/compare/rust-v0.97.0...rust-v0.98.0)

  - [#10709](https://github.com/openai/codex/pull/10709) fix: ensure resume args precede image args [@cryptonerdcn](https://github.com/cryptonerdcn)
  - [#10705](https://github.com/openai/codex/pull/10705) chore(config) Default Personality Pragmatic [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10651](https://github.com/openai/codex/pull/10651) fix(core) switching model appends model instructions [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10666](https://github.com/openai/codex/pull/10666) Sync collaboration mode naming across Default prompt, tools, and TUI [@charley-oai](https://github.com/charley-oai)
  - [#10690](https://github.com/openai/codex/pull/10690) Make steer stable by default [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10692](https://github.com/openai/codex/pull/10692) Fix remote compaction estimator/payload instruction small mismatch [@charley-oai](https://github.com/charley-oai)
  - [#10725](https://github.com/openai/codex/pull/10725) Reload cloud requirements after user login [@xl-openai](https://github.com/xl-openai)
  - [#10719](https://github.com/openai/codex/pull/10719) fix(core,app-server) resume with different model [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.98.0)
- 2026-02-05

  ### Codex CLI 0.97.0

  ```
  $ npm install -g @openai/codex@0.97.0
  ```

    View details

  ## New Features

  - Added a session-scoped “Allow and remember” option for MCP/App tool approvals, so repeated calls to the same tool can be auto-approved during the session. ([#10584](https://github.com/openai/codex/pull/10584))
  - Added live skill update detection, so skill file changes are picked up without restarting. ([#10478](https://github.com/openai/codex/pull/10478))
  - Added support for mixed text and image content in dynamic tool outputs for app-server integrations. ([#10567](https://github.com/openai/codex/pull/10567))
  - Added a new `/debug-config` slash command in the TUI to inspect effective configuration. ([#10642](https://github.com/openai/codex/pull/10642))
  - Introduced initial memory plumbing (API client + local persistence) to support thread memory summaries. ([#10629](https://github.com/openai/codex/pull/10629), [#10634](https://github.com/openai/codex/pull/10634))
  - Added configurable `log_dir` so logs can be redirected (including via `-c` overrides) more easily. ([#10678](https://github.com/openai/codex/pull/10678))

  ## Bug Fixes

  - Fixed jitter in the TUI apps/connectors picker by stabilizing description-column rendering. ([#10593](https://github.com/openai/codex/pull/10593))
  - Restored and stabilized the TUI “working” status indicator/shimmer during preamble and early exec flows. ([#10700](https://github.com/openai/codex/pull/10700), [#10701](https://github.com/openai/codex/pull/10701))
  - Improved cloud requirements reliability with higher timeouts, retries, and corrected precedence over MDM settings. ([#10631](https://github.com/openai/codex/pull/10631), [#10633](https://github.com/openai/codex/pull/10633), [#10659](https://github.com/openai/codex/pull/10659))
  - Persisted pending-input user events more consistently for mid-turn injected input handling. ([#10656](https://github.com/openai/codex/pull/10656))

  ## Documentation

  - Documented how to opt in to the experimental app-server API. ([#10667](https://github.com/openai/codex/pull/10667))
  - Updated docs/schema coverage for new `log_dir` configuration behavior. ([#10678](https://github.com/openai/codex/pull/10678))

  ## Chores

  - Added a gated Bubblewrap (`bwrap`) Linux sandbox path to improve filesystem isolation options. ([#9938](https://github.com/openai/codex/pull/9938))
  - Refactored model client lifecycle to be session-scoped and reduced implicit client state. ([#10595](https://github.com/openai/codex/pull/10595), [#10664](https://github.com/openai/codex/pull/10664))
  - Added caching for MCP actions from apps to reduce repeated load latency for users with many installed apps. ([#10662](https://github.com/openai/codex/pull/10662))
  - Added a `none` personality option in protocol/config surfaces. ([#10688](https://github.com/openai/codex/pull/10688))

  ## Changelog

  Full Changelog: [rust-v0.96.0...rust-v0.97.0](https://github.com/openai/codex/compare/rust-v0.96.0...rust-v0.97.0)

  - [#10595](https://github.com/openai/codex/pull/10595) Stop client from being state carrier [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10584](https://github.com/openai/codex/pull/10584) Add option to approve and remember MCP/Apps tool usage [@canvrno-oai](https://github.com/canvrno-oai)
  - [#10644](https://github.com/openai/codex/pull/10644) fix: flaky test [@jif-oai](https://github.com/jif-oai)
  - [#10629](https://github.com/openai/codex/pull/10629) feat: add phase 1 mem client [@jif-oai](https://github.com/jif-oai)
  - [#10633](https://github.com/openai/codex/pull/10633) Cloud Requirements: take precedence over MDM [@gt-oai](https://github.com/gt-oai)
  - [#10659](https://github.com/openai/codex/pull/10659) Increase cloud req timeout [@gt-oai](https://github.com/gt-oai)
  - [#9938](https://github.com/openai/codex/pull/9938) feat(linux-sandbox): add bwrap support [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10656](https://github.com/openai/codex/pull/10656) Persist pending input user events [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10634](https://github.com/openai/codex/pull/10634) feat: add phase 1 mem db [@jif-oai](https://github.com/jif-oai)
  - [#10593](https://github.com/openai/codex/pull/10593) Fix jitter in TUI apps/connectors picker [@canvrno-oai](https://github.com/canvrno-oai)
  - [#10662](https://github.com/openai/codex/pull/10662) [apps] Cache MCP actions from apps. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#10649](https://github.com/openai/codex/pull/10649) Fix test\_shell\_command\_interruption flake [@gt-oai](https://github.com/gt-oai)
  - [#10642](https://github.com/openai/codex/pull/10642) Add /debug-config slash command [@gt-oai](https://github.com/gt-oai)
  - [#10478](https://github.com/openai/codex/pull/10478) Added support for live updates to skills [@etraut-openai](https://github.com/etraut-openai)
  - [#10688](https://github.com/openai/codex/pull/10688) add none personality option [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10567](https://github.com/openai/codex/pull/10567) feat(app-server, core): allow text + image content items for dynamic tool outputs [@owenlin0](https://github.com/owenlin0)
  - [#10667](https://github.com/openai/codex/pull/10667) chore(app-server): document experimental API opt-in [@owenlin0](https://github.com/owenlin0)
  - [#10664](https://github.com/openai/codex/pull/10664) Session-level model client [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10678](https://github.com/openai/codex/pull/10678) feat(core): add configurable log\_dir [@joshka-oai](https://github.com/joshka-oai)
  - [#10631](https://github.com/openai/codex/pull/10631) Cloud Requirements: increase timeout and retries [@gt-oai](https://github.com/gt-oai)
  - [#10650](https://github.com/openai/codex/pull/10650) chore(core) personality migration tests [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10701](https://github.com/openai/codex/pull/10701) fix(tui): restore working shimmer after preamble output [@joshka-oai](https://github.com/joshka-oai)
  - [#10700](https://github.com/openai/codex/pull/10700) fix: ensure status indicator present earlier in exec path [@sayan-oai](https://github.com/sayan-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.97.0)
- 2026-02-04

  ### Codex app v260204

  ### New features

  - Added **Zed** and **Textmate** as options to open files and folders.
  - Added PDF preview in the review panel.

  ### Bug fixes

  - Performance improvements.
- 2026-02-04

  ### Codex CLI 0.96.0

  ```
  $ npm install -g @openai/codex@0.96.0
  ```

    View details

  ## New Features

  - Added `thread/compact` to the v2 app-server API as an async trigger RPC, so clients can start compaction immediately and track completion separately. ([#10445](https://github.com/openai/codex/pull/10445))
  - Added websocket-side rate limit signaling via a new `codex.rate_limits` event, with websocket parity for ETag/reasoning metadata handling. ([#10324](https://github.com/openai/codex/pull/10324))
  - Enabled `unified_exec` on all non-Windows platforms. ([#10641](https://github.com/openai/codex/pull/10641))
  - Constrained requirement values now include source provenance, enabling source-aware config debugging in UI flows like `/debug-config`. ([#10568](https://github.com/openai/codex/pull/10568))

  ## Bug Fixes

  - Fixed `Esc` handling in the TUI `request_user_input` overlay: when notes are open, `Esc` now exits notes mode instead of interrupting the session. ([#10569](https://github.com/openai/codex/pull/10569))
  - Thread listing now queries the state DB first (including archived threads) and falls back to filesystem traversal only when needed, improving listing correctness and resilience. ([#10544](https://github.com/openai/codex/pull/10544))
  - Fixed thread path lookup to require that the resolved file actually exists, preventing invalid thread-id resolutions. ([#10618](https://github.com/openai/codex/pull/10618))
  - Dynamic tool injection now runs in a single transaction to avoid partial state updates. ([#10614](https://github.com/openai/codex/pull/10614))
  - Refined `request_rule` guidance used in approval-policy prompting to correct rule behavior. ([#10379](https://github.com/openai/codex/pull/10379), [#10598](https://github.com/openai/codex/pull/10598))

  ## Documentation

  - Updated app-server docs for `thread/compact` to clarify its asynchronous behavior and thread-busy lifecycle. ([#10445](https://github.com/openai/codex/pull/10445))
  - Updated TUI docs to match the mode-specific `Esc` behavior in `request_user_input`. ([#10569](https://github.com/openai/codex/pull/10569))

  ## Chores

  - Migrated state DB helpers to a versioned SQLite filename scheme and cleaned up legacy state files during runtime initialization. ([#10623](https://github.com/openai/codex/pull/10623))
  - Expanded runtime telemetry with websocket timing metrics and simplified internal metadata flow in core client plumbing. ([#10577](https://github.com/openai/codex/pull/10577), [#10589](https://github.com/openai/codex/pull/10589))

  ## Changelog

  Full Changelog: [rust-v0.95.0...rust-v0.96.0](https://github.com/openai/codex/compare/rust-v0.95.0...rust-v0.96.0)

  - [#10569](https://github.com/openai/codex/pull/10569) tui: make Esc clear request\_user\_input notes while notes are shown [@charley-oai](https://github.com/charley-oai)
  - [#10577](https://github.com/openai/codex/pull/10577) feat: log webscocket timing into runtime metrics [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#10445](https://github.com/openai/codex/pull/10445) Add thread/compact v2 [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10589](https://github.com/openai/codex/pull/10589) Move metadata calculation out of client [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10379](https://github.com/openai/codex/pull/10379) fix(core) updated request\_rule guidance [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10598](https://github.com/openai/codex/pull/10598) fix(core) Request Rule guidance tweak [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10544](https://github.com/openai/codex/pull/10544) Prefer state DB thread listings before filesystem [@jif-oai](https://github.com/jif-oai)
  - [#10614](https://github.com/openai/codex/pull/10614) fix: single transaction for dyn tools injection [@jif-oai](https://github.com/jif-oai)
  - [#10568](https://github.com/openai/codex/pull/10568) Requirements: add source to constrained requirement values [@gt-oai](https://github.com/gt-oai)
  - [#10611](https://github.com/openai/codex/pull/10611) chore: simplify user message detection [@jif-oai](https://github.com/jif-oai)
  - [#10618](https://github.com/openai/codex/pull/10618) fix: make sure file exist in `find_thread_path_by_id_str_in_subdir` [@jif-oai](https://github.com/jif-oai)
  - [#10619](https://github.com/openai/codex/pull/10619) nit: cleaning [@jif-oai](https://github.com/jif-oai)
  - [#10324](https://github.com/openai/codex/pull/10324) Add a codex.rate\_limits event for websockets [@rasmusrygaard](https://github.com/rasmusrygaard)
  - [#10623](https://github.com/openai/codex/pull/10623) Migrate state DB path helpers to versioned filename [@jif-oai](https://github.com/jif-oai)
  - [#10638](https://github.com/openai/codex/pull/10638) Update tests to stop using sse\_completed fixture [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10641](https://github.com/openai/codex/pull/10641) feat: land unified\_exec [@jif-oai](https://github.com/jif-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.96.0)
- 2026-02-04

  ### Codex CLI 0.95.0

  ```
  $ npm install -g @openai/codex@0.95.0
  ```

    View details

  ## New Features

  - Added `codex app <path>` on macOS to launch Codex Desktop from the CLI, with automatic DMG download if it is missing. ([#10418](https://github.com/openai/codex/pull/10418))
  - Added personal skill loading from `~/.agents/skills` (with `~/.codex/skills` compatibility), plus app-server APIs/events to list and download public remote skills. ([#10437](https://github.com/openai/codex/pull/10437), [#10448](https://github.com/openai/codex/pull/10448))
  - `/plan` now accepts inline prompt arguments and pasted images, and slash-command editing/highlighting in the TUI is more polished. ([#10269](https://github.com/openai/codex/pull/10269))
  - Shell-related tools can now run in parallel, improving multi-command execution throughput. ([#10505](https://github.com/openai/codex/pull/10505))
  - Shell executions now receive `CODEX_THREAD_ID`, so scripts and skills can detect the active thread/session. ([#10096](https://github.com/openai/codex/pull/10096))
  - Added vendored Bubblewrap + FFI wiring in the Linux sandbox as groundwork for upcoming runtime integration. ([#10413](https://github.com/openai/codex/pull/10413))

  ## Bug Fixes

  - Hardened Git command safety so destructive or write-capable invocations no longer bypass approval checks. ([#10258](https://github.com/openai/codex/pull/10258))
  - Improved resume/thread browsing reliability by correctly showing saved thread names and fixing thread listing behavior. ([#10340](https://github.com/openai/codex/pull/10340), [#10383](https://github.com/openai/codex/pull/10383))
  - Fixed first-run trust-mode handling so sandbox mode is reported consistently, and made `$PWD/.agents` read-only like `$PWD/.codex`. ([#10415](https://github.com/openai/codex/pull/10415), [#10524](https://github.com/openai/codex/pull/10524))
  - Fixed `codex exec` hanging after interrupt in websocket/streaming flows; interrupted turns now shut down cleanly. ([#10519](https://github.com/openai/codex/pull/10519))
  - Fixed review-mode approval event wiring so `requestApproval` IDs align with the corresponding command execution items. ([#10416](https://github.com/openai/codex/pull/10416))
  - Improved 401 error diagnostics by including server message/body details plus `cf-ray` and `requestId`. ([#10508](https://github.com/openai/codex/pull/10508))

  ## Documentation

  - Expanded TUI chat composer docs to cover slash-command arguments and attachment handling in plan/review flows. ([#10269](https://github.com/openai/codex/pull/10269))
  - Refreshed issue templates and labeler prompts to better separate CLI/app bug reporting and feature requests. ([#10411](https://github.com/openai/codex/pull/10411), [#10453](https://github.com/openai/codex/pull/10453), [#10548](https://github.com/openai/codex/pull/10548), [#10552](https://github.com/openai/codex/pull/10552))

  ## Chores

  - Completed migration off the deprecated `mcp-types` crate to `rmcp`-based protocol types/adapters, then removed the legacy crate. ([#10356](https://github.com/openai/codex/pull/10356), [#10349](https://github.com/openai/codex/pull/10349), [#10357](https://github.com/openai/codex/pull/10357))
  - Updated the `bytes` dependency for a security advisory and cleaned up resolved advisory configuration. ([#10525](https://github.com/openai/codex/pull/10525))

  ## Changelog

  Full Changelog: [rust-v0.94.0...rust-v0.95.0](https://github.com/openai/codex/compare/rust-v0.94.0...rust-v0.95.0)

  - [#10340](https://github.com/openai/codex/pull/10340) Session picker shows thread\_name if set [@pap-openai](https://github.com/pap-openai)
  - [#10381](https://github.com/openai/codex/pull/10381) chore: collab experimental [@jif-oai](https://github.com/jif-oai)
  - [#10231](https://github.com/openai/codex/pull/10231) feat: experimental flags [@jif-oai](https://github.com/jif-oai)
  - [#10382](https://github.com/openai/codex/pull/10382) nit: shell snapshot retention to 3 days [@jif-oai](https://github.com/jif-oai)
  - [#10383](https://github.com/openai/codex/pull/10383) fix: thread listing [@jif-oai](https://github.com/jif-oai)
  - [#10386](https://github.com/openai/codex/pull/10386) fix: Rfc3339 casting [@jif-oai](https://github.com/jif-oai)
  - [#10356](https://github.com/openai/codex/pull/10356) feat: add MCP protocol types and rmcp adapters [@bolinfest](https://github.com/bolinfest)
  - [#10269](https://github.com/openai/codex/pull/10269) Nicer highlighting of slash commands, /plan accepts prompt args and pasted images [@charley-oai](https://github.com/charley-oai)
  - [#10274](https://github.com/openai/codex/pull/10274) Add credits tooltip [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10394](https://github.com/openai/codex/pull/10394) chore: ignore synthetic messages [@jif-oai](https://github.com/jif-oai)
  - [#10398](https://github.com/openai/codex/pull/10398) feat: drop sqlx logging [@jif-oai](https://github.com/jif-oai)
  - [#10281](https://github.com/openai/codex/pull/10281) Select experimental features with space [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10402](https://github.com/openai/codex/pull/10402) feat: add `--experimental` to `generate-ts` [@jif-oai](https://github.com/jif-oai)
  - [#10258](https://github.com/openai/codex/pull/10258) fix: unsafe auto-approval of git commands [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10411](https://github.com/openai/codex/pull/10411) Updated labeler workflow prompt to include "app" label [@etraut-openai](https://github.com/etraut-openai)
  - [#10399](https://github.com/openai/codex/pull/10399) emit a separate metric when the user cancels UAT during elevated setup [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10377](https://github.com/openai/codex/pull/10377) chore(tui) /personalities tip [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10252](https://github.com/openai/codex/pull/10252) [feat] persist thread\_dynamic\_tools in db [@celia-oai](https://github.com/celia-oai)
  - [#10437](https://github.com/openai/codex/pull/10437) feat: Read personal skills from .agents/skills [@gverma-openai](https://github.com/gverma-openai)
  - [#10145](https://github.com/openai/codex/pull/10145) make codex better at git [@pash-openai](https://github.com/pash-openai)
  - [#10418](https://github.com/openai/codex/pull/10418) Add `codex app` macOS launcher [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10447](https://github.com/openai/codex/pull/10447) Fix plan implementation prompt reappearing after /agent thread switch [@charley-oai](https://github.com/charley-oai)
  - [#10064](https://github.com/openai/codex/pull/10064) TUI: Render request\_user\_input results in history and simplify interrupt handling [@charley-oai](https://github.com/charley-oai)
  - [#10349](https://github.com/openai/codex/pull/10349) feat: replace custom mcp-types crate with equivalents from rmcp [@bolinfest](https://github.com/bolinfest)
  - [#10415](https://github.com/openai/codex/pull/10415) Fixed sandbox mode inconsistency if untrusted is selected [@etraut-openai](https://github.com/etraut-openai)
  - [#10452](https://github.com/openai/codex/pull/10452) Hide short worked-for label in final separator [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10357](https://github.com/openai/codex/pull/10357) chore: remove deprecated mcp-types crate [@bolinfest](https://github.com/bolinfest)
  - [#10454](https://github.com/openai/codex/pull/10454) app tool tip [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10455](https://github.com/openai/codex/pull/10455) chore: add phase to message responseitem [@sayan-oai](https://github.com/sayan-oai)
  - [#10414](https://github.com/openai/codex/pull/10414) Require models refresh on cli version mismatch [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10271](https://github.com/openai/codex/pull/10271) [Codex][CLI] Gate image inputs by model modalities [@ccy-oai](https://github.com/ccy-oai)
  - [#10374](https://github.com/openai/codex/pull/10374) Trim compaction input [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10453](https://github.com/openai/codex/pull/10453) Updated bug and feature templates [@etraut-openai](https://github.com/etraut-openai)
  - [#10465](https://github.com/openai/codex/pull/10465) Restore status after preamble [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10406](https://github.com/openai/codex/pull/10406) fix: clarify deprecation message for features.web\_search [@sayan-oai](https://github.com/sayan-oai)
  - [#10474](https://github.com/openai/codex/pull/10474) Ignore remote\_compact\_trims\_function\_call\_history\_to\_fit\_context\_window on windows [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10413](https://github.com/openai/codex/pull/10413) feat(linux-sandbox): vendor bubblewrap and wire it with FFI [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10142](https://github.com/openai/codex/pull/10142) feat(secrets): add codex-secrets crate [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10157](https://github.com/openai/codex/pull/10157) chore: nuke chat/completions API [@jif-oai](https://github.com/jif-oai)
  - [#10498](https://github.com/openai/codex/pull/10498) feat: drop wire\_api from clients [@jif-oai](https://github.com/jif-oai)
  - [#10501](https://github.com/openai/codex/pull/10501) feat: clean codex-api part 1 [@jif-oai](https://github.com/jif-oai)
  - [#10508](https://github.com/openai/codex/pull/10508) Add more detail to 401 error [@gt-oai](https://github.com/gt-oai)
  - [#10521](https://github.com/openai/codex/pull/10521) Avoid redundant transactional check before inserting dynamic tools [@jif-oai](https://github.com/jif-oai)
  - [#10525](https://github.com/openai/codex/pull/10525) chore: update bytes crate in response to security advisory [@bolinfest](https://github.com/bolinfest)
  - [#10408](https://github.com/openai/codex/pull/10408) fix WebSearchAction type clash between v1 and v2 [@sayan-oai](https://github.com/sayan-oai)
  - [#10404](https://github.com/openai/codex/pull/10404) Cleanup collaboration mode variants [@charley-oai](https://github.com/charley-oai)
  - [#10505](https://github.com/openai/codex/pull/10505) Enable parallel shell tools [@jif-oai](https://github.com/jif-oai)
  - [#10532](https://github.com/openai/codex/pull/10532) feat: `find_thread_path_by_id_str_in_subdir` from DB [@jif-oai](https://github.com/jif-oai)
  - [#10524](https://github.com/openai/codex/pull/10524) fix: make $PWD/.agents read-only like $PWD/.codex [@bolinfest](https://github.com/bolinfest)
  - [#10096](https://github.com/openai/codex/pull/10096) Inject CODEX\_THREAD\_ID into the terminal environment [@maxj-oai](https://github.com/maxj-oai)
  - [#10536](https://github.com/openai/codex/pull/10536) Revert "Load untrusted rules" [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10412](https://github.com/openai/codex/pull/10412) fix(app-server): fix TS annotations for optional fields on requests [@owenlin0](https://github.com/owenlin0)
  - [#10416](https://github.com/openai/codex/pull/10416) fix(app-server): fix approval events in review mode [@owenlin0](https://github.com/owenlin0)
  - [#10545](https://github.com/openai/codex/pull/10545) Improve Default mode prompt (less confusion with Plan mode) [@charley-oai](https://github.com/charley-oai)
  - [#10289](https://github.com/openai/codex/pull/10289) [apps] Gateway MCP should be blocking. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#10189](https://github.com/openai/codex/pull/10189) implement per-workspace capability SIDs for workspace specific ACLs [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10548](https://github.com/openai/codex/pull/10548) Updated bug templates and added a new one for app [@etraut-openai](https://github.com/etraut-openai)
  - [#10531](https://github.com/openai/codex/pull/10531) [codex] Default values from requirements if unset [@gt-oai](https://github.com/gt-oai)
  - [#10552](https://github.com/openai/codex/pull/10552) Fixed icon for CLI bug template [@etraut-openai](https://github.com/etraut-openai)
  - [#10039](https://github.com/openai/codex/pull/10039) chore(arg0): advisory-lock janitor for codex tmp paths [@viyatb-oai](https://github.com/viyatb-oai)
  - [#10448](https://github.com/openai/codex/pull/10448) feat: add APIs to list and download public remote skills [@xl-openai](https://github.com/xl-openai)
  - [#10519](https://github.com/openai/codex/pull/10519) Handle exec shutdown on Interrupt (fixes immortal `codex exec` with websockets) [@rasmusrygaard](https://github.com/rasmusrygaard)
  - [#10556](https://github.com/openai/codex/pull/10556) Feat: add upgrade to app server modelList [@shijie-oai](https://github.com/shijie-oai)
  - [#10461](https://github.com/openai/codex/pull/10461) feat(tui): pace catch-up stream chunking with hysteresis [@joshka-oai](https://github.com/joshka-oai)
  - [#10367](https://github.com/openai/codex/pull/10367) chore: add `codex debug app-server` tooling [@celia-oai](https://github.com/celia-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.95.0)
- 2026-02-02

  ### Introducing the Codex app

  #### Codex app

  ![Codex app showing a project sidebar, thread list, and review pane](/images/codex/app/codex-app-basic-light.webp) ![Codex app showing a project sidebar, thread list, and review pane](/images/codex/app/codex-app-basic-dark.webp)

  ![Codex app showing a project sidebar, thread list, and review pane](/images/codex/app/codex-app-basic-light.webp) ![Codex app showing a project sidebar, thread list, and review pane](/images/codex/app/codex-app-basic-dark.webp)

  The Codex app for macOS is a desktop interface for running agent threads in parallel and collaborating with agents on long-running tasks. It includes a project sidebar, thread list, and review pane for tracking work across projects.

  Key features:

  - [Multitask across projects](/codex/app/features#multitask-across-projects)
  - [Built-in worktree support](/codex/app/worktrees)
  - [Voice dictation](/codex/app/features#voice-dictation)
  - [Built-in Git tooling](/codex/app/features#built-in-git-tools)
  - [Skills](/codex/app/features#skills-support)
  - [Automations](/codex/app/automations)

  For a limited time, **ChatGPT Free and Go include Codex**, and **Plus, Pro, Business, Enterprise, and Edu** plans get **double rate limits**. Those higher limits apply in the app, the CLI, your IDE, and the cloud.

  Learn more in the [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/) blog post.

  Check out the [Codex app documentation](/codex/app) for more.

  [Get started with the Codex app](https://persistent.oaistatic.com/codex-app-prod/Codex.dmg)
- 2026-02-02

  ### Codex CLI 0.94.0

  ```
  $ npm install -g @openai/codex@0.94.0
  ```

    View details

  ## New Features

  - Plan mode is now enabled by default with updated interaction guidance in the plan prompt. ([#10313](https://github.com/openai/codex/pull/10313), [#10308](https://github.com/openai/codex/pull/10308), [#10329](https://github.com/openai/codex/pull/10329))
  - Personality configuration is now stable: default is friendly, the config key is `personality`, and existing settings migrate forward. ([#10305](https://github.com/openai/codex/pull/10305), [#10314](https://github.com/openai/codex/pull/10314), [#10310](https://github.com/openai/codex/pull/10310), [#10307](https://github.com/openai/codex/pull/10307))
  - Skills can be loaded from `.agents/skills`, with clearer relative-path instructions and nested-folder markers supported. ([#10317](https://github.com/openai/codex/pull/10317), [#10282](https://github.com/openai/codex/pull/10282), [#10350](https://github.com/openai/codex/pull/10350))
  - Console output now includes runtime metrics for easier diagnostics. ([#10278](https://github.com/openai/codex/pull/10278))

  ## Bug Fixes

  - Unarchiving a thread updates its timestamp so sidebar ordering refreshes. ([#10280](https://github.com/openai/codex/pull/10280))
  - Conversation rules output is capped and prefix rules are deduped to avoid repeated rules. ([#10351](https://github.com/openai/codex/pull/10351), [#10309](https://github.com/openai/codex/pull/10309))
  - Override turn context no longer appends extra items. ([#10354](https://github.com/openai/codex/pull/10354))

  ## Documentation

  - Fixed a broken image link in the npm README. ([#10303](https://github.com/openai/codex/pull/10303))

  ## Changelog

  Full Changelog: [rust-v0.93.0...rust-v0.94.0](https://github.com/openai/codex/compare/rust-v0.93.0...rust-v0.94.0)

  - [#10278](https://github.com/openai/codex/pull/10278) feat: show runtime metrics in console [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#10285](https://github.com/openai/codex/pull/10285) display promo message in usage error [@willwang-openai](https://github.com/willwang-openai)
  - [#10302](https://github.com/openai/codex/pull/10302) fix(nix): update flake for newer Rust toolchain requirements [@douglaz](https://github.com/douglaz)
  - [#10296](https://github.com/openai/codex/pull/10296) chore(features) remove Experimental tag from UTF8 [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10303](https://github.com/openai/codex/pull/10303) Fix npm README image link [@fouad-openai](https://github.com/fouad-openai)
  - [#10306](https://github.com/openai/codex/pull/10306) chore(app-server) add personality update test [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10308](https://github.com/openai/codex/pull/10308) plan mode prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10305](https://github.com/openai/codex/pull/10305) chore(core) Default to friendly personality [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10307](https://github.com/openai/codex/pull/10307) feat(core,tui,app-server) personality migration [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10313](https://github.com/openai/codex/pull/10313) enable plan mode [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10120](https://github.com/openai/codex/pull/10120) feat: fire tracking events for skill invocation [@alexsong-oai](https://github.com/alexsong-oai)
  - [#10317](https://github.com/openai/codex/pull/10317) feat: Support loading skills from .agents/skills [@gverma-openai](https://github.com/gverma-openai)
  - [#10282](https://github.com/openai/codex/pull/10282) Make skills prompt explicit about relative-path lookup [@xl-openai](https://github.com/xl-openai)
  - [#10316](https://github.com/openai/codex/pull/10316) Add websocket telemetry metrics and labels [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#10314](https://github.com/openai/codex/pull/10314) chore(config) Rename config setting to personality [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10310](https://github.com/openai/codex/pull/10310) chore(features) Personality => Stable [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10320](https://github.com/openai/codex/pull/10320) Sync system skills from public repo [@gverma-openai](https://github.com/gverma-openai)
  - [#10322](https://github.com/openai/codex/pull/10322) Sync system skills from public repo for openai yaml changes [@gverma-openai](https://github.com/gverma-openai)
  - [#10323](https://github.com/openai/codex/pull/10323) fix(config) config schema newline [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10329](https://github.com/openai/codex/pull/10329) Improve plan mode interaction rules [@charley-oai](https://github.com/charley-oai)
  - [#10280](https://github.com/openai/codex/pull/10280) Bump thread updated\_at on unarchive to refresh sidebar ordering [@charley-oai](https://github.com/charley-oai)
  - [#10350](https://github.com/openai/codex/pull/10350) fix: System skills marker includes nested folders recursively [@gverma-openai](https://github.com/gverma-openai)
  - [#10351](https://github.com/openai/codex/pull/10351) fix(rules) Limit rules listed in conversation [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10354](https://github.com/openai/codex/pull/10354) Do not append items on override turn context [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10309](https://github.com/openai/codex/pull/10309) fix(core) Deduplicate prefix\_rules before appending [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10373](https://github.com/openai/codex/pull/10373) chore(core) gpt-5.2-codex personality template [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10375](https://github.com/openai/codex/pull/10375) fix(personality) prompt patch [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10371](https://github.com/openai/codex/pull/10371) feat: vendor app-server protocol schema fixtures [@bolinfest](https://github.com/bolinfest)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.94.0)

## January 2026

- 2026-01-31

  ### Codex CLI 0.93.0

  ```
  $ npm install -g @openai/codex@0.93.0
  ```

    View details

  ## New Features

  - Added an optional SOCKS5 proxy listener with policy enforcement and config gating. ([#9803](https://github.com/openai/codex/pull/9803))
  - Plan mode now streams proposed plans into a dedicated TUI view, plus a feature-gated `/plan` shortcut for quick mode switching. ([#9786](https://github.com/openai/codex/pull/9786), [#10103](https://github.com/openai/codex/pull/10103))
  - Added `/apps` to browse connectors in TUI and `$` insertion for app prompts. ([#9728](https://github.com/openai/codex/pull/9728))
  - App-server can now run in external auth mode, accepting ChatGPT auth tokens from a host app and requesting refreshes when needed. ([#10012](https://github.com/openai/codex/pull/10012))
  - Smart approvals are now enabled by default, with explicit approval prompts for MCP tool calls. ([#10286](https://github.com/openai/codex/pull/10286), [#10200](https://github.com/openai/codex/pull/10200))
  - Introduced a SQLite-backed log database with an improved logs client, thread-id filtering, retention, and heuristic coloring. ([#10086](https://github.com/openai/codex/pull/10086), [#10087](https://github.com/openai/codex/pull/10087), [#10150](https://github.com/openai/codex/pull/10150), [#10151](https://github.com/openai/codex/pull/10151), [#10229](https://github.com/openai/codex/pull/10229), [#10228](https://github.com/openai/codex/pull/10228))

  ## Bug Fixes

  - MCP tool image outputs render reliably even when image blocks aren’t first or are partially malformed. ([#9815](https://github.com/openai/codex/pull/9815))
  - Input history recall now restores local image attachments and rich text elements. ([#9628](https://github.com/openai/codex/pull/9628))
  - File search now tracks session CWD changes and supports multi-root traversal with better performance. ([#9279](https://github.com/openai/codex/pull/9279), [#9939](https://github.com/openai/codex/pull/9939), [#10240](https://github.com/openai/codex/pull/10240))
  - Resuming a thread no longer updates `updated_at` until the first turn actually starts. ([#9950](https://github.com/openai/codex/pull/9950))
  - Shell snapshots no longer inherit stdin, avoiding hangs from startup scripts. ([#9735](https://github.com/openai/codex/pull/9735))
  - Connections fall back to HTTP when WebSocket proxies fail. ([#10139](https://github.com/openai/codex/pull/10139))

  ## Documentation

  - Documented app-server AuthMode usage and behavior. ([#10191](https://github.com/openai/codex/pull/10191))

  ## Chores

  - Upgraded the Rust toolchain to 1.93. ([#10080](https://github.com/openai/codex/pull/10080))
  - Updated pnpm versions used in the repo. ([#9992](https://github.com/openai/codex/pull/9992), [#10161](https://github.com/openai/codex/pull/10161))
  - Bazel build and runfiles handling improvements, including remote cache compression. ([#10079](https://github.com/openai/codex/pull/10079), [#10098](https://github.com/openai/codex/pull/10098), [#10102](https://github.com/openai/codex/pull/10102), [#10104](https://github.com/openai/codex/pull/10104))

  ## Changelog

  Full Changelog: [rust-v0.92.0...rust-v0.93.0](https://github.com/openai/codex/compare/rust-v0.92.0...rust-v0.93.0)

  - [#9988](https://github.com/openai/codex/pull/9988) nit: better tool description [@jif-oai](https://github.com/jif-oai)
  - [#9991](https://github.com/openai/codex/pull/9991) nit: better unused prompt [@jif-oai](https://github.com/jif-oai)
  - [#9994](https://github.com/openai/codex/pull/9994) chore: clean orchestrator prompt [@jif-oai](https://github.com/jif-oai)
  - [#10001](https://github.com/openai/codex/pull/10001) backend-client: add get\_config\_requirements\_file [@gt-oai](https://github.com/gt-oai)
  - [#9992](https://github.com/openai/codex/pull/9992) update pnpm to 10.28.2 to address security issues [@mjr-openai](https://github.com/mjr-openai)
  - [#9993](https://github.com/openai/codex/pull/9993) description in role type [@jif-oai](https://github.com/jif-oai)
  - [#9944](https://github.com/openai/codex/pull/9944) TUI footer: right-align context and degrade shortcut summary + mode cleanly [@charley-oai](https://github.com/charley-oai)
  - [#9803](https://github.com/openai/codex/pull/9803) feat(network-proxy): add a SOCKS5 proxy with policy enforcement [@viyatb-oai](https://github.com/viyatb-oai)
  - [#9950](https://github.com/openai/codex/pull/9950) fix(app-server, core): defer initial context write to rollout file until first turn [@owenlin0](https://github.com/owenlin0)
  - [#10003](https://github.com/openai/codex/pull/10003) feat: make it possible to specify --config flags in the SDK [@bolinfest](https://github.com/bolinfest)
  - [#9797](https://github.com/openai/codex/pull/9797) remove sandbox globals. [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10009](https://github.com/openai/codex/pull/10009) chore: introduce \*Args types for new() methods [@bolinfest](https://github.com/bolinfest)
  - [#10011](https://github.com/openai/codex/pull/10011) really fix pwd for windows codex zip [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10007](https://github.com/openai/codex/pull/10007) Remove load from SKILL.toml fallback [@alexsong-oai](https://github.com/alexsong-oai)
  - [#10008](https://github.com/openai/codex/pull/10008) enable live web search for DangerFullAccess sandbox policy [@sayan-oai](https://github.com/sayan-oai)
  - [#9815](https://github.com/openai/codex/pull/9815) Fix: Render MCP image outputs regardless of ordering [@Kbediako](https://github.com/Kbediako)
  - [#9654](https://github.com/openai/codex/pull/9654) Show OAuth error descriptions in callback responses [@blevy-oai](https://github.com/blevy-oai)
  - [#10030](https://github.com/openai/codex/pull/10030) Clarify external editor env var message [@joshka-oai](https://github.com/joshka-oai)
  - [#9949](https://github.com/openai/codex/pull/9949) Ask user question UI footer improvements [@charley-oai](https://github.com/charley-oai)
  - [#9359](https://github.com/openai/codex/pull/9359) tui: stabilize shortcut overlay snapshots on WSL [@slkzgm](https://github.com/slkzgm)
  - [#10040](https://github.com/openai/codex/pull/10040) fix: enable per-turn updates to web search mode [@sayan-oai](https://github.com/sayan-oai)
  - [#10041](https://github.com/openai/codex/pull/10041) fix: allow unknown fields on Notice in schema [@sayan-oai](https://github.com/sayan-oai)
  - [#9628](https://github.com/openai/codex/pull/9628) Restore image attachments/text elements when recalling input history (Up/Down) [@charley-oai](https://github.com/charley-oai)
  - [#9982](https://github.com/openai/codex/pull/9982) [skills] Auto install MCP dependencies when running skils with dependency specs. [@mzeng-openai](https://github.com/mzeng-openai)
  - [#9986](https://github.com/openai/codex/pull/9986) fix(core) info cleanup [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#9941](https://github.com/openai/codex/pull/9941) error code/msg details for failed elevated setup [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#9489](https://github.com/openai/codex/pull/9489) feat(core) RequestRule [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10026](https://github.com/openai/codex/pull/10026) Add exec policy TOML representation [@gt-oai](https://github.com/gt-oai)
  - [#9821](https://github.com/openai/codex/pull/9821) feat: codex exec auto-subscribe to new threads [@jif-oai](https://github.com/jif-oai)
  - [#10004](https://github.com/openai/codex/pull/10004) feat: sqlite 1 [@jif-oai](https://github.com/jif-oai)
  - [#10083](https://github.com/openai/codex/pull/10083) feat: sort metadata by date [@jif-oai](https://github.com/jif-oai)
  - [#10092](https://github.com/openai/codex/pull/10092) Update shell-tool-mcp.yml [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10079](https://github.com/openai/codex/pull/10079) [bazel] Enable remote cache compression [@zbarsky-openai](https://github.com/zbarsky-openai)
  - [#10025](https://github.com/openai/codex/pull/10025) Refine request\_user\_input TUI interactions and option UX [@charley-oai](https://github.com/charley-oai)
  - [#10080](https://github.com/openai/codex/pull/10080) Upgrade to rust 1.93 [@zbarsky-openai](https://github.com/zbarsky-openai)
  - [#10095](https://github.com/openai/codex/pull/10095) Update shell-tool-mcp.yml [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#9939](https://github.com/openai/codex/pull/9939) file-search: improve file query perf [@nornagon-openai](https://github.com/nornagon-openai)
  - [#10097](https://github.com/openai/codex/pull/10097) chore: deprecate old web search feature flags [@sayan-oai](https://github.com/sayan-oai)
  - [#10034](https://github.com/openai/codex/pull/10034) compaction [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10028](https://github.com/openai/codex/pull/10028) allow elevated sandbox to be enabled without base experimental flag [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10101](https://github.com/openai/codex/pull/10101) fix(ci) fix shell-tool-mcp version v2 [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10043](https://github.com/openai/codex/pull/10043) Added `tui.notifications_method` config option [@etraut-openai](https://github.com/etraut-openai)
  - [#10104](https://github.com/openai/codex/pull/10104) [bazel] Fix the build [@zbarsky-openai](https://github.com/zbarsky-openai)
  - [#10102](https://github.com/openai/codex/pull/10102) default enable compression, update test helpers [@sayan-oai](https://github.com/sayan-oai)
  - [#10111](https://github.com/openai/codex/pull/10111) fix(ci) more shell-tool-mcp issues [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10115](https://github.com/openai/codex/pull/10115) update the ci pnpm workflow for shell-tool-mcp to use corepack for pnpm versioning [@mjr-openai](https://github.com/mjr-openai)
  - [#10098](https://github.com/openai/codex/pull/10098) [bazel] Improve runfiles handling [@zbarsky-openai](https://github.com/zbarsky-openai)
  - [#10129](https://github.com/openai/codex/pull/10129) Ensure auto-compaction starts after turn started [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10116](https://github.com/openai/codex/pull/10116) chore(config) personality as a feature [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10123](https://github.com/openai/codex/pull/10123) Add app-server compaction item notifications tests [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10114](https://github.com/openai/codex/pull/10114) chore(config) Update personality instructions [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10128](https://github.com/openai/codex/pull/10128) removing quit from dropdown menu, but not autocomplete [cli] [@natea-oai](https://github.com/natea-oai)
  - [#9728](https://github.com/openai/codex/pull/9728) [connectors] Support connectors part 2 - slash command and tui [@mzeng-openai](https://github.com/mzeng-openai)
  - [#10133](https://github.com/openai/codex/pull/10133) chore(core) personality under development [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10125](https://github.com/openai/codex/pull/10125) emit a metric when we can't spawn powershell [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#10134](https://github.com/openai/codex/pull/10134) fix(tui) reorder personality command [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10135](https://github.com/openai/codex/pull/10135) fix(ci) missing package.json for shell-mcp-tool [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10131](https://github.com/openai/codex/pull/10131) fix: ignore key release events during onboarding [@joshka-oai](https://github.com/joshka-oai)
  - [#10138](https://github.com/openai/codex/pull/10138) fix: remove references to corepack [@bolinfest](https://github.com/bolinfest)
  - [#10086](https://github.com/openai/codex/pull/10086) feat: add log db [@jif-oai](https://github.com/jif-oai)
  - [#10089](https://github.com/openai/codex/pull/10089) feat: async backfill [@jif-oai](https://github.com/jif-oai)
  - [#10087](https://github.com/openai/codex/pull/10087) feat: log db client [@jif-oai](https://github.com/jif-oai)
  - [#10149](https://github.com/openai/codex/pull/10149) chore: improve client [@jif-oai](https://github.com/jif-oai)
  - [#10161](https://github.com/openai/codex/pull/10161) nit: update npm [@jif-oai](https://github.com/jif-oai)
  - [#10163](https://github.com/openai/codex/pull/10163) [experimental] nit: try to speed up apt-install [@jif-oai](https://github.com/jif-oai)
  - [#10164](https://github.com/openai/codex/pull/10164) [experimental] nit: try to speed up apt-install 2 [@jif-oai](https://github.com/jif-oai)
  - [#10150](https://github.com/openai/codex/pull/10150) feat: adding thread ID to logs + filter in the client [@jif-oai](https://github.com/jif-oai)
  - [#10151](https://github.com/openai/codex/pull/10151) feat: add log retention and delete them after 90 days [@jif-oai](https://github.com/jif-oai)
  - [#10152](https://github.com/openai/codex/pull/10152) chore: unify log queries [@jif-oai](https://github.com/jif-oai)
  - [#10175](https://github.com/openai/codex/pull/10175) Add OpenAI docs MCP tooltip [@joshka-oai](https://github.com/joshka-oai)
  - [#10171](https://github.com/openai/codex/pull/10171) feat: reduce span exposition [@jif-oai](https://github.com/jif-oai)
  - [#10139](https://github.com/openai/codex/pull/10139) Fall back to http when websockets fail [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10140](https://github.com/openai/codex/pull/10140) chore: ensure pnpm-workspace.yaml is up-to-date [@bolinfest](https://github.com/bolinfest)
  - [#9017](https://github.com/openai/codex/pull/9017) Better handling skill depdenencies on ENV VAR. [@xl-openai](https://github.com/xl-openai)
  - [#10182](https://github.com/openai/codex/pull/10182) fix: unify `npm publish` call across shell-tool-mcp.yml and rust-release.yml [@bolinfest](https://github.com/bolinfest)
  - [#10180](https://github.com/openai/codex/pull/10180) Add features enable/disable subcommands [@joshka-oai](https://github.com/joshka-oai)
  - [#10184](https://github.com/openai/codex/pull/10184) fix: /approvals -> /permissions [@bolinfest](https://github.com/bolinfest)
  - [#10179](https://github.com/openai/codex/pull/10179) Remove WebSocket wire format [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10186](https://github.com/openai/codex/pull/10186) updating comment to better indicate intent of skipping `quit` in the main slash command menu [@natea-oai](https://github.com/natea-oai)
  - [#10118](https://github.com/openai/codex/pull/10118) [Codex][CLI] Show model-capacity guidance on 429 [@ccy-oai](https://github.com/ccy-oai)
  - [#10012](https://github.com/openai/codex/pull/10012) feat(app-server): support external auth mode [@owenlin0](https://github.com/owenlin0)
  - [#10103](https://github.com/openai/codex/pull/10103) tui: add feature-gated /plan slash command to switch to Plan mode [@charley-oai](https://github.com/charley-oai)
  - [#10191](https://github.com/openai/codex/pull/10191) chore(app-server): document AuthMode [@owenlin0](https://github.com/owenlin0)
  - [#10130](https://github.com/openai/codex/pull/10130) [feat] persist dynamic tools in session rollout file [@celia-oai](https://github.com/celia-oai)
  - [#10181](https://github.com/openai/codex/pull/10181) add error messages for the go plan type [@willwang-openai](https://github.com/willwang-openai)
  - [#10198](https://github.com/openai/codex/pull/10198) feat(tui): route employee feedback follow-ups to internal link [@joshka-oai](https://github.com/joshka-oai)
  - [#10194](https://github.com/openai/codex/pull/10194) load from yaml [@alexsong-oai](https://github.com/alexsong-oai)
  - [#10147](https://github.com/openai/codex/pull/10147) chore(personality) new schema with fallbacks [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10200](https://github.com/openai/codex/pull/10200) MCP tool call approval (simplified version) [@mzeng-openai](https://github.com/mzeng-openai)
  - [#10154](https://github.com/openai/codex/pull/10154) feat: add output to `/ps` [@jif-oai](https://github.com/jif-oai)
  - [#10217](https://github.com/openai/codex/pull/10217) nit: actually run tests [@jif-oai](https://github.com/jif-oai)
  - [#10177](https://github.com/openai/codex/pull/10177) Add community links to startup tooltips [@joshka-oai](https://github.com/joshka-oai)
  - [#10210](https://github.com/openai/codex/pull/10210) Chore: plan mode do not include free form question and always include isOther [@shijie-oai](https://github.com/shijie-oai)
  - [#10218](https://github.com/openai/codex/pull/10218) feat: backfill timing metric [@jif-oai](https://github.com/jif-oai)
  - [#10220](https://github.com/openai/codex/pull/10220) chore: unify metric [@jif-oai](https://github.com/jif-oai)
  - [#8991](https://github.com/openai/codex/pull/8991) Conversation naming [@pap-openai](https://github.com/pap-openai)
  - [#10167](https://github.com/openai/codex/pull/10167) Fetch Requirements from cloud [@gt-oai](https://github.com/gt-oai)
  - [#10225](https://github.com/openai/codex/pull/10225) explorer prompt [@jif-oai](https://github.com/jif-oai)
  - [#10222](https://github.com/openai/codex/pull/10222) fix: make sure the shell exists [@jif-oai](https://github.com/jif-oai)
  - [#10232](https://github.com/openai/codex/pull/10232) chore: do not clean the DB anymore [@jif-oai](https://github.com/jif-oai)
  - [#10229](https://github.com/openai/codex/pull/10229) feat: improve logs client [@jif-oai](https://github.com/jif-oai)
  - [#10228](https://github.com/openai/codex/pull/10228) feat: heuristic coloring of logs [@jif-oai](https://github.com/jif-oai)
  - [#10237](https://github.com/openai/codex/pull/10237) nit: fix db with multiple metadata lines [@jif-oai](https://github.com/jif-oai)
  - [#10208](https://github.com/openai/codex/pull/10208) feat: refactor CodexAuth so invalid state cannot be represented [@bolinfest](https://github.com/bolinfest)
  - [#10212](https://github.com/openai/codex/pull/10212) chore(feature) Experimental: Personality [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10211](https://github.com/openai/codex/pull/10211) chore(feature) Experimental: Smart Approvals [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#10190](https://github.com/openai/codex/pull/10190) Load exec policy rules from requirements [@gt-oai](https://github.com/gt-oai)
  - [#10195](https://github.com/openai/codex/pull/10195) plan mode: add TL;DR checkpoint and client behavior note [@baumann-oai](https://github.com/baumann-oai)
  - [#10239](https://github.com/openai/codex/pull/10239) chore: fix the build breakage that came from a merge race [@bolinfest](https://github.com/bolinfest)
  - [#9786](https://github.com/openai/codex/pull/9786) Plan mode: stream proposed plans, emit plan items, and render in TUI [@charley-oai](https://github.com/charley-oai)
  - [#10063](https://github.com/openai/codex/pull/10063) Tui: hide Code mode footer label [@charley-oai](https://github.com/charley-oai)
  - [#10244](https://github.com/openai/codex/pull/10244) chore: rename ChatGpt -> Chatgpt in type names [@bolinfest](https://github.com/bolinfest)
  - [#10238](https://github.com/openai/codex/pull/10238) Plan mode prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10251](https://github.com/openai/codex/pull/10251) Fix deploy [@charley-oai](https://github.com/charley-oai)
  - [#10255](https://github.com/openai/codex/pull/10255) plan prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#10253](https://github.com/openai/codex/pull/10253) Make plan highlight use popup grey background [@charley-oai](https://github.com/charley-oai)
  - [#10207](https://github.com/openai/codex/pull/10207) Skip loading codex home as project layer [@daniel-oai](https://github.com/daniel-oai)
  - [#10256](https://github.com/openai/codex/pull/10256) Update copy [@pakrym-oai](https://github.com/pakrym-oai)
  - [#9735](https://github.com/openai/codex/pull/9735) core: prevent shell\_snapshot from inheriting stdin [@swordfish444](https://github.com/swordfish444)
  - [#10262](https://github.com/openai/codex/pull/10262) Fix main [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10265](https://github.com/openai/codex/pull/10265) Hide /approvals from the slash-command list [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10267](https://github.com/openai/codex/pull/10267) Update announcement\_tip.toml [@pakrym-oai](https://github.com/pakrym-oai)
  - [#10240](https://github.com/openai/codex/pull/10240) file-search: multi-root walk [@nornagon-openai](https://github.com/nornagon-openai)
  - [#10266](https://github.com/openai/codex/pull/10266) fix: dont auto-enable web\_search for azure [@sayan-oai](https://github.com/sayan-oai)
  - [#9279](https://github.com/openai/codex/pull/9279) fix: update file search directory when session CWD changes [@yuvrajangadsingh](https://github.com/yuvrajangadsingh)
  - [#10249](https://github.com/openai/codex/pull/10249) Validate CODEX\_HOME before resolving [@etraut-openai](https://github.com/etraut-openai)
  - [#10272](https://github.com/openai/codex/pull/10272) chore: implement Mul for TruncationPolicy [@bolinfest](https://github.com/bolinfest)
  - [#10241](https://github.com/openai/codex/pull/10241) Wire up cloud reqs in exec, app-server [@gt-oai](https://github.com/gt-oai)
  - [#10263](https://github.com/openai/codex/pull/10263) Add enforce\_residency to requirements [@gt-oai](https://github.com/gt-oai)
  - [#10276](https://github.com/openai/codex/pull/10276) add missing fields to WebSearchAction and update app-server types [@sayan-oai](https://github.com/sayan-oai)
  - [#10283](https://github.com/openai/codex/pull/10283) Turn on cloud requirements for business too [@gt-oai](https://github.com/gt-oai)
  - [#10287](https://github.com/openai/codex/pull/10287) Fix minor typos in comments and documentation [@ruyut](https://github.com/ruyut)
  - [#10286](https://github.com/openai/codex/pull/10286) feat(core) Smart approvals on [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.93.0)
- 2026-01-28

  ### Web search is now enabled by default

  Codex now enables web search for local tasks in the Codex CLI and IDE Extension.
  By default, Codex uses a web search cache, which is an OpenAI-maintained index of web results. Cached mode returns pre-indexed results instead of fetching live pages, while live mode fetches the most recent data from the web. If you are using `--yolo` or another [full access sandbox setting](/codex/security), web search defaults to live results. To disable this behavior or switch modes, use the `web_search` configuration option:

  - `web_search = "cached"` (default; serves results from the web search cache)
  - `web_search = "live"` (fetches the most recent data from the web; same as `--search`)
  - `web_search = "disabled"` to remove the tool

  To learn more, check out the [configuration documentation](/codex/config-basic).
- 2026-01-27

  ### Codex CLI 0.92.0

  ```
  $ npm install -g @openai/codex@0.92.0
  ```

    View details

  ## New Features

  - API v2 threads can now inject dynamic tools at startup and route their calls/responses end-to-end through the server and core tool pipeline. ([#9539](https://github.com/openai/codex/pull/9539))
  - Added filtering on the thread list in the app server to make large thread sets easier to browse. ([#9897](https://github.com/openai/codex/pull/9897))
  - Introduced a `thread/unarchive` RPC to restore archived rollouts back into active sessions. ([#9843](https://github.com/openai/codex/pull/9843))
  - MCP servers can now define OAuth scopes in `config.toml`, reducing the need to pass `--scopes` on each login. ([#9647](https://github.com/openai/codex/pull/9647))
  - Multi-agent collaboration is more capable and safer, with an explorer role, better collab event mapping, and max-depth guardrails. ([#9817](https://github.com/openai/codex/pull/9817), [#9818](https://github.com/openai/codex/pull/9818), [#9918](https://github.com/openai/codex/pull/9918), [#9899](https://github.com/openai/codex/pull/9899))
  - Cached `web_search` is now the default client behavior. ([#9974](https://github.com/openai/codex/pull/9974))

  ## Bug Fixes

  - Fixed a TUI deadlock/freeze under high streaming throughput by avoiding blocking sends on the main Tokio thread. ([#9951](https://github.com/openai/codex/pull/9951))
  - The `web_search` tool now handles and displays all action types, and shows in-progress activity instead of appearing stuck. ([#9960](https://github.com/openai/codex/pull/9960))
  - Reduced high CPU usage in collaboration flows by eliminating busy-waiting on subagents. ([#9776](https://github.com/openai/codex/pull/9776))
  - Fixed `codex resume --last --json` so prompts parse correctly without conflicting argument errors. ([#9475](https://github.com/openai/codex/pull/9475))
  - Windows sandbox logging now handles UTF-8 safely, preventing failures when truncating multibyte content. ([#8647](https://github.com/openai/codex/pull/8647))
  - `request_user_input` is now rejected outside Plan/Pair modes to prevent invalid tool calls. ([#9955](https://github.com/openai/codex/pull/9955))

  ## Documentation

  - Updated the contribution guidelines for clearer onboarding and workflow expectations. ([#9933](https://github.com/openai/codex/pull/9933))
  - Refreshed protocol/MCP docs to reflect `thread/unarchive` and the updated `request_user_input` question shape. ([#9843](https://github.com/openai/codex/pull/9843), [#9890](https://github.com/openai/codex/pull/9890))

  ## Chores

  - Self-update via Homebrew now uses an explicit cask upgrade command to avoid warnings and ambiguity. ([#9823](https://github.com/openai/codex/pull/9823))
  - Release packaging now consistently writes the bundle zip to `dist/`. ([#9934](https://github.com/openai/codex/pull/9934))
  - Updated key dependencies in the Rust workspace (including `axum`, `tracing`, `globset`, and `tokio-test`). ([#9880](https://github.com/openai/codex/pull/9880), [#9882](https://github.com/openai/codex/pull/9882), [#9883](https://github.com/openai/codex/pull/9883), [#9884](https://github.com/openai/codex/pull/9884))
  - Aligned feature stage naming with public maturity stages and added clearer warnings for underdevelopment features. ([#9929](https://github.com/openai/codex/pull/9929), [#9954](https://github.com/openai/codex/pull/9954))

  ## Changelog

  Full Changelog: [rust-v0.91.0...rust-v0.92.0](https://github.com/openai/codex/compare/rust-v0.91.0...rust-v0.92.0)

  - [#9850](https://github.com/openai/codex/pull/9850) chore: remove extra newline in println [@SohailRaoufi](https://github.com/SohailRaoufi)
  - [#9868](https://github.com/openai/codex/pull/9868) Adjust modes masks [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9874](https://github.com/openai/codex/pull/9874) Prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9877](https://github.com/openai/codex/pull/9877) Plan prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9718](https://github.com/openai/codex/pull/9718) feat(tui) /personality [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#9871](https://github.com/openai/codex/pull/9871) chore(core) move model\_instructions\_template config [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#9539](https://github.com/openai/codex/pull/9539) feat: dynamic tools injection [@jif-oai](https://github.com/jif-oai)
  - [#9818](https://github.com/openai/codex/pull/9818) feat: rebase multi-agent tui on `config_snapshot` [@jif-oai](https://github.com/jif-oai)
  - [#9789](https://github.com/openai/codex/pull/9789) Fix flakey resume test [@gt-oai](https://github.com/gt-oai)
  - [#9784](https://github.com/openai/codex/pull/9784) Fix flakey conversation flow test [@gt-oai](https://github.com/gt-oai)
  - [#9918](https://github.com/openai/codex/pull/9918) feat: explorer collab [@jif-oai](https://github.com/jif-oai)
  - [#9899](https://github.com/openai/codex/pull/9899) feat: disable collab at max depth [@jif-oai](https://github.com/jif-oai)
  - [#9916](https://github.com/openai/codex/pull/9916) Fix up config disabled err msg [@gt-oai](https://github.com/gt-oai)
  - [#9890](https://github.com/openai/codex/pull/9890) Feat: add isOther to question returned by request user input tool [@shijie-oai](https://github.com/shijie-oai)
  - [#9817](https://github.com/openai/codex/pull/9817) feat: codex exec mapping of collab tools [@jif-oai](https://github.com/jif-oai)
  - [#9919](https://github.com/openai/codex/pull/9919) Fix flakey shell snapshot test [@gt-oai](https://github.com/gt-oai)
  - [#9776](https://github.com/openai/codex/pull/9776) fix: attempt to reduce high cpu usage when using collab [@eugeneoden](https://github.com/eugeneoden)
  - [#9928](https://github.com/openai/codex/pull/9928) prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9925](https://github.com/openai/codex/pull/9925) chore: update interrupt message [@jif-oai](https://github.com/jif-oai)
  - [#9843](https://github.com/openai/codex/pull/9843) Add thread/unarchive to restore archived rollouts [@charley-oai](https://github.com/charley-oai)
  - [#9929](https://github.com/openai/codex/pull/9929) Aligned feature stage names with public feature maturity stages [@etraut-openai](https://github.com/etraut-openai)
  - [#9934](https://github.com/openai/codex/pull/9934) ensure codex bundle zip is created in dist/ [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#9897](https://github.com/openai/codex/pull/9897) [app-server] feat: add filtering on thread list [@jif-oai](https://github.com/jif-oai)
  - [#9647](https://github.com/openai/codex/pull/9647) Add MCP server `scopes` config and use it as fallback for OAuth login [@blevy-oai](https://github.com/blevy-oai)
  - [#9943](https://github.com/openai/codex/pull/9943) plan prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#8647](https://github.com/openai/codex/pull/8647) fix: handle utf-8 in windows sandbox logs [@davidgilbertson](https://github.com/davidgilbertson)
  - [#9891](https://github.com/openai/codex/pull/9891) Add composer config and shared menu surface helpers [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9880](https://github.com/openai/codex/pull/9880) chore(deps): bump tracing from 0.1.43 to 0.1.44 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#9882](https://github.com/openai/codex/pull/9882) chore(deps): bump tokio-test from 0.4.4 to 0.4.5 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#9883](https://github.com/openai/codex/pull/9883) chore(deps): bump axum from 0.8.4 to 0.8.8 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#9884](https://github.com/openai/codex/pull/9884) chore(deps): bump globset from 0.4.16 to 0.4.18 in /codex-rs [@dependabot](https://github.com/dependabot)
  - [#9901](https://github.com/openai/codex/pull/9901) fix: remove cli tooltip references to custom prompts [@mattridley](https://github.com/mattridley)
  - [#9823](https://github.com/openai/codex/pull/9823) fix: use `brew upgrade --cask codex` to avoid warnings and ambiguity [@JBallin](https://github.com/JBallin)
  - [#9951](https://github.com/openai/codex/pull/9951) fix: try to fix freezes 2 [@jif-oai](https://github.com/jif-oai)
  - [#9955](https://github.com/openai/codex/pull/9955) Reject request\_user\_input outside Plan/Pair [@charley-oai](https://github.com/charley-oai)
  - [#9933](https://github.com/openai/codex/pull/9933) Updated contribution guidelines [@etraut-openai](https://github.com/etraut-openai)
  - [#9892](https://github.com/openai/codex/pull/9892) Reuse ChatComposer in request\_user\_input overlay [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9957](https://github.com/openai/codex/pull/9957) NIT larger buffer [@jif-oai](https://github.com/jif-oai)
  - [#9953](https://github.com/openai/codex/pull/9953) feat: load interface metadata from SKILL.json [@alexsong-oai](https://github.com/alexsong-oai)
  - [#9954](https://github.com/openai/codex/pull/9954) Warn users on enabling underdevelopment features [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9961](https://github.com/openai/codex/pull/9961) Use test\_codex more [@pakrym-oai](https://github.com/pakrym-oai)
  - [#9960](https://github.com/openai/codex/pull/9960) fix: handle all web\_search actions and in progress invocations [@sayan-oai](https://github.com/sayan-oai)
  - [#9966](https://github.com/openai/codex/pull/9966) plan prompt v7 [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9968](https://github.com/openai/codex/pull/9968) Improve plan mode prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9969](https://github.com/openai/codex/pull/9969) prompt final [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9475](https://github.com/openai/codex/pull/9475) Fix `resume --last` with `--json` option [@etraut-openai](https://github.com/etraut-openai)
  - [#9970](https://github.com/openai/codex/pull/9970) prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9975](https://github.com/openai/codex/pull/9975) plan prompt [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9974](https://github.com/openai/codex/pull/9974) make cached web\_search client-side default [@sayan-oai](https://github.com/sayan-oai)
  - [#9971](https://github.com/openai/codex/pull/9971) tui: wrapping user input questions [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9977](https://github.com/openai/codex/pull/9977) make plan prompt less detailed [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9980](https://github.com/openai/codex/pull/9980) Fixing main and make plan mode reasoning effort medium [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9759](https://github.com/openai/codex/pull/9759) Fix: cap aggregated exec output consistently [@Kbediako](https://github.com/Kbediako)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.92.0)
- 2026-01-25

  ### Codex CLI 0.91.0

  ```
  $ npm install -g @openai/codex@0.91.0
  ```

    View details

  ## Chores

  - Reduced the maximum allowed number of sub-agents to 6 to tighten resource usage and guardrails in agent fan-out behavior ([#9861](https://github.com/openai/codex/pull/9861))

  ## Changelog

  Full Changelog: [rust-v0.90.0...rust-v0.91.0](https://github.com/openai/codex/compare/rust-v0.90.0...rust-v0.91.0)

  - [#9861](https://github.com/openai/codex/pull/9861) chore: half max number of sub-agents [@jif-oai](https://github.com/jif-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.91.0)
- 2026-01-25

  ### Codex CLI 0.90.0

  ```
  $ npm install -g @openai/codex@0.90.0
  ```

    View details

  ## New Features

  - Added a network sandbox proxy with policy enforcement to better control outbound network access. ([#8442](https://github.com/openai/codex/pull/8442))
  - Introduced the first phase of connectors support via the app server and MCP integration, including new config/docs updates. ([#9667](https://github.com/openai/codex/pull/9667))
  - Shipped collaboration mode as beta in the TUI, with a clearer plan → execute handoff and simplified mode selection (Coding vs Plan). ([#9690](https://github.com/openai/codex/pull/9690), [#9712](https://github.com/openai/codex/pull/9712), [#9802](https://github.com/openai/codex/pull/9802), [#9834](https://github.com/openai/codex/pull/9834))
  - Added ephemeral threads and improved collaboration tool provenance metadata for spawned threads. ([#9765](https://github.com/openai/codex/pull/9765), [#9769](https://github.com/openai/codex/pull/9769))
  - WebSocket connections now support proxy configuration. ([#9719](https://github.com/openai/codex/pull/9719))
  - More strict limitation on multi-agents

  ## Bug Fixes

  - Fixed exec policy parsing for multiline quoted arguments. ([#9565](https://github.com/openai/codex/pull/9565))
  - `--yolo` now skips the git repository check instead of failing outside a repo. ([#9590](https://github.com/openai/codex/pull/9590))
  - Improved resume reliability by handling out-of-order events and prompting for the working directory when it differs. ([#9512](https://github.com/openai/codex/pull/9512), [#9731](https://github.com/openai/codex/pull/9731))
  - Backspace no longer deletes a text element when the cursor is at the element’s left edge. ([#9630](https://github.com/openai/codex/pull/9630))
  - Config loading errors are clearer and more actionable across surfaces. ([#9746](https://github.com/openai/codex/pull/9746))
  - Default model selection now respects filtered presets to avoid invalid defaults. ([#9782](https://github.com/openai/codex/pull/9782))

  ## Documentation

  - Corrected a typo in the experimental collaboration prompt template. ([#9716](https://github.com/openai/codex/pull/9716))
  - Added documentation for the new connectors configuration surface. ([#9667](https://github.com/openai/codex/pull/9667))

  ## Chores

  - Refreshed the bundled model catalog/presets. ([#9726](https://github.com/openai/codex/pull/9726))
  - Updated GitHub Actions for Node 24 compatibility. ([#9722](https://github.com/openai/codex/pull/9722))

  ## Changelog

  Full Changelog: [rust-v0.89.0...rust-v0.90.0](https://github.com/openai/codex/compare/rust-v0.89.0...rust-v0.90.0)

  - [#9715](https://github.com/openai/codex/pull/9715) feat: fix formatting of `codex features list` [@bolinfest](https://github.com/bolinfest)
  - [#9716](https://github.com/openai/codex/pull/9716) Fix typo in experimental\_prompt.md [@iudizm](https://github.com/iudizm)
  - [#9719](https://github.com/openai/codex/pull/9719) feat: support proxy for ws connection [@apanasenko-oai](https://github.com/apanasenko-oai)
  - [#9712](https://github.com/openai/codex/pull/9712) TUI: prompt to implement plan and switch to Execute [@charley-oai](https://github.com/charley-oai)
  - [#9713](https://github.com/openai/codex/pull/9713) use machine scope instead of user scope for dpapi. [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#9726](https://github.com/openai/codex/pull/9726) Update models.json @github-actions
  - [#9667](https://github.com/openai/codex/pull/9667) [connectors] Support connectors part 1 - App server & MCP [@mzeng-openai](https://github.com/mzeng-openai)
  - [#9674](https://github.com/openai/codex/pull/9674) feat(app-server) Expose `personality` [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  - [#9733](https://github.com/openai/codex/pull/9733) Change the prompt for planning and reasoning effort [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9730](https://github.com/openai/codex/pull/9730) Hide mode cycle hint while a task is running [@charley-oai](https://github.com/charley-oai)
  - [#9720](https://github.com/openai/codex/pull/9720) feat: add session source as otel metadata tag [@alexsong-oai](https://github.com/alexsong-oai)
  - [#9565](https://github.com/openai/codex/pull/9565) Fix execpolicy parsing for multiline quoted args [@jdsalasca](https://github.com/jdsalasca)
  - [#9745](https://github.com/openai/codex/pull/9745) chore: use some raw strings to reduce quoting [@bolinfest](https://github.com/bolinfest)
  - [#9753](https://github.com/openai/codex/pull/9753) nit: exclude PWD for rc sourcing [@jif-oai](https://github.com/jif-oai)
  - [#9690](https://github.com/openai/codex/pull/9690) feat: tui beta for collab [@jif-oai](https://github.com/jif-oai)
  - [#9116](https://github.com/openai/codex/pull/9116) Persist text element ranges and attached images across history/resume [@charley-oai](https://github.com/charley-oai)
  - [#9777](https://github.com/openai/codex/pull/9777) plan mode prompt change [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9590](https://github.com/openai/codex/pull/9590) fix(exec): skip git repo check when --yolo flag is used [@zerone0x](https://github.com/zerone0x)
  - [#9722](https://github.com/openai/codex/pull/9722) Upgrade GitHub Actions for Node 24 compatibility [@salmanmkc](https://github.com/salmanmkc)
  - [#9611](https://github.com/openai/codex/pull/9611) Print warning if we skip config loading [@gt-oai](https://github.com/gt-oai)
  - [#9782](https://github.com/openai/codex/pull/9782) Select default model from filtered presets [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9512](https://github.com/openai/codex/pull/9512) Fix resume picker when user event appears after head [@jdsalasca](https://github.com/jdsalasca)
  - [#9787](https://github.com/openai/codex/pull/9787) Remove stale TODO comment from defs.bzl [@jcoens-openai](https://github.com/jcoens-openai)
  - [#9700](https://github.com/openai/codex/pull/9700) still load skills [@gt-oai](https://github.com/gt-oai)
  - [#9791](https://github.com/openai/codex/pull/9791) Load untrusted rules [@gt-oai](https://github.com/gt-oai)
  - [#9707](https://github.com/openai/codex/pull/9707) bundle sandbox helper binaries in main zip, for winget. [@iceweasel-oai](https://github.com/iceweasel-oai)
  - [#9792](https://github.com/openai/codex/pull/9792) Chore: remove mode from header [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9793](https://github.com/openai/codex/pull/9793) change collaboration mode to struct [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#8442](https://github.com/openai/codex/pull/8442) feat: introducing a network sandbox proxy [@viyatb-oai](https://github.com/viyatb-oai)
  - [#9802](https://github.com/openai/codex/pull/9802) Have a coding mode and only show coding and plan [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9746](https://github.com/openai/codex/pull/9746) Another round of improvements for config error messages [@etraut-openai](https://github.com/etraut-openai)
  - [#9812](https://github.com/openai/codex/pull/9812) Remove batman reference from experimental prompt [@charley-oai](https://github.com/charley-oai)
  - [#9769](https://github.com/openai/codex/pull/9769) feat: add thread spawn source for collab tools [@jif-oai](https://github.com/jif-oai)
  - [#9765](https://github.com/openai/codex/pull/9765) feat: ephemeral threads [@jif-oai](https://github.com/jif-oai)
  - [#9819](https://github.com/openai/codex/pull/9819) fix: libcc link [@jif-oai](https://github.com/jif-oai)
  - [#9820](https://github.com/openai/codex/pull/9820) fix: musl build [@jif-oai](https://github.com/jif-oai)
  - [#9316](https://github.com/openai/codex/pull/9316) fix(windows-sandbox): remove request files after read [@MaxMiksa](https://github.com/MaxMiksa)
  - [#9630](https://github.com/openai/codex/pull/9630) Prevent backspace from removing a text element when the cursor is at the element’s left edge [@charley-oai](https://github.com/charley-oai)
  - [#9840](https://github.com/openai/codex/pull/9840) Revert "fix: musl build" [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9778](https://github.com/openai/codex/pull/9778) Raise welcome animation breakpoint to 37 rows [@mzeng-openai](https://github.com/mzeng-openai)
  - [#9731](https://github.com/openai/codex/pull/9731) Ask for cwd choice when resuming session from different cwd [@charley-oai](https://github.com/charley-oai)
  - [#9841](https://github.com/openai/codex/pull/9841) Revert "fix: libcc link" [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9806](https://github.com/openai/codex/pull/9806) Use collaboration mode masks without mutating base settings [@aibrahim-oai](https://github.com/aibrahim-oai)
  - [#9834](https://github.com/openai/codex/pull/9834) Mark collab as beta [@pakrym-oai](https://github.com/pakrym-oai)
  - [#9847](https://github.com/openai/codex/pull/9847) Revert "Revert "fix: musl build"" [@jif-oai](https://github.com/jif-oai)
  - [#9855](https://github.com/openai/codex/pull/9855) feat: cap number of agents [@jif-oai](https://github.com/jif-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.90.0)
- 2026-01-23

  ### Team Config for shared configuration

  Team Config groups the files teams use to standardize Codex across repositories and machines. Use it to share:

  - `config.toml` defaults
  - `rules/` for command controls outside the sandbox
  - `skills/` for reusable workflows

  Codex loads these layers from `.codex/` folders in the current working directory, parent folders, and the repo root, plus user (`~/.codex/`) and system (`/etc/codex/`) locations. Higher-precedence locations override lower-precedence ones.

  Admins can still enforce constraints with `requirements.toml`, which overrides defaults regardless of location.

  Learn more in [Team Config](/codex/enterprise/admin-setup#team-config).
- 2026-01-22

  ### Custom prompts deprecated

  Custom prompts are now deprecated. Use [skills](/codex/skills) for reusable instructions and workflows instead.
- 2026-01-14

  ### GPT-5.2-Codex API availability

  GPT-5.2-Codex is now available in the API and for users who sign into Codex with the API.

  To learn more about using GPT-5.2-Codex check out our [API documentation](https://platform.openai.com/docs/models/gpt-5.2-codex).

## December 2025

- 2025-12-19

  ### Agent skills in Codex

  Codex now supports **agent skills**: reusable bundles of instructions (plus optional scripts and resources) that help Codex reliably complete specific tasks.

  Skills are available in both the Codex CLI and IDE extensions.

  You can invoke a skill explicitly by typing `$skill-name` (for example, `$skill-installer` or the experimental `$create-plan` skill after installing it), or let Codex select a skill automatically based on your prompt.

  Learn more in the [skills documentation](/codex/skills).

  ![](/images/codex/skills/skills-selector-cli-light.webp)![](/images/codex/skills/skills-selector-cli-dark.webp)

  ![](/images/codex/skills/skills-selector-ide-light.webp)![](/images/codex/skills/skills-selector-ide-dark.webp)

  #### Folder-based standard (agentskills.io)

  Following the open [agent skills specification](https://agentskills.io/specification), a skill is a folder with a required `SKILL.md` and optional supporting files:

  ```
  my-skill/
    SKILL.md       # Required: instructions + metadata
    scripts/       # Optional: executable code
    references/    # Optional: documentation
    assets/        # Optional: templates, resources
  ```

  #### Install skills per-user or per-repo

  You can install skills for just yourself in `~/.codex/skills`, or for everyone on a project by checking them into `.codex/skills` in the repository.

  Codex also ships with a few built-in system skills to get started, including `$skill-creator` and `$skill-installer`. The `$create-plan` skill is experimental and needs to be installed (for example: `$skill-installer install the create-plan skill from the .experimental folder`).

  #### Curated skills directory

  Codex ships with a [small curated set of skills](https://github.com/openai/skills) inspired by popular workflows at OpenAI. Install them with `$skill-installer`, and expect more over time.
- 2025-12-18

  ### Introducing GPT-5.2-Codex

  [Today we are releasing GPT-5.2-Codex](http://www.openai.com/index/gpt-5-2-codex), the most advanced agentic coding model yet for complex, real-world software engineering.

  GPT-5.2-Codex is a version of [GPT-5.2](https://openai.com/index/introducing-gpt-5-2/) further optimized for agentic coding in Codex, including improvements on long-horizon work through context compaction, stronger performance on large code changes like refactors and migrations, improved performance in Windows environments, and significantly stronger cybersecurity capabilities.

  Starting today, the CLI and IDE Extension will default to `gpt-5.2-codex` for users who are signed in with ChatGPT. API access for the model will come soon.

  If you have a model specified in your [`config.toml` configuration file](/codex/local-config), you can instead try out `gpt-5.2-codex` for a new Codex CLI session using:

  ```
  codex --model gpt-5.2-codex
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5.2-Codex from the dropdown menu.

  If you want to switch for all sessions, you can change your default model to `gpt-5.2-codex` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5.2-codex”
  ```
- 2025-12-04

  ### Introducing Codex for Linear

  Assign or mention @Codex in an issue to kick-off a Codex cloud task. As Codex works, it posts updates back to Linear, providing a link to the completed task so you can review, open a PR, or keep working.

  ![Screenshot of a successful Codex task started in Linear](/images/codex/integrations/linear-codex-example.png)

  To learn more about how to connect Codex to Linear both locally through MCP and through the new integration, check out the [Codex for Linear documentation](/codex/integrations/linear).

## November 2025

- 2025-11-24

  ### Usage and credits fixes

  Minor updates to address a few issues with Codex usage and credits:

  - Adjusted all usage dashboards to show “limits remaining” for consistency. The CLI previously displayed “limits used.”
  - Fixed an issue preventing users from buying credits if their ChatGPT subscription was purchased via iOS or Google Play.
  - Fixed an issue where the CLI could display stale usage information; it now refreshes without needing to send a message first.
  - Optimized the backend to help smooth out usage throughout the day, irrespective of overall Codex load or how traffic is routed. Before, users could get unlucky and hit a few cache misses in a row, leading to much less usage.
- 2025-11-18

  ### Introducing GPT-5.1-Codex-Max

  [Today we are releasing GPT-5.1-Codex-Max](http://www.openai.com/index/gpt-5-1-codex-max), our new frontier agentic coding model.

  GPT‑5.1-Codex-Max is built on an update to our foundational reasoning model, which is trained on agentic tasks across software engineering, math, research, and more. GPT‑5.1-Codex-Max is faster, more intelligent, and more token-efficient at every stage of the development cycle–and a new step towards becoming a reliable coding partner.

  Starting today, the CLI and IDE Extension will default to `gpt-5.1-codex-max` for users that are signed in with ChatGPT. API access for the model will come soon.

  For non-latency-sensitive tasks, we’ve also added a new Extra High (`xhigh`) reasoning effort, which lets the model think for an even longer period of time for a better answer. We still recommend medium as your daily driver for most tasks.

  If you have a model specified in your [`config.toml` configuration file](/codex/local-config), you can instead try out `gpt-5.1-codex-max` for a new Codex CLI session using:

  ```
  codex --model gpt-5.1-codex-max
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5.1-Codex from the dropdown menu.

  If you want to switch for all sessions, you can change your default model to `gpt-5.1-codex-max` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5.1-codex-max”
  ```
- 2025-11-13

  ### Introducing GPT-5.1-Codex and GPT-5.1-Codex-Mini

  Along with the [GPT-5.1 launch in the API](https://openai.com/index/gpt-5-1-for-developers/), we are introducing new `gpt-5.1-codex-mini` and `gpt-5.1-codex` model options in Codex, a version of GPT-5.1 optimized for long-running, agentic coding tasks and use in coding agent harnesses in Codex or Codex-like harnesses.

  Starting today, the CLI and IDE Extension will default to `gpt-5.1-codex` on macOS and Linux and `gpt-5.1` on Windows.

  If you have a model specified in your [`config.toml` configuration file](/codex/local-config), you can instead try out `gpt-5.1-codex` for a new Codex CLI session using:

  ```
  codex --model gpt-5.1-codex
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5.1-Codex from the dropdown menu.

  If you want to switch for all sessions, you can change your default model to `gpt-5.1-codex` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5.1-codex”
  ```
- 2025-11-07

  ### Introducing GPT-5-Codex-Mini

  Today we are introducing a new `gpt-5-codex-mini` model option to Codex CLI and the IDE Extension. The model is a smaller, more cost-effective, but less capable version of `gpt-5-codex` that provides approximately 4x more usage as part of your ChatGPT subscription.

  Starting today, the CLI and IDE Extension will automatically suggest switching to `gpt-5-codex-mini` when you reach 90% of your 5-hour usage limit, to help you work longer without interruptions.

  You can try the model for a new Codex CLI session using:

  ```
  codex --model gpt-5-codex-mini
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5-Codex-Mini from the dropdown menu.

  Alternatively, you can change your default model to `gpt-5-codex-mini` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5-codex-mini”
  ```
- 2025-11-06

  ### GPT-5-Codex model update

  We’ve shipped a minor update to GPT-5-Codex:

  - More reliable file edits with `apply_patch`.
  - Fewer destructive actions such as `git reset`.
  - More collaborative behavior when encountering user edits in files.
  - 3% more efficient in time and usage.

## October 2025

- 2025-10-30

  ### Credits on ChatGPT Pro and Plus

  Codex users on ChatGPT Plus and Pro can now use on-demand credits for more Codex usage beyond what’s included in your plan. [Learn more.](https://developers.openai.com/codex/pricing)
- 2025-10-22

  ### Tag @Codex on GitHub Issues and PRs

  You can now tag `@codex` on a teammate’s pull request to ask clarifying questions, request a follow-up, or ask Codex to make changes. GitHub Issues now also support `@codex` mentions, so you can kick off tasks from any issue, without leaving your workflow.

  ![Codex responding to a GitHub pull request and issue after an @Codex mention.](/images/codex/integrations/github-example.png)
- 2025-10-06

  ### Codex is now GA

  Codex is now generally available with 3 new features — @Codex in Slack, Codex SDK, and new admin tools.

  #### @Codex in Slack

  ![](/images/codex/integrations/slack-example.png)

  You can now questions and assign tasks to Codex directly from Slack. See the [Slack guide](/codex/integrations/slack) to get started.

  #### Codex SDK

  Integrate the same agent that powers the Codex CLI inside your own tools and workflows with the Codex SDK in Typescript. With the new Codex GitHub Action, you can easily add Codex to CI/CD workflows. See the [Codex SDK guide](/codex/sdk) to get started.

  ```
  import { Codex } from "@openai/codex-sdk";

  const agent = new Codex();
  const thread = await agent.startThread();

  const result = await thread.run("Explore this repo");
  console.log(result);

  const result2 = await thread.run("Propose changes");
  console.log(result2);
  ```

  #### New admin controls and analytics

  ![](/images/codex/enterprise/analytics.png)

  ChatGPT workspace admins can now edit or delete Codex Cloud environments. With managed config files, they can set safe defaults for CLI and IDE usage and monitor how Codex uses commands locally. New analytics dashboards help you track Codex usage and code review feedback. Learn more in the [enterprise admin guide.](/codex/enterprise/admin-setup)

  #### Availability and pricing updates

  The Slack integration and Codex SDK are available to developers on ChatGPT Plus, Pro, Business, Edu, and Enterprise plans starting today, while the new admin features will be available to Business, Edu, and Enterprise.
  Beginning October 20, Codex Cloud tasks will count toward your Codex usage. Review the [Codex pricing guide](/codex/pricing) for plan-specific details.

## September 2025

- 2025-09-23

  ### GPT-5-Codex in the API

  GPT-5-Codex is now available in the Responses API, and you can also use it with your API Key in the Codex CLI.
  We plan on regularly updating this model snapshot.
  It is available at the same price as GPT-5. You can learn more about pricing and rate limits for this model on our [model page](http://platform.openai.com/docs/models/gpt-5-codex).
- 2025-09-15

  ### Introducing GPT-5-Codex

  #### New model: GPT-5-Codex

  ![codex-switch-model](https://cdn.openai.com/devhub/docs/codex-switch-model.png)

  GPT-5-Codex is a version of GPT-5 further optimized for agentic coding in Codex.
  It’s available in the IDE extension and CLI when you sign in with your ChatGPT account.
  It also powers the cloud agent and Code Review in GitHub.

  To learn more about GPT-5-Codex and how it performs compared to GPT-5 on software engineering tasks, see our [announcement blog post](https://openai.com/index/introducing-upgrades-to-codex/).

  #### Image outputs

  ![codex-image-outputs](https://cdn.openai.com/devhub/docs/codex-image-output.png)

  When working in the cloud on front-end engineering tasks, GPT-5-Codex can now display screenshots of the UI in Codex web for you to review. With image output, you can iterate on the design without needing to check out the branch locally.

  #### New in Codex CLI

  - You can now resume sessions where you left off with `codex resume`.
  - Context compaction automatically summarizes the session as it approaches the context window limit.

  Learn more in the [latest release notes](https://github.com/openai/codex/releases/tag/rust-v0.36.0)

## August 2025

- 2025-08-27

  ### Late August update

  #### IDE extension (Compatible with VS Code, Cursor, Windsurf)

  ![](/images/codex/changelog/local_task.gif)

  Codex now runs in your IDE with an interactive UI for fast local iteration. Easily switch between modes and reasoning efforts.

  #### Sign in with ChatGPT (IDE & CLI)

  ![](/images/codex/changelog/sign-in-with-chat.gif)

  One-click authentication that removes API keys and uses ChatGPT Enterprise credits.

  #### Move work between local ↔ cloud

  ![](/images/codex/changelog/cloud_task.gif)

  Hand off tasks to Codex web from the IDE with the ability to apply changes locally so you can delegate jobs without leaving your editor.

  #### Code Reviews

  ![](/images/codex/changelog/codex_review.gif)

  Codex goes beyond static analysis. It checks a PR against its intent, reasons across the codebase and dependencies, and can run code to validate the behavior of changes.
- 2025-08-21

  ### Mid August update

  #### Image inputs

  ![](/images/codex/changelog/image_input.png)

  You can now attach images to your prompts in Codex web. This is great for asking Codex to implement frontend changes or follow up on whiteboarding sessions.

  #### Container caching

  ![](/images/codex/changelog/container_caching.png)

  Codex now caches containers to start new tasks and followups 90% faster, dropping the median start time from 48 seconds to 5 seconds. You can optionally configure a maintenance script to update the environment from its cached state to prepare for new tasks. See the docs for more.

  #### Automatic environment setup

  Now, environments without manual setup scripts automatically run the standard installation commands for common package managers like yarn, pnpm, npm, go mod, gradle, pip, poetry, uv, and cargo. This reduces test failures for new environments by 40%.

## June 2025

- 2025-06-13

  ### Best of N

  ![](/images/codex/changelog/best-of-n.png)

  Codex can now generate multiple responses simultaneously for a single task, helping you quickly explore possible solutions to pick the best approach.

  #### Fixes & improvements

  - Added some keyboard shortcuts and a page to explore them. Open it by pressing ⌘-/ on macOS and Ctrl+/ on other platforms.
  - Added a “branch” query parameter in addition to the existing “environment”, “prompt” and “tab=archived” parameters.
  - Added a loading indicator when downloading a repo during container setup.
  - Added support for cancelling tasks.
  - Fixed issues causing tasks to fail during setup.
  - Fixed issues running followups in environments where the setup script changes files that are gitignored.
  - Improved how the agent understands and reacts to network access restrictions.
  - Increased the update rate of text describing what Codex is doing.
  - Increased the limit for setup script duration to 20 minutes for Pro and Business users.
  - Polished code diffs: You can now option-click a code diff header to expand/collapse all of them.
- 2025-06-03

  ### June update

  #### Agent internet access

  ![](/images/codex/changelog/internet_access.png)

  Now you can give Codex access to the internet during task execution to install dependencies, upgrade packages, run tests that need external resources, and more.

  Internet access is off by default. Plus, Pro, and Business users can enable it for specific environments, with granular control of which domains and HTTP methods Codex can access. Internet access for Enterprise users is coming soon.

  Learn more about usage and risks in the [docs](/codex/cloud/agent-internet).

  #### Update existing PRs

  ![](/images/codex/changelog/update_prs.png)

  Now you can update existing pull requests when following up on a task.

  #### Voice dictation

  ![](/images/codex/changelog/voice_dictation.gif)

  Now you can dictate tasks to Codex.

  #### Fixes & improvements

  - Added a link to this changelog from the profile menu.
  - Added support for binary files: When applying patches, all file operations are supported. When using PRs, only deleting or renaming binary files is supported for now.
  - Fixed an issue on iOS where follow up tasks where shown duplicated in the task list.
  - Fixed an issue on iOS where pull request statuses were out of date.
  - Fixed an issue with follow ups where the environments were incorrectly started with the state from the first turn, rather than the most recent state.
  - Fixed internationalization of task events and logs.
  - Improved error messages for setup scripts.
  - Increased the limit on task diffs from 1 MB to 5 MB.
  - Increased the limit for setup script duration from 5 to 10 minutes.
  - Polished GitHub connection flow.
  - Re-enabled Live Activities on iOS after resolving an issue with missed notifications.
  - Removed the mandatory two-factor authentication requirement for users using SSO or social logins.

## May 2025

- 2025-05-22

  ### Reworked environment page

  It’s now easier and faster to set up code execution.

  ![](/images/codex/changelog/environment_setup.png)

  #### Fixes & improvements

  - Added a button to retry failed tasks
  - Added indicators to show that the agent runs without network access after setup
  - Added options to copy git patches after pushing a PR
  - Added support for unicode branch names
  - Fixed a bug where secrets were not piped to the setup script
  - Fixed creating branches when there’s a branch name conflict.
  - Fixed rendering diffs with multi-character emojis.
  - Improved error messages when starting tasks, running setup scripts, pushing PRs, or disconnected from GitHub to be more specific and indicate how to resolve the error.
  - Improved onboarding for teams.
  - Polished how new tasks look while loading.
  - Polished the followup composer.
  - Reduced GitHub disconnects by 90%.
  - Reduced PR creation latency by 35%.
  - Reduced tool call latency by 50%.
  - Reduced task completion latency by 20%.
  - Started setting page titles to task names so Codex tabs are easier to tell apart.
  - Tweaked the system prompt so that agent knows it’s working without network, and can suggest that the user set up dependencies.
  - Updated the docs.
- 2025-05-19

  ### Codex in the ChatGPT iOS app

  Start tasks, view diffs, and push PRs—while you’re away from your desk.

  ![](/images/codex/changelog/mobile_support.png)

