---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/deploy-app-or-website'
source_last_modified: '2026-06-03T19:26:41Z'
source_etag: 'W/"4395fe6d2857c9ce2d157d59933fc273"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0"]
---

# Deploy an app or website | Codex use cases

Source: https://developers.openai.com/codex/use-cases/deploy-app-or-website

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Deploy an app or website

Build or update a web app, deploy a preview, and get a live URL.

Difficulty **Intermediate**

Time horizon **30m**

Use Codex with Build Web Apps and Vercel to turn a repo, screenshot, design, or rough app idea into a working preview deployment you can share.

## Best for

- Turning a screenshot, map, design brief, or rough app idea into a working web preview
- Deploying a branch or local app without manually wiring Vercel commands
- Sharing a live URL after Codex runs the build and checks the deployment

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/deploy-app-or-website/?export=pdf)

Use Codex with Build Web Apps and Vercel to turn a repo, screenshot, design, or rough app idea into a working preview deployment you can share.

Intermediate

30m

Related links

[Build Web Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)  [Vercel plugin](https://github.com/openai/plugins/tree/main/plugins/vercel)  [Vercel deployments](https://vercel.com/docs/deployments/overview)

## Best for

- Turning a screenshot, map, design brief, or rough app idea into a working web preview
- Deploying a branch or local app without manually wiring Vercel commands
- Sharing a live URL after Codex runs the build and checks the deployment

## Skills & Plugins

- [Build Web Apps](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)

  Build, review, and prepare web apps with React, UI, deployment, payments, and database guidance.
- [Vercel](https://github.com/openai/plugins/tree/main/plugins/vercel)

  Deploy previews, inspect deployments, read build logs, and manage Vercel project settings.

| Skill | Why use it |
| --- | --- |
| [Build Web Apps](https://github.com/openai/plugins/tree/main/plugins/build-web-apps) | Build, review, and prepare web apps with React, UI, deployment, payments, and database guidance. |
| [Vercel](https://github.com/openai/plugins/tree/main/plugins/vercel) | Deploy previews, inspect deployments, read build logs, and manage Vercel project settings. |

## Starter prompt

Use @build-web-apps to turn [repo, screenshot, design, or rough app idea] into a working website.
Then use @vercel to deploy a preview and hand me the live URL.
Context:
- [what the site should do]
- [source data, API, docs, or assets to use]
- [style or product constraints]
- [anything not to change]
Before you hand it back, run the local build and verify the deployment is ready.

[Open in the Codex app](codex://threads/new?prompt=Use+%40build-web-apps+to+turn+%5Brepo%2C+screenshot%2C+design%2C+or+rough+app+idea%5D+into+a+working+website.%0A%0AThen+use+%40vercel+to+deploy+a+preview+and+hand+me+the+live+URL.%0A%0AContext%3A%0A-+%5Bwhat+the+site+should+do%5D%0A-+%5Bsource+data%2C+API%2C+docs%2C+or+assets+to+use%5D%0A-+%5Bstyle+or+product+constraints%5D%0A-+%5Banything+not+to+change%5D%0A%0ABefore+you+hand+it+back%2C+run+the+local+build+and+verify+the+deployment+is+ready. "Open in the Codex app")

Use @build-web-apps to turn [repo, screenshot, design, or rough app idea] into a working website.
Then use @vercel to deploy a preview and hand me the live URL.
Context:
- [what the site should do]
- [source data, API, docs, or assets to use]
- [style or product constraints]
- [anything not to change]
Before you hand it back, run the local build and verify the deployment is ready.

## Start with the site and the deploy target

Codex can build or update a website or app, run the project checks, deploy it with Vercel, and return the URL.

The useful handoff is concrete: a repo, screenshot, map, design brief, product note, API doc, or data source. Codex should inspect the project before changing it, then use the Vercel plugin to deploy a preview by default.

Use `@build-web-apps` when Codex needs to build or polish the app. Use `@vercel` when it should deploy, inspect the deployment, or read Vercel build logs.

Use @build-web-apps to turn [repo, screenshot, design, or rough app idea] into a working website.
Then use @vercel to deploy a preview and hand me the live URL.
Context:
- [what the site should do]
- [source data, API, docs, or assets to use]
- [style or product constraints]
- [anything not to change]
Before you hand it back, run the local build and verify the deployment is ready.

## Check the result before you share it

Codex should tell you what it changed, which command it used to build the project, and whether the Vercel deployment is ready. If the deploy needs an environment variable, team choice, domain setting, or login step, Codex should call that out instead of pretending the site is finished.

Keep production changes explicit. A preview deployment is the default; ask for production only when you mean it.

## Iterate from the live URL

Once you have the preview, keep the same thread open. Ask Codex to open the URL, fix layout issues, update copy, wire missing data, or read Vercel logs if the deploy fails. The thread already has the repo, deployment, and build context.

Good follow-ups are specific:

- “The mobile layout is cramped. Fix it and redeploy the preview.”
- “Use the same project and add the latest data from [source].”
- “Read the failed build logs and fix the deploy.”

## Related use cases

[![](/codex/use-cases/build-and-deploy-internal-apps.webp)

### Build and deploy internal apps

Use Codex with Sites to build, test, and deploy internal apps, with built-in storage and...

Front-end  Integrations](/codex/use-cases/build-and-deploy-internal-apps)[![](/codex/use-cases/idea-to-proof-of-concept.webp)

### Get from idea to proof of concept

Use Codex with ImageGen to turn a rough idea into a visual direction, implement the smallest...

Front-end  Engineering](/codex/use-cases/idea-to-proof-of-concept)[![](/codex/use-cases/make-granular-ui-changes.webp)

### Make granular UI changes

Use Codex to make one small UI adjustment at a time in an existing app, verify it in the...

Front-end  Design](/codex/use-cases/make-granular-ui-changes)

