---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/sdk'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0"]
---

# Codex Security TypeScript SDK

Source: https://learn.chatgpt.com/docs/security/sdk

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use the Codex Security TypeScript SDK to run security scans on repositories and
code changes from your application or developer tool. The SDK returns typed
findings, coverage details, and paths to scan artifacts. For longer scans, it
supports preflight checks, cost limits, progress callbacks, and cancellation.

The SDK uses ECMAScript modules (ESM) and runs server-side with Node.js 22
(22.13.0 or later), 24, or 26. Scanning also requires Python 3.10 or later.
Python 3.10 also requires the `tomli` package.

The Codex Security SDK is [publicly available on
  GitHub](https://github.com/openai/codex-security). Running scans requires
  Codex Security access. For general coding agents, see the [Codex SDK
  guide](https://learn.chatgpt.com/docs/codex-sdk). For terminal and CI workflows, see the [Codex
  Security CLI quickstart](https://learn.chatgpt.com/docs/security/cli).

## Set up the SDK

Install the SDK:

```bash
npm install @openai/codex-security
```

Before starting a scan, set `OPENAI_API_KEY` or `CODEX_API_KEY`, use an
existing file-backed Codex sign-in, or [configure another
provider](#configure-the-runtime-and-credentials). Amazon Bedrock uses AWS
credentials; OpenRouter and Fireworks use provider-specific API keys and
configuration.

For best results, use an account verified for [Trusted Access for
Cyber](https://chatgpt.com/cyber). Signing in or providing an API key does not
grant Trusted Access.

## Run a scan

Scan only repositories you trust and have permission to assess. The SDK runs
with your local operating-system permissions and never pauses for approval.
Scan processes can inherit your environment, so remove unrelated credentials
before you start. See [Local scan
permissions](https://learn.chatgpt.com/docs/security/cli/reference#local-scan-permissions).

Create one `CodexSecurity` client, run a standard repository scan, and close
the client when the work completes. Pass `outputDir` to choose a private
results directory outside the enclosing Git worktree.

If you omit `outputDir`, Codex Security saves results in its own persistent
state directory. Results can include source excerpts and vulnerability
details, so choose appropriate permissions and retention policies.

```ts

const security = new CodexSecurity();

try {
  const result = await security.run("/path/to/repository", {
    outputDir: "/path/outside/repository/results",
  });

  console.log(result.reportPath);
  console.log(result.coverage.completeness);
  console.log(result.findings.findings.length);
} finally {
  await security.close();
}
```

`run` starts the scan, waits for completion, validates the sealed artifacts,
and returns a `ScanResult`. `close` releases the isolated runtime and supports
repeated calls.

## Check inputs with preflight

Use `preflight` to check a repository, target, mode, knowledge-base documents,
output location, and Codex configuration before starting a scan:

```ts
const plan = await security.preflight("/path/to/repository", {
  target: ["services/billing", "packages/auth"],
  knowledgeBasePaths: ["/path/to/architecture.md"],
  outputDir: "/path/outside/repository/results",
});

console.log(plan.repository);
console.log(plan.target.kind);
console.log(plan.mode);
console.log(plan.outputDir);
```

Preflight leaves the Codex runtime and credentials untouched. It also leaves
plugin and Python discovery for the scan itself. This makes preflight useful
for checking user input before a long-running or credentialed operation.

To preview archival for an existing result directory, set
`archiveExisting: true`:

```ts
const plan = await security.preflight("/path/to/repository", {
  outputDir: "/path/outside/repository/results",
  archiveExisting: true,
});

console.log(plan.archiveDir);
```

The returned `archiveDir` previews the archive naming. The final path can
differ because `run` generates its own unique destination. Capture the actual
archive path with `onOutputArchived`:

```ts
await security.run("/path/to/repository", {
  outputDir: "/path/outside/repository/results",
  archiveExisting: true,
  onOutputArchived(archiveDir) {
    console.log("Archived results:", archiveDir);
  },
});
```

The scan archives the earlier results and starts with an empty output
directory.

## Choose a scan target

The SDK supports repository, path, committed-diff, and working-tree targets.
The default target is the complete repository.

### Scan selected paths

Pass an array of paths inside the repository:

```ts
const result = await security.run("/path/to/repository", {
  target: ["services/billing", "packages/auth"],
});
```

Paths can identify files or directories. The SDK resolves each path inside the
repository and removes duplicates.

### Scan committed changes

Use `DiffTarget.refs` to scan committed changes between two locally available
Git revisions:

```ts

const target = DiffTarget.refs({
  base: "origin/main",
  head: "HEAD",
});

const result = await security.run("/path/to/repository", { target });
```

The head defaults to `HEAD`. Diff targets require the repository argument to
be the Git worktree root.

### Scan the working tree

Use `DiffTarget.workingTree` to scan staged and unstaged changes against a base
revision:

```ts
const target = DiffTarget.workingTree({ base: "HEAD" });
const result = await security.run("/path/to/repository", { target });
```

The base defaults to `HEAD`. Fetch the selected revisions before starting a
diff or working-tree scan.

### Select deep mode

Set `mode: "deep"` for a repository or path scan that needs broader review:

```ts
const result = await security.run("/path/to/repository", {
  target: ["services/billing"],
  mode: "deep",
  workers: 2,
  subagents: 0,
  stopAfterNoNew: 3,
  maxDiscoveryRuns: 10,
  maxTimeHours: 1.5,
});
```

Deep mode supports repository and path targets. Use standard mode for diff and
working-tree scans. The optional settings control concurrent independent
standard-scan workers, subagents per worker, consecutive completed worker scans
without new findings, and the total number and duration of worker runs. They
require `mode: "deep"`.

`maxTimeHours` defaults to `96` and accepts a positive number up to `96`,
including fractional hours. At the deadline, Codex Security stops unfinished
workers, keeps completed scan results, and aggregates them into the final
report. Review `result.coverage.completeness` before treating a time-limited
scan as evidence of full coverage.

### Add a security knowledge base

Pass architecture documents, threat models, or security policies through
`knowledgeBasePaths`:

```ts
const result = await security.run("/path/to/repository", {
  knowledgeBasePaths: [
    "/path/to/architecture.md",
    "/path/to/security-policies",
  ],
});
```

The SDK accepts files or directories and searches directories recursively.
Supported document formats are `.md`, `.markdown`, `.txt`, `.pdf`, and `.docx`.
The SDK rejects linked input paths, skips linked directory entries, and keeps
extracted document content outside the saved scan results.

### Add scan and follow-up instructions

Use `scanPrompt` to focus the scan and `postScanPrompt` to request a follow-up:

```ts
const result = await security.run("/path/to/repository", {
  scanPrompt: "Focus on tenant isolation and authorization checks.",
  postScanPrompt: "Write confirmed findings to post-scan-summary.md.",
});
```

If the follow-up fails, the SDK keeps the completed scan and reports the
error through `onWarning`. It restores any completed scan artifacts that the
follow-up changed.

### Set a scan budget

Set `maxCostUsd` to stop a scan when its estimated model cost exceeds a limit.
Use `onCost` to track cost as the scan runs:

```ts
const result = await security.run("/path/to/repository", {
  maxCostUsd: 5,
  onCost(cost) {
    console.log(cost.estimatedUsd);
  },
});

console.log(result.cost?.estimatedUsd);
```

The limit estimates spending but isn't a hard cap, so requests already in
progress can finish slightly above it. If a deep scan reaches the limit after
Codex Security aggregates completed worker results, `run` returns a result
with `coverage.completeness` set to `"partial"` and reports the budget warning
through `onWarning`.

If the scan can't produce a completed partial result, `run` throws
`ScanCostLimitExceededError` and preserves any available output.

## Work with scan results

`ScanResult` exposes the structured documents, scan metadata, and artifact
paths:

| Property             | Contents                                                                           |
| -------------------- | ---------------------------------------------------------------------------------- |
| `manifest`           | The sealed scan manifest, including target, scope, producer, and artifact records. |
| `findings`           | Findings from the current scan. Read finding objects from `findings.findings`.     |
| `repositoryFindings` | Open findings across repository scans, when scan history is available.             |
| `coverage`           | Reviewed surfaces, exclusions, deferred work, open questions, and completeness.    |
| `scanDir`            | The scan directory.                                                                |
| `threadId`           | The Codex thread identifier for the scan.                                          |
| `turnResult`         | Turn status, response, and available usage metadata.                               |
| `cost`               | Estimated model and token cost, or `null` when unavailable.                        |
| `reportPath`         | The path to `report.md`.                                                           |
| `manifestPath`       | The path to `scan-manifest.json`.                                                  |
| `findingsPath`       | The path to `findings.json`.                                                       |
| `coveragePath`       | The path to `coverage.json`.                                                       |
| `artifactsDir`       | The supporting-artifacts directory.                                                |
| `sarifPath`          | The generated SARIF path, or `null` when SARIF is absent.                          |
| `pluginVersion`      | The version recorded by the scan producer.                                         |

To require the same plugin for a later scan, pass
`expectedPluginVersion: result.pluginVersion`. The SDK rejects the scan if
the installed plugin version differs.

Use the structured findings and coverage directly:

```ts
for (const finding of result.findings.findings) {
  const location = finding.locations[0];
  if (location === undefined) continue;

  console.log(
    finding.severity.level,
    `${location.path}:${location.startLine}`,
    finding.title
  );
}

for (const deferred of result.coverage.deferred) {
  console.log(deferred.id, deferred.reason);
}
```

Findings can include optional `codeEvidence`, `rootCause`, `validation`,
`attackPath`, `remediationTests`, and `preventiveControls` fields.

For repository-wide findings, `confirmedInLatestScan` distinguishes findings
seen in the latest scan from earlier findings that remain open:

```ts
for (const finding of result.repositoryFindings ?? []) {
  console.log(finding.title, finding.confirmedInLatestScan);
}
```

Coverage completeness is `complete`, `partial`, or `unknown`. Review deferred
surfaces, exclusions, and open questions before using a scan as evidence for a
security decision.

`result.toJSON()` returns the manifest, repository and current-scan findings,
coverage, scan and thread identifiers, `reportPath`, `artifactsDir`,
`sarifPath`, cost, and turn metadata in one JSON-ready object.

## Track or cancel a scan

Pass `ScanOptions` callbacks to report scan startup, worker progress, and
connection retries:

```ts
const result = await security.run("/path/to/repository", {
  outputDir: "/path/outside/repository/results",
  onScanStarted() {
    console.log("Scan started");
  },
  onProgress(progress) {
    console.log(progress.phase, progress.filesCompleted, progress.filesTotal);
  },
  onWorkerStatus(status) {
    console.log(status.kind, status);
  },
  onSessionEvent(session) {
    console.log(session.threadId, session.worker, session.event["type"]);
  },
  onReconnect(attempt, maxAttempts) {
    console.log(`Reconnect attempt ${attempt} of ${maxAttempts}`);
  },
  onObserverError(observer, error) {
    console.error(`${observer} failed`, error);
  },
});

console.log(result.reportPath);
```

Pass an `AbortSignal` when cancellation comes from a request, job controller,
or timeout:

```ts

const controller = new AbortController();

try {
  const scan = security.run("/path/to/repository", {
    outputDir: "/path/outside/repository/results",
    signal: controller.signal,
  });

  controller.abort();
  await scan;
} catch (error) {
  if (error instanceof ScanInterruptedError) {
    console.error(error.scanDir);
  } else {
    throw error;
  }
}
```

An interrupted scan can leave partial output in `scanDir`. Preserve that
directory when the result needs investigation.

Applications that display scan setup progress can also use the `ScanOptions`
lifecycle callbacks:

| Callback                            | Called when                                          |
| ----------------------------------- | ---------------------------------------------------- |
| `onAuthentication(authentication)`  | The scan selects its authentication method.          |
| `onOutputArchived(archiveDir)`      | Existing results move to the archive directory.      |
| `onOutputDirReady(scanDir)`         | The private scan directory is ready.                 |
| `onScanStarted()`                   | Scan setup completes and execution begins.           |
| `onTrustedAccessStatus(status)`     | Trusted Access status becomes available.             |
| `onReconnect(attempt, maxAttempts)` | The SDK retries a disconnected scan stream.          |
| `onActivity(activity)`              | A command, tool, reasoning step, or message updates. |
| `onProgress(progress)`              | The scan phase or reviewed file count changes.       |
| `onWorkerStatus(status)`            | Worker preflight or dispatch status changes.         |
| `onSessionEvent(session)`           | A scan or worker session emits an event.             |
| `onCost(cost)`                      | An updated estimated scan cost is available.         |
| `onWarning(warning)`                | The scan reports a warning.                          |
| `onObserverError(observer, error)`  | Another scan lifecycle callback raises an error.     |

Trusted Access status is `granted`, `not_granted`, or `unknown`. Missing or
unknown access also triggers `onWarning`.

`onSessionEvent` receives events that aren't redacted and can contain source
code or credentials. Filter them before sending them to shared logs or other
services.

## Configure the runtime and credentials

Pass runtime configuration when you need a specific plugin, interpreter, or
Codex setting:

```ts
const security = new CodexSecurity({
  pluginPath: "/path/to/codex-security-plugin",
  pythonPath: "/path/to/python",
  codexOverrides: {
    model: "gpt-5.6-terra",
    model_reasoning_effort: "high",
  },
});
```

`pluginPath` accepts a plugin directory or ZIP. `pythonPath` selects the
plugin interpreter. `codexOverrides` merges supported values into the isolated
Codex configuration. Scans use `gpt-5.6-sol` with extra-high reasoning effort
by default. Set `model` and `model_reasoning_effort` in `codexOverrides` to use
a different model or reasoning effort. To use [Amazon
Bedrock](https://learn.chatgpt.com/docs/security/cli/reference#use-amazon-bedrock), set
`model_provider` and `model` in `codexOverrides`.

`codexOverrides` can't restrict the scan's filesystem access or change its
approval policy. See [Local scan
permissions](https://learn.chatgpt.com/docs/security/cli/reference#local-scan-permissions).

For OpenRouter or Fireworks, also provide the matching API key and a complete
provider configuration in `codexOverrides`. For example, set
`OPENROUTER_API_KEY` and configure OpenRouter:

```ts
const security = new CodexSecurity({
  codexOverrides: {
    model: "anthropic/claude-sonnet-4.5",
    model_provider: "openrouter",
    model_providers: {
      openrouter: {
        name: "OpenRouter",
        base_url: "https://openrouter.ai/api/v1",
        env_key: "OPENROUTER_API_KEY",
        wire_api: "responses",
      },
    },
  },
});
```

For Fireworks, change both `openrouter` keys to `fireworks`, set `name` to
`Fireworks AI`, set `env_key` to `FIREWORKS_API_KEY`, use
`https://api.fireworks.ai/inference/v1` as `base_url`, and select a Fireworks
model.

The client also exposes supported authentication methods:

| Method                     | Purpose                                                     |
| -------------------------- | ----------------------------------------------------------- |
| `loginApiKey(apiKey)`      | Authenticate the isolated runtime with an API key.          |
| `loginChatGPT()`           | Start a browser sign-in flow and return a login handle.     |
| `loginChatGPTDeviceCode()` | Start a device-code sign-in flow and return a login handle. |
| `account()`                | Return the current authentication state.                    |
| `logout()`                 | Clear isolated authentication.                              |

A login handle provides `waitForInstructions`, `authUrl`, `verificationUrl`,
`userCode`, `wait`, and `cancel` so an application can present and complete the
selected sign-in flow. The SDK can reuse a file-backed Codex sign-in. API keys
are a useful fit for CI and server-side automation.

When both an API key and a stored sign-in are available, the SDK uses the API
key by default. To use your ChatGPT sign-in instead, select it for the scan:

```ts
const result = await security.run("/path/to/repository", {
  auth: "chatgpt",
});
```

Set `auth: "api-key"` to require an environment API key. `preflight` accepts
the same `auth` option.

## Handle scan errors

Catch the exported error class that matches the action your application can
take:

| Error                            | Meaning                                                            |
| -------------------------------- | ------------------------------------------------------------------ |
| `AuthenticationRequiredError`    | A scan needs a supported credential.                               |
| `ConfigurationError`             | Codex configuration or an override is unsuitable.                  |
| `InvalidTargetError`             | The repository, path, mode, or Git target is unsuitable.           |
| `OutputDirectoryError`           | The output location or its permissions are unsuitable.             |
| `OutputInsideProtectedRootError` | The output directory is inside the scanned repository or worktree. |
| `PluginPythonUnavailableError`   | A usable Python interpreter is unavailable.                        |
| `PluginBootstrapError`           | The plugin runtime could not start.                                |
| `ScanCostLimitExceededError`     | The scan exceeded its estimated cost limit.                        |
| `IncompleteScanError`            | The scan ended before producing the required result.               |
| `ContractValidationError`        | A completed scan returned a structured-contract error.             |
| `ScanInterruptedError`           | An interruption stopped the scan and may have left partial output. |

Continue with the [CLI quickstart](https://learn.chatgpt.com/docs/security/cli), [CI
guide](https://learn.chatgpt.com/docs/security/cli/ci), or [CLI
reference](https://learn.chatgpt.com/docs/security/cli/reference).
