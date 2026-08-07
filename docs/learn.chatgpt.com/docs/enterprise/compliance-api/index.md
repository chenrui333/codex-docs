---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/compliance-api'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Compliance API and audit events

Source: https://learn.chatgpt.com/docs/enterprise/compliance-api

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use the Compliance API for security, legal, governance, and investigation
workflows that require auditable records. Use analytics, not compliance records,
to measure adoption and trends.

The authenticated [Admin API reference](https://chatgpt.com/admin/api-reference)
is the source of truth for current access requirements, event coverage, routes,
schemas, filters, retention, and request behavior.

For an overview of the available compliance surfaces and common integration
patterns, see the [Compliance Platform guide](https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers).

## When to use the Compliance API

The Compliance API is appropriate when you need to:

- Export supported records into an audit or investigation system.
- Apply organizational retention and legal-hold processes.
- Correlate Codex activity with other security or identity data.
- Support approved security, legal, or governance investigations.

It's not a productivity dashboard. Don't use it to infer code quality or
individual performance. Use [Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics)
or the [Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api) for adoption reporting.

## Get started

1. Open the [Admin API reference](https://chatgpt.com/admin/api-reference) and
   confirm that your administrator role can access the compliance resources
   you need.
2. Use the append-only compliance log stream for ongoing collection. Check the
   authenticated reference for the currently supported resources and retrieval
   patterns.
3. Test ingestion into a non-production security information and event
   management (SIEM) system or data lake. The
   [Compliance Platform guide](https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers)
   links to the current API documentation and quickstart notebook.
4. Schedule continuous collection and apply your organization's access,
   retention, and legal-hold controls to exported records. Don't assume the
   source retention window replaces your organization's retention policy.

For example, a security team can stream immutable compliance events into its
SIEM for investigations, or route those events into an approved electronic
discovery workflow. Use the authenticated reference for the current routes and
schemas rather than copying an endpoint contract from this guide.

## Confirm the administration boundaries

Compliance coverage follows the ChatGPT workspace and the products represented
in the current authenticated reference. Platform API organization data follows
its own API data and administration controls.

The authenticated reference owns the current routes, event coverage, schemas,
filters, retention behavior, permission requirements, and request mechanics.
This page doesn't duplicate that contract.

## Related docs

- [Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics)
- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
- [Governance](https://learn.chatgpt.com/docs/enterprise/governance)
- [Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api)
