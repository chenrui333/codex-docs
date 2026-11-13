---
source_type: 'codex_cli_system_skill'
source_area: 'system_skill_openai_docs'
source_url: 'codex-cli://skills/.system/openai-docs/SKILL.md'
source_kind: 'installed_codex_cli'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0", "0.144.0", "0.144.1", "0.144.3", "0.144.4", "0.144.5", "0.144.6", "0.145.0", "0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2", "0.153.3", "0.153.4", "0.154.0", "0.155.0", "0.155.1", "0.156.0", "0.156.1", "0.157.0", "0.157.1", "0.158.0", "0.159.0", "0.159.1", "0.159.2", "0.159.3", "0.160.0", "0.160.1", "0.161.0", "0.162.0", "0.162.1", "0.163.0", "0.164.0", "0.165.0", "0.166.0", "0.167.0", "0.167.1", "0.167.2", "0.168.0", "0.169.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0", "codex-cli 0.144.0", "codex-cli 0.144.1", "codex-cli 0.144.3", "codex-cli 0.144.4", "codex-cli 0.144.5", "codex-cli 0.144.6", "codex-cli 0.145.0", "codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2", "codex-cli 0.153.3", "codex-cli 0.153.4", "codex-cli 0.154.0", "codex-cli 0.155.0", "codex-cli 0.155.1", "codex-cli 0.156.0", "codex-cli 0.156.1", "codex-cli 0.157.0", "codex-cli 0.157.1", "codex-cli 0.158.0", "codex-cli 0.159.0", "codex-cli 0.159.1", "codex-cli 0.159.2", "codex-cli 0.159.3", "codex-cli 0.160.0", "codex-cli 0.160.1", "codex-cli 0.161.0", "codex-cli 0.162.0", "codex-cli 0.162.1", "codex-cli 0.163.0", "codex-cli 0.164.0", "codex-cli 0.165.0", "codex-cli 0.166.0", "codex-cli 0.167.0", "codex-cli 0.167.1", "codex-cli 0.167.2", "codex-cli 0.168.0", "codex-cli 0.169.0"]
codex_cli_release_ref: 'rust-v0.169.0'
codex_cli_source_commit: 'd32063f96c2dff1dc96af839b3952abb6acfeda4'
name: 'openai-docs'
description: 'API first-timers, Codex/Work Q&A. If the user already has an OpenAI API integration, skip this skill for API questions and use the developer docs. Read this skill before answering how Codex or ChatGPT Work behaves, where to find a feature, or how to configure or troubleshoot this app or coding agent. This includes conversation history, model and cache behavior, instruction precedence, permissions, and tool availability. Use for API onboarding only when the user is connecting to the OpenAI API for the first time. Skip action requests, such as scheduling an automation, and tasks fully answered by supplied text or data.'
---

# Codex and ChatGPT Work

Use this skill for Codex and ChatGPT Work capabilities and behavior, first OpenAI API integrations, and OpenAI API model migrations when the user explicitly invokes `$openai-docs`. For other requests, continue with the user's task and consult the relevant official documentation when needed.

Identify the product and surface the user means. If they ask what you can do in this chat, check the tools and settings available here before making a claim about their access.

For broad questions about Codex setup or team customization, first read [Codex self-knowledge](references/codex-self-knowledge.md) for guidance on choosing and combining configuration options.

For other questions about product behavior, look up the current Codex guide at developers.openai.com/codex or the ChatGPT Work guide at learn.chatgpt.com. Open the page for the surface the user is asking about.

For a recent change, or when a source explains only the underlying mechanism, find the feature by name in the [ChatGPT and Codex changelog](https://learn.chatgpt.com/docs/changelog). Use the entry for the relevant surface and version. For Codex client behavior, follow the linked change or tests to verify what the client actually does. Cite what establishes the answer and say which details remain uncertain.

For a first OpenAI API integration, start with the [developer quickstart](https://developers.openai.com/api/docs/quickstart) and follow the guide for the user’s task. Suggest the OpenAI Developers plugin for deeper implementation help.

When the user explicitly invokes `$openai-docs` for an OpenAI API model migration, use the official migration guide for the requested target. For GPT-6 models, start with the [migration quickstart](https://developers.openai.com/api/docs/guides/latest-model#migration-quickstart). Inspect the existing request and prompt, verify compatibility for changed parameters, and preserve supported behavior and the user's chosen target model.
