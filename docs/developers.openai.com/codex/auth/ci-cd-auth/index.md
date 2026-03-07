# Maintain Codex account auth in CI/CD (advanced)

Source: https://developers.openai.com/codex/auth/ci-cd-auth

This guide shows how to keep ChatGPT-managed Codex auth working on a trusted
CI/CD runner without calling the OAuth token endpoint yourself.

The right way to authenticate automation is with an API key. Use this guide
only if you specifically need to run the workflow as your Codex account.

The pattern is:

1. Create `auth.json` once on a trusted machine with `codex login`.
2. Put that file on the runner.
3. Run Codex normally.
4. Let Codex refresh the session when it becomes stale.
5. Keep the refreshed `auth.json` for the next run.

This is an advanced workflow for enterprise and other trusted private
automation. API keys are still the recommended option for most CI/CD jobs.

Treat `~/.codex/auth.json` like a password: it contains access tokens. Don’t
commit it, paste it into tickets, or share it in chat. Do not use this
workflow for public or open-source repositories.

## Why this works

Codex already knows how to refresh a ChatGPT-managed session.

As of the current open-source client:

- Codex loads the local auth cache from `auth.json`
- if `last_refresh` is older than about 8 days, Codex refreshes the token
  bundle before the run continues
- after a successful refresh, Codex writes the new tokens and a new
  `last_refresh` back to `auth.json`
- if a request gets a `401`, Codex also has a built-in refresh-and-retry path

That means the supported CI/CD strategy is not “call the refresh API yourself.”
It is “run Codex and persist the updated `auth.json`.”

## When to use this

Use this guide only when all of the following are true:

- you need ChatGPT-managed Codex auth rather than an API key
- `codex login` cannot run on the remote runner
- the runner is trusted private infrastructure
- you can preserve the refreshed `auth.json` between runs
- only one machine or serialized job stream will use a given `auth.json` copy

This guide applies to Codex-managed ChatGPT auth (`auth_mode: "chatgpt"`).

It does not apply to:

- API key auth
- external-token host integrations (`auth_mode: "chatgptAuthTokens"`)
- generic OAuth clients outside Codex

If your credentials are stored in the OS keyring, switch to file-backed storage
first. See [Credential storage](/codex/auth#credential-storage).

## Seed `auth.json` once

On a trusted machine where browser login is possible:

1. Configure Codex to store credentials in a file:

```
cli_auth_credentials_store = "file"
```

2. Run:

```
codex login
```

3. Verify the file looks like managed ChatGPT auth:

```
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"

jq '{
  auth_mode,
  has_tokens: (.tokens != null),
  has_refresh_token: ((.tokens.refresh_token // "") != ""),
  last_refresh
}' "$AUTH_FILE"
```

Continue only if:

- `auth_mode` is `"chatgpt"`
- `has_refresh_token` is `true`

Then place the contents of `auth.json` into your CI/CD secret manager or copy
it to a trusted persistent runner.

## Recommended pattern: GitHub Actions on a self-hosted runner

The simplest fully automated setup is a self-hosted GitHub Actions runner with a
persistent `CODEX_HOME`.

Why this pattern works well:

- the runner can keep `auth.json` on disk between jobs
- Codex can refresh the file in place
- later jobs automatically pick up the refreshed tokens
- you only need the original secret for bootstrap or reseeding

The critical detail is to seed `auth.json` only if it is missing. If you
rewrite the file from the original secret on every run, you throw away the
refreshed tokens that Codex just wrote.

Example scheduled workflow:

```
name: Keep Codex auth fresh

on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:

jobs:
  keep-codex-auth-fresh:
    runs-on: self-hosted
    steps:
      - name: Bootstrap auth.json if needed
        shell: bash
        env:
          CODEX_AUTH_JSON: ${{ secrets.CODEX_AUTH_JSON }}
        run: |
          export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
          mkdir -p "$CODEX_HOME"
          chmod 700 "$CODEX_HOME"

          if [ ! -f "$CODEX_HOME/auth.json" ]; then
            printf '%s' "$CODEX_AUTH_JSON" > "$CODEX_HOME/auth.json"
            chmod 600 "$CODEX_HOME/auth.json"
          fi

      - name: Run Codex
        shell: bash
        run: |
          codex exec --json "Reply with the single word OK." >/dev/null
```

What this does:

- the first run seeds `auth.json`
- later runs reuse the same file
- once the cached session is old enough, Codex refreshes it during the normal
  `codex exec` step
- the refreshed file remains on disk for the next workflow run

A weekly schedule is usually enough because Codex treats the session as stale
after roughly 8 days in the current open-source client.

## Ephemeral runners: restore, run Codex, persist the updated file

If you use GitHub-hosted runners, GitLab shared runners, or any other ephemeral
environment, the runner filesystem disappears after each job. In that setup,
you need a round-trip:

1. restore the current `auth.json` from secure storage
2. run Codex
3. write the updated `auth.json` back to secure storage

Generic GitHub Actions shape:

```
name: Run Codex with managed auth

on:
  workflow_dispatch:

jobs:
  codex-job:
    runs-on: ubuntu-latest
    steps:
      - name: Restore auth.json
        shell: bash
        run: |
          export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
          mkdir -p "$CODEX_HOME"
          chmod 700 "$CODEX_HOME"

          # Replace this with your secret manager or secure storage command.
          my-secret-cli read codex-auth-json > "$CODEX_HOME/auth.json"
          chmod 600 "$CODEX_HOME/auth.json"

      - name: Run Codex
        shell: bash
        run: |
          codex exec --json "summarize the failing tests"

      - name: Persist refreshed auth.json
        if: always()
        shell: bash
        run: |
          # Replace this with your secret manager or secure storage command.
          my-secret-cli write codex-auth-json < "$CODEX_HOME/auth.json"
```

The key requirement is that the write-back step stores the refreshed file that
Codex produced during the run, not the original seed.

## You do not need a separate refresh command

Any normal Codex run can refresh the session.

That means you have two good options:

- let your existing CI/CD Codex job refresh the file naturally
- add a lightweight scheduled maintenance job, like the GitHub Actions example
  above, if your real jobs do not run often enough

The first Codex run after the session becomes stale is the one that refreshes
`auth.json`.

## Operational rules that matter

- Use one `auth.json` per runner or per serialized workflow stream.
- Do not share the same file across concurrent jobs or multiple machines.
- Do not overwrite a persistent runner’s refreshed file from the original seed
  on every run.
- Do not store `auth.json` in the repository, logs, or public artifact storage.
- Reseed from a trusted machine if built-in refresh stops working.

## What to do when refresh stops working

This flow reduces manual work, but it does not guarantee the same session lasts
forever.

Reseed the runner with a fresh `auth.json` if:

- Codex starts returning `401` and the runner can no longer refresh
- the refresh token was revoked or expired
- another machine or concurrent job rotated the token first
- your secure-storage round trip failed and an old file was restored

To reseed:

1. Run `codex login` on a trusted machine.
2. Replace the stored CI/CD copy of `auth.json`.
3. Let the next runner job continue using Codex’s built-in refresh flow.

## Verify that the runner is maintaining the session

Check that the runner still has managed auth tokens and that `last_refresh`
exists:

```
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"

jq '{
  auth_mode,
  last_refresh,
  has_access_token: ((.tokens.access_token // "") != ""),
  has_id_token: ((.tokens.id_token // "") != ""),
  has_refresh_token: ((.tokens.refresh_token // "") != "")
}' "$AUTH_FILE"
```

If your runner is persistent, you should see the same file continue to exist
between runs. If your runner is ephemeral, confirm that your write-back step is
storing the updated file from the last job.

## Source references

If you want to verify this behavior in the open-source client:

- [`codex-rs/core/src/auth.rs`](https://github.com/openai/codex/blob/main/codex-rs/core/src/auth.rs)
  covers stale-token detection, automatic refresh, refresh-on-401 recovery, and
  persistence of refreshed tokens
- [`codex-rs/core/src/auth/storage.rs`](https://github.com/openai/codex/blob/main/codex-rs/core/src/auth/storage.rs)
  covers file-backed `auth.json` storage

