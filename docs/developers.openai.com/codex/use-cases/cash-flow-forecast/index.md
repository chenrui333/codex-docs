---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/cash-flow-forecast'
source_last_modified: '2026-05-20T00:58:21Z'
source_etag: 'W/"3d1b09e7eb11549174649bde3769ddb3"'
codex_cli_versions: ["0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0"]
codex_cli_versions_raw: ["codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0"]
---

# Forecast cash flow | Codex use cases

Source: https://developers.openai.com/codex/use-cases/cash-flow-forecast

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Forecast cash flow

Find the liquidity low point in an editable forecast workbook.

Difficulty **Intermediate**

Time horizon **30m**

Give Codex cash-flow inputs and model constraints, then ask it to create an editable workbook that preserves the source cadence, flags safety-balance breaches, and shows which assumptions drive cash pressure.

## Best for

- Finance and operations teams building a 13-week or monthly cash forecast.
- Forecasts that need receipts, payroll, vendor payments, and working-capital assumptions in one workbook.
- Teams reviewing runway, safety-balance breaches, and scenario drivers before a planning meeting.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/cash-flow-forecast/?export=pdf)

Give Codex cash-flow inputs and model constraints, then ask it to create an editable workbook that preserves the source cadence, flags safety-balance breaches, and shows which assumptions drive cash pressure.

Intermediate

30m

Related links

[Agent skills](/codex/skills)

## Best for

- Finance and operations teams building a 13-week or monthly cash forecast.
- Forecasts that need receipts, payroll, vendor payments, and working-capital assumptions in one workbook.
- Teams reviewing runway, safety-balance breaches, and scenario drivers before a planning meeting.

## Skills & Plugins

- Spreadsheets

  Build editable forecast workbooks, wire formulas to assumptions, and add checks for scenarios and input gaps.

| Skill | Why use it |
| --- | --- |
| Spreadsheets | Build editable forecast workbooks, wire formulas to assumptions, and add checks for scenarios and input gaps. |

## Starter prompt

Use $spreadsheets to build an editable cash-flow forecast workbook from the attached source files.
Use beginning cash, expected receipts, payroll, vendor payments, debt, tax, capex, working-capital items, and timing assumptions where available. Preserve the source cadence, whether weekly or monthly.
Include a summary view that flags the liquidity low point, the minimum ending cash balance, and any breach of the safety cash threshold. Use formulas so I can change assumptions later, and call out missing timing assumptions before using placeholders.

[Open in the Codex app](codex://new?prompt=Use+%24spreadsheets+to+build+an+editable+cash-flow+forecast+workbook+from+the+attached+source+files.%0A%0AUse+beginning+cash%2C+expected+receipts%2C+payroll%2C+vendor+payments%2C+debt%2C+tax%2C+capex%2C+working-capital+items%2C+and+timing+assumptions+where+available.+Preserve+the+source+cadence%2C+whether+weekly+or+monthly.%0A%0AInclude+a+summary+view+that+flags+the+liquidity+low+point%2C+the+minimum+ending+cash+balance%2C+and+any+breach+of+the+safety+cash+threshold.+Use+formulas+so+I+can+change+assumptions+later%2C+and+call+out+missing+timing+assumptions+before+using+placeholders. "Open in the Codex app")

Use $spreadsheets to build an editable cash-flow forecast workbook from the attached source files.
Use beginning cash, expected receipts, payroll, vendor payments, debt, tax, capex, working-capital items, and timing assumptions where available. Preserve the source cadence, whether weekly or monthly.
Include a summary view that flags the liquidity low point, the minimum ending cash balance, and any breach of the safety cash threshold. Use formulas so I can change assumptions later, and call out missing timing assumptions before using placeholders.

## Introduction

When you are building a cash-flow forecast, you want to make sure it is accurate and reflects the reality of your business. You can use Codex to help you create a forecast workbook that you can inspect and revise in Codex. Attach the cash-flow inputs, operating assumptions, and model constraints. You can also use file references when the inputs live in Google Drive or another connected source.

[
Your browser does not support the video tag.
](https://openaiassets.blob.core.windows.net/$web/codex/docs/developers-website/use-cases/Cash-flow%20forecast.mp4)

## Make the forecast

1. Attach the cash-flow inputs, operating assumptions, and model constraints.
2. Run the starter prompt and ask for an editable `.xlsx` workbook.
3. Open the workbook in Codex. Expand it into the full-screen view to inspect assumptions, formulas, scenarios, and the summary tab.
4. Continue in the same thread to change collections, payroll, vendor payment, growth, or safety-balance assumptions.

When the workbook appears in the thread, open it in Codex and expand it full-screen. Review the timing assumptions, formulas, scenarios, and summary tab, then ask Codex to revise the same workbook from there.

## Review cash pressure

Before using the forecast, ask Codex to identify the low point, tie the workbook back to the source inputs, and list assumptions that need review.

Review the cash-flow forecast.
Tell me:
- the first week or month cash drops below the safety balance
- the liquidity low point
- the main drivers of cash pressure
- formulas or tabs that do not tie to the source inputs
- assumptions that need human review
- which scenario I should review before using this with the team
Fix safe formatting or formula issues, then list anything I should review manually.

## Run a scenario

After reviewing the workbook in Codex, use follow-up prompts to change one scenario driver at a time.

Add a scenario where [collections slow by X days, payroll increases by X%, vendor payments move earlier, or bookings increase by X% with collection timing of N days].
Keep the base case visible, update dependent formulas, and tell me how ending cash and the liquidity low point change.

## Related use cases

[![](/codex/use-cases/dcf-model.webp)

### Model a DCF valuation

Attach historical financials, valuation assumptions, and modeling notes, then ask Codex for...

Data  Knowledge Work](/codex/use-cases/dcf-model)[![](/codex/use-cases/budget-vs-actuals-review.webp)

### Review budget vs. actuals

Give Codex a budget, actuals export, and close notes, then ask it to map actuals to plan...

Data  Knowledge Work](/codex/use-cases/budget-vs-actuals-review)[![](/codex/use-cases/clean-messy-data.webp)

### Clean and prepare messy data

Drag in or mention a messy CSV or spreadsheet, describe the problems you see, and ask Codex...

Data  Knowledge Work](/codex/use-cases/clean-messy-data)

