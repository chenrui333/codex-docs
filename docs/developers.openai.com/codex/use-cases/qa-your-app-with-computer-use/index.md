---
source_type: 'developers'
source_url: 'https://developers.openai.com/codex/use-cases/qa-your-app-with-computer-use'
source_last_modified: '2026-04-25T06:53:02Z'
source_etag: 'W/"ef1d068fb74acbec873ac0c69ebde4cb"'
codex_cli_versions: ["0.125.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0"]
---

# QA your app with Computer Use | Codex use cases

Source: https://developers.openai.com/codex/use-cases/qa-your-app-with-computer-use

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# QA your app with Computer Use

Click through real product flows and log what breaks.

Difficulty **Intermediate**

Time horizon **30m**

Use Computer Use to exercise key flows, catch issues, and finish with a bug report.

## Best for

- Teams validating real user flows before a release
- QA loops that should end with severity, repro steps, and a short triage summary

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/qa-your-app-with-computer-use/?export=pdf)

Use Computer Use to exercise key flows, catch issues, and finish with a bug report.

Intermediate

30m

Related links

[Computer Use](/codex/app/computer-use)  [Codex skills](/codex/skills)

## Best for

- Teams validating real user flows before a release
- QA loops that should end with severity, repro steps, and a short triage summary

## Starter prompt

@Computer Use Test my app in [environment].
Test these flows:
- [hero use case 1]
- [hero use case 2]
- [hero use case 3]
For every bug you find, include:
- repro steps
- expected result
- actual result
- severity
Keep going past non-blocking issues and end with a short triage summary.

[Open in the Codex app](codex://new?prompt=%40Computer+Use+Test+my+app+in+%5Benvironment%5D.%0A%0ATest+these+flows%3A%0A-+%5Bhero+use+case+1%5D%0A-+%5Bhero+use+case+2%5D%0A-+%5Bhero+use+case+3%5D%0A%0AFor+every+bug+you+find%2C+include%3A%0A-+repro+steps%0A-+expected+result%0A-+actual+result%0A-+severity%0A%0AKeep+going+past+non-blocking+issues+and+end+with+a+short+triage+summary. "Open in the Codex app")

@Computer Use Test my app in [environment].
Test these flows:
- [hero use case 1]
- [hero use case 2]
- [hero use case 3]
For every bug you find, include:
- repro steps
- expected result
- actual result
- severity
Keep going past non-blocking issues and end with a short triage summary.

## Introduction

Computer Use is a strong fit for QA passes because it can see the interface, click through flows, type into fields, and record what fails. That makes it useful for catching both functional bugs and UI issues across realistic user journeys.

The key is to tell Codex what environment to test, which flows matter most, and what kind of report you want back.

## How to use

1. Install the [Computer Use plugin](/codex/app/computer-use).
2. Tell Codex which app, build, or environment to test.
3. Name the flows or hero use cases you care about most.
4. Ask for a structured report so the output is easy to triage or hand off.

You can keep this broad:

- `@Computer Use Test my app. Find any major issues and give me a report.`

Or make it more explicit:

- `@Computer Use Test my app in staging. Cover signup, invite a teammate, and upgrade billing. Log every bug with repro steps, expected result, actual result, and severity.`

If you already maintain a test-plan file in the repo, attach it to the thread or point Codex at it so the QA pass follows your existing flows.

## Practical tips

### Be explicit about setup

If account state, test data, feature flags, or environment choice affect the flow, include that up front. Codex will produce much better results when it knows whether it is testing local, staging, or production-like behavior.

### Name the issue types you care about

Call out whether you want Codex to focus on broken functionality, layout issues, confusing copy, visual regressions, or all of the above.

### Decide whether to stop or continue

If one blocking issue should end the run, say so. Otherwise, tell Codex to continue through the rest of the flow and collect all non-blocking issues before it summarizes.

## Good follow-ups

After the QA pass, keep the same thread open and ask Codex to fix one of the bugs it found, turn the findings into Linear or GitHub-ready drafts, or narrow the next pass to one specific failing flow.

## Suggested prompt

**Run a Structured QA Pass**

@Computer Use Test my app in [environment].
Test these flows:
- [hero use case 1]
- [hero use case 2]
- [hero use case 3]
For every bug you find, include:
- repro steps
- expected result
- actual result
- severity
Keep going past non-blocking issues and end with a short triage summary.

## Related use cases

[![](/images/codex/codex-wallpaper-3.webp)

### Automate bug triage

Ask Codex to check recent alerts, issues, failed checks, logs, and chat reports, tune the...

Automation  Quality](/codex/use-cases/automation-bug-triage)[![](/images/codex/codex-wallpaper-2.webp)

### Debug in iOS simulator

Use Codex to discover the right Xcode scheme and simulator, launch the app, inspect the UI...

iOS  Code](/codex/use-cases/ios-simulator-bug-debugging)[![](/images/codex/codex-wallpaper-2.webp)

### Deploy an app or website

Use Codex with Build Web Apps and Vercel to turn a repo, screenshot, design, or rough app...

Front-end  Integrations](/codex/use-cases/deploy-app-or-website)

