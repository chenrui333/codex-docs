---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/threat-model'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Improving the threat model

Source: https://learn.chatgpt.com/docs/security/threat-model

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Learn what a threat model is and how editing it improves Codex Security's suggestions.

## What a threat model is

A threat model is a short security summary of how your repository works. In Codex Security, you edit it as a `project overview`, and the system uses it as scan context for future scans, prioritization, and review.

Codex Security creates the first draft from the code. If the findings feel off, this is the first thing to edit.

A useful threat model calls out:

- entry points and untrusted inputs
- trust boundaries and auth assumptions
- sensitive data paths or privileged actions
- the areas your team wants reviewed first

For example:

> Public API for account changes. Accepts JSON requests and file uploads. Uses an internal auth service for identity checks and writes billing changes through an internal service. Focus review on auth checks, upload parsing, and service-to-service trust boundaries.

That gives Codex Security a better starting point for future scans and finding prioritization.

## Improving and revisiting the threat model

If you want to improve the results, edit the threat model first. Use it when findings are missing the areas you care about or showing up in places you don't expect. The threat model changes future scan context.

Some users copy the current threat model into Codex, use a chat to improve it
  based on the areas they want reviewed more closely, and then paste the updated
  version back into the web UI.

### Where to edit

To review or update the threat model, go to [Codex Security scans](https://chatgpt.com/codex/security/scans), open the repository, and click **Edit**.

## Related docs

- [Codex Security cloud setup](https://learn.chatgpt.com/docs/security/setup) covers repository setup and findings review.
- [Codex Security](https://learn.chatgpt.com/docs/security) gives the product overview.
- [Codex Security cloud FAQ](https://learn.chatgpt.com/docs/security/faq) covers common cloud questions.
