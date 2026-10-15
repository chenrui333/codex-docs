---
source_type: 'learn'
source_area: 'learn_sites'
source_url: 'https://learn.chatgpt.com/docs/sites/publishing-and-sharing'
source_kind: 'learn_markdown'
---

# Publish and share

Source: https://learn.chatgpt.com/docs/sites/publishing-and-sharing

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Review your site before publishing it, then choose who can visit and who can help edit it.

<a id="review-and-share-your-site"></a>

## Review before you share

Before you share a site:

<WorkflowSteps variant="headings">

1. ### Try the site
   - Review its content, generated text and images, links, uploaded files, forms,
     and interactive behavior.
   - Test the site from the intended visitor experience, including its access and
     sign-in behavior.

   For a site built from a local project, also review the source changes and any
   database migrations in the Codex [review pane](https://learn.chatgpt.com/docs/code-review?surface=app).

2. ### Check data and access
   - Confirm that it doesn't expose confidential or sensitive information, secret
     values, or third-party content you don't have the right to share.
   - Review features that collect personal information or other visitor content.
     Decide whether the site should collect, share, or publish that information.
   - If the site uses Sign in with ChatGPT, explain what visitor information it
     receives and how it uses that information.
   - If the site collects or processes personal data, comply with
     [applicable privacy and data-protection laws](https://help.openai.com/en/articles/20001340).

3. ### Choose the audience
   - Choose the narrowest sharing option that fits the intended audience.
   - Open the shared site and confirm that the intended audience can visit it.

</WorkflowSteps>

<a id="control-access-and-secrets"></a>

Keep access limited while you review the content, data handling, and expected audience.

Use the sharing options shown for your site to choose who can visit. Visitor access lets people open the site; it doesn't give them editing access.

For limited sharing, invited visitors must sign in with the account that
received access. A public site is available without ChatGPT workspace access. A
site's audience setting and any sign-in feature built into the site are separate
controls.

For sharing controls and site management instructions, see [Creating and managing ChatGPT sites](https://help.openai.com/articles/20001339) in the Help Center.

<a id="update-your-site"></a>

## Publish an update

Open your site in ChatGPT and describe the changes you want. Review the result, save a version, and deploy it. Check the changes at the published URL.

Review the site code and any data the site saves or displays. Test the published
site with an account from its intended audience.

## Choose who can visit

A new site is limited to its owner and workspace admins until you change its access. Depending on your account and workspace settings, the sharing options can include:

- **Owner and workspace admins**
- **Selected active users or groups**, where supported
- **Invited external viewers**, when external invitations are available
- **Anyone in the workspace**, where supported
- **Anyone on the internet**, only when public publishing is enabled

In Enterprise workspaces, public publishing is off by default. An admin must
  enable it before eligible members can publish publicly. Visitor access lets
  someone open a site; it doesn't give them editing access. [See the Sites
  administration guide](https://learn.chatgpt.com/docs/enterprise/sites#enable-sites-and-permissions).

For example, you could ask:

**Prompt:**

```text
Change this site's access to everyone in my workspace after showing me the current site and confirming its URL.
```

## Invite people outside your workspace

External invitations let you share a site with named viewers without making it public. You can invite people outside your workspace or share a private site from a personal account.

External invitations are rolling out to sites users on Plus, Pro, Business,
  and Enterprise plans. If the invitation option is missing, check the selected
  account, site ownership, workspace permissions, and rollout availability.

<WorkflowSteps>

1. Open a site you own and select **Share**.
2. To keep the site private, set **Who has access** to **Only those invited**.
3. Enter the viewer's email address under **Search for people or groups**, or
   **Enter an email address** for a personal site, then select the recipient.
4. Review the audience and the recipient's **Viewer** access, then select
   **Invite**.
5. Confirm that the viewer appears in the saved access list. Share the site's
   link and ask them to sign in with the account that received access.

</WorkflowSteps>

External viewers can open and use the site. They don't become workspace
members or site editors, and can't edit or publish the site. The invitation
grants access to this site; review its content and connected data before sharing.

In Enterprise, admins manage **Allow members to invite external visitors to sites** under **Workspace settings > Permissions & roles**. This permission is separate from permission to publish sites publicly. Business workspaces don't have a separate external-invitation toggle; sites must be enabled and the feature must be available to the account.

To remove a viewer, open the site's sharing controls and remove their access.
Also check the remaining audience settings: removing one invitation doesn't
remove access the person has through public, workspace, or group sharing.

## Collaborate on a site

Site collaboration requires a workspace. When the feature is available, a site owner can invite active members of the same workspace as editors.

Invite only people you trust to edit the site's code and content.

<WorkflowSteps>

1. Open the site and select **Share**.
2. Under **Add people or groups**, find and select a workspace member. They
   are added as a visitor.
3. Open **Can view** next to that person and choose **Can edit**. Access saves
   automatically. The site appears under **Shared with you** in the member's
   sites view.
4. The editor can open the site, make changes, save versions, and publish
   updates after the owner has published the site for the first time.

</WorkflowSteps>

The site owner manages editor access and can promote an existing visitor to
editor, change an editor to **Can view**, or remove their access. Co-editing
doesn't add a separate workspace permission toggle.

Editors can't change the site's audience, invite or remove other people, manage
settings or analytics, or transfer ownership. An
editor also can't perform the site's first publish; the owner must publish the
site before editors can publish later updates.

Editor access is separate from visitor access. The steps above first add the
person as a visitor, then grant editing access. Promoting a visitor to editor
doesn't change the site's audience setting.

<SitesReferenceNavigation />
