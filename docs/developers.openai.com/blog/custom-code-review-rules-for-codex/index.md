---
source_type: 'developers'
source_area: 'codex_blog'
source_url: 'https://developers.openai.com/blog/custom-code-review-rules-for-codex'
source_last_modified: '2026-08-29T10:18:17Z'
source_etag: 'W/"ca961af1fc6501361ae23269c01601a6"'
codex_cli_versions: ["0.151.0", "0.152.0"]
codex_cli_versions_raw: ["codex-cli 0.151.0", "codex-cli 0.152.0"]
---

# Custom Code Review rules for Codex | OpenAI Developers

Source: https://developers.openai.com/blog/custom-code-review-rules-for-codex

When doing code reviews with Codex, some comments keep coming back. It could be about preserving an older API contract, keeping customer data out of logs, or avoiding a rename that would break another service. These checks are important, but they are easy to miss when the context lives with a handful of reviewers.

Codex Code Review can now use custom repository rules in `AGENTS.md` to catch those issues and point authors to the guidance behind a finding. If you already use `AGENTS.md` to guide coding tasks, the same file can help guide reviews, too. This is especially useful when contributors or coding agents are working in an unfamiliar part of a repository and may not know its history yet. In this post, we’ll show where repository rules fit and how to write them well, including what we learned while testing them.

## Shipping more code

Coding agents can take on larger changes and work over longer horizons, helping teams move more of their ideas into code. At OpenAI, weekly PR volume has more than doubled since Q4, and we’re seeing similar trends for many of our customers. More code is good: it helps teams ship new features and solve more problems. It also means more pull requests waiting for someone who knows what to look for, and code review can quickly become the bottleneck.

![Weekly PR volume increases across three quarters](/images/blog/codex-pr-volume-trend.svg)

Review gets harder when several changes arrive at once. A diff can look completely reasonable and still break an older client or cross a boundary the author did not know about. Someone has to remember that context and share it while the author can still act on it.

## The review bottleneck

When more pull requests land, reviewers have less time to work out what each change is trying to do and gather the relevant context before leaving feedback. Once an author moves on to something else, even a small revision can take longer. Fast feedback helps teams make the most of faster development without asking people to become the bottleneck.

Some issues are also hard to spot from the diff alone. Renaming a response field might look like routine cleanup, but it can break clients that still depend on the existing contract. An experienced reviewer may remember why that field needs to stay; a new contributor or an agent working in the service for the first time probably won’t.

## Rules as an interface

So how do you give a coding agent the context your team normally picks up over time? The new repository-rules interface lets you put concise, scoped review guidance in `AGENTS.md`. Codex Code Review can apply the rules that matter to a change and cite them in a finding. Instead of repeating the same explanation in every pull request, you can keep it close to the code it applies to.

As coding models become more steerable, a short, well-scoped instruction can help focus a long review on the things your team actually cares about. The [Codex repository itself keeps Code Review rules in `AGENTS.md`](https://github.com/openai/codex/blob/5c18cc0acc3734f0e78e422a7fd94ea4a2be652e/AGENTS.md#L85-L110), covering concerns such as model-visible context and breaking changes.

Here’s a real example:

The Codex app-server emits an internal notification named `rawResponseItem/completed`. It is marked experimental, but Codex Cloud already consumes it. The repository’s [breaking-change review rule](https://github.com/openai/codex/blob/5c18cc0acc3734f0e78e422a7fd94ea4a2be652e/AGENTS.md#L102-L110) explicitly calls out `rawResponseItem/*` as an integration surface that reviewers should preserve, even while experimental.

The [existing wire name is defined in the app-server protocol](https://github.com/openai/codex/blob/5c18cc0acc3734f0e78e422a7fd94ea4a2be652e/codex-rs/app-server-protocol/src/protocol/common.rs#L1665-L1670). Imagine a cleanup changed one line:

```
-RawResponseItemCompleted => "rawResponseItem/completed"
+RawResponseItemCompleted => "rawResponseItem/done"
```

The change compiles, but clients listening for the existing notification would stop receiving it. The relevant repository-rule excerpt is concise:

```
## Code Review Rules

### Breaking changes

Search for breaking changes in external integration surfaces:

- raw response item events (`rawResponseItem/*`), even while experimental
```

For that illustrative diff, a Code Review finding could read:

> **Keep the existing `rawResponseItem/completed` notification.** Codex Cloud consumers listen for this wire name, so renaming it will break them even though the event is experimental. Keep the existing name or add a backward-compatible event, as described in `AGENTS.md`.

The Codex team [added this rule specifically to protect Codex Cloud consumers](https://github.com/openai/codex/pull/29086). Keep repository-wide rules at the root and service-specific rules in the relevant directory. During review, Codex can apply the guidance that covers the changed files and point authors to the relevant rule; an unrelated change does not need app-server context.

Rules sit alongside the other tools teams already rely on. Tests and linters work well for checks you can express deterministically; repository rules help capture the judgment that is harder to encode. Compatibility requirements and data boundaries are good places to start. Authors do not need to know every past incident or local convention before they make a change; the relevant guidance is already there.

## Writing rules that hold up

We tested how well Code Review could use repository guidance with an eval suite that included known rule violations and safe counterexamples. In the primary suite, rule-guided variants recovered 98% of the required custom findings, compared with 58.3% in the baseline control.

Finding a rule violation is only part of the job. We also wanted to know what happens when several rules compete for attention or a pull request is already busy. We tested both consequential violations and changes that should be left alone, then organized the results around four questions:

What we evaluated

Coverage

Can Codex surface intended violations when diffs are busy and rules
compete for attention?

Restraint

Do clean changes and valid exceptions avoid unnecessary findings?

Retention

Does Code Review continue to catch ordinary bugs outside the repository
rules?

Actionability

Does each finding identify the relevant guidance, location, and
priority?

We also tried familiar ways of writing guidance, from short bullet lists to sections owned by a specific team.

We found the same pattern while using rules in internal repositories. Codex could find and cite local guidance that a default review might miss, but broad instructions could easily create noise. Small, scoped sets with an explicit safe path helped Codex focus on what was most useful without applying a rule to every nearby change.

**Start with a consequential, non-obvious invariant.** Encode a check reviewers repeatedly explain, such as a compatibility requirement or data boundary. If removing a rule would not change the review, leave it out.

**Scope rules to the code they govern.** Put repository-wide guidance at the root and service-specific guidance in a nested `AGENTS.md`. Narrow scope keeps unrelated instructions from competing for attention and makes ownership clear.

**State the invariant and the safe path.** The `rawResponseItem/*` rule identifies the compatibility risk. “Keep the existing name or add a backward-compatible event” gives authors a clear alternative.

**Keep rules durable and current.** Describe outcomes, not function names that may change. Review updates to the rules and narrow or remove guidance that repeatedly produces noise.

Keep formatting and other mechanical checks in CI. Save repository rules for the questions a reviewer would otherwise have to ask again.

## Getting started

If your repository already has Codex Code Review enabled, add two or three rules to the applicable `AGENTS.md` file and open a representative pull request. If you are new to Code Review, the [Code Review quickstart](/codex/third-party/github) explains how to turn it on for a GitHub repository. You can also request a review directly with `@codex review`.

Start with an explanation reviewers keep repeating or a repository-specific mistake that would be consequential to miss. Try one change that should trigger the rule, one safe counterexample, and one unrelated change. Check that the first produces a useful finding and the others do not create noise, then refine the guidance from what you see.

Codex Code Review is still an additional reviewer; tests, branch protections, and required approvals continue to provide hard enforcement.

If you find yourself spending more time reviewing changes than writing them, start with one check your team keeps repeating. Add it to `AGENTS.md` and try Codex Code Review on your next pull request.
