---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/ai-app-evals'
source_last_modified: '2026-05-20T00:58:19Z'
source_etag: 'W/"65019a0d160c342c558c3007cd130234"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0"]
---

# Add evals to your AI application | Codex use cases

Source: https://developers.openai.com/codex/use-cases/ai-app-evals

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Add evals to your AI application

Use Codex to turn expected behavior into a Promptfoo eval suite.

Difficulty **Intermediate**

Time horizon **1h**

Ask Codex to inspect your AI application, identify the behavior you want to evaluate, and add a runnable Promptfoo eval suite.

## Best for

- AI applications that already have prompts, model calls, tools, retrieval, agents, or product requirements but no repeatable eval suite.
- Teams preparing a model, prompt, retrieval, or agent change and wanting regression tests before the pull request merges.
- Quality reviews where repeated manual checks should become committed eval cases.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/ai-app-evals/?export=pdf)

Ask Codex to inspect your AI application, identify the behavior you want to evaluate, and add a runnable Promptfoo eval suite.

Intermediate

1h

Related links

[Promptfoo configuration](https://www.promptfoo.dev/docs/configuration/guide/)  [Evaluation best practices](/api/docs/guides/evaluation-best-practices)

## Best for

- AI applications that already have prompts, model calls, tools, retrieval, agents, or product requirements but no repeatable eval suite.
- Teams preparing a model, prompt, retrieval, or agent change and wanting regression tests before the pull request merges.
- Quality reviews where repeated manual checks should become committed eval cases.

## Skills & Plugins

- [Promptfoo](https://github.com/promptfoo/promptfoo/tree/main/plugins/promptfoo)

  Plugin that includes `$promptfoo-evals` and `$promptfoo-provider-setup` for creating, connecting, running, and QAing eval suites.

| Skill | Why use it |
| --- | --- |
| [Promptfoo](https://github.com/promptfoo/promptfoo/tree/main/plugins/promptfoo) | Plugin that includes `$promptfoo-evals` and `$promptfoo-provider-setup` for creating, connecting, running, and QAing eval suites. |

## Starter prompt

Use $promptfoo-evals to add a Promptfoo eval suite for this AI application. If there is not already a working Promptfoo provider or target adapter, use $promptfoo-provider-setup first.
Behavior to evaluate: [support answer quality / tool-call correctness / retrieval grounding / business rules / agent task completion]
Before editing:
- Inspect the app path users hit and any existing evals or tests.
- Propose the smallest useful eval plan: target adapter, seed cases, assertions, files, commands, and required env vars or local services.
- Do not change production prompts, model settings, or app behavior until the baseline eval exists and has been run.
Requirements:
- Exercise the application path users hit when possible, not only the raw model prompt.
- Keep fixtures free of secrets, customer data, and sensitive personal data.
- Add a local eval command such as `npm run evals` or document the exact command to run.
Finish with:
- Files changed
- Eval commands run
- Passing and failing cases
- Recommended next evals to add

[Open in the Codex app](codex://new?prompt=Use+%24promptfoo-evals+to+add+a+Promptfoo+eval+suite+for+this+AI+application.+If+there+is+not+already+a+working+Promptfoo+provider+or+target+adapter%2C+use+%24promptfoo-provider-setup+first.%0A%0ABehavior+to+evaluate%3A+%5Bsupport+answer+quality+%2F+tool-call+correctness+%2F+retrieval+grounding+%2F+business+rules+%2F+agent+task+completion%5D%0A%0ABefore+editing%3A%0A-+Inspect+the+app+path+users+hit+and+any+existing+evals+or+tests.%0A-+Propose+the+smallest+useful+eval+plan%3A+target+adapter%2C+seed+cases%2C+assertions%2C+files%2C+commands%2C+and+required+env+vars+or+local+services.%0A-+Do+not+change+production+prompts%2C+model+settings%2C+or+app+behavior+until+the+baseline+eval+exists+and+has+been+run.%0A%0ARequirements%3A%0A-+Exercise+the+application+path+users+hit+when+possible%2C+not+only+the+raw+model+prompt.%0A-+Keep+fixtures+free+of+secrets%2C+customer+data%2C+and+sensitive+personal+data.%0A-+Add+a+local+eval+command+such+as+%60npm+run+evals%60+or+document+the+exact+command+to+run.%0A%0AFinish+with%3A%0A-+Files+changed%0A-+Eval+commands+run%0A-+Passing+and+failing+cases%0A-+Recommended+next+evals+to+add "Open in the Codex app")

Use $promptfoo-evals to add a Promptfoo eval suite for this AI application. If there is not already a working Promptfoo provider or target adapter, use $promptfoo-provider-setup first.
Behavior to evaluate: [support answer quality / tool-call correctness / retrieval grounding / business rules / agent task completion]
Before editing:
- Inspect the app path users hit and any existing evals or tests.
- Propose the smallest useful eval plan: target adapter, seed cases, assertions, files, commands, and required env vars or local services.
- Do not change production prompts, model settings, or app behavior until the baseline eval exists and has been run.
Requirements:
- Exercise the application path users hit when possible, not only the raw model prompt.
- Keep fixtures free of secrets, customer data, and sensitive personal data.
- Add a local eval command such as `npm run evals` or document the exact command to run.
Finish with:
- Files changed
- Eval commands run
- Passing and failing cases
- Recommended next evals to add

## Introduction

When you are building an AI application, or making changes to an existing one, you want to make sure it behaves as expected. Evals are a way to systematically test a set of scenarios and catch regressions before they ship.

You can use Promptfoo to run evals on your AI application, and Codex to help you create and maintain the evals.

## How to use

Use Codex with the Promptfoo plugin’s `$promptfoo-evals` skill to turn one AI app behavior into a repeatable eval suite. When the app does not already have a working Promptfoo target, `$promptfoo-provider-setup` helps connect the suite to the application path you want to test.

Codex can inspect the app, propose high-signal cases, add the Promptfoo config and test data, run the suite locally, and give you a command to keep using.

This use case works best when the behavior is concrete: support answer quality, retrieval grounding, classifier labels, tool calls, JSON shape, business rules, or prompt and model migration confidence.

A strong first pass should be reviewable code and test data: a `promptfooconfig.yaml` or equivalent config, a small `evals/` directory, test cases, any target adapter needed to call the app, and a local command such as `npm run evals`.

## Choose what to evaluate

Start with one user-visible promise. Avoid asking Codex to evaluate the entire AI system in one pass. A smaller suite is easier to trust, review, and keep running.

Good first targets include:

- **Correctness:** classification, extraction, summarization, routing, or transformation.
- **Grounding:** answers that should stay tied to retrieved documents or cited sources.
- **Tool use:** choosing the right tool, passing valid arguments, and handling tool errors.
- **Format or business rules:** JSON schemas, field names, business-rule limits, or UI-facing copy contracts.
- **Prompt or model migration:** making sure a new prompt, model, system message, or retrieval setting does not break important cases.

Start from product requirements, bug reports, support escalations, or sanitized examples your team is comfortable committing to the repo.

## Ask for an eval plan

Codex should inspect before it edits. Ask for a plan that names the target path, fixtures, assertions, adapter, and commands. This gives you a chance to catch the wrong target or weak test cases before files are added.

Review the plan before implementation. It should name the app path or endpoint Promptfoo will call, the first seed cases, the assertions, the files Codex will create, the local command, and any required secrets or services. If the plan tests the raw model instead of the application path users hit, ask Codex whether that is intentional.

## Implement, run, and iterate

Once the plan is correct, ask Codex to implement it. The first implementation should be boring: config, cases, fixtures, a target adapter if needed, a command, and proof that the command ran.

A small app-backed suite might look like this:

```
evals/
  promptfooconfig.yaml
  tests/
    cases.yaml
  providers/
    provider.js  # only if the built-in provider cannot call the app directly
```

Run the suite before changing behavior. The baseline tells you whether the app already fails the cases, whether the assertions need tuning, or whether the target adapter is wrong. Tune assertions when they are too brittle or vague, but keep real product failures visible.

After the first run, use the suite to compare app changes before they ship. Add new cases whenever a bug, launch requirement, or product review shows behavior you want to keep stable. Once the local command is stable, ask Codex to add it to CI or your release checklist.

## Related use cases

[![](/codex/use-cases/api-integration-migrations.webp)

### Upgrade your API integration

Use Codex to update your existing OpenAI API integration to the latest recommended models...

Evaluation  Engineering](/codex/use-cases/api-integration-migrations)[![](/codex/use-cases/dependency-incident-audits.webp)

### Audit dependency incidents

Use Codex to turn a public package or supply chain advisory into a read-only audit, then...

Engineering  Quality](/codex/use-cases/dependency-incident-audits)[![](/codex/use-cases/agent-friendly-clis.webp)

### Create a CLI Codex can use

Ask Codex to create a composable CLI it can run from any folder, combine with repo scripts...

Engineering  Code](/codex/use-cases/agent-friendly-clis)

