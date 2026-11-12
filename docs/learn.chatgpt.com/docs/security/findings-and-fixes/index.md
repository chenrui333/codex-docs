---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/findings-and-fixes'
source_kind: 'learn_markdown'
---

# Review findings and fixes in Daybreak

Source: https://learn.chatgpt.com/docs/security/findings-and-fixes

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Daybreak allows you to quickly review proposed fixes based on findings from your scans.
Open **Overview** in Daybreak. Under **Proposed fixes**, select **Review** to
inspect a patch. To investigate an issue first, open **Findings** and select a
finding.

## What’s on the findings page?

The chart groups findings by severity and status. The table below it shows who
owns each finding, which scanner reported it, and when it was detected. You
can search the list or filter it by repository.

> Illustration: Findings for the reporting API, grouped by severity and status above a table of issues and their owners.

Select a finding to see its summary, root cause, and supporting evidence.
The detail page explains how someone could exploit the issue and shows its
reported severity and current status.

> Illustration: A sample finding about project membership checks with its attack path and status choices.

## Import findings from other scanners

Open **Settings → Integrations**. Select **Connect** to link a scanner or **Import** to use an existing connection. Check the count, repository, and destination. If the confirmation names a shared destination, confirming authorizes assessment and publication of eligible **Reportable** results there.

You can save or assess an uploaded report privately, or share eligible results. Reopen **My recent imports** for the private outcomes. Each shared finding lists the evidence from its scanners under **Observations**. See [Import scanner findings](https://learn.chatgpt.com/docs/security/scanner-imports) for the steps and limits.

> Illustration: The observations table shows Daybreak and Wiz reporting the same export handler at the same revision.

## Review a proposed fix

1. Under **Findings**, select **Fix** on a finding to generate a patch. You can also select multiple findings in the list. For example, select two findings and choose **Generate 2 fixes**. Daybreak prepares the patches in the background. Open **Fixes** to review them.
2. Open a proposed fix. Read its summary and diff under **Proposed changes**. Read the **Patch checker** result to see what Daybreak verified. For the export issue shown below, look for a test that rejects a request from another project and one that still allows an authorized export.
3. If you have questions or want a change, choose **Fix with Codex** from the menu next to **Create PR**. When the patch is ready for your team, select **Create PR** to open a draft pull request on GitHub.

> Illustration: A proposed fix for the reporting API. The diff adds a project membership check before downloading a report, and Create PR opens it for review.

Review and test the change in the pull request. After it merges, verify that
the original attack path fails on the merged revision before marking the
finding **Fixed**.
