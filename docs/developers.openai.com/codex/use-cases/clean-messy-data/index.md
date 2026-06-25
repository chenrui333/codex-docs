---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/clean-messy-data'
source_last_modified: '2026-06-05T16:53:10Z'
source_etag: 'W/"1eaf66c1e04df1edaf7420fd2dfbf2c4"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1"]
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

- Spreadsheet

  Inspect tabular files, clean columns, and produce reviewable outputs.

| Skill | Why use it |
| --- | --- |
| Spreadsheet | Inspect tabular files, clean columns, and produce reviewable outputs. |

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

Open in the Codex app

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

[![](/codex/use-cases/analyze-data-export.webp)

### Query tabular data

Use Codex with a CSV, spreadsheet, dashboard export, Google Sheet, or local data file to...

Data  Knowledge Work](/codex/use-cases/analyze-data-export)[![](/codex/use-cases/feedback-synthesis.webp)

### Turn feedback into actions

Connect Codex to multiple data sources such as Slack, GitHub, Linear, or Google Drive to...

Data  Integrations](/codex/use-cases/feedback-synthesis)[![](/codex/use-cases/cash-flow-forecast.webp)

### Forecast cash flow

Give Codex cash-flow inputs and model constraints, then ask it to create an editable...

Data  Knowledge Work](/codex/use-cases/cash-flow-forecast)

