---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/analyze-data-export'
source_last_modified: '2026-06-05T16:50:09Z'
source_etag: 'W/"a3911d9427924167c59a8e139af10db6"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0"]
---

# Query tabular data | Codex use cases

Source: https://developers.openai.com/codex/use-cases/analyze-data-export

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Query tabular data

Ask a question about a CSV, spreadsheet, export, or data folder.

Difficulty **Easy**

Time horizon **30m**

Use Codex with a CSV, spreadsheet, dashboard export, Google Sheet, or local data file to answer a question, create a browser visualization, and save the result.

## Best for

- Questions that can be answered through a quick calculation, chart, table, or short summary.
- Roles that need to analyze data and create visualizations.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/analyze-data-export/?export=pdf)

Use Codex with a CSV, spreadsheet, dashboard export, Google Sheet, or local data file to answer a question, create a browser visualization, and save the result.

Easy

30m

Related links

[File inputs](/api/docs/guides/file-inputs)  [Agent skills](/codex/skills)

## Best for

- Questions that can be answered through a quick calculation, chart, table, or short summary.
- Roles that need to analyze data and create visualizations.

## Skills & Plugins

- Spreadsheet

  Inspect tabular data, run calculations, and create charts or tables.
- [Google Sheets](/codex/plugins)

  Analyze approved Google Sheets when the data lives in a shared spreadsheet.

| Skill | Why use it |
| --- | --- |
| Spreadsheet | Inspect tabular data, run calculations, and create charts or tables. |
| [Google Sheets](/codex/plugins) | Analyze approved Google Sheets when the data lives in a shared spreadsheet. |

## Starter prompt

Analyze @sales-export.csv
Question: Which customer segment changed the most last quarter?
Please:
- inspect the columns before analyzing
- answer the question from the data
- create a simple browser visualization as an HTML file
- start a local preview so I can open it in the Codex browser

Open in the Codex app

Analyze @sales-export.csv
Question: Which customer segment changed the most last quarter?
Please:
- inspect the columns before analyzing
- answer the question from the data
- create a simple browser visualization as an HTML file
- start a local preview so I can open it in the Codex browser

## Analyze the data

Use Codex when you have a CSV, spreadsheet, dashboard export, Google Sheet, or local data file and want to answer a question from it. Start with the file and the question. Codex can inspect the columns, run the analysis, and create a browser visualization you can open in the Codex app.

[
Your browser does not support the video tag.
](https://cdn.openai.com/codex/docs/developers-website/use-cases/data-analysis-fraud-spike.mp4)

1. Attach the file or mention the connected data source.
2. Ask the question you want answered.
3. Have Codex inspect the columns, run the calculation, and create an HTML visualization.
4. Open the local preview in the Codex browser, then continue in the same thread to adjust the chart or slice the data another way.

Use `@` to attach the CSV or mention the Google Sheet. If the data came from a dashboard, export the rows first so Codex can inspect the raw columns.

## Follow-up analysis

After Codex gives you the first answer, ask for the next comparison you would normally check.

Use the same data and compare the result by [region, cohort, product, week, model version, or account type].
Update the browser visualization for that comparison.

You can keep going in the same thread: clean a column, exclude a test segment, compare two time windows, make the chart easier to read, or turn the result into a short note for a meeting.

## Related use cases

[![](/codex/use-cases/feedback-synthesis.webp)

### Turn feedback into actions

Connect Codex to multiple data sources such as Slack, GitHub, Linear, or Google Drive to...

Data  Integrations](/codex/use-cases/feedback-synthesis)[![](/codex/use-cases/clean-messy-data.webp)

### Clean and prepare messy data

Drag in or mention a messy CSV or spreadsheet, describe the problems you see, and ask Codex...

Data  Knowledge Work](/codex/use-cases/clean-messy-data)[![](/codex/use-cases/cash-flow-forecast.webp)

### Forecast cash flow

Give Codex cash-flow inputs and model constraints, then ask it to create an editable...

Data  Knowledge Work](/codex/use-cases/cash-flow-forecast)

