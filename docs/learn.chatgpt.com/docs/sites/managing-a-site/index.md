---
source_type: 'learn'
source_area: 'learn_sites'
source_url: 'https://learn.chatgpt.com/docs/sites/managing-a-site'
source_kind: 'learn_markdown'
---

# Manage a site

Source: https://learn.chatgpt.com/docs/sites/managing-a-site

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Return to your site in ChatGPT to review its traffic, change its settings, or manage its saved versions.

## Review site analytics

Sites records traffic automatically, without an analytics SDK. The analytics view shows total unique visitors and page views, plus both metrics over time. Change the date range or granularity to compare periods.

Open **sites** in the ChatGPT desktop app, or go to [sites in ChatGPT](https://chatgpt.com/sites) on the web. Find the site, then select **More actions** > **Analytics**.

> Illustration: Interactive sites analytics dashboard showing unique visitors and page views over seven days.

Analytics is currently available for sites that aren't owned by an Enterprise
  workspace.

## Change a site URL

Site owners can manage the site's name and URL in its settings. For the current
controls and instructions, see [Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites) in the Help Center.

## Connect a custom domain

Where custom domains are available, you can connect an apex domain or subdomain
that you already own. Sites doesn't register domains for you, so you must be
able to change the domain's DNS records.

Custom domains aren't available in Enterprise workspaces at launch.

To connect a domain:

1. Open the site's settings and select **Add domain**.
2. Enter the apex domain or subdomain you want to use.
3. Copy the DNS records and values sites provides, then add them through your
   domain provider.
4. Wait a few minutes, then return to the site's settings and refresh the domain
   status.

You can also ask ChatGPT to help point the domain at your site. If browsing or
computer use is enabled, ChatGPT can help you navigate your domain provider
after you sign in.

## Configure runtime environment values

Open **sites**, then open the site's settings to add, update, or remove hosted
environment variables and secrets. Keep secret values out of prompts, attached
files, and site content.

Go to [sites in ChatGPT](https://chatgpt.com/sites), find the site, then select
**More actions** > **Settings**.

If you're working with a local source project, also follow this file guidance:

Don't store these values in `.openai/hosting.json`. Keep local `.env` and
`.env.example` files aligned with the keys needed for local development, and
don't commit secret values.

Follow the configuration instructions shown in the site's settings. For current
owner controls, see [Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites) in the Help Center.

## Take down or delete a site

To remove access without deleting a site, open its sharing settings and restrict
access to yourself or selected people. Confirm that the previous audience can no
longer open it.

To permanently delete a site:

1. Open **sites** and locate the site.
2. Select **Delete site** and follow the instructions in the prompt.
3. Enter the site slug, then select **Permanently delete**.

Deleting a site permanently removes it. You can't restore a deleted site.

## Understand projects, versions, and deployments

For an existing local project, ask sites to check compatibility and prepare it for publishing.

A site stays available in **sites** in ChatGPT, where you can reopen, refine, configure, and share it.

For a local source project, a sites project links your source to hosting managed through sites.
Sites stores that linkage and optional storage binding names in
`.openai/hosting.json`. A newly created local starter can begin without a
`project_id`; sites adds one after it provisions the hosted project.

For example, a provisioned site that uses a relational database binding and no
file storage can contain:

```json
{
  "project_id": "<project-id>",
  "d1": "DB",
  "r2": null
}
```

A site appears in your sites list even after the ChatGPT Work chat that created it ends.
You don't need a local project or manifest to start a site on the web. A site is
separate from a ChatGPT Project.

Sites publishing has two separate stages:

1. **Save a version.** ChatGPT builds a deployable version. For a local source
   project, ChatGPT associates the version with the Git commit used for the
   build. Use this stage when you want a reviewable deployment candidate.
2. **Deploy a version.** ChatGPT publishes a saved version and reports the
   production URL when deployment succeeds. Use this only when you intend for
   the selected audience to access the site.

Ask ChatGPT to list or inspect saved versions when you need to identify a
previous deployment candidate.

<SitesReferenceNavigation />
