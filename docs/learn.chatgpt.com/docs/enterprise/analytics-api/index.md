---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/analytics-api'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Analytics API

Source: https://learn.chatgpt.com/docs/enterprise/analytics-api

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

The Analytics APIs provide aggregated usage and activity metrics for a ChatGPT
workspace. The unified Daily Usage Analytics API reports daily ChatGPT, Codex,
and Work usage. Confirm that the endpoint is enabled for your workspace before
using it.

The [Admin API reference](https://chatgpt.com/public/admin/api-reference)
is the source of truth for current access requirements, routes, request and
response schemas, metrics, time semantics, and pagination.

## When to use the Analytics API

The Analytics API is appropriate when you need to:

- Automate recurring workspace usage reporting.
- Join aggregated usage metrics with internal organizational data.
- Build a controlled reporting layer for approved audiences.
- Avoid coupling an integration to an interactive dashboard.

It's not a raw audit-log interface. Use the
[Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api) when the workflow requires
auditable activity records.

## Confirm the administration boundaries

Analytics API results are scoped to a ChatGPT workspace. For the unified Daily
Usage Analytics API, use a workspace-scoped Admin key with
`enterprise.analytics.usage.read`. The Codex scope
`codex.enterprise.analytics.read` doesn't grant access to that endpoint.

The API reference owns current key provisioning, scope requirements,
routes, schemas, fields, time semantics, and pagination behavior. This page
doesn't duplicate that contract.

## Related docs

- [Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics)
- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
- [Governance](https://learn.chatgpt.com/docs/enterprise/governance)
- [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api)
