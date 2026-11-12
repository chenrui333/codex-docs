---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/scanner-imports'
source_kind: 'learn_markdown'
---

# Import scanner findings into Daybreak

Source: https://learn.chatgpt.com/docs/security/scanner-imports

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

You can import findings into Daybreak Defense Factory by connecting a scanner or
[uploading a report](#upload-a-scanner-report). Daybreak can assess those findings
against your code and share eligible results with your team.

Open **Settings → Integrations**, or select **Import** from **Findings**. The
available options depend on your workspace. Assessment requires access to the
scanner evidence and the repository commit. Sharing also requires an environment
where you can publish findings.

> Illustration: Daybreak Settings open to Integrations. Snyk and Wiz offer Connect, and Endor Labs offers Import.

## Import from a connected scanner

1. Select **Connect** beside the scanner, **Reconnect** if your connection expired, or **Import** to use an existing connection.
2. Choose the source and the findings to import. If **Import all for a repository** is available for Snyk or Endor, choose a connected GitHub repository to include all matching projects in the selected organization or namespace. Otherwise, choose a project and select findings. In Wiz, you can also use a supported saved view.
3. Review the finding count, repository, and commit for assessment. The count on **Import 12 findings**, for example, includes all 12 selected scanner findings, even those that can't be assessed. It can differ from the number of shared findings.
4. Check what the confirmation will do. If it names a shared workspace and destination, confirming authorizes assessment and publication of eligible **Reportable** results there. People with access to that destination can read the published assessment and source evidence. Daybreak preselects the only eligible environment. If several environments are eligible, choose one before confirming. If the review offers private assessment or saving only, the results stay private.
5. Confirm when the count and destination are correct. If the review expires or the source changes, review it again. Once the import starts, you can close Settings and follow it in **My recent imports**.

### Choose a source

| Scanner          | Connection                                                                                                                               | What you can select                                                                                                                                                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wiz              | Sign in to your Wiz account and approve the connection.                                                                                  | Package vulnerabilities in a project, or a saved vulnerability findings view filtered to one container repository and container images. **Filter this page** searches the current page. You can select findings across pages. |
| Snyk Open Source | Use a Snyk US-01 API token with REST read access to the organization, projects, and issues.                                              | Choose the organization that monitors your repository. Separate manifests can appear as separate monitored projects. If you lack REST access, use an Issues Detail CSV instead.                                               |
| Endor Labs       | Enter your US namespace, API key, and API secret. Use an expiring read-only key scoped to the namespace, with child namespaces disabled. | Choose findings from a project’s main context, or use repository import when available.                                                                                                                                       |

Daybreak uses the scanner’s reported revision when it can verify it. If Snyk omits the commit, the review can offer a fallback for that repository. For a Wiz finding that needs a checkout, choose the GitHub repository and enter the full 40-character commit SHA your connection can read. This is the code Daybreak will assess. It can differ from the code used to build the container image. The import keeps the scanner’s original evidence.

### Fit a connected import within the limits

| Scanner          | Limit for one source read                                                                                                                        | If you reach it                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Wiz              | 5,000 matching occurrences per filtered project or saved view, up to 100 pages of 50, within 32 MiB.                                             | Narrow the severity, fix availability, or CVE filters before previewing again.                                                   |
| Snyk Open Source | 10,000 package issues per monitored project, up to 100 pages of 100. The encoded original pages and converted report together must fit in 8 MiB. | Choose a smaller project or upload a filtered export. Selecting fewer issues after preview still requires the full project read. |
| Endor Labs       | 5,000 findings per project preview, in pages of up to 100, within a 32 MiB read budget.                                                          | Choose a smaller project or upload a filtered export. If the full evidence exceeds the limit, select fewer individual findings.  |

Each captured report and its evidence must total no more than 32 MiB. A repository import must finish reading all matching projects before it can confirm the repository count.

An individual selection accepts up to 10,000 scanner occurrences. A review can assess up to 10,000 rows with verified targets. The list of rows and their assigned revisions must also fit in 512 KiB, so you may need to split a smaller selection. For Wiz, the checkout limit counts **findings assigned a checkout**, even when several use the same commit. Depending on the picker available in your workspace, you can assign up to 16 or 100 findings per review. Split your selection at the limit shown. A confirmation can authorize up to 100 destination environments, one per repository connection.

## Upload a scanner report

Select **Upload file** beside the scanner. Settings detects the format and shows which exports your workspace accepts.

| Scanner          | File for Settings                                                                                                                                                                                                                                                                                                                 |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wiz              | A complete package vulnerability report in Detailed JSON, or one native finding per line in JSON Lines. In Wiz **Vulnerability Findings**, filter the report, select **Save as → Report**, and choose **Repository Branch**, **JSON**, and **Detailed** for a repository export. Enter the exporting Wiz tenant ID when prompted. |
| Snyk Open Source | An Issues Detail CSV from one organization. Check the organization in the preview.                                                                                                                                                                                                                                                |
| Endor Labs       | Native Finding JSON from `endorctl` for the namespace you want to import. Keep the original finding UUIDs and complete any paginated export.                                                                                                                                                                                      |

The uploaded file and its expanded contents must each fit in **32 MiB**, including for gzip uploads. For Snyk CSV and Wiz JSON Lines, Settings recognizes up to **10,000 data rows** per file. Split larger files before uploading. A single JSON finding over 1 MiB can be rejected. For Snyk CSV, keep the header within 32,768 characters, each field within 131,072 characters, and each logical row within 1,048,576 characters.

### Choose whether to assess or share

Saving the file uploads it for review. Check the verified repositories and commits, the rows that still need a checkout, and any rejected inputs before you start the import.

- To keep the evidence for later, choose **Save without assessment** when the review offers assessment, or **Save privately** when it doesn’t.
- To assess eligible rows and keep all results private, choose **Import and assess privately**. You can choose targets later for rows that still need one. If more than 10,000 rows have targets, split the report or save it without assessment.
- To share eligible results, select **Also publish Reportable findings**, which starts unchecked. Review the workspace and destinations. If a repository has several eligible environments, choose one or select **Keep private**. Confirm with **Import and publish reportable findings**.

Automatic sharing requires a Reportable assessment, a scanner-reported severity, and a destination you authorized. The original report stays private. In **Activity**, **Stop automatic sharing** stops future publication from that import.

## Import from the CLI

You can import a saved scanner export with `codex-security publish findings`. Preview locally with `--to local --dry-run`. To preview a cloud import, use `--to cloud --dry-run --format json` with a connected repository. A cloud preview contacts Daybreak and requires a file-backed ChatGPT login.

Inspect the preview before removing `--dry-run` and confirming. A `privateImport` entry saves the findings to your private inbox. Entries in `requests` publish to the repository environments listed there. Check the receipt for exclusions, failures, and unprocessed rows. See the [CLI reference](https://learn.chatgpt.com/docs/security/cli/reference#codex-security-publish-findings) for local and cloud import examples and the [scanner import guides](https://github.com/openai/codex-security/blob/main/docs/scanner-imports/README.md) for CLI formats and commands.

## Reopen an import

Open **My recent imports** from **Settings → Integrations** or **Findings → Import** in the workspace where you made the import. You can also reopen a private import from its row in **Scans**. The summary accounts for each row, including rejected inputs and their reasons. Open an accepted row to see its scanner ID and saved evidence, along with any assessment or published finding. Disconnecting the scanner stops new reads through that connection. You can still reopen your saved imports.

Choose **Assess** on a private finding to check its evidence against the selected commit. Read the reason beside **Reportable**, **Deferred**, **Suppressed**, or **Not applicable**. For example, a commit Daybreak can’t read can leave a finding Deferred. To share a privately assessed Reportable result, select an authorized destination environment and **Publish to shared findings**. If the scanner didn’t supply a recognized severity, choose one before publishing.

## Recognize repeat imports

If confirmation was interrupted, reopen the original receipt or select **Check original import** when offered. Retrying the original request recovers that import with the choices you already made.

When you start a new import, Daybreak compares each row with the evidence it already has.

- With the same Endor connection and project, or the same Wiz connection and project or saved repository view, unchanged scanner IDs and evidence can point to the existing private observation. A new connected Snyk import captures a new private observation for each issue. Requesting assessment again can assess even an unchanged row.
- Uploading the identical Snyk CSV for the same organization reuses the accepted rows. For example, uploading the same five issues again can show five unchanged and zero new. Changed evidence creates a new version. An earlier assessment still refers to the evidence and commit it reviewed.
- If one report repeats a scanner finding ID, Daybreak flags both occurrences and can import the other valid rows. Keep one correct record and import the corrected report. Separate IDs can describe different affected packages or repositories, even when they cite the same CVE.

After publication, Daybreak checks for an existing shared finding in the same repository and environment. A match adds the published evidence to that issue. A distinct issue can create a new finding. Two scanner observations can therefore appear on one shared finding. Retrying the same publication doesn’t add the evidence twice. Open **Observations** on the shared finding to inspect its sources. See [Review findings and fixes](https://learn.chatgpt.com/docs/security/findings-and-fixes).
