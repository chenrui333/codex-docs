---
source_type: 'learn'
source_area: 'learn_sites'
source_url: 'https://learn.chatgpt.com/docs/sites'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Sites

Source: https://learn.chatgpt.com/docs/sites

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Sites is in public beta and is available with ChatGPT Plus, Pro, Business,
  Enterprise and Edu plans. Plan-specific usage limits apply across all Sites
  during the beta. ChatGPT shows the current limits and notifies you as you
  approach one. Reaching a limit can prevent you from creating a Site, adding
  storage, or keeping a high-usage Site public, but you can still edit and
  manage existing Sites.

Sites lets ChatGPT create, host, refine, and share websites, web apps, and games.
Use Sites when you want to turn a prompt or compatible existing project into a
hosted experience without setting up a separate deployment workflow.

<ContentModeSwitch group="codex-surface" id="app">

Open **Sites** in the ChatGPT desktop app. You can start a site from a prompt or
from a compatible local project, then return to the Sites view to manage it.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

Use Sites in ChatGPT on the web to create and manage hosted sites. Select
**More** > **Sites**, or go directly to
[chatgpt.com/sites](https://chatgpt.com/sites), to find Sites you've created.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

Sites doesn't have a standalone Codex CLI management view. Use ChatGPT web or
the desktop app to create, save, deploy, and manage a Sites project. You can
still use Codex CLI to edit and test a local project before publishing it.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

Sites doesn't have a standalone IDE extension management view. Use ChatGPT web
or the desktop app for Sites operations, and use the IDE extension to edit and
test the local source project.

</ContentModeSwitch>

Every Sites deployment URL is a production deployment. If you want to review a
  build before it becomes live, ask ChatGPT to save a version without deploying
  it.

## Get started with Sites

In ChatGPT, include the word "website" in your prompt or mention `@Sites` to
start the Sites workflow explicitly.

<WorkflowSteps variant="headings">

1. Describe the Site

   Describe the audience, purpose, required behavior, and information the Site
   should use.

2. Review the Site

   Review the generated content and behavior. Check that the Site uses the
   intended information and handles data as expected.

3. Refine the Site

   Describe the changes you want. Add relevant files or visual context when
   they will help ChatGPT make the change.

4. Manage and share the Site

   Return to **Sites** to reopen or refine the Site. When it's ready, choose who
   can visit it and share the resulting link.

</WorkflowSteps>

<ContentModeSwitch group="codex-surface" id="web">

In the preview, select **Edit**. Under **Describe website edits**, describe the
changes you want. Use **Screenshot** or **Add files and more** when additional
context would help.

</ContentModeSwitch>

## Prompt Sites for common tasks

For a new website, dashboard, or internal tool, include the audience, core
experience, and required information:

```text
Build a project request dashboard for my operations team. Let team members
submit requests, see who owns each one, update the status, and filter the list.
Require people to sign in with their workspace account, and keep the request
data saved between visits.
```

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

For an existing project, ask Sites to prepare and publish the current app:

```text
Deploy this project with Sites. Check whether it is compatible, make any
required changes, and give me the deployment URL.
```

</ContentModeSwitch>

When a site needs durable application data or uploaded files, say so in the
request:

```text
Add player scores and avatar uploads to this game. Keep the scores and uploaded
avatars between visits.
```

Browse the [Sites showcase](https://developers.openai.com/showcase) for deployed internal apps and the full
  prompts used to create them.

## Review Site analytics

Sites records traffic automatically, so you can see how people use a deployed
Site without adding an analytics SDK. The analytics view shows total unique
visitors and page views, plus both metrics over time. Change the date range or
granularity to inspect a different period.

<ContentModeSwitch group="codex-surface" id="app">

Open **Sites**, find the Site, then select **More actions** > **Analytics**.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

Go to [chatgpt.com/sites](https://chatgpt.com/sites), find the Site, then select
**More actions** > **Analytics**.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="cli,ide">

Sites doesn't have a standalone analytics view in the CLI or IDE extension. Open
the Site in ChatGPT on the web or in the desktop app to review its analytics.

</ContentModeSwitch>

<Illustration description="Interactive Sites analytics dashboard showing unique visitors and page views over seven days.">
  <SitesAnalyticsIllustration />
</Illustration>

Analytics is currently available for Sites that aren't owned by an Enterprise
  workspace.

## Add Sign in with ChatGPT

Public Sites can remain open to everyone while offering optional Sign in with
ChatGPT for identity-aware features, such as saved progress, personalized views,
or records that belong to a specific person. Workspace-restricted Sites already
use ChatGPT identity to enforce their sharing settings.

Ask Sites to add the sign-in experience:

```text
Add Sign in with ChatGPT to this public Site. Keep the Site available to signed-out visitors. Show a Sign in with ChatGPT action when someone is signed out. After they sign in, greet them with their full name when available, or their email address otherwise. Add a Sign out action, and keep authorization decisions in server-side code.
```

<ToggleSection title="How it works">

Sites handles the sign-in and sign-out flows through platform-provided paths,
then returns the visitor to your Site:

```html
<a href="/signin-with-chatgpt">Sign in with ChatGPT</a>
<a href="/signout-with-chatgpt">Sign out</a>
```

After a visitor signs in, Sites forwards their identity to the server through
these request headers:

- `oai-authenticated-user-email` contains the authenticated email address.
- `oai-authenticated-user-full-name` may contain a non-empty profile name. Treat
  it as optional and fall back to the email address.

Keep authorization decisions in server-side code, and don't depend on
name-split headers.

</ToggleSection>

## Understand projects, versions, and deployments

A Site is a persistent hosted output that you can reopen, refine, configure,
and share from **Sites** in ChatGPT.

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

A Sites project links a local source project to hosting managed through Sites.
Sites stores that linkage and optional storage binding names in
`.openai/hosting.json`. A newly created local starter can begin without a
`project_id`; Sites adds one after it provisions the hosted project.

For example, a provisioned site that uses a relational database binding and no
file storage can contain:

```json
{
  "project_id": "<project-id>",
  "d1": "DB",
  "r2": null
}
```

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

A Site appears in your Sites list even after the ChatGPT Work chat that created it ends.
You don't need a local project or manifest to start a Site on the web. A Site is
separate from a ChatGPT Project.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

Sites publishing has two separate stages:

1. **Save a version.** ChatGPT builds a deployable version. For a local source
   project, ChatGPT associates the version with the Git commit used for the
   build. Use this stage when you want a reviewable deployment candidate.
2. **Deploy a version.** ChatGPT publishes a saved version and reports the
   production URL when deployment succeeds. Use this only when you intend for
   the selected audience to access the site.

Ask ChatGPT to list or inspect saved versions when you need to identify a
previous deployment candidate.

</ContentModeSwitch>

## Choose a supported site shape

For new projects, the Sites workflow can start with its recommended Site
starter. For an existing project, ask ChatGPT to confirm that the project can
produce compatible deployment artifacts before you request a deployment.

Tell ChatGPT about the product behavior you need so it can select the appropriate
site shape:

| Site need                                                      | What to ask Sites for                                                         |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Content-led website or landing page                            | A Site with no persistent application state unless the experience requires it |
| Saved records, user progress, or game scores                   | D1, a relational database for durable structured data                         |
| Images, documents, audio, video, or other uploads              | R2, object storage for files                                                  |
| Uploaded files with searchable metadata                        | D1 for metadata and R2 for file contents                                      |
| Internal site that needs the current workspace user's identity | Workspace-authenticated user identity                                         |
| Public sign-in or an external identity provider                | An authentication-enabled Site                                                |

Don't request durable storage for temporary presentation state, such as a
theme choice or a dismissed banner. Do request it for product data that people
expect the hosted site to remember.

## Control access and secrets

A new Site is limited to its owner and workspace admins until you change its
access. Keep access limited while you review the content, data handling, and
expected audience.

Depending on your account and workspace settings, sharing options can include:

- **Owner and workspace admins**
- **Selected active users or groups**, where supported
- **Anyone in the workspace**, where supported
- **Anyone on the internet**, only when public publishing is enabled

Sharing lets people visit the Site; it doesn't let them edit it. In Enterprise
workspaces, public publishing is off by default and must be enabled by an admin.

For limited sharing, invited visitors must sign in with the account that
received access. A public Site is available without ChatGPT workspace access. A
Site's audience setting and any sign-in feature built into the Site are separate
controls.

For example:

```text
Change this Site's access to everyone in my workspace after showing me the
current Site and confirming its URL.
```

### Configure runtime environment values

Open **Sites**, then open the Site's settings to add, update, or remove hosted
environment variables and secrets. Keep secret values out of prompts, attached
files, and Site content.

<ContentModeSwitch group="codex-surface" id="web">

Go to [chatgpt.com/sites](https://chatgpt.com/sites), find the Site, then select
**More actions** > **Settings**.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

Don't store these values in `.openai/hosting.json`. Keep local `.env` and
`.env.example` files aligned with the keys needed for local development, and
don't commit secret values.

When you add, update, or remove hosted environment values, ask ChatGPT to
redeploy the approved saved version so the next deployment uses the updated
configuration.

</ContentModeSwitch>

## Connect a custom domain

Where custom domains are available, you can connect an apex domain or subdomain
that you already own. Sites doesn't register domains for you, so you must be
able to change the domain's DNS records. Custom domains aren't available in
Enterprise workspaces at launch.

To connect a domain:

1. Open the Site's settings and select **Add domain**.
2. Enter the apex domain or subdomain you want to use.
3. Copy the DNS records and values Sites provides, then add them through your
   domain provider.
4. Wait a few minutes, then return to the Site's settings and refresh the domain
   status.

You can also ask ChatGPT to help point the domain at your Site. If browsing or
computer use is enabled, ChatGPT can help you navigate your domain provider
after you sign in.

## Review before you share

Before you share a Site:

- Review its content, generated text and images, links, uploaded files, forms,
  and interactive behavior.
- Confirm that it doesn't expose confidential or sensitive information, secret
  values, or third-party content you don't have the right to share.
- Test the Site from the intended visitor experience, including its access and
  sign-in behavior.
- Review features that collect personal information or other visitor content.
  Decide whether the Site should collect, share, or publish that information.
- If the Site uses Sign in with ChatGPT, explain what visitor information it
  receives and how it uses that information.
- If the Site collects or processes personal data, comply with
  [applicable privacy and data-protection laws](https://help.openai.com/en/articles/20001340).
- Choose the narrowest sharing option that fits the intended audience.
- Open the shared Site and confirm that the intended audience can visit it.

<ContentModeSwitch group="codex-surface" id="app">

For a Site built from a local project, also review the source changes and any
database migrations in the Codex [review pane](https://learn.chatgpt.com/docs/code-review?surface=app).

</ContentModeSwitch>

## Take down or delete a Site

To remove access without deleting a Site, open its sharing settings and restrict
access to yourself or selected people. Confirm that the previous audience can no
longer open it.

To permanently delete a Site:

1. Open **Sites** and locate the Site.
2. Select **Delete site** and follow the instructions in the prompt.
3. Enter the Site slug, then select **Permanently delete**.

Deleting a Site permanently removes it. You can't restore a deleted Site.

## Understand limits and unsupported uses

Sites hosts web experiences that run in the supported Sites runtime. Some
frameworks, private networks, databases, background services, and hosting
patterns aren't supported.

Each Site has these storage limits:

| Resource            | Limit                  |
| ------------------- | ---------------------- |
| D1 database storage | 10 GB                  |
| R2 object storage   | No fixed storage limit |

Sites doesn't support data residency or inference residency at launch. This
includes deployed Sites, Site code, D1 and R2 data and file storage, generated
artifacts, and logs.

Don't use Sites to process Protected Health Information or payment-card data;
target children under 13 or the applicable age of digital consent; enable
financial transactions; distribute malware; enable phishing; impersonate people
or organizations; or otherwise violate OpenAI policies. See
[Creating and managing ChatGPT Sites](https://help.openai.com/en/articles/20001339)
for the current limits and policy links.

## Related documentation

<ContentModeSwitch group="codex-surface" id="app">

- [ChatGPT desktop app](https://learn.chatgpt.com/docs/app) introduces app navigation, projects, and chats.
- [Review and ship changes](https://learn.chatgpt.com/docs/code-review?surface=app) explains how to inspect source
  changes before publishing them.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="cli,ide">

- [Projects and chats](https://learn.chatgpt.com/docs/projects) explains how folder and workspace
  context carries across chats.
- [Review and ship changes](https://learn.chatgpt.com/docs/code-review) explains the review workflow for
  each Codex client.
- [Sandboxing](https://learn.chatgpt.com/docs/sandboxing) explains the local execution boundary.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

- [Open Sites in ChatGPT](https://chatgpt.com/sites) to return to Sites you've
  created.
- [Projects and chats](https://learn.chatgpt.com/docs/projects?surface=web) explains how to keep
  related chats and source files together.
- [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer?surface=web) explains how to review
  generated files in ChatGPT web.

</ContentModeSwitch>
