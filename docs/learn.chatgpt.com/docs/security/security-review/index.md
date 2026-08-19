---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/security-review'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Security Review

Source: https://learn.chatgpt.com/docs/security/security-review

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security Review is available in research preview.
It is available to ChatGPT Enterprise, Business, Edu, and Pro customers; it is
not available on Plus. During the introductory period, Codex Security Review does
not consume ChatGPT credits. Usage limits may apply.

Codex Security Review is an additional review for customers that want to
pay particular attention to security issues in pull requests.

Codex Security Review goes deeper than [Code
Review](https://learn.chatgpt.com/docs/third-party/github) on security-specific risks by analyzing the
pull request diff, supporting repository context, and configured threat models
or security guidance. Code Review can also identify security-related issues as
part of its general review, so you may see occasional overlap between findings.

## Before you start

To configure automatic Codex Security Review, you need:

- Codex Security Review research preview access for your workspace
- [Codex cloud](https://learn.chatgpt.com/docs/cloud) set up with a connected GitHub repository
- GitHub push or admin permission for the repository settings

An existing Codex Security scan is optional.

<a id="configure-security-review"></a>

## Configure Codex Security Review

1. Go to [Codex settings](https://chatgpt.com/codex/settings/code-review).
2. Under **Repository preferences**, choose which pull requests get Codex
   Security Review:
   - **Follow personal** lets each contributor opt in with their personal
     Codex Security Review settings.
   - **Review all PRs** applies to every pull request in the repository.
   - **Review team PRs**, when available, applies to pull requests opened by
     members of your ChatGPT workspace, not members of a GitHub team.
3. Choose when Codex Security Review runs:
   - **On PR open** runs independently when a pull request is opened.
   - **Every push** runs independently after new commits are pushed.
   - **Whenever code review runs** requires Code Review and runs Codex Security
     Review alongside it.

## Add threat-model context

You can configure a threat model to give Codex context about your application's
assets, trust boundaries, security assumptions, and repository-specific risks.
If the repository has an existing Codex Security scan configuration, you can use
its threat model. Otherwise, provide the path to a threat model file checked
into the repository. If you do not specify a source, Codex regenerates the
threat model for every review.

## Set reporting thresholds

By default, automatic Codex Security Reviews report **High** and **Critical**
findings, while manually requested reviews report **Medium**, **High**, and
**Critical** findings. You can change the minimum severity independently for
automatic and manual reviews, and add path-based overrides.

Findings posted to a pull request inherit that pull request's GitHub
visibility. Anyone who can view the pull request can view those findings,
including on public repositories or pull requests from contributors outside
your workspace. Choose reporting thresholds carefully for repositories where
pull request comments may be broadly visible. The reporting threshold controls
what Codex posts to GitHub; the full Codex Security Review report remains in
Codex.

<a id="request-a-security-review"></a>

## Request a Codex Security Review

To request a Codex Security Review manually, add this comment to a pull request:

`@codex security review`

Codex reacts while the review is running, then posts findings that meet your
manual reporting threshold directly on the pull request. Open the associated
Codex task and select the **Security Report** tab to view the full report,
including severity, attack path, supporting evidence, validation, and
remediation guidance. If no issues meet the reporting threshold, Codex does not
post findings to the pull request.

## Related docs

- [Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github) explains Code Review and the GitHub integration.
- [Codex Security](https://learn.chatgpt.com/docs/security) gives the product overview.
- [Codex Security cloud setup](https://learn.chatgpt.com/docs/security/setup) explains repository scans and findings review.
- [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model) explains how to tune repository context.
