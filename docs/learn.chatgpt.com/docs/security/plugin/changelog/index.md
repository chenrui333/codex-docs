---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/changelog'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0"]
---

# Codex Security plugin changelog

Source: https://learn.chatgpt.com/docs/security/plugin/changelog

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use this changelog to see what changed in the Codex Security plugin.

**Latest plugin version:** `0.1.20`.

Check the plugin version in your current Codex environment before you use a
feature from a newer release.

Changelog entries follow the plugin version, not the package version. CLI and
SDK users can run `npx @openai/codex-security info --json` to check the
package and bundled plugin versions together.

## 0.1.20 (August 17, 2026)

### Run deep scans as complete independent audits

- Run each deep scan worker through the same end-to-end audit used by standard
  scans, including threat modeling, validation, attack-path analysis, and
  coverage reporting.
- Combine completed worker reports into one scan while preserving configured
  time limits, partial coverage, restart recovery, and cancellation.
- Use four concurrent workers by default, stop after four consecutive completed
  scans add no new findings, and limit a deep scan to 40 worker runs. Existing
  `workers = "auto"` settings now resolve to four workers. See
  [Configure deep-scan runtime](https://learn.chatgpt.com/docs/security/plugin/deep-scans#configure-deep-scan-runtime).
- Resume workers that finished source review but lost their final draft instead
  of repeating the complete audit.

### Check Trusted Access for Cyber before hosted scans

- In Codex hosts that expose the Codex Security Access app, check Trusted Access
  status before standard, change, and deep scans begin.
- See a prominent warning when protected scan output might not be available,
  with an enrollment link when access isn't granted.
- Continue the scan when the check can't verify Trusted Access status or access
  isn't granted; the advisory doesn't control whether the scan runs.
- The public CLI and SDK packages don't run this advisory in `0.1.20`.

### Run deep scans in more environments

- Launch deep scan workers from packaged CLI and SDK installations, including
  Windows installations without a global `codex` executable.
- Keep standalone CLI and SDK deep scan settings isolated from other running
  scans.
- Keep non-interactive approval settings in nested deep scan workers.

### Preserve scan results through more failures

- Preserve more saved scans and completed worker results across restart,
  archive, and handoff recovery paths.
- Recover valid findings from older or incomplete scan data.
- Complete scans when independent coverage reports overlap.
- Report cached input correctly in token usage totals across current and older
  provider responses.

## 0.1.19 (August 13, 2026)

### Set a time limit for deep scans

- Set `[deep_scan].max_time_hours` to a positive duration of up to 96 hours.
  You can use fractional hours.
- Keep completed discovery results when the deadline expires, then continue
  with validation and reporting.
- Mark the report as partial if no source review finishes before the deadline.

### Improve scan reliability

- Keep completed discovery work when a worker stops or a reducer retries.
- Read larger source files and generate reports without the previous fixed
  size limits.
- Read committed changes from the selected revision and preserve
  repository-relative paths on Windows.
- Pass OpenRouter and Fireworks credentials to deep-scan workers.

## 0.1.18 (August 7, 2026)

### Use Amazon Bedrock for security scans

- Run scans with Amazon Bedrock bearer tokens and AWS profiles, regional
  settings, web identity, or container credentials.
- Keep AWS authentication available to delegated deep-scan workers.

### Run standard scans with less coordination

- Use a simpler workflow for standard repository and scoped-path scans.
- Preserve nested `SECURITY.md` guidance, exact scan scope, progress updates,
  and final scan reports.

### Start and complete scans more reliably

- Give prompt-started scans up to five minutes to initialize large
  repositories instead of timing out after 30 seconds.
- Complete standard and deep scans when a host enforces tool-name length
  limits.

### Keep remediation available after filesystem changes

- Remediate findings from completed scans after a filesystem remount changes
  its device identifier.
- Continue requiring the original checkout and Git revision before applying a
  fix.

## 0.1.17 (August 5, 2026)

### Follow scan progress as it happens

- Track the current scan phase, elapsed time, active workers, reviewed files, and
  token usage from a single live progress view.
- See repository review progress update as files finish instead of waiting for a
  scan to complete.

### Resume interrupted deep scans

- Continue an in-progress deep scan after its coordinator restarts without
  repeating completed file reviews.
- Preserve completed discovery results, scan ownership, and pending work across
  app updates or interrupted scan sessions.

### Start and complete scans with less overhead

- Start standard, change, and deep scans directly in native workflows without
  opening the retired embedded scan widget.
- Reuse completed scan summaries without reloading every finding unless you
  request the complete structured results.

## 0.1.16 (August 4, 2026)

### Track measured scan usage

- Review total, input, cached input, and output token usage across the main scan
  and its delegated workers.
- Distinguish complete, partial, and unavailable measurements instead of showing
  missing usage as zero.

### Run deeper scans with consistent results

- Use the same threat-modeling, discovery, validation, attack-path analysis, and
  reporting phases for standard and deep scans.
- Configure deep scan workers, per-worker delegation, saturation, and discovery
  limits from the CLI or SDK.
- Run deep scans with the model's supported worker runtime and recover older
  scan state without losing existing scan history.
- Generate the primary report for change and deep scans without requiring
  separate vulnerability write-ups or hardening recommendations.

### Keep scan guidance and repository targets accurate

- Update security guidance during an active scan and carry it into later phases
  and delegated deep scan workers.
- Preserve repository URLs, pull request references, and longer security context
  without allowing network access you didn't request.
- Fail scans when the repository or scan target changes during execution so
  automation doesn't accept stale findings.
- Honor enterprise proxy and trusted certificate settings in managed network
  environments.

### Write clearer vulnerability reports

- Produce source-backed vulnerability reports that separate observed behavior
  from unverified hypotheses.
- Include realistic proof-of-concept limitations, affected versions, security
  boundaries, and actionable remediation guidance.

## 0.1.15 (July 30, 2026)

### Preserve scan results when the repository changes

- Keep completed findings and reports tied to the original revision or
  working-tree snapshot, even if files or the repository revision change while a
  scan runs.
- Show a completion warning when the selected code changes or the target becomes
  unavailable instead of discarding the scan results.
- Archive an existing scan before reusing its output directory for another scan.

### Apply reviewed finding feedback

- Record a reason when you close a finding as a false positive.
- Carry reviewed false-positive decisions into later scans of the same target
  without applying them to another checkout or unrelated target.
- Suppress a recurring finding only when the earlier reason still applies to
  the current code and security controls.

### Recover valid findings without overstating coverage

- Keep valid findings when another finding, report, or hardening artifact is
  malformed, and show a warning for the skipped data.
- Remove duplicate findings and keep the strongest finding by severity,
  confidence, and supporting evidence.
- Mark coverage as partial when Codex can't verify findings, review receipts, or
  follow-up areas.
- Include incomplete coverage and deferred-review warnings in SARIF exports.

### Keep scan settings and progress visible

- Save the selected model and reasoning effort with standard and deep scans so
  scan history and progress stay consistent across reloads.
- Show the number of active and completed independent deep-scan reviews and
  when result consolidation starts.
- Adapt standard-scan discovery to the available worker capacity while keeping
  one in-scope file list and one candidate review pass.

### Support more repository and filesystem layouts

- Include nested Git repositories when capturing a working-tree snapshot.
- Preserve literal in-scope file paths and handle case-insensitive Windows
  paths.
- Expand a configured `CODEX_HOME` that starts with `~` during scan preflight.

## 0.1.14 (July 28, 2026)

### Review scan history and recurring findings

- Filter repositories, findings, and scan history with bounded result pages and
  clearer status details.
- Rerun a scan with its saved settings and compare completed scans to distinguish
  new, persisting, resolved, and not-rescanned findings.
- Group worktrees from the same repository and use stable repository and finding
  identities across views.

### Define repository security policy

- Use `$codex-security:define-security-policy` to review or update scoped
  `SECURITY.md` guidance for trust boundaries, security invariants, reportable
  findings, severity, exclusions, and accepted risk.
- Apply the closest policy file while bounding its size and rejecting symbolic
  links that leave the repository.

### Review findings before tracking them

- Select up to 25 findings from a completed scan for tracking in Linear or GitHub
  Issues.
- Return the selected findings to Codex for review and approval instead of
  creating issues directly from the findings workspace.

### Run standard scans with a simpler workflow

- Use one deterministic in-scope file list and a compact candidate ledger for
  standard repository and scoped-path scans.
- Preserve the existing manifest, findings, coverage, report, and SARIF outputs
  while reducing repeated scan stages.

## 0.1.13 (July 25, 2026)

### Review findings across more environments

- Keep real security findings when affected code is local, internal, used for
  training, or not deployed to production.
- Use deployment and exposure context to calibrate severity and confidence
  instead of automatically suppressing the finding.

## 0.1.12 (July 23, 2026)

### Run deeper scans with clearer progress

- Run deep scans that coordinate workers across an entire repository
  or a selected directory.
- Carry your model and reasoning settings into delegated scan work.
- See preflight results, scan progress, available worker capacity, and fallback
  behavior before and during a scan.

### Review and rerun previous scans

- Open current and previous scans from the security scan list.
- Reopen a saved scan in the findings workspace, or rerun it to refresh the
  results.
- See clearer completion states and more consistent finding details and scan
  history.

### Configure scans with fewer interruptions

- Start scans from the native setup flow without leaving your current task.
- Keep scan setup in the side panel, even when Codex is in full-screen mode.
- Dismiss setup when you don't need it and keep that preference for later
  scans.

### Review and remediate validated findings

- Keep validated low-severity findings in completed results.
- Review more consistent finding details across scans, reports, and exports.
- Retry remediation and carry relevant scan context into follow-up fixes.

### Export results for existing security workflows

- Export completed findings as JSON, CSV, or SARIF.
- Generate SARIF results locally for code-scanning and security-tool
  integrations.
- Preserve consistent finding details across exported formats.

## 0.1.11 (July 10, 2026)

### Produce detailed finding and hardening reports

- Generate one source-backed vulnerability report for every reportable scan
  finding, with supporting proof-of-concept files when available.
- Review a structural hardening portfolio that analyzes the complete finding
  set, engineering tradeoffs, migration options, and supporting diagrams.
- Use `report.md` as the entry point to these derived outputs under `findings/`
  and `hardening/`. Keep the full scan directory together when sharing or
  archiving results.

### Run reporting workflows directly

- Use `$codex-security:vulnerability-writeup` to turn disclosure documents,
  rough findings, PoCs, and source code into polished reports without first
  running a Codex Security scan.
- Use `$codex-security:propose-security-hardening` to develop evidence-backed
  structural or architectural options from scans, findings, incident or
  assessment documents, and source code.

### Apply repository guidance and coverage consistently

- Define threat-model context, security invariants, reportable finding
  criteria, exclusions, and severity context in root or nested `SECURITY.md`
  files. The closest applicable file takes precedence.
- Improve repository review coverage before validation while preserving
  explicitly deferred surfaces and proof gaps.
- Review deleted source files in change scans and expand the default repository
  review coverage before validation.
- Check deep-scan phase skills, delegated workers, and worker capacity before a
  deep scan starts.

## 0.1.10 (June 23, 2026)

### Improve Jira and Linear ticket intake

- Ask before importing Linear sub-issues and preserve parent-child
  relationships in the results.
- Distinguish missing connections, insufficient permissions, inaccessible
  tickets, and temporary connector failures.
- Stop instead of creating a verdict when the requested ticket content isn't
  available.
- Assign unique positive integer ranks starting at `1` within each confirmed
  or needs-review queue.

### Review code changes more reliably

- Compare an inspected commit with its actual parent and preserve the diff
  target in the findings workspace.
- Report unavailable patch state instead of reviewing a different change.
- Review more consistent triage results and finding context.

## 0.1.9 (June 18, 2026)

### Review scans in the findings workspace

- Review completed scans in a dedicated workspace that brings findings,
  coverage, severity, confidence, and scan artifacts together.
- Filter and sort findings, including sorting by highest confidence, while
  preserving your workspace state during refreshes.
- Open a finding to review source evidence, validation details, reachability,
  impact, and remediation guidance in one place.

### Run scans with less setup

- Run standard scans against Git repositories, individual folders, or
  codebases without Git history. Deep scans can also target a specific folder.
- Cancel an active scan explicitly, resume an interrupted scan without another
  setup prompt, and receive a warning before starting concurrent deep scans.
- Follow clearer setup and progress states, with more compact progress
  summaries and errors that remain visible until you address them.

### Export portable, verifiable results

- Use a consistent completed-scan format with a manifest, structured findings,
  coverage data, and a Markdown report derived from the same canonical result.
- Export findings as JSON, CSV, or SARIF for analysis, archiving, and integration
  with other security tools.
- Complete scans more reliably, including when Windows paths or scan locking
  affect filesystem access.

### Triage and track existing findings

- Triage existing findings from scanners, advisories, bug bounty reports,
  GitHub, Jira, Linear, or Codex Security results against the current codebase.
  The triage workflow returns an evidence-backed verdict and a prioritized
  action queue.
- Track selected validated findings in Linear, Jira, or GitHub issues, or create
  a private draft GitHub Security Advisory when the repository meets the
  advisory requirements.
- Review duplicate checks, source context, destination visibility, and the
  exact proposed content before approving a write. Codex reads the result back
  after creation or update to verify it.

## 0.1.7 (June 4, 2026)

### Run evidence-backed security reviews

- Scan an authorized repository or selected folder for security
  vulnerabilities.
- Run repeated discovery across an entire repository when you need more
  thorough coverage.
- Review pull requests, commits, branch differences, and local patches for
  security regressions.
- Move each candidate through threat modeling, finding discovery, validation,
  and impact analysis before generating scan reports.
- Fix one accepted finding with a focused patch, regression coverage, and
  verification of the original issue.
