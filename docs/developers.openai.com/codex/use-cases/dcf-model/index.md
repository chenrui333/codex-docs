---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/dcf-model'
source_last_modified: '2026-06-05T16:58:22Z'
source_etag: 'W/"ac98cfa0b5a20c1189426af3c37dd786"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0"]
---

# Model a DCF valuation | Codex use cases

Source: https://developers.openai.com/codex/use-cases/dcf-model

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Model a DCF valuation

Turn financial inputs into an editable valuation workbook.

Difficulty **Intermediate**

Time horizon **30m**

Attach historical financials, valuation assumptions, and modeling notes, then ask Codex for an editable DCF workbook you can inspect and revise in Codex.

## Best for

- Analysts turning historical financials and assumptions into a DCF workbook.
- Finance teams that want to inspect and iterate on the workbook in Codex.
- Teams preparing a valuation model from source files.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/dcf-model/?export=pdf)

Attach historical financials, valuation assumptions, and modeling notes, then ask Codex for an editable DCF workbook you can inspect and revise in Codex.

Intermediate

30m

Related links

[Agent skills](/codex/skills)  [File inputs](/api/docs/guides/file-inputs)

## Best for

- Analysts turning historical financials and assumptions into a DCF workbook.
- Finance teams that want to inspect and iterate on the workbook in Codex.
- Teams preparing a valuation model from source files.

## Skills & Plugins

- Spreadsheets

  Create editable spreadsheet workbooks from attached inputs, formulas, and assumptions.

| Skill | Why use it |
| --- | --- |
| Spreadsheets | Create editable spreadsheet workbooks from attached inputs, formulas, and assumptions. |

## Starter prompt

Use $spreadsheets to build a DCF workbook for the company in the attached source files.
Include explicit operating drivers for revenue growth, margins, capex, and working capital. Calculate unlevered free cash flow, WACC, terminal value, and enterprise value. If capital structure and diluted share count are provided, bridge to implied equity value and implied equity value per share.
Use any assumptions included in the source files. If an assumption is missing, add a clearly labeled placeholder in the assumptions tab instead of hiding it in a formula. If full balance sheet or cash-flow statement inputs are missing, create the operating forecast needed for unlevered free cash flow and flag the missing statement inputs.
Generate the result as an editable .xlsx workbook.

Open in the Codex app

Use $spreadsheets to build a DCF workbook for the company in the attached source files.
Include explicit operating drivers for revenue growth, margins, capex, and working capital. Calculate unlevered free cash flow, WACC, terminal value, and enterprise value. If capital structure and diluted share count are provided, bridge to implied equity value and implied equity value per share.
Use any assumptions included in the source files. If an assumption is missing, add a clearly labeled placeholder in the assumptions tab instead of hiding it in a formula. If full balance sheet or cash-flow statement inputs are missing, create the operating forecast needed for unlevered free cash flow and flag the missing statement inputs.
Generate the result as an editable .xlsx workbook.

## Introduction

Codex can help you create a fully functional DCF workbook that you can inspect and revise.

It can use multiple files as context, including the historical financials, valuation assumptions, and any modeling notes.
You can provide these files directly, or use file references when the inputs live in Google Drive or another connected source. If so, provide the exact file references, as it will be more effective than asking Codex to search through all of your files.

[
Your browser does not support the video tag.
](https://openaiassets.blob.core.windows.net/$web/codex/docs/developers-website/use-cases/create-a-dcf.mp4)

## Create the workbook

1. Attach the historical financials, valuation assumptions, and any modeling notes, or provide exact file references along with the source.
2. Run the starter prompt and ask for an editable `.xlsx` workbook.
3. Open the generated workbook in Codex. Expand it into the full-screen view to inspect the model tabs, formulas, assumptions, and valuation summary.
4. Continue in the same thread to check formula links, change assumptions, add scenarios, or tighten the model.

When the workbook appears in the thread, open it in Codex and expand it full-screen. Review the source inputs, forecast drivers, valuation outputs, and sensitivity tables, then ask Codex to revise the same workbook from there.

## Check the valuation

Before using the workbook, ask Codex to review the model like a finance teammate would: source tie-outs, formulas, hardcoded assumptions, and valuation outputs.

Review the DCF workbook before I use it.
Check:
- historicals tied to the source files
- forecast drivers and visible assumptions
- formulas versus hardcoded values
- unlevered free cash flow calculation
- WACC, terminal value, enterprise value, and any equity-value bridge
- sensitivity table formulas
- missing capital structure, diluted share count, or assumptions that need human review
Fix safe formatting or formula issues, then list anything I should review manually.

## Revise one assumption

After reviewing the workbook in Codex, ask for targeted revisions in the same thread. Change one driver at a time so the impact is easy to inspect.

Update the DCF model so [revenue growth, EBITDA margin, WACC, terminal growth, or capex] uses [new assumption].
Keep the old assumption visible in a note, update dependent formulas, and tell me which tabs changed.

## Related use cases

[![](/codex/use-cases/cash-flow-forecast.webp)

### Forecast cash flow

Give Codex cash-flow inputs and model constraints, then ask it to create an editable...

Data  Knowledge Work](/codex/use-cases/cash-flow-forecast)[![](/codex/use-cases/budget-vs-actuals-review.webp)

### Review budget vs. actuals

Give Codex a budget, actuals export, and close notes, then ask it to map actuals to plan...

Data  Knowledge Work](/codex/use-cases/budget-vs-actuals-review)[![](/codex/use-cases/clean-messy-data.webp)

### Clean and prepare messy data

Drag in or mention a messy CSV or spreadsheet, describe the problems you see, and ask Codex...

Data  Knowledge Work](/codex/use-cases/clean-messy-data)

