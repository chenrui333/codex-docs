---
source_type: 'learn'
source_area: 'learn_whats_new'
source_url: 'https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol'
source_kind: 'learn_markdown'
---

# GPT-6.2

Source: https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

[Back to What's new](https://learn.chatgpt.com/docs/whats-new#november-17-2026)

November 17, 2026

GPT-6.2 Astra and Sol launch in ChatGPT Work, Codex, and the API. Choose Astra for your hardest projects or Sol for everyday coding and writing.

## What’s new

### ChatGPT Work

Use Astra or Sol in Work on the web, desktop, or mobile with Plus, Pro, Business, Enterprise, or Edu. Enterprise and Edu admins must first [enable the models in workspace settings](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability#gpt-62-astra-and-gpt-62-sol-in-enterprise-and-edu).

On supported consumer plans, new Work chats default to Sol at **Light** reasoning effort. Enterprise workspaces with model access default to Sol at **Medium**. If you see the Power slider, open **Advanced** to [choose a model and reasoning effort](https://learn.chatgpt.com/docs/models).

### Codex

In the Codex app and CLI, choose Astra to trace a bug across services, fix it, and test the affected workflows. Choose Sol to review a pull request or revise code in response to feedback. Use the model picker in the app or `/model` in the CLI.

Codex and Work share usage. Pro $200 subscribers can use Ultrafast with Sol. Pro $500 subscribers can use it with either model, as can eligible Enterprise and Edu workspaces once an owner enables Ultrafast. See [speed options](https://learn.chatgpt.com/docs/agent-configuration/speed#gpt-62-speed-options) and [plan and client availability](https://learn.chatgpt.com/docs/pricing#feature-availability).

### Chat

To use GPT-6.2 Astra or Sol in ChatGPT, open Work. For the models you can select in Chat, see [models in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt).

### Responses API

Use `gpt-6.2-astra` or `gpt-6.2-sol` in the Responses API. Both models support Ultrafast at launch.

In standard, single-agent mode, you can change reasoning effort or switch from plain text to structured output between replies. Append a `configuration_update` item before the next user message and keep the request-level settings unchanged. [Keeping earlier input intact](https://developers.openai.com/api/docs/guides/keep-prefix-unchanged) helps preserve reasoning across turns and keeps that input eligible for prompt caching.

If your project uses data residency, both models support US and EU regions for Standard, Fast, and Batch processing. Ultrafast supports US data residency only. See the [GPT-6.2 migration guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra) and [API pricing by service tier](https://developers.openai.com/api/docs/pricing#text-tokens).

## Choose your model

### GPT-6.2 Astra

Astra is the stronger choice for complex reasoning. It can work through a research question across multiple sources and check its conclusions against the data.

#### Example use cases

- **Diagnose a bug across services.** Give Astra the failing workflow and ask it to trace the cause, implement a fix, and run the affected tests.
- **Build a deck from a report.** Give Astra the report and your slide template. Ask it to present the findings in your team’s layout and writing style.
- **Investigate a research question.** Give Astra the sources and ask it to compare their findings and identify where the evidence disagrees.

### GPT-6.2 Sol

Sol handles everyday coding, writing, and work that takes several steps. Compared with GPT-6.1 Sol, it lets you complete more tasks on the same paid plan.

#### Example use cases

- **Review a pull request.** Ask Sol to walk through a change and flag issues for the author to address.
- **Revise code after review.** Give Sol the reviewer’s feedback and ask it to update the implementation and run the relevant tests.
- **Turn meeting notes into a project brief.** Ask Sol to pull together decisions, next steps, and open questions from your notes.

Explore the benchmarks and safety evaluations in the [release announcement](https://openai.com/index/introducing-gpt-6-2-astra-sol/).
