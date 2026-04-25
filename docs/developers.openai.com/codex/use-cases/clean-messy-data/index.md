---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/clean-messy-data'
source_last_modified: '2026-04-25T06:50:35Z'
source_etag: 'W/"de2d63864b5be71d55cae3470b1f135e"'
codex_cli_versions: ["0.125.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0"]
---

# Clean and prepare messy data | Codex use cases

Source: https://developers.openai.com/codex/use-cases/clean-messy-data

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Clean and prepare messy data

Process tabular data without affecting the original.

Difficulty **Easy**

Time horizon **5m**

Drag in or mention a messy CSV or spreadsheet, describe the problems you see, and ask Codex to write a cleaned copy while keeping the original file unchanged.

## Best for

- CSV or spreadsheet exports with mixed dates, currencies, duplicates, summary rows, or missing values.
- Teams who work with data from multiple sources.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/clean-messy-data/?export=pdf)

Drag in or mention a messy CSV or spreadsheet, describe the problems you see, and ask Codex to write a cleaned copy while keeping the original file unchanged.

Easy

5m

Related links

[Analyze data with Codex](/codex/use-cases/analyze-data-export)  [File inputs](/api/docs/guides/file-inputs)  [Agent skills](/codex/skills)

## Best for

- CSV or spreadsheet exports with mixed dates, currencies, duplicates, summary rows, or missing values.
- Teams who work with data from multiple sources.

## Skills & Plugins

- [Spreadsheet](https://github.com/openai/skills/tree/main/skills/.curated/spreadsheet)

  Inspect tabular files, clean columns, and produce reviewable outputs.

| Skill | Why use it |
| --- | --- |
| [Spreadsheet](https://github.com/openai/skills/tree/main/skills/.curated/spreadsheet) | Inspect tabular files, clean columns, and produce reviewable outputs. |

## Starter prompt

Clean @marketplace-risk-rollout-export.csv.
What's wrong:
- dates are mixed between MM/DD/YYYY and YYYY-MM-DD
- currency values include $, commas, and blank cells
- a few duplicate customer rows came from repeated exports
- region and category names use several aliases
- there are pasted summary rows mixed into the data
What I want:
- write a cleaned CSV
- keep the original file unchanged
- use one date format
- keep blank currency cells blank
- preserve source row IDs when possible
- add a short data-quality note with rows you changed, removed, or could not clean confidently

[Open in the Codex app](codex://new?prompt=Clean+%40marketplace-risk-rollout-export.csv.%0A%0AWhat%27s+wrong%3A%0A-+dates+are+mixed+between+MM%2FDD%2FYYYY+and+YYYY-MM-DD%0A-+currency+values+include+%24%2C+commas%2C+and+blank+cells%0A-+a+few+duplicate+customer+rows+came+from+repeated+exports%0A-+region+and+category+names+use+several+aliases%0A-+there+are+pasted+summary+rows+mixed+into+the+data%0A%0AWhat+I+want%3A%0A-+write+a+cleaned+CSV%0A-+keep+the+original+file+unchanged%0A-+use+one+date+format%0A-+keep+blank+currency+cells+blank%0A-+preserve+source+row+IDs+when+possible%0A-+add+a+short+data-quality+note+with+rows+you+changed%2C+removed%2C+or+could+not+clean+confidently "Open in the Codex app")

Clean @marketplace-risk-rollout-export.csv.
What's wrong:
- dates are mixed between MM/DD/YYYY and YYYY-MM-DD
- currency values include $, commas, and blank cells
- a few duplicate customer rows came from repeated exports
- region and category names use several aliases
- there are pasted summary rows mixed into the data
What I want:
- write a cleaned CSV
- keep the original file unchanged
- use one date format
- keep blank currency cells blank
- preserve source row IDs when possible
- add a short data-quality note with rows you changed, removed, or could not clean confidently

## Introduction

Codex is great at cleaning systematically tabular data.
When a CSV or spreadsheet has mixed dates, duplicate rows, currency strings, blank cells, aliases, or pasted summary rows, ask Codex to clean a copy and leave the original file unchanged.

[
Your browser does not support the video tag.
](https://cdn.openai.com/codex/docs/developers-website/use-cases/data-analysis-cleaning-csv.mp4)

## How to use

1. Drag the file into Codex or mention it in your prompt, such as `@customer-export.csv`.
2. Describe the problems you already see.
3. Tell Codex what the cleaned version should be: CSV, spreadsheet tab, or upload-ready file.
4. Review the cleaned copy before using it.

Use the starter prompt on this page for the first cleaning pass. Replace the file name and bullets with your own. The useful details are the problems you already see and the file you need next: a cleaned CSV, a clean spreadsheet tab, or an upload-ready file. After Codex writes the clean copy, open the cleaned file and the data-quality note from the thread before using the data downstream.

## Related use cases

[![](/images/codex/codex-wallpaper-1.webp)

### Query tabular data

Use Codex with a CSV, spreadsheet, dashboard export, Google Sheet, or local data file to...

Data  Knowledge Work](/codex/use-cases/analyze-data-export)[![](/images/codex/codex-wallpaper-3.webp)

### Turn feedback into actions

Connect Codex to multiple data sources such as Slack, GitHub, Linear, or Google Drive to...

Data  Integrations](/codex/use-cases/feedback-synthesis)[![](/images/codex/codex-wallpaper-2.webp)

### Coordinate new-hire onboarding

Use Codex to gather approved new-hire context, stage tracker updates, draft team-by-team...

Integrations  Data](/codex/use-cases/new-hire-onboarding)

