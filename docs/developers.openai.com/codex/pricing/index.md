---
source_type: 'developers'
source_area: 'codex_reference'
source_url: 'https://developers.openai.com/codex/pricing'
source_last_modified: '2026-05-05T17:59:09Z'
source_etag: 'W/"ed36c63b5d0f9c0a1bca9fa9ab44c279"'
codex_cli_versions: ["0.125.0", "0.128.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0"]
---

# Pricing – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/pricing

Teams can now get started with Codex with no fixed monthly costs. For a
limited time, eligible ChatGPT Business workspaces can earn up to $500 in
credits when their team members start using Codex. [View
terms](https://help.openai.com/en/articles/20001150-codex-for-business-promotion-earn-up-to-500-in-credits)
or [get started](https://chatgpt.com/codex/team/start).

## Pricing options

### Free

Explore Codex capabilities on quick coding tasks.

$0/month

[Get Free](https://chatgpt.com/plans/free/)

### Go

Use Codex for lightweight coding tasks.

$8/month

[Get Go](https://chatgpt.com/plans/go)

### Plus

Power a few focused coding sessions each week.

$20/month

[Get Plus](https://chatgpt.com/explore/plus?utm_internal_source=openai_developers_codex)

- Codex on the web, in the CLI, in the IDE extension, and on iOS
- Cloud-based integrations like automatic code review and Slack
  integration
- The latest models, including GPT-5.5, GPT-5.4, and GPT-5.3-Codex
- GPT-5.4-mini for higher usage limits on routine local messages
- Flexibly extend usage with [ChatGPT credits](#credits-overview)
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
  Plus plan

### Pro

Choose 5x or 20x higher rate limits than Plus.

From

$100/month

[Get Pro](https://chatgpt.com/explore/pro?utm_internal_source=openai_developers_codex)

Everything in Plus and:

**Double your normal Codex usage on the $100/month tier until May 31, 2026.**

- Access to GPT-5.3-Codex-Spark (research preview), a fast Codex model
  for day-to-day coding tasks
- ~~5x~~ 10x or 20x more Codex usage than Plus\*
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
  Pro plan

[\*Learn more about limits and promos on both tiers.](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans)

### API Key

Great for automation in shared environments like CI.

[Learn more](/codex/auth)

- Codex in the CLI, SDK, or IDE extension
- No cloud-based features (GitHub code review, Slack, etc.)
- Delayed access to new models like GPT-5.3-Codex and
  GPT-5.3-Codex-Spark
- Pay only for the tokens Codex uses, based on [API
  pricing](https://platform.openai.com/docs/pricing)

### Business

Bring Codex into your startup or growing business.

Pay as you go

[Get Business](https://chatgpt.com/codex/team/start)

Everything in Plus and:

- Assign standard or usage-based Codex seats based on your team’s needs.
  [Learn
  more](https://help.openai.com/en/articles/8792828-what-is-chatgpt-business)
- Larger virtual machines to run cloud tasks faster
- Flexibly extend usage with [ChatGPT credits](#credits-overview)
- A secure, dedicated workspace with essential admin controls, SAML SSO,
  and MFA
- No training on your business data by default. [Learn
  more](https://openai.com/business-data/)
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
  Business plan

### Enterprise & Edu

Unlock Codex for your entire organization with enterprise-grade functionality.

[Contact sales](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex)

Everything in Business and:

- Priority request processing
- Enterprise-level security and controls, including SCIM, EKM, user
  analytics, domain verification, and role-based access control
  ([RBAC](https://help.openai.com/en/articles/11750701-rbac))
- Audit logs and usage monitoring via the [Compliance
  API](https://chatgpt.com/admin/api-reference#tag/Codex-Tasks)
- Data retention and data residency controls
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
  Enterprise plan

### API Key

Great for automation in shared environments like CI.

[Learn more](/codex/auth)

- Codex in the CLI, SDK, or IDE extension
- No cloud-based features (GitHub code review, Slack, etc.)
- Delayed access to new models like GPT-5.3-Codex and
  GPT-5.3-Codex-Spark
- Pay only for the tokens Codex uses, based on [API
  pricing](https://platform.openai.com/docs/pricing)

## Frequently asked questions

### What are the usage limits for my plan?

The number of Codex messages you can send depends on the model used, size and
complexity of your coding tasks and whether you run them locally or in the
cloud. Small scripts or routine functions may consume only a fraction of your
allowance, while larger codebases, long-running tasks, or extended sessions that
require Codex to hold more context will use significantly more per message.

GPT-5.5 uses significantly fewer tokens to achieve results comparable to
GPT-5.4. Its Codex setup runs faster and delivers higher-quality results for
most users. These efficiency gains support generous usage limits despite
GPT-5.5 being a significantly more capable model.

Plus

|  | Local Messages[\*](#shared-limits-plus) / 5h | Cloud Tasks[\*](#shared-limits-plus) / 5h | Code Reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 15-80 | Not available | Not available |
| GPT-5.4 | 20-100 | Not available | Not available |
| GPT-5.4-mini | 60-350 | Not available | Not available |
| GPT-5.3-Codex | 30-150 | 10-60 | 20-50 |
|  |  |  |  |
| --- | --- | --- | --- |
| \*The usage limits for local messages and cloud tasks share a **five-hour window**. Additional weekly limits may apply. | | | |
| For Enterprise/Edu users, there are no fixed rate limits - usage scales with [credits](#credits-overview) | | | |
| Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features | | | |

Pro 5x

|  | Local Messages[\*](#shared-limits-pro) / 5h | Cloud Tasks[\*](#shared-limits-pro) / 5h | Code Reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 80-400 | Not available | Not available |
| GPT-5.4 | 100-500 | Not available | Not available |
| GPT-5.4-mini | 300-1750 | Not available | Not available |
| GPT-5.3-Codex | 150-750 | 50-300 | 100-250 |
|  |  |  |  |
| --- | --- | --- | --- |
| \*The usage limits for local messages and cloud tasks share a **five-hour window**. Additional weekly limits may apply. | | | |
| Pro $100 gets 2x the usage shown above until May 31, 2026. | | | |
| For Enterprise/Edu users, there are no fixed rate limits - usage scales with [credits](#credits-overview) | | | |
| Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features | | | |

Pro 20x

|  | Local Messages[\*](#shared-limits-pro-20x) / 5h | Cloud Tasks[\*](#shared-limits-pro-20x) / 5h | Code Reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 300-1600 | Not available | Not available |
| GPT-5.4 | 400-2000 | Not available | Not available |
| GPT-5.4-mini | 1200-7000 | Not available | Not available |
| GPT-5.3-Codex | 600-3000 | 200-1200 | 400-1000 |
|  |  |  |  |
| --- | --- | --- | --- |
| \*The usage limits for local messages and cloud tasks share a **five-hour window**. Additional weekly limits may apply. | | | |
| Pro $200 gets a boost on the usage shown above until May 31, 2026. [Learn more](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans). | | | |
| For Enterprise/Edu users, there are no fixed rate limits - usage scales with [credits](#credits-overview) | | | |
| Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features | | | |

Business

|  | Local Messages[\*](#shared-limits-business) / 5h | Cloud Tasks[\*](#shared-limits-business) / 5h | Code Reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 15-80 | Not available | Not available |
| GPT-5.4 | 20-100 | Not available | Not available |
| GPT-5.4-mini | 60-350 | Not available | Not available |
| GPT-5.3-Codex | 30-150 | 10-60 | 20-50 |
|  |  |  |  |
| --- | --- | --- | --- |
| \*The usage limits for local messages and cloud tasks share a **five-hour window**. Additional weekly limits may apply. | | | |
| For Enterprise/Edu users, there are no fixed rate limits - usage scales with [credits](#credits-overview) | | | |
| Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features | | | |

API Key

|  | Local Messages[\*](#shared-limits-api-key) / 5h | Cloud Tasks[\*](#shared-limits-api-key) / 5h | Code Reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | Not available | Not available | Not available |
| GPT-5.4 | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |
| GPT-5.4-mini | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |
| GPT-5.3-Codex | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |
|  |  |  |  |
| --- | --- | --- | --- |
| \*The usage limits for local messages and cloud tasks share a **five-hour window**. Additional weekly limits may apply. | | | |
| For Enterprise/Edu users, there are no fixed rate limits - usage scales with [credits](#credits-overview) | | | |
| Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features | | | |

Codex usage limits are shared with other agentic features once pricing for
those features is effective. This currently includes [ChatGPT for
Excel](https://help.openai.com/articles/20001063) on Plus and Pro.

Speed configurations increase credit consumption for all applicable models, so
they also use included limits faster. Fast mode consumes credits at a higher
rate for supported models. See [Speed](/codex/speed) for supported models and
rates. Image generations also use included limits ~3-5x faster on average,
depending on image quality and size. GPT-5.3-Codex-Spark is in research preview
for ChatGPT Pro users only, and isn’t available in the API at launch. Because it
runs on specialized low-latency hardware, usage is governed by a separate usage
limit that may adjust based on demand.

### What happens when you hit usage limits?

ChatGPT Plus and Pro users who reach their usage limit can purchase additional
credits to continue working without needing to upgrade their existing plan.

Business, Edu, and Enterprise plans with [flexible
pricing](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)
can purchase additional workspace credits to continue using Codex.

If you are approaching usage limits, you can also switch to a smaller model to
make your usage limits last longer.

All users may also run extra local tasks using an API key, with usage charged at
[standard API rates](https://platform.openai.com/docs/pricing).

### How does image generation count toward usage limits?

Image generation counts toward the same general Codex usage limits as local
messages and cloud tasks. Image generations use included limits 3-5x faster on
average than similar turns without image generation, depending on
image quality and size. After you reach your included limits, image generation
also draws from [credits](#credits-overview).

Image generation isn’t available on the Free plan. When you use Codex with an
API key, API pricing applies to image generation instead of included ChatGPT
usage limits.

### What’s the current Codex usage promo on Pro?

We’re currently offering extra Codex usage on both Pro tiers.

For **Pro $100**, to celebrate the launch, you’ll get **2x Codex usage through May 31, 2026**. That means 10x usage instead of the standard 5x.

**For Pro $200**, as a thank you to our most loyal customers, we’re carrying forward the benefits of our earlier 2x promo, which means Pro $200 now includes 20x Plus on an ongoing basis. In addition, we’re continuing to honor the higher 5-hour Codex limits for a limited time, so those remain at 25x Plus through May 31, 2026 instead of the standard 20x Plus.

### Where can I see my current usage limits?

You can find your current limits in the [Codex usage
dashboard](https://chatgpt.com/codex/settings/usage). If you want to see your
remaining limits during an active Codex CLI session, you can use `/status`.

### How do credits work?

Credits let you continue using Codex after you reach your included usage
limits. Usage draws down from your available credits based on the models and
features you use, allowing you to extend work without interruption.

As of April 2nd, we’re moving pricing to API token-based rates. Credits remain
the core pricing unit that customers purchase and consume, but usage is based
on tokens consumed, calculated as credits per million input tokens, cached
input tokens and output tokens your workspace consumes. Read about tokens
[here](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them).

This format replaces average per-message estimates for your plan with a direct
mapping between token usage and credits. It’s most useful when you want a
clearer view of how input, cached input, and output affect credit consumption.

Under this model, actual credit usage depends on the mix of input, cached input,
and output tokens in each task. The new rate card is displayed in the table
below, and is currently applicable to **new and existing Business customers,
and new Enterprise customers**.

**New and existing customers on all other plan types** should continue to use
the previous message based rate card, until we migrate you to the new rates in
the upcoming weeks.

Select your appropriate plan type in the table below to see rates.

Business & New Enterprise Customers

| Credits per 1M tokens | Input Tokens | Cached input tokens | Output Tokens |
| --- | --- | --- | --- |
| GPT-5.5 | 125 credits | 12.50 credits | 750 credits |
| GPT-5.4 | 62.50 credits | 6.250 credits | 375 credits |
| GPT-5.4-mini | 18.75 credits | 1.875 credits | 113 credits |
| GPT-5.3-Codex | 43.75 credits | 4.375 credits | 350 credits |
| GPT-5.2 | 43.75 credits | 4.375 credits | 350 credits |
| GPT-5.3-Codex-Spark | research preview | | |
| GPT-Image-2 (image) | 200 credits | 50 credits | 750 credits |
| GPT-Image-2 (text) | 125 credits | 31.25 credits | 250 credits |
|  |  |  |  |
| --- | --- | --- | --- |
| Fast mode consumes credits at a higher rate for supported models. See [Speed](/codex/speed) for rates. | | | |
| Cloud tasks and code review run on GPT-5.3-Codex. | | | |

Plus, Pro, Existing Enterprise/Edu and New Edu

|  | Unit | GPT-5.5 | GPT-5.4 | GPT-5.3-Codex | GPT-5.4-mini |
| --- | --- | --- | --- | --- | --- |
| Local Tasks | 1 message | ~14 credits | ~7 credits | ~5 credits | ~2 credits |
| Cloud Tasks | 1 message | Not available | Not available | ~25 credits | Not available |
| Code Review | 1 pull request | Not available | Not available | ~25 credits | Not available |
| Image generation | 1 image (1024px × 1024px) | ~5-6 credits | | | |
| Image generation | 1 image (1024px × 1536px) | ~7-8 credits | | | |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Fast mode consumes credits at a higher rate for supported models. See [Speed](/codex/speed) for rates. | | | | | |
| These averages also apply to GPT-5.2. | | | | | |

Speed configurations will increase credit consumption for all models that apply.
Fast mode consumes credits at a higher rate for supported models. See
[Speed](/codex/speed) for supported models and rates.

[Learn more about credits in ChatGPT Plus and
Pro.](https://help.openai.com/en/articles/12642688)

[Learn more about credits in ChatGPT Business, Enterprise, and
Edu.](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)

### What counts as Code Review usage?

Code Review usage applies only when Codex runs reviews through GitHub—for
example, when you tag `@Codex` for review in a pull request or enable automatic
reviews on your repository. Reviews run locally or outside of GitHub count
toward your general usage limits.

### What can I do to make my usage limits last longer?

The usage limits and credits above are average rates. You can try the following
tips to maximize your limits:

- **Control the size of your prompts.** Be precise with the instructions you
  give Codex, but remove unnecessary context.
- **Reduce the size of your AGENTS.md.** If you work on a larger project, you
  can control how much context you inject through AGENTS.md files by [nesting
  them within your repository](/codex/guides/agents-md#layer-project-instructions).
- **Limit the number of MCP servers you use.** Every [MCP](/codex/mcp) you add
  to Codex adds more context to your messages and uses more of your limit.
  Disable MCP servers when you don’t need them.
- **Switch to a smaller model for routine tasks.** Using GPT-5.4 or
  GPT-5.4-mini can extend your local-message usage limits, depending on the
  model you switch from.

