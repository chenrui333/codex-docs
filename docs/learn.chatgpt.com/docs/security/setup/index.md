---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/setup'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Set up Daybreak Defense Factory

Source: https://learn.chatgpt.com/docs/security/setup

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Daybreak Defense Factory scans code in a connected GitHub repository and shares
the findings with your team. Start with one repository or folder. Once you’ve
reviewed the results, you can monitor new commits or set a schedule.

> Illustration: Daybreak welcome screen with options to set up PR reviews, run an agentic scan, or connect your tools.

## Open Daybreak and connect GitHub

1. Open **Plugins** on the web or in the desktop app using a ChatGPT workspace with access to Daybreak. Search for **Daybreak Defense Factory (Preview)**, then install and enable it.
2. Open **Daybreak** in the sidebar. On the welcome screen, select **Run an agentic scan**.
3. If prompted, select **Connect GitHub** and sign in with an account that can access the repository.

<CtaPillLink
  href="https://chatgpt.com/plugins/plugin_connector_1p_6317a32dbf5c81919acd66de6722daf5"
  label="Open Daybreak in the marketplace"
  target="_blank"
  rel="noopener noreferrer"
  icon="external"
  class="my-8"
/>

Cloud scans run in [Codex cloud](https://learn.chatgpt.com/docs/cloud). Each person who starts a scan
needs a personal GitHub connection. Daybreak Defense Factory doesn't support workspace connections. If the repository doesn’t appear, check
which repositories the GitHub app can access under **Configure access**. Ask your GitHub administrator to
add the repository if needed.

## Run your first scan

1. On **Configure your scan**, select a repository.
2. Choose **Full repository** to scan the default branch, or **Specific folder or files** to narrow the scan. Enter one path per line, relative to the repository root. For example, enter `src/` to scan only the application code in that folder.
3. Select **Start Scan**. When **First scan queued** appears, select **View scan**. Check the repository and paths in the scan record. You can return to it from **Scans**.

> Illustration: Configure your scan with the src/ folder selected in the sample reporting-api repository.

When the scan finishes, open a finding to see the affected code and how an
attacker could reach it. If the scan failed or stopped early, check what it
covered before interpreting the results. See [Review findings and fixes](https://learn.chatgpt.com/docs/security/findings-and-fixes).

## Choose how to scan a repository

From **New scan**, choose **Cloud**, select the repository, and check the
[cloud environment](https://learn.chatgpt.com/docs/environments/cloud-environment) that Daybreak will use.

| Scan method               | When to use it                                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Repository scan**       | Check the current code once. Use this to look for existing issues, including bugs that span several commits.     |
| **Continuous monitoring** | Check new commits on the default branch. Choose how far back to start if you also want to review recent history. |
| **Scheduled scan**        | Repeat a repository scan on a schedule. Use this for a regular review of the default branch.                     |

> Illustration: New scan panel with the Cloud option selected, the three scan methods, and the choice of a full repository or specific paths.

You can change or pause monitoring in **Continuous scanning settings**. Open
**Repositories** and select the repository to find these settings. The owner, people with edit access,
and Daybreak Defense Factory administrators can change these settings for the whole team. You can also
[edit the repository’s threat model](https://learn.chatgpt.com/docs/security/threat-model) to update the context for future scans.

You can [enable pull request reviews](https://learn.chatgpt.com/docs/security/security-review) to check
changes before they merge. [Workspace notifications](https://learn.chatgpt.com/docs/security/notifications)
let you send scan events to a service you control.

## Scan your local checkout

In the desktop app, select **New scan**, then **Local**. Choose **Codebase** to
scan the checkout or **Changes** to review uncommitted work. For a codebase
scan, you can limit the scope to one folder. Turn on **Deep scan** if you want
multiple passes and can spend more time and tokens.

Local findings appear in **Overview** on this device. A local scan can send
relevant code and prompts to the configured model provider. Local scans with
Daybreak Blue require trusted access. If you see **Apply for Daybreak**, use it
to request access.
