---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security/plugin/code-changes'
source_last_modified: '2026-06-18T22:38:43Z'
source_etag: 'W/"e4568fd53b425cdbac6b7205fe9ce2ee"'
codex_cli_versions: ["0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.141.0"]
---

# Review code changes for security – Codex Security | OpenAI Developers

Source: https://developers.openai.com/codex/security/plugin/code-changes

Use a security change review when you need evidence about regressions introduced
by one Git-backed change set. The workflow reviews every changed source-like
file and directly supporting code without turning the task into a general
repository audit.

If you want to scan a full repository instead of a specific change, see [Run a
security scan](/codex/security/plugin/scans).

## Run a manual review

For uncommitted changes, send:

```
Use $codex-security:security-diff-scan to review my current uncommitted changes for security regressions.
```

For a commit or branch range, identify both ends when needed:

```
Use $codex-security:security-diff-scan to review the changes from origin/main to HEAD for security regressions. Focus on authentication, authorization, input handling, filesystem access, network requests, and secrets.
```

You can also name a pull request when its base and head revisions are available
in the local checkout.

## Confirm the change in setup

1. Confirm **Scan type** is `Changes`.
2. Confirm the checked-out **Codebase**, **Current branch**, and **Last commit**.
3. Under **Changes to review**, choose:
   - `Uncommitted changes` for the current working tree.
   - The latest commit for a single-commit review.
   - A base and head revision for a branch or pull-request range.
4. Confirm that the summary describes the change you intended to review.
5. Select **Start scan**.

The workflow doesn’t check out another branch or change the selected working
tree. If a requested revision isn’t available locally, fetch it before the
review or provide a locally available base and head.

## Act on findings

After reviewing the results, [fix and verify an accepted
finding](/codex/security/plugin/fix-findings) or [export and track
findings](/codex/security/plugin/export-findings).

## Automate reviews in CI/CD

You can run a change review from any CI/CD system that can check out the target
revisions and invoke the Codex CLI without interaction. Resolve the exact base
and head revisions, use a read-only sandbox, save the Markdown result, and
publish it through your CI/CD system.

### GitHub Actions example

The following GitHub Actions workflow is one implementation of this pattern. It
uses `openai/codex-action` to install the Codex CLI and run `codex exec` with a
read-only sandbox. It produces a Markdown review for every in-scope pull
request.

Before you add the workflow:

1. Create an `OPENAI_API_KEY` repository or organization secret.
2. Save the workflow as `.github/workflows/codex-security-review.yml`.
3. Start with advisory comments. Tune the prompt and review the results before
   making the workflow a required check.

```
name: Codex Security pull request review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  security_review:
    if: github.event.pull_request.head.repo.full_name == github.repository
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      final_message: ${{ steps.run_codex.outputs.final-message }}

    steps:
      - uses: actions/checkout@v5
        with:
          ref: refs/pull/${{ github.event.pull_request.number }}/merge
          fetch-depth: 0
          persist-credentials: false

      - name: Fetch pull request refs
        env:
          PR_BASE_REF: ${{ github.event.pull_request.base.ref }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          git fetch --no-tags origin \
            "$PR_BASE_REF" \
            "+refs/pull/$PR_NUMBER/head"

      - name: Run Codex Security review
        id: run_codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          sandbox: read-only
          output-file: codex-security-review.md
          prompt: |
            Review the pull request changes from
            ${{ github.event.pull_request.base.sha }} to
            ${{ github.event.pull_request.head.sha }} for security regressions.

            Focus on authentication, authorization, input handling, filesystem
            access, network requests, secrets, and changes to shared security
            controls. Return a concise Markdown review with affected paths and
            lines, evidence, impact, and remediation guidance. If there are no
            findings, summarize the security-sensitive surfaces reviewed and
            any coverage gaps.

      - name: Upload the review
        uses: actions/upload-artifact@v4
        with:
          name: codex-security-review
          path: codex-security-review.md

  post_review:
    needs: security_review
    if: needs.security_review.outputs.final_message != ''
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write

    steps:
      - name: Post the review
        uses: actions/github-script@v7
        env:
          CODEX_FINAL_MESSAGE: ${{ needs.security_review.outputs.final_message }}
        with:
          github-token: ${{ github.token }}
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: process.env.CODEX_FINAL_MESSAGE,
            });
```

This workflow checks out the pull request merge commit and fetches the base and
head refs so Codex can resolve the exact change. The security review job has
read-only repository permissions. A separate job receives permission to post
the final Markdown review, but it never receives the OpenAI API key.

For action inputs, privilege controls, and troubleshooting, see the [Codex
GitHub Action guide](/codex/github-action).

