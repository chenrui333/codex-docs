---
source_type: 'developers'
source_area: 'codex_blog'
source_url: 'https://developers.openai.com/blog/building-security-review-into-your-sdlc-with-codex-security'
source_last_modified: '2026-11-23T20:58:19Z'
source_etag: 'W/"75f8d78588669e37d2348e16478848e6"'
---

# Building security review into your SDLC with Codex Security | OpenAI Developers

Source: https://developers.openai.com/blog/building-security-review-into-your-sdlc-with-codex-security

As AI accelerates the SDLC, it’s putting pressure on security workflows. Security teams need to prevent insecure code from being committed in the first place, but manual security reviews for PRs can’t scale at the same pace that agents are producing and revising code.

Application security programs have followed the pace of human development: a design review before implementation, a manual pass on the riskiest pull requests, and periodic work to triage vulnerability backlogs. **To keep up, we must now deploy agentic security workflows that match the speed of agentic SDLC.**

This post presents four principles for agentic security workflows, then shares how to build and run those workflows through Codex Security and our CLI.

## Four principles for agentic security workflows

Expanding security review capacity requires a clear basis for evaluating changes and a clear way for teams to assess the results. We recommend four principles for integrating security agents into development:

1. ### Give agents system-specific context

   Agents need to understand the application’s assets, trust boundaries, and security requirements to evaluate a change. Threat models, repository security policies, and architecture documents make that knowledge available. Regularly reviewing these artifacts and keeping them current gives agents a reliable foundation for their investigations.
2. ### Integrate review into development

   Security feedback should reach developers while changes are still in progress. Connect reviews to local work, pull requests, and CI workflows, with clear triggers for when they should run. This makes security review a consistent part of the development process.
3. ### Set review scope and reporting thresholds deliberately

   Review scope should reflect the change and the components it could affect. A diff scan, a component assessment, and a full repository scan serve different purposes. Reporting thresholds should also reflect risk, giving sensitive areas such as authentication and billing appropriate attention.
4. ### Make findings inspectable

   Reviewers need enough information to evaluate a finding and determine what action to take. Reports should explain the relevant code locations, reasoning, severity, confidence, and remediation guidance. They should also identify what was reviewed, excluded, or deferred so teams can understand the investigation’s limits.

## Seeding context for security reviews

### Differences among threat models, `AGENTS.md`, `SECURITY.md`, and knowledge bases

[`AGENTS.md`](/codex/agent-configuration/agents-md) keeps shared engineering instructions that establish consistent expectations. `SECURITY.md` tells Codex how your organization wants that reality evaluated and reported. A threat model describes the security reality of the system. They overlap, but the threat model is usually one part of the broader policy.

For example, a threat model would include details about assets, entry points, attacker-controlled inputs, trust boundaries, authentication assumptions, privileged operations, and risky components. Commit it as a separate file, `docs/security/threat-model.md`, so Codex Security can reference it during pull request reviews and security scans.

```
<!-- docs/security/threat-model.md -->

# Threat Model

The public API accepts untrusted JSON and file uploads.
Requests cross from the internet-facing API into internal billing and
identity services. Attackers are unauthenticated users or compromised
tenant accounts. Protect tenant data, billing mutations, and service credentials.
```

The `SECURITY.md` file tells Codex how your organization wants that reality evaluated and reported.

```
<!-- SECURITY.md -->

# Security Policy

## Security Invariants

- Every billing mutation must be authorized for the active tenant.
- Uploaded content must be parsed within explicit size and resource limits.
- Service credentials must never be returned to clients.

## Reportable Findings

Report realistic violations of tenant isolation, authentication bypass,
unsafe parsing, secret exposure, or unauthorized billing mutations.

## Severity Context

Cross-tenant access is Critical.
Single-tenant unauthorized mutation is High.

## Out of Scope

Development-only tools that cannot be included in production builds.
```

Finally, a knowledge base supplies supporting documents to particular scans. This can include architecture documents, policies, additional threat models, or operational context that the CLI scanner should consider. Here’s an example of a Markdown architecture document you can pass to the CLI when running a security scan against a codebase.

```
<!-- docs/security/payment-service-context.md -->

# Payment Service Security Context

## Purpose

The payment service creates charges, issues refunds, and stores references
to payment-provider customers. It does not store full card numbers or CVVs.

## Deployment and Exposure

- `POST /api/payments` is internet-facing through the API gateway.
- `POST /internal/refunds` is reachable only from the support service.
- Background workers consume messages from the `payment-events` queue.
- The service runs with access to the payment-provider API and billing database.

## Authentication and Authorization

- Public endpoints use JWTs issued by the identity service.
- The API gateway validates signatures, issuer, and expiration.
- This service remains responsible for tenant authorization.
- Internal requests use workload identity; network location alone is not trusted.
- Refunds above £1,000 require a previously recorded approval.

## Trust Boundaries

1. Internet client → API gateway
2. API gateway → payment service
3. Payment service → payment provider
4. Payment service → billing database
5. Message producers → `payment-events` consumer

Inputs crossing any of these boundaries must be treated as untrusted unless
the receiving component performs the documented validation.

## Sensitive Assets and Operations

- Payment-provider API credentials
- Customer-to-provider identifier mappings
- Charge creation
- Refund issuance
- Webhook signature secrets
- Tenant billing history

## Important Data Flows

### Creating a charge

1. The API receives an authenticated request containing an order identifier.
2. The service retrieves the order using both tenant ID and order ID.
3. The service calculates the amount from server-side order data.
4. The service creates the provider charge with an idempotency key.
5. The resulting provider identifier is stored in the billing database.

Client-supplied amounts must never be passed directly to the provider.

### Processing a webhook

1. The raw request body is retained.
2. The provider signature is verified over the raw bytes.
3. The event timestamp must be within five minutes.
4. Duplicate event IDs are ignored.
5. State changes occur only after all validation succeeds.

## Relevant Code

- `src/http/payments.ts`: public payment endpoints
- `src/http/refunds.ts`: refund endpoints
- `src/webhooks/provider.ts`: webhook validation
- `src/workers/payment-events.ts`: asynchronous event processing
- `src/auth/tenant.ts`: tenant authorization
- `src/provider/client.ts`: provider API wrapper

## Security Assumptions

- The identity service is trusted to authenticate users, but not to authorize
  access to payment records.
- Queue publishers may be compromised; consumers must validate message content.
- API-gateway authentication does not replace service-level tenant checks.
- Provider webhook payloads are attacker-controlled until signature validation
  completes.

## Known Limitations

- Legacy refunds created before 2025 do not have idempotency keys.
- Webhook replay protection is local to one region.
- The development payment-provider emulator does not validate signatures.
```

It can be supplied to the scan using the following command:

```
npx @openai/codex-security scan . \
  --knowledge-base docs/security/payment-service-context.md
```

Putting it all together, a useful arrangement could look like the following:

```
SECURITY.md
docs/security/
├── threat-model.md
├── architecture.md
├── payment-service-context.md
├── authentication.md
└── deployment-boundaries.md
```

### Seeding a threat model

Committing a threat model is a core component of informing how Codex should conduct security reviews. You can initialize a threat model by invoking the threat model skill within Codex and committing it.

Generate a  Threat Model  of this repository that covers entry points and untrusted inputs, sensitive data paths, and privileged actions.

GPT-6.1 SolExtra High

You can invoke the threat model skill through Codex by simply typing `$threat-model`. Once a threat model has been created, commit it to the repository under `/docs/security` and then link to the threat model within the Codex Cloud settings for the selected repo. If a threat model is not specified, Codex will regenerate the threat model for every security review.

![Example Security Review settings for a demo repository.](/images/codex/secure-sdlc/cloud-settings.webp)

When generating a threat model, pay particular attention to assumptions that the code alone can’t establish, such as compensating controls and responsibilities shared with other services.

Want an even better example? Look at the [trust model](https://github.com/backstage/backstage/blob/943687f3db8caebe2a2ec062f0a06b2e5ec531d8/docs/overview/threat-model.md) for Backstage, an open-source framework for building an internal developer portal. A generated model might treat its authentication and catalog plugins as isolated because they run on separate hosts. However, [Backstage’s threat model](https://github.com/backstage/backstage/blob/943687f3db8caebe2a2ec062f0a06b2e5ec531d8/docs/overview/threat-model.md#common-backend-configuration) explains that this separation does not establish a security boundary if the catalog plugin can still access the authentication plugin’s database.

Correcting the model allows a review to inspect deployment configuration and access grants to determine whether another plugin can read or modify authentication data. This turns an architectural assumption into a requirement. Changes to database access, shared caches, or plugin placement should trigger another review of that boundary.

Lastly, don’t forget to revisit the threat model when entry points, trust boundaries, or privileged operations change. Those are useful triggers for keeping the review context aligned with the application.

### Seeding a `SECURITY.md`

You can use the `$define-security-policy` skill to generate a seeded security policy within the repository.

Define Security Policy  for the Northstar Bank API. Here are key policies that should be included:
Authentication and Authorization:
- Every non-public endpoint must authenticate the caller.
- Sessions and tokens must be validated for issuer, audience, signature, expiry, revocation, and intended authentication context.
- Authentication failures must fail closed.
- Sensitive operations must require recent or stronger authentication where appropriate.
- Password-reset, account-recovery, MFA, and identity-linking flows must not permit account takeover.

GPT-6.1 SolExtra High

A strong security policy should include thorough details about how the application operates. Here’s an example of what to ask Codex to include in `SECURITY.md`:

```
<!-- SECURITY.md -->

### Authentication and Authorization

- Every non-public endpoint must authenticate the caller.
- Sessions and tokens must be validated for issuer, audience, signature, expiry, revocation, and intended authentication context.
- Authentication failures must fail closed.
- Sensitive operations must require recent or stronger authentication where appropriate.
- Password-reset, account-recovery, MFA, and identity-linking flows must not permit account takeover.
- Authentication secrets and tokens must never appear in logs, URLs, analytics, or error responses.
- Authorization must occur before every read, mutation, transaction, export, or administrative action.
- Possession of a valid account or resource identifier never proves authorization.
- Customer, account, and tenant isolation must hold across list, detail, search, bulk, export, and indirect-reference endpoints.
- Server-side authorization must not rely on client-supplied roles, ownership fields, prices, balances, or approval state.
- Administrative and service-to-service permissions must use least privilege.
- Failures allowing cross-customer access are reportable even when only one endpoint is affected.

### Transaction and ledger integrity

- Transactions must be authorized against the authenticated customer and eligible source account.
- Amounts, currencies, destinations, fees, limits, and approval state must be validated server-side.
- Transaction requests must be protected against replay, duplication, race conditions, and idempotency-key confusion.
- Balance checks and ledger updates must be atomic.
- Posted ledger entries must be immutable or corrected through auditable compensating entries.
- High-risk transactions must enforce applicable limits, step-up authentication, approval, or fraud controls.
- No failure path may produce an ambiguous transaction state without reconciliation.

### Data protection

- Sensitive data must be encrypted in transit and at rest using approved controls.
- Secret material must come from an approved secret-management system rather than source code or ordinary configuration files.
- Logs, traces, metrics, support tooling, and security artifacts must exclude credentials and minimize personal and financial data.
- Data exports and backups must receive equivalent authorization and protection to primary data.
- Error responses must not expose internals, sensitive records, credentials, or authorization details.
- Retention and deletion behavior must follow the system’s approved data-governance requirements.

### Input and output handling

- Treat headers, paths, query parameters, bodies, uploaded files, webhook payloads, third-party responses, and stored customer content as untrusted.
- Apply schema, type, range, length, and format validation before security-sensitive use.
- Database access must use parameterized queries.
- Outbound requests must restrict destinations, protocols, redirects, DNS behavior, and response sizes.
- Parsers, uploads, decompression, and serialization must be bounded against resource exhaustion.
- Customer-controlled content must be safely encoded for its output context.
```

Let’s take a look at [Apache Superset, an open-source business intelligence web application,](https://github.com/apache/superset/blob/master/SECURITY.md#async-execution-and-realtime-notifications) as an example. The application connects to databases and lets users explore data, run SQL in SQL Lab, and build and share charts and dashboards. The security policy within their open-source repo establishes detailed context concerning roles and capabilities, as well as how async execution and realtime notifications operate. For example, the policy defines:

> Asynchronous execution paths do not create a separate data-access capability. A background task is a continuation of an already-authorized action, such as reading chart data or executing SQL through SQL Lab. The initiating route, command, or scheduler must enforce the same route-level and object-level checks the synchronous path would enforce before it creates the task, and the worker must execute under the initiating principal’s effective identity when row-level security, impersonation, embedded guest-token scope, or similar controls affect the result.

This makes vulnerability reporting more precise because it defines **what must remain true as execution moves from a request into a background worker**. A reviewer can trace the initiating user, the requested resource, the authorization checks before task creation, and the identity used during execution. As a result, reports from both security researchers and agents can test the policy requirement, the code paths that could violate it, the attacker’s starting permissions, and the resulting unauthorized capability.

## Codex Security

Once context is established, you should choose a review workflow that works with your team’s existing development process. Local review gives a developer feedback before a PR is opened. Automatic PR review provides a consistent team checkpoint. The CLI supports workflows that need explicit targets, saved artifacts, or custom CI integration.

You can also use multiple workflows. However, you should start with one workflow, inspect its results on a change the team understands, and then expand once the review is producing evidence people can use.

### Codex Security Review in GitHub Cloud

The fastest way to automate security reviews in GitHub Cloud is through the [Security Review](/codex/security/security-review) feature within ChatGPT. This is available through the same product surface as Codex Code Reviews available within your organization at [<https://chatgpt.com/codex/cloud/settings/code-review>](https://chatgpt.com/codex/cloud/settings/code-review).

Codex Security Review goes deeper than Code Review on security-specific risks by analyzing the pull request diff, supporting repository context, and configured threat models or security guidance.

#### Difference between Code Review and Security Review

Code Review is a broad engineering review that assesses code quality. For example, Code Review asks: “Could this change break the product or introduce a serious engineering problem?” It reviews issues such as incorrect control flow, data corruption or loss, compatibility regressions, or incorrect API behavior. The intended users for Code Review are software developers within the organization.

Codex Security is a specialized, deeper assessment of security risks in the same PR changes. Security Review is for both software developers responsible for remediating vulnerabilities, as well as application security engineers responsible for securing CI/CD pipelines and source code. It assesses issues such as authentication and authorization bypasses, cross-tenant access, injection and unsafe parsing, or sensitive data exposure.

#### Configuring security reviews

There are two options for configuring security reviews. The auto-review reporting determines which findings Codex posts to the PR when Security Review runs automatically. It is defaulted to High, so only High and Critical findings are posted.

The option for manual review controls which findings Codex posts after someone explicitly requests a Security Review. It is defaulted to Medium, so Medium, High, and Critical findings are posted.

When configured, posted vulnerabilities will surface within the PR.

![Security finding posted on a GitHub pull request.](/images/codex/secure-sdlc/github-review-finding.webp)

It’s best to choose automatic reporting thresholds around what the team is prepared to investigate consistently. For a targeted investigation, use the manual review settings to surface the additional detail relevant to that question.

#### Setting path overrides

Path-based reporting overrides the minimum severity published to the GitHub PR. Given that a repository’s risk is rarely uniform, this feature can tailor the risk threshold for more critical paths, such as:

- Lowering the threshold for authentication, authorization, payments, cryptography, CI workflows, or infrastructure.
- Keeping a higher threshold for lower-risk or especially noisy areas.

You can modify the path overrides within the Codex Cloud settings for the selected repo. In this example below, we have established that `src/**` should have auto reviews for low vulnerabilities or higher. Changes to GitHub workflows or dependencies will enforce reporting for medium vulnerabilities.

![Path overrides for source files, workflows, and dependencies.](/images/codex/secure-sdlc/path-overrides.webp)

A practical starting point is to identify the application’s sensitive operations and map them to paths with their owners. For the payment service example at the beginning of this post, that includes tenant authorization and billing mutations. I would review those paths with the team that owns them and choose a reporting threshold that reflects the consequence of a missed issue.

Going back to our [Apache Superset](https://github.com/apache/superset) example, I would keep a **High** repository-wide reporting threshold, but lower it for these paths:

| Repository-relative path prefix | Minimum severity to report | Why it deserves additional attention |
| --- | --- | --- |
| `superset/security/` | Low | Path contains code for central authorization, guest tokens, password recovery, and session invalidation |
| `superset/row_level_security/` | Low | Path controls the policies determining which data rows users can access |
| `superset/sqllab/` and `superset/commands/sql_lab/` | Medium | Path focuses on SQL execution, query authorization, result retrieval, and exports |
| `superset/embedded/` | Medium | Path focuses on boundaries for dashboards embedded in other applications |

If these settings were applied, then Codex Security Review would only report **High** vulnerabilities for all paths except those stated above. In those paths, **Low** and **Medium** would be reported given the additional sensitivity of the code.

### Codex Security Review in Codex Desktop

For a more interactive experience reviewing PRs or uncommitted changes, you can also execute reviews through the security tab within Codex.

![The Security workbench with the Changes scan type selected.](/images/codex/secure-sdlc/changes-scan.webp)

Alternatively, you can prompt Codex within the repository project of Codex by invoking the skill.

Please run a  Security Diff Scan  on the changes in the current branch.

GPT-6.1 SolExtra High

This workflow is most useful when the implementation is still fresh in your mind and you can investigate a finding immediately. If the review points to an authorization assumption, you can inspect the caller and the affected operation before the change moves into a separate review queue.

### Codex Security Review in the CLI

#### Reviewing uncommitted local work

You can use the CLI to review uncommitted local work with seeded context about the repository and security policies.

Run the examples in the same shell from your Git checkout. They assume your security policy is in `SECURITY.md` and your supporting documents are in `docs/security/`. The setup creates a temporary directory for scan results.

```
northstar_repo="$(git rev-parse --show-toplevel)"
northstar_kb="$northstar_repo/docs/security"
northstar_results="$(mktemp -d)"
```

```
npx @openai/codex-security scan "$northstar_repo" \
  --working-tree \
  --base HEAD \
  --knowledge-base "$northstar_repo/SECURITY.md" \
  --knowledge-base "$northstar_kb" \
  --output-dir "$northstar_results/working-tree"
```

This reviews staged and unstaged changes relative to `HEAD`.

Before starting, be sure to confirm that the working tree contains the change you intend to assess. Unrelated edits broaden the investigation and can make it harder to connect the findings to the question that prompted the review.

#### Reviewing PRs or branch commits

Another option is to review a PR or branch for security issues. Check out the branch to review and fetch its target branch. This example uses `origin/main`.

```
northstar_pr_base="$(git -C "$northstar_repo" merge-base origin/main HEAD)"

npx @openai/codex-security scan "$northstar_repo" \
  --diff "$northstar_pr_base" \
  --head HEAD \
  --knowledge-base "$northstar_repo/SECURITY.md" \
  --knowledge-base "$northstar_kb" \
  --output-dir "$northstar_results/branch"
```

Note that a diff scan evaluates the proposed changes and does not scan the entire repository. Once complete, the output directory will contain the following files:

- `report.md`: readable review
- `scan-manifest.json`: confirms the exact base, head, target, and artifacts
- `findings.json`: presents the severity, confidence, locations, and remediation
- `coverage.json`: identifies the reviewed surfaces, exclusions, deferred work, and completeness

#### Scanning monorepos

In a monorepo, a change to a shared library can affect multiple services. Codex should receive enough context to review those interactions, while CI determines which components and checks are required.

##### Repository context

Keep shared engineering instructions in `AGENTS.md` and security expectations in `SECURITY.md`. A typical repository could look like this:

```
monorepo/
├── AGENTS.md
├── SECURITY.md
├── docs/security/
│   ├── architecture.md
│   └── threat-model.md
├── packages/auth/
└── services/
    ├── billing/
    └── reporting/
```

Use existing ownership and build metadata to connect each component to its dependencies, consumers, and tests. For example, a change to `packages/auth` may require reviewing both services even when their files are unchanged. This scope mapping is maintained by your organization; it is not automatically configured by adding Codex.

##### Component assessment

Large repositories may not always require scanning the entire codebase for each PR. One option is to use a path scan when a monorepo contains separate services or packages. Repeat `--path` to assess a shared library and its consumers together.

```
npx @openai/codex-security scan "$northstar_repo" \
  --path packages/auth \
  --path services/billing \
  --path services/reporting \
  --knowledge-base "$northstar_repo/SECURITY.md" \
  --knowledge-base "$northstar_kb" \
  --output-dir "$northstar_results/paths"
```

This scans only the selected paths rather than the entire repository.

##### PR and diff scanning

For a PR, use its exact base and head commit hashes from authenticated GitHub metadata. Both revisions and their history must be available in the checkout. The following example reuses the variables above and saves the diff results separately:

```
BASE_SHA="<full PR base commit SHA>"
HEAD_SHA="<full PR head commit SHA>"

BASE_REVISION="$(
  git -C "$northstar_repo" merge-base "$BASE_SHA" "$HEAD_SHA"
)" || exit

npx @openai/codex-security scan "$northstar_repo" \
  --diff "$BASE_REVISION" \
  --head "$HEAD_SHA" \
  --knowledge-base "$northstar_kb" \
  --auth chatgpt \
  --output-dir "$northstar_results/pr"
```

A diff scan focuses on the proposed changes. If a shared-library change requires broader consumer review, also run the component assessment against a clean checkout of that PR’s head revision. Keep the results distinct: `--diff` and `--path` are separate scan modes and cannot be combined.

#### Scanning alerts from GitHub

You can also assess code scanning alerts from the default branch using the Codex Security CLI.

```
northstar_github_repository="example/northstar"
northstar_github_alerts="$northstar_results/github-alerts.json"

# Import all open alerts as complete JSON.
npx @openai/codex-security import github "$northstar_github_repository" \
  --format json \
  > "$northstar_github_alerts"

# Or import a selected subset.
npx @openai/codex-security import github "$northstar_github_repository" \
  --github-alert 12 \
  --github-alert 18 \
  --format json \
  > "$northstar_github_alerts"

# Run from the corresponding local repository; imported contents are data.
cd "$northstar_repo"
npx @openai/codex-security validate "$northstar_github_alerts"
```

### GitHub Actions workflows

Instead of enforcing security reviews through Codex, it is also possible to create custom workflows that run the Codex Security CLI. We’ve packaged this workflow to easily be used as a GitHub Action.

```
# .github/workflows/codex-security-repository.yml
name: Codex Security review
on:
  workflow_dispatch:
  schedule:
    - cron: "23 7 * * 1" # Mondays at 07:23 UTC

permissions:
  contents: read

jobs:
  security:
    runs-on: ubuntu-24.04
    steps:
      - name: Set up the Ubuntu sandbox
        run: |
          sudo apt-get update
          sudo apt-get install --yes bubblewrap apparmor-profiles
          sudo apparmor_parser -r /usr/share/apparmor/extra-profiles/bwrap-userns-restrict

      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: openai/codex-security@3f61e5150981a5087c32e4395bbaa8ce5ce0c3e3 # action-v0.3.0
        with:
          model: gpt-5.6-sol
          effort: high
        env:
          OPENAI_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
```

These workflows can also be applied to other source code management tools like GitLab, BitBucket, or Jenkins. Take a look at our documentation page to learn more: [Run Codex Security in CI](/codex/security/cli/ci).

## Managing supply chain risk in CI/CD

You can also leverage the Codex Security CLI to assess dependencies in the codebase, such as when a new dependency is introduced or a version is bumped.

This is extremely useful in preventing vulnerable packages from presenting supply chain risk – you can achieve this by deploying the Codex Security CLI as commands within custom workflows.

### Validating Dependabot alerts

Codex Security provides a skill for validating existing third-party vulnerabilities, including Dependabot, for reachability and exploitability. You can invoke the skill directly in the UI or through the CLI.

Use  Triage Finding  to import and triage Dependabot vulnerabilities against this repository.

GPT-6.1 SolExtra High

Codex will triage each of the Dependabot alerts and subsequently present a ledger of each presented risk with a reason why the alert was validated or not.

![Dependabot triage results with verdicts and static rationale.](/images/codex/secure-sdlc/dependabot-ledger.webp)

Looking at Apache Superset again, we can take its [documentation toolchain](https://github.com/apache/superset/blob/master/superset-embedded-sdk/package.json) to identify a security advisory related to it (such as [webpack-dev-server advisory](https://github.com/webpack/webpack-dev-server/security/advisories/GHSA-f5vj-f2hx-8m93)).

Using Codex, we can trace the dependency through Docusaurus, check the resolved version, and follow the development, build, and deployment paths to establish where the affected functionality could run. The [reviewed lockfile](https://github.com/apache/superset/blob/2c275ed0a5b5878a1473408e5479b96adcccb6a8/docs/yarn.lock#L15019-L15021) selected version 5.2.6, which the advisory identifies as patched.

Codex’s analysis therefore supported a specific conclusion: the advisory did not affect the version selected by that documentation revision. Before closing a corresponding Dependabot alert, we would reconcile its reported version and revision with this evidence and verify the installed dependency.

### Running scans when package versions change

It is also possible to run security scans against the latest version of a dependency when the version is changed.

```
# .github/workflows/codex-security-dependency.yml
name: Codex Security dependency scan

on:
  pull_request:
    paths:
      - package.json
      - package-lock.json

permissions:
  contents: read

jobs:
  scan:
    name: Scan dependency changes
    if: github.event.pull_request.head.repo.full_name == github.repository
    runs-on: ubuntu-24.04
    timeout-minutes: 45
    steps:
      - name: Set up the Ubuntu sandbox
        run: |
          sudo apt-get update
          sudo apt-get install --yes bubblewrap apparmor-profiles
          sudo apparmor_parser -r /usr/share/apparmor/extra-profiles/bwrap-userns-restrict

      - name: Set up Node.js
        uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7
        with:
          node-version: "26"

      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7
        with:
          python-version: "3.14"

      - name: Install Codex Security
        run: |
          set -euo pipefail
          npm install \
            --prefix "$RUNNER_TEMP/codex-security" \
            --ignore-scripts \
            --no-audit \
            --no-fund \
            @openai/codex-security

      - name: Verify Codex Security
        env:
          CODEX_SECURITY_BIN: ${{ runner.temp }}/codex-security/node_modules/.bin/codex-security
        run: |
          set -euo pipefail
          test -x "$CODEX_SECURITY_BIN"
          "$CODEX_SECURITY_BIN" --version

      - name: Check out the pull request
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0
          persist-credentials: false

      - name: Install project dependencies
        run: |
          set -euo pipefail
          npm ci --ignore-scripts --no-audit --no-fund

      - name: Run full repository scan
        env:
          OPENAI_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
          CODEX_SECURITY_BIN: ${{ runner.temp }}/codex-security/node_modules/.bin/codex-security
          CODEX_SECURITY_STATE_DIR: ${{ runner.temp }}/codex-security-state
          SCAN_DIR: ${{ runner.temp }}/codex-security-results
        run: |
          set -euo pipefail
          "$CODEX_SECURITY_BIN" scan . \
            --auth api-key \
            --output-dir "$SCAN_DIR" \
            --fail-on-severity high \
            --json > "$RUNNER_TEMP/codex-security.json"

      - name: Preserve scan results
        if: always()
        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7
        with:
          name: codex-security-dependency-results
          path: |
            ${{ runner.temp }}/codex-security-results
            ${{ runner.temp }}/codex-security.json
          if-no-files-found: warn
          retention-days: 7
```

## Wrapping up

As agents contribute more code, security teams must carve the right scaffolding for agentic systems to reason across the codebase for application security reviews and enforce gates when insecure code could be committed.

Start with a few critical repositories, commit your threat models and security policies, then review the pull requests to assess how accurately agents are reasoning against enterprise context and the codebase. When you begin to feel confident in the quality of the results, begin to expand into a broader number of repositories or pipelines as you expand agentic security coverage in the SDLC.

Curious about learning more or wondering what to tackle next? Review our [security use cases](https://learn.chatgpt.com/use-cases/collections/security) within our developer docs or explore details about the [Daybreak Defense Factory](https://learn.chatgpt.com/docs/security/setup) for continuous security reviews.
