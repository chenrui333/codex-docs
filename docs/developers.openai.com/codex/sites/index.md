---
source_type: 'developers'
source_area: 'codex_sites'
source_url: 'https://developers.openai.com/codex/sites'
source_last_modified: '2026-06-02T19:20:44Z'
source_etag: 'W/"6d7bcc6b92dbefe6451e2958608df816"'
codex_cli_versions: ["0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0"]
codex_cli_versions_raw: ["codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0"]
---

# Sites – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/sites

Sites lets Codex create, save, deploy, and inspect websites, web apps, and
games hosted by OpenAI. Use the **Sites** plugin when you want to turn a prompt
or a compatible existing project into a hosted site without setting up a
separate deployment workflow.

Every Sites deployment URL is a production deployment. If you want to review a
build before it becomes live, ask Codex to save a version without deploying
it.

## Get started with Sites

Sites is in preview and currently available for ChatGPT Business and Enterprise
workspaces, with more plans rolling out later. For ChatGPT Enterprise
workspaces, an admin must turn it on through role-based access control (RBAC)
before members can use it. Compare support by plan in
[Feature availability](/codex/pricing#feature-availability).

1. Enable Sites for an Enterprise workspace

   If you use ChatGPT Enterprise, ask your workspace admin to open the RBAC
   controls in [ChatGPT admin settings](https://chatgpt.com/admin/settings) and
   turn on Sites for the appropriate role. ChatGPT Business workspaces can skip
   this step because Sites is enabled by default.
2. Add the Sites plugin

   If **Sites** isn’t already available, open **Plugins** in the Codex app, find
   **Sites**, and add it to Codex. Start a new thread after installing a plugin.
3. Start a Sites task

   In a thread, describe the site you want to create or publish. You can name
   the plugin explicitly with `@Sites`, especially when your task should end in
   a hosted deployment.

   ![Codex app composer with the Sites plugin and connected apps mentioned in a prompt](/images/codex/sites/prompt-input-light.jpg)
4. Review whether to save or deploy

   Ask Codex to validate the site’s build. Then tell it either to save a
   deployable version for review or to deploy the approved saved version.
5. Return to deployed sites

   Open **Sites** in the app sidebar to return to your Sites projects. You can
   also ask Codex to inspect saved versions, check deployment status, or change
   who can access a deployed site.

   ![Sites project list in the Codex app](/images/codex/sites/sites-list-light.jpg)

## Prompt Sites for common tasks

For a new website, dashboard, or internal tool, include the audience, core
experience, and required data:

```
@Sites Build a project request dashboard for my operations team. Let team
members submit requests, see who owns each one, update the status, and filter
the list. Require people to sign in with their workspace account, and keep the
request data saved between visits.
```

For an existing project, ask Sites to prepare and publish the current app:

```
@Sites Deploy this project. Check whether it is compatible with Sites, make any
required changes, and give me the deployment URL.
```

When a site needs durable application data or uploaded files, say so in the
request:

```
@Sites Add persistent player scores and avatar uploads to this game. Use
the appropriate Sites storage and deploy the updated game.
```

Browse the [Sites showcase](/showcase/sites) for deployed internal apps and
the full prompts used to create them.

## Understand projects, versions, and deployments

A Sites project links a local source project to hosting managed through Sites.
Codex stores that linkage and optional storage binding names in
`.openai/hosting.json`. A newly created local starter can begin without a
`project_id`; Sites adds one after it provisions the hosted project.

For example, a provisioned site that uses a relational database binding and no
file storage can contain:

```
{
  "project_id": "<project-id>",
  "d1": "DB",
  "r2": null
}
```

Sites publishing has two separate stages:

1. **Save a version.** Codex builds the deployable site and associates that
   version with the source Git commit used for the build. Use this stage when
   you want a reviewable deployment candidate.
2. **Deploy a version.** Codex publishes a saved version and reports the
   production URL when deployment succeeds. Use this only when you intend for
   the selected audience to access the site.

Ask Codex to list or inspect saved versions when you need to identify a
previous deployment candidate.

## Choose a supported site shape

Sites hosts projects that build Cloudflare Worker-compatible output as ES
modules. For new projects, the Sites workflow can start with its recommended
site starter. For an existing site, ask Codex to confirm that the project’s
build can produce compatible deployment artifacts before you request a
deployment.

Tell Codex about the product behavior you need so it can select the appropriate
site shape:

| Site need | What to ask Sites for |
| --- | --- |
| Content-led website or landing page | A site with no persistent application state unless the experience requires it |
| Saved records, user progress, or game scores | D1, a relational database for durable structured data |
| Images, documents, audio, video, or other uploads | R2, object storage for files |
| Uploaded files with searchable metadata | D1 for metadata and R2 for file contents |
| Internal site that needs the current workspace user’s identity | Workspace-authenticated user identity |
| Public sign-in or an external identity provider | An authentication-enabled Sites project |

Don’t request durable storage for temporary presentation state, such as a
theme choice or a dismissed banner. Do request it for product data that people
expect the hosted site to remember.

## Control access and secrets

Set the audience before you share a deployed URL. For a new site, keep access
limited to the owner and workspace admins until you have reviewed the content,
data handling, and expected audience.

You can ask Sites to apply one of these access modes:

| Access mode | Who can access the site |
| --- | --- |
| Owner and admins (`admins_only`) | The site owner and workspace admins |
| Workspace (`workspace_all`) | All active users in the workspace |
| Custom (`custom`) | Specific active users or workspace groups that you choose; Sites continues to allow the owner |

For example:

```
@Sites Change this deployed site's access to everyone in my workspace after
showing me the current site and confirming the deployment URL.
```

### Configure runtime environment values

Open **Sites** in the app sidebar and select a project to add, update, or remove
hosted environment variables and secrets in the Sites panel. Don’t store these
values in `.openai/hosting.json`. Keep local `.env` and `.env.example` files
aligned with the keys needed for local development, and don’t commit secret
values.

When you add, update, or remove hosted environment values, ask Codex to
redeploy the approved saved version so the next deployment uses the updated
configuration.

## Review before you share

Before you deploy or widen access:

- Review the source changes and any database migrations in the Codex
  [review pane](/codex/app/review).
- Confirm that the build succeeded and that the selected saved version is the
  version you intend to publish.
- Check that only the intended audience can access the site.
- Confirm that you configured runtime secret values through Sites and didn’t
  commit them in source files.
- After deployment, ask Codex to confirm deployment status and the production
  URL before you share it.

## Related documentation

- [Plugins](/codex/plugins) explains how to install and invoke Codex plugins.
- [Codex app](/codex/app) introduces app navigation and project threads.
- [Review and ship changes](/codex/app/review) explains how to inspect source
  changes before publishing them.

