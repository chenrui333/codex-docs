---
source_type: 'learn'
source_area: 'learn_sites'
source_url: 'https://learn.chatgpt.com/docs/sites/creating-a-site'
source_kind: 'learn_markdown'
---

# Create a site

Source: https://learn.chatgpt.com/docs/sites/creating-a-site

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Start by describing what you want to build in ChatGPT or Codex. Then review the first version and refine it as you go.

## Get started with sites

Open ChatGPT on the web or in the desktop app. Include the word "website" in your prompt or mention `@Sites` to start the sites workflow. For example, you could ask for a project request dashboard for an operations team:

**Prompt:**

```text
Build a project request dashboard website for my operations team. Let team members submit requests, see who owns each one, update the status, and filter the list. Require people to sign in with their workspace account, and keep the request data saved between visits.
```

**For ChatGPT Enterprise users:** A workspace admin must enable sites for your
  workspace or role before you can create one. If you don't see sites, ask your
  admin about access. [See the Sites administration
  guide](https://learn.chatgpt.com/docs/enterprise/sites).

The dashboard is one example. You can adapt the following flow to the site you want to build.

<WorkflowSteps variant="headings">

1. Describe the site

   Tell ChatGPT who the site is for and what you'd like people to do. Share the documents or data it needs. For a request dashboard, you might include sample requests, owners, and status labels.

2. Review the site

   Try the actions you asked for, and check the content and results against your source material. For the dashboard, you might submit a request, change its status, or filter by owner. Confirm how the site uses and saves information.

3. Refine the site

   Tell ChatGPT what you'd like to change, and share a screenshot or reference site if it would help. For the dashboard, you might ask: “Put the owner and status filters above the request list.”

4. Manage and share the site

   Return to **sites** to reopen or edit the site. Before publishing, follow the [review and sharing checks](https://learn.chatgpt.com/docs/sites/publishing-and-sharing#review-before-you-share). Choose who can visit and check the published link as an intended visitor.

</WorkflowSteps>

<ToggleSection title="Find sites and edit in the preview">

In the ChatGPT desktop app, open **sites**. You can start a site from a prompt or
from a compatible local project, then return to the sites view to manage it.

On the web, select **More** > **sites**, or go directly to [sites in ChatGPT](https://chatgpt.com/sites), to find sites you've created.
In the preview, select **Edit**. Under **Describe website edits**, describe the
changes you want. Use **Screenshot** or **Add files and more** when more
context would help.

Sites doesn't have a standalone management view in the Codex CLI or IDE
extension. Use ChatGPT on the web or in the desktop app to create, save, deploy,
and manage a site. You can still use the CLI or IDE extension to edit and test
a local project before publishing it.

</ToggleSection>

Every sites deployment URL is a production deployment. If you want to review a
  build before it becomes live, ask ChatGPT to save a version without deploying
  it.

## Save records and progress

Saving a site version preserves its content, design, and behavior. Visitor requests, status updates, uploaded files, and personal progress need their own storage. Tell ChatGPT or Codex what to save and who should be able to read or change it.

For shared or personal records, ask for access rules enforced on the server. Check that updates stay saved after reload, and use separate accounts to confirm each person's access. Hiding a button doesn't protect the underlying record.

For supplied files, specify whether the site should use a copy or refresh from the source. Check when the information was last updated.

For storage and sign-in options, see [Data and connections](https://learn.chatgpt.com/docs/sites/data-and-connections#choose-storage-and-sign-in-features).

<a id="describe-your-site"></a>

<a id="build-on-and-edit-your-site"></a>

## Tips for building your site

- **Use your source material.** Attach the files, links, definitions, and formulas the site should use. Ask ChatGPT or Codex to flag missing information instead of filling it in.
- **Describe empty and error states.** Explain what visitors should see when a search has no matches, a form is incomplete, or a connected app is unavailable. Include a way to retry or correct the problem.
- **Share a visual reference.** Attach a screenshot or link to a page, and point out the details you want to use, such as compact cards or search placement. Include any brand colors, fonts, or writing guidelines.
- **Plan for phones.** Describe how cards, tables, and forms should fit a narrow screen. Check that navigation, filters, and form controls remain usable without horizontal scrolling.
- **Label sample data.** If the final content isn't ready, ask for sample records labeled as examples. Replace them before sharing the site.
- **Make focused changes.** Ask for one change at a time and say what to keep. For example, move a filter without changing the saved records, access rules, or existing actions. Try the affected interaction after each change.

The [Sites showcase](https://developers.openai.com/showcase) shares example web apps you could build with Sites.

### Example prompts

For a resource hub, start with a short prompt:

**Prompt:**

```text
Build a resource hub website where project leads can search our kickoff resources by task. Use the resource list I attach. Save a version without deploying it so I can review it.
```

You could expand that request with visitor actions, search rules, and design preferences:

**Prompt:**

```text
Build a resource hub website for project leads preparing a kickoff. Use the resource list I attach, with its titles, descriptions, task labels, and source links.

Visitor actions:

- Choose a task, such as preparing an agenda.
- Search within that task's resources.
- Select a result to open its source link.

Search rules:

- When the search is empty, show all resources for the selected task.
- If no task is selected, show the full list.
- If there are no matches, offer a way to clear the filters and show the help contact from my list.
- Flag entries with missing titles or links for my review.
- Search filters can reset when the visitor returns.

Design preferences:

- Use a white background and dark text. Keep descriptions to one sentence, with a layout that works on a phone.
- If I provide a reference screenshot, use it for the search placement and compact resource cards.
- If I provide a brand guide, use its accent color.

Save a version without deploying it so I can review the layout and try the search.
```

For an existing project, ask ChatGPT to check compatibility and prepare it for publishing:

**Prompt:**

```text
Deploy this project with sites. Check whether it is compatible, make any required changes, and give me the deployment URL.
```

When a site needs to remember records or uploaded files, include that in your request:

**Prompt:**

```text
Add player scores and avatar uploads to this game. Keep the scores and uploaded avatars between visits.
```

<SitesReferenceNavigation />
