---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/chatgpt-work-usage-and-cost'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.151.0"]
---

# ChatGPT Work: usage and cost

Source: https://learn.chatgpt.com/docs/enterprise/chatgpt-work-usage-and-cost

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

ChatGPT Work helps employees complete multi-step tasks, such as researching a
topic, analyzing information, or creating a finished document or presentation.
Completing these tasks can require additional reasoning, tools, and processing,
which may consume credits. Whether that usage affects your invoice depends on
your remaining credits, contracted rates, and workspace overage settings.

Use this guide to understand how Work affects usage, plan employee adoption,
and apply the spending controls available to your organization.

## Usage and cost at a glance

- For eligible credit-based agreements, Work activity draws from a shared pool
  of workspace credits.
- Consuming committed credits differs from incurring new invoiced
  charges.
- Employees can use both Chat and Work; evaluate their combined eligible usage
  when estimating adoption.
- Role-based estimates support planning but aren't fixed per-user prices or
  guaranteed billing amounts.
- User usage limits and workspace overage limits are separate controls. Alerts
  provide notice but don't stop spending.
- Assess a rollout using your organization's observed usage and measurable
  workflow outcomes.

## Why Work uses credits

For organizations with credit-based agreements, eligible Work activity consumes
credits from the shared workspace allocation. Other eligible ChatGPT features
can draw from the same allocation, so Work doesn't necessarily have a separate
balance.

Consumption varies with:

- The model, execution environment, and applicable reasoning or speed settings.
- The task's complexity and any eligible tools or features used—for example,
  preparing a quarterly business review using CRM records, documents, or messages
  from approved apps and systems the employee is authorized to access.
- How frequently employees run tasks.

Employees don't need to stop using Chat when they start using Work. To
understand the change in total consumption, compare the same employees'
earlier Chat usage with their combined Chat and Work usage over a comparable
period.

Your agreement and applicable rate card determine the credits each eligible
activity consumes. Existing subscription or seat fees are separate from an
estimate of credits consumed.

## When usage affects your bill

Whether eligible Work usage results in an additional charge depends on your
agreement, remaining credits, and applicable billing settings. Using committed
credits reduces your available balance but doesn't, by itself, create a new
invoice charge:

- **Committed credits remain:** Eligible activity draws down the available
  credit allocation. Using those credits doesn't, by itself, create a new charge
  beyond your existing agreement.
- **No credits remain and your account permits overage:** Eligible usage can
  continue within the configured workspace overage limit and may incur charges
  at your contracted overage rate.
- **No credits remain and your account doesn't permit overage:** Eligible
  features can pause until credits become available or the applicable limit
  changes.

Overage behavior depends on both account eligibility and the configured
workspace limit. If your agreement doesn't permit overages, eligible usage
stops when no available credits remain. If your account permits overages, an
unset limit can allow eligible usage beyond the credit balance. Where supported,
an overage limit of zero prevents the workspace from continuing into overage,
while **No limit** isn't a zero-spend cap.

Usage reports and dollar estimates are planning or monitoring tools, not issued
invoices. Some displayed estimates use the contracted overage rate, which can
differ from the rate for committed credits. Confirm actual charges against the
invoice, billing period, and terms in your organization's agreement.

## Estimate usage for a role or team

A role-based estimate can help plan adoption for employees with similar
responsibilities, such as Finance, Marketing, or Sales. Start with the
employees and workflows your organization expects to support.

To develop an estimate:

1. Identify the proposed user group and a comparable period of existing Chat
   activity.
2. Estimate combined Chat and Work consumption using observed pilot usage or an
   approved, relevant role-based benchmark.
3. Review the remaining committed credit balance. Apply the appropriate
   contracted rates for committed credits and, separately, any overage.
4. Determine whether projected usage stays within available credits or could
   reach your contracted overage terms.
5. Update the estimate using actual adoption, task mix, and observed
   consumption.

An approved benchmark may reflect observed enterprise-customer usage and the
actual mix of models used. Its usefulness depends on the comparison period,
role classification, workflow, and account assumptions. A broad role-based
estimate doesn't establish an industry-specific or task-specific benchmark.

An **annualized consumed-credit estimate** projects observed usage value across
a year. It isn't a separate Work license price, a standard per-user charge,
OpenAI's infrastructure cost, or a prediction that your invoice will increase
by the same amount. Actual incremental charges depend on remaining committed
credits, contracted pricing, permitted overages, and the billing period.

### Illustrative Marketing planning example

An observed analysis of first-time enterprise Work adopters in Marketing showed
the following changes in annualized consumed-credit value:

- **Median:** Approximately **$53 per employee per year**.
- **90th percentile:** Approximately **$1,154 per employee per year**.
- **Average:** Approximately **$309 per employee per year**.

The median represents the midpoint of observed individual usage. The average is
higher because a smaller number of employees consume more credits. The 90th
percentile describes an observed higher-usage threshold, not a spending cap or
maximum.

For **100 employees** with a similar mix of usage, applying the **$309
per-employee average** represents approximately **$30,900 annually**, or
**$2,575 per month as a planning equivalent**.

These directional estimates reflect observed enterprise-customer usage and its
actual model mix, annualized from one week of adoption-period usage. They
aren't guaranteed savings, fixed per-user prices, automatic bills, or
guaranteed increases to your invoice. Actual charges depend on remaining
committed credits, contracted rates, and permitted overages.

Your account team can help interpret approved estimates against your
organization's agreement.

## Administrator controls and reporting

Workspace owners and administrators can use supported settings to manage access
and eligible credit-based usage:

- **Work access:** Choose which people or groups can access Work through the
  permissions available to your workspace.
- **Model and speed settings:** Where available, configure the starting Work &
  Codex model, reasoning level, speed, and Fast Mode availability in Workspace
  settings > Models. Fast Mode can consume more credits for supported models.
- **User usage limits:** Set supported monthly workspace defaults, group
  limits, or individual overrides to manage each user's eligible usage.
- **Workspace overage limit:** Control how much eligible usage can continue
  after the shared credit allocation runs out.
- **Usage alerts:** In Billing, configure available usage thresholds and
  recipients where supported. Alerts notify; they don't stop spending.
- **Credit balance and reporting:** In Billing, review remaining credits and
  download usage reports available to your role. Where your agreement includes
  committed credits, compare observed usage with your contracted allocation and
  billing period to assess pacing.
- **Invoices:** Review issued invoices and the corresponding billing period
  when your workspace role includes invoice access.

An individual user override takes precedence over group and workspace defaults.
When a person belongs to more than one group, the highest applicable group limit
applies. A group without a configured limit doesn't impose a zero-credit cap.
Check the effective limit for each pilot participant.

Usage limits don't add credits or determine who can access Work. A model
default or employee guidance can influence consumption, but neither replaces an
enforced usage limit or workspace overage setting.

Control availability, reporting detail, invoice access, and billing behavior
depend on your plan, workspace configuration, and agreement. Reports might not
reflect activity immediately; compare the report timestamp and billing period
before reconciling usage with an invoice. For cross-product applicability and
current setup procedures, see
[ChatGPT usage limits and spend controls](https://learn.chatgpt.com/docs/enterprise/usage-limits).

## Measure usage alongside outcomes

Choose a recurring workflow with a clear existing baseline, such as account
research, meeting preparation, or finance reporting. Use the access, tools,
and model capabilities appropriate to the work rather than assuming every task
requires the most advanced option.

During a pilot, compare the same workflow before and after you introduce Work.
Depending on the task, your organization might measure:

- Time required to complete the work.
- Output quality, completeness, or consistency.
- Rework, manual coordination, or error rates.
- Whether the team completed the intended deliverable.

Review these customer-measured outcomes alongside observed credit consumption
and any actual billing impact. Usage alone doesn't establish savings, and
projected time improvements aren't guaranteed financial returns.

## Start with a controlled rollout

Before expanding access:

1. Confirm your agreement, remaining credits, applicable rates, and overage
   settings.
2. Select a limited group and a workflow your organization can evaluate.
3. Configure supported access permissions, user limits, alerts, and the
   workspace overage limit.
4. Compare combined Chat and Work consumption against the group's existing
   baseline.
5. Review observed outcomes and any actual billing impact before expanding the
   rollout.

For broader access, data, governance, and rollout guidance, see the
[ChatGPT Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq). For
contract-specific pricing, credit availability, and invoicing questions,
contact your account team.
