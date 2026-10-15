---
source_type: 'learn'
source_area: 'learn_sites'
source_url: 'https://learn.chatgpt.com/docs/sites/data-and-connections'
source_kind: 'learn_markdown'
---

# Data and connections

Source: https://learn.chatgpt.com/docs/sites/data-and-connections

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Your site might need to save requests, remember progress, or show information from connected apps. Tell ChatGPT what to save, where the information comes from, and who should have access.

<a id="choose-a-supported-site-shape"></a>

## Choose storage and sign-in features

For new projects, the sites workflow can start with its recommended site
starter. For an existing project, ask ChatGPT to confirm that the project can
produce compatible deployment artifacts before you request a deployment.

Describe what the site should do so ChatGPT can choose the required storage and identity features:

| Site need                                                      | What to ask sites for                                                         |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Content-led website or landing page                            | A site with no persistent application state unless the experience requires it |
| Saved records, user progress, or game scores                   | D1, a relational database for durable structured data                         |
| Images, documents, audio, video, or other uploads              | R2, object storage for files                                                  |
| Uploaded files with searchable metadata                        | D1 for metadata and R2 for file contents                                      |
| Internal site that needs the current workspace user's identity | Workspace-authenticated user identity                                         |
| Public sign-in or an external identity provider                | An authentication-enabled site                                                |

Don't request durable storage for temporary presentation state, such as a
theme choice or a dismissed banner. Do request it for product data that people
expect the hosted site to remember.

## Add Sign in with ChatGPT

Public sites can remain open to everyone while offering optional Sign in with
ChatGPT for identity-aware features, such as saved progress, personalized views,
or records that belong to a specific person. Workspace-restricted sites already
use ChatGPT identity to enforce their sharing settings.

Ask sites to add the sign-in experience:

**Prompt:**

```text
Add Sign in with ChatGPT to this public site. Keep the site available to signed-out visitors. Show a Sign in with ChatGPT action when someone is signed out. After they sign in, greet them with their full name when available, or their email address otherwise. Add a Sign out action, and keep authorization decisions in server-side code.
```

<ToggleSection title="How it works">

Sites handles the sign-in and sign-out flows through platform-provided paths,
then returns the visitor to your site:

```html
<a href="/signin-with-chatgpt">Sign in with ChatGPT</a>
<a href="/signout-with-chatgpt">Sign out</a>
```

After a visitor signs in, sites forwards their identity to the server through
these request headers:

- `oai-authenticated-user-email` contains the authenticated email address.
- `oai-authenticated-user-full-name` may contain a non-empty profile name. Treat
  it as optional and fall back to the email address.

Keep authorization decisions in server-side code, and don't depend on
name-split headers.

</ToggleSection>

<a id="load-visitor-data-via-plugins"></a>

## Bring user data to your site with plugins

Use plugins in sites to build a site that loads
data from each site viewer's own connected apps. For example, an issue dashboard
can show your assigned issues to you and your teammate's assigned issues to
them. Each visitor signs in with ChatGPT and chooses which connected accounts
and access to allow.

Plugin use must be enabled in the workspace, and the site must be private to
  that workspace. Visitors need to belong to the workspace and use their
  existing app permissions. Admins can review individual plugin permissions and
  tenant restrictions in [Enable plugin use in
  sites](https://learn.chatgpt.com/docs/enterprise/sites#enable-plugin-use-in-sites).

### Build a site with connected data

<WorkflowSteps>

1. Ask ChatGPT Work or Codex to build a site. Name the plugin connector and what it should do, or ask which plugins are available.
2. Try the preview with real data. The agent uses your available connections
   while building and previewing the site.
3. Ask the agent to publish the site for your workspace and
   share its link with teammates.

</WorkflowSteps>

For example:

**Prompt:**

```text
Build a site using my connected issue tracker that shows issues assigned to me, grouped by priority. Add project filters, links to the original issues, and a Refresh button.
```

You can also build a document finder that links to original documents or a
project overview that combines tickets and messages.

### Data loading

On page load, sites reads connected data using the visitor's connection and permissions. Sites manages caching and reloading; ask ChatGPT Work or Codex to add a manual refresh action if needed.

By default, sites uses a **Load more** action to fetch another page when the connector returns a cursor.

<ToggleSection title="Technical reference: Plugin discovery">

Sites uses `getContext()` to find a plugin's actions. It returns cached tool names, descriptions, and schemas; it doesn't refresh discovery.

</ToggleSection>

For supported connected-app actions and availability, see [Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites) in the Help Center.

### Let visitors choose their connections

To use connected features, a visitor signs in with ChatGPT, reviews the app
access the site requests, chooses the connected account and access to allow,
and returns to the site. Sharing the site doesn't grant access to your
connected accounts. The site receives data from the apps each visitor allows.

Visitors can continue without granting app access, but features that need it
won't work. If an app is unavailable, check that it's connected in the right
workspace and allowed by workspace settings.

<SitesReferenceNavigation />
