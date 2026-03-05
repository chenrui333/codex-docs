# Codex Pricing

Source: https://developers.openai.com/codex/pricing

For a limited time, **try Codex for free in ChatGPT Free and Go**, or enjoy
**2x Codex rate limits** with Plus, Pro, Business and Enterprise
subscriptions.

### Plus

Power a few focused coding sessions each week.

$20/month

[Get Plus](https://chatgpt.com/explore/plus?utm_internal_source=openai_developers_codex)

- Codex on the web, in the CLI, in the IDE extension, and on iOS
- Cloud-based integrations like automatic code review and Slack integration
- The latest models, including GPT-5.4 and GPT-5.3-Codex
- GPT-5.1-Codex-Mini for up to 4x higher usage limits for local messages
- Flexibly extend usage with [ChatGPT credits](#credits-overview)
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Plus plan

### Pro

Rely on Codex for daily full-time development.

$200/month

[Get Pro](https://chatgpt.com/explore/pro?utm_internal_source=openai_developers_codex)

Everything in Plus and:

- Priority request processing
- Access to GPT-5.3-Codex-Spark (research preview), a fast Codex model for day-to-day coding tasks
- 6x higher usage limits for local and cloud tasks
- 10x more cloud-based code reviews
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Pro plan

### Business

Bring Codex into your startup or growing business.

$30/user/month

[Try for free](https://chatgpt.com/team-sign-up?utm_internal_source=openai_developers_codex)

Everything in Plus and:

- Larger virtual machines to run cloud tasks faster
- Flexibly extend usage with [ChatGPT credits](#credits-overview)
- A secure, dedicated workspace with essential admin controls, SAML SSO, and MFA
- No training on your business data by default. [Learn more](https://openai.com/business-data/)
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Business plan

### Enterprise & Edu

Unlock Codex for your entire organization with enterprise-grade functionality.

[Contact sales](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex)

Everything in Business and:

- Priority request processing
- Enterprise-level security and controls, including SCIM, EKM, user analytics, domain verification, and role-based access control ([RBAC](https://help.openai.com/en/articles/11750701-rbac))
- Audit logs and usage monitoring via the [Compliance API](https://chatgpt.com/admin/api-reference#tag/Codex-Tasks)
- Data retention and data residency controls
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Enterprise plan

### API Key

Great for automation in shared environments like CI.

[Learn more](/codex/auth)

- Codex in the CLI, SDK, or IDE extension
- No cloud-based features (GitHub code review, Slack, etc.)
- Delayed access to new models like GPT-5.3-Codex and GPT-5.3-Codex-Spark
- Pay only for the tokens Codex uses, based on [API pricing](https://platform.openai.com/docs/pricing)

## Frequently asked questions

### What are the usage limits for my plan?

The number of Codex messages you can send depends on the model used, size and complexity of your coding tasks and whether you run them locally or in the cloud. Small scripts or routine functions may consume only a fraction of your allowance, while larger codebases, long-running tasks, or extended sessions that require Codex to hold more context will use significantly more per message.

GPT-5.4

|  | Local Messages[\*](#shared-limits) / 5h | Cloud Tasks[\*](#shared-limits) / 5h | Code Reviews / week |
| --- | --- | --- | --- |
| ChatGPT Plus | 33-168 | Not available | Not available |
| ChatGPT Pro | 223-1120 | Not available | Not available |
| ChatGPT Business | 33-168 | Not available | Not available |
| ChatGPT Enterprise & Edu | No fixed limits — usage scales with [credits](#credits-overview) | | |
| API Key | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |

GPT-5.3-Codex

|  | Local Messages[\*](#shared-limits) / 5h | Cloud Tasks[\*](#shared-limits) / 5h | Code Reviews / week |
| --- | --- | --- | --- |
| ChatGPT Plus | 45-225 | 10-60 | 10-25 |
| ChatGPT Pro | 300-1500 | 50-400 | 100-250 |
| ChatGPT Business | 45-225 | 10-60 | 10-25 |
| ChatGPT Enterprise & Edu | No fixed limits — usage scales with [credits](#credits-overview) | | |
| API Key | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |

GPT-5.1-Codex-Mini

|  | Local Messages[\*](#shared-limits) / 5h | Cloud Tasks[\*](#shared-limits) / 5h | Code Reviews / week |
| --- | --- | --- | --- |
| ChatGPT Plus | 180-900 | Not available | Not available |
| ChatGPT Pro | 1200-6000 | Not available | Not available |
| ChatGPT Business | 180-900 | Not available | Not available |
| ChatGPT Enterprise & Edu | Local usage scales with [credits](#credits-overview) | Not available | Not available |
| API Key | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |

\*The usage limits for local messages and cloud tasks share a **five-hour
window**. Additional weekly limits may apply.

Speed configurations increase credit consumption for all applicable models, so
they also use included limits faster. Details can be found
[here](/codex/speed).

Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features.

GPT-5.3-Codex-Spark is in research preview for ChatGPT Pro users only, and isn’t available in the API at launch. Because it runs on specialized low-latency hardware, usage is governed by a separate usage limit that may adjust based on demand.

### What happens when you hit usage limits?

ChatGPT Plus and Pro users who reach their usage limit can purchase additional credits to continue working without needing to upgrade their existing plan.

Business, Edu, and Enterprise plans with [flexible pricing](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans) can purchase additional workspace credits to continue using Codex.

If you are approaching usage limits, you can also switch to the GPT-5.1-Codex-Mini model to make your usage limits last longer.

All users may also run extra local tasks using an API key, with usage charged at [standard API rates](https://platform.openai.com/docs/pricing).

### Where can I see my current usage limits?

You can find your current limits in the [Codex usage dashboard](https://chatgpt.com/codex/settings/usage). If you want to see your remaining limits during an active Codex CLI session, you can use `/status`.

### How do credits work?

Credits let you continue using Codex after you reach your included usage limits. Usage draws down from your available credits based on the models and features you use, allowing you to extend work without interruption.

Credit cost per message varies based on the model used, the task size and complexity, and the reasoning required. The table shows average credit costs. Average rates may evolve over time as new capabilities are introduced.

GPT-5.4

|  | Unit | Average credit cost |
| --- | --- | --- |
| Local Tasks | 1 message | ~7 credits |
| Cloud Tasks | 1 message | ~34 credits |
| Code Review | 1 pull request | ~34 credits |

GPT-5.3-Codex

|  | Unit | Average credit cost |
| --- | --- | --- |
| Local Tasks | 1 message | ~5 credits |
| Cloud Tasks | 1 message | ~25 credits |
| Code Review | 1 pull request | ~25 credits |

GPT-5.1-Codex-Mini

|  | Unit | Average credit cost |
| --- | --- | --- |
| Local Tasks | 1 message | ~1 credit |
| Cloud Tasks | 1 message | Not available |
| Code Review | 1 pull request | Not available |

These averages also apply to legacy GPT-5.2, GPT-5.2-Codex, GPT-5.1, GPT-5.1-Codex-Max, GPT-5, GPT-5-Codex, and GPT-5-Codex-Mini.

Speed configurations will increase credit consumption for all models that apply.
Details can be found [here](/codex/speed).

[Learn more about credits in ChatGPT Plus and Pro.](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-freegopluspro-sora)
[Learn more about credits in ChatGPT Business, Enterprise, and Edu.](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)

### What counts as Code Review usage?

Code Review usage applies only when Codex runs reviews through GitHub—for example, when you tag `@Codex` for review in a pull request or enable automatic reviews on your repository. Reviews run locally or outside of GitHub count toward your general usage limits.

### What can I do to make my usage limits last longer?

The usage limits and credits above are average rates. You can try the following tips to maximize your limits:

- **Control the size of your prompts.** Be precise with the instructions you give Codex, but remove unnecessary context.
- **Reduce the size of your AGENTS.md.** If you work on a larger project, you can control how much context you inject through AGENTS.md files by [nesting them within your repository](/codex/guides/agents-md#layer-project-instructions).
- **Limit the number of MCP servers you use.** Every [MCP](/codex/mcp) you add to Codex adds more context to your messages and uses more of your limit. Disable MCP servers when you don’t need them.
- **Switch to GPT-5.1-Codex-Mini for routine tasks.** Using the mini model should extend your usage limits by roughly 4x.

