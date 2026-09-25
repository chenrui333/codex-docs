---
source_type: 'learn'
source_area: 'learn_migrate_custom_gpts'
source_url: 'https://learn.chatgpt.com/docs/migrate-custom-gpts'
source_kind: 'learn_markdown'
---

# Moving your custom GPT workflows to plugins

Source: https://learn.chatgpt.com/docs/migrate-custom-gpts

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Custom GPTs helped you make ChatGPT your own. Plugins build on that work, bringing your instructions and knowledge into workflows that can do more.

This guide is for ChatGPT Enterprise workspace admins and people migrating GPTs they created. Start with the path that fits your role:

- **Workspace admins:** [Prepare your workspace](#plan-your-transition), check permissions, and [migrate GPTs in bulk](#admin-bulk-migration).
- **GPT creators:** [Prepare your GPT](#identify-gpts-that-may-need-extra-attention), then [migrate, test, and share it](#migrate-test-and-share).

**Using someone else’s GPT?** Ask its creator or a workspace admin to migrate it, then [install the replacement they share with you](#step-3-share-and-verify-access).

**Create or refine a plugin**

See [Build plugins](https://learn.chatgpt.com/docs/build-plugins) for guidance on building a new plugin or updating one after migration.

## Understand the change

We’re transitioning custom GPTs to plugins. Use the milestones below to plan your migration before custom GPTs are retired.

A [plugin](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex) is a reusable package for a workflow that can include skills, apps, or both. [**Skills**](https://help.openai.com/en/articles/20001066) explain how to do a task, such as writing in your team's style. [**Apps**](https://help.openai.com/en/articles/11487775) connect ChatGPT to other services for information or supported actions.

> Illustration: A plugin is a package for a workflow. It can include skills, which provide instructions for how to do the work, apps, which connect to tools and information, or both.

In an enterprise workspace, [your admin](https://help.openai.com/en/articles/11509118) decides which plugins you can use, including access by role where supported. They can make plugins available for you to install or install them automatically for eligible users. Sharing a plugin or publishing it to the workspace requires separate permissions.

**Your existing permissions still apply**

Plugins respect your [existing app access](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex). For example, signing in to Google Drive through ChatGPT lets its plugin work with documents your account can already access. It doesn’t unlock other files or add Google Drive permissions.

You may need to [connect your account](https://help.openai.com/en/articles/20001494) or [approve an action](https://help.openai.com/en/articles/20001495). Available features depend on your app access, workspace settings, and where you use ChatGPT.

Plugins with only skills and reference files need no app connection. For each required app, users need access and any account connection or action permissions the workflow needs. If an optional app is unavailable, other capabilities may still work; capabilities that require an unavailable app cannot.

<ToggleSection title="Example Plugin Page">

Here’s an example of a plugin page, showing its app and skills. The **Disabled by admin** label means this example plugin is not available to use in the workspace.

> Illustration: An example Intuit QuickBooks plugin page, annotated to show its availability, sample requests, description, connected app, and included skills.

</ToggleSection>

With a custom GPT, you explicitly [choose the GPT](https://help.openai.com/en/articles/8554407-gpts-in-chatgpt) (by opening it or mentioning it with @ on ChatGPT web), then send it your request.

With plugins, you can choose an available plugin or skill directly. In ChatGPT, [use an @ mention or open + and select More](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex), where supported.

<figure class="mx-auto w-full max-w-[640px]">

[Select a plugin from the ChatGPT composer](https://cdn.openai.com/devhub/docs/codex/migrate-custom-gpts/invoke-plugin-hq.webm)

  <figcaption class="text-center">
    Select an available plugin from the composer, then describe the task you
    want it to help with.
  </figcaption>
</figure>

You can also describe your task: ChatGPT can [automatically use a relevant installed skill](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills), including a skill packaged in a plugin, when its description matches what you need.

**Test how your plugin gets selected**

Automatic skill selection depends on the task and available capabilities; an installed plugin won’t run on every request. After migration, test both explicit selection and a normal task request.

### What can a plugin do compared with a custom GPT?

| What you want to do        | With a custom GPT                                                                          | With a plugin                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Reuse instructions         | You add instructions to guide the GPT’s responses.                                         | A skill provides reusable instructions that guide how a task is done.                              |
| Use team knowledge         | You upload reference files as GPT knowledge.                                               | Skills can include reference files. Review the migrated resources and test how they’re used.       |
| Connect to other services  | Custom actions connect the GPT to external services.                                       | Apps connect to services and supported actions. GPT custom actions need to be rebuilt separately.  |
| Use tools and create files | You enable available capabilities such as web search, image generation, and data analysis. | Available tools depend on the experience and workspace settings. Test the outputs your team needs. |
| Start a workflow           | You open or explicitly select the GPT.                                                     | You can select a plugin or skill. ChatGPT may also use a relevant installed skill automatically.   |
| Share with your team       | You share the GPT with an allowed audience.                                                | You share or publish the plugin under workspace permissions. Review access before rollout.         |

<figure id="clip-what-transfers" class="my-8 w-full scroll-mt-32">
  <h4 class="!mb-4 !mt-0 text-lg">What transfers to a plugin</h4>

[What transfers to a plugin](https://cdn.openai.com/devhub/docs/codex/migrate-custom-gpts/01-what-transfers-hq.mp4)

  <figcaption
    id="01-what-transfers-description"
    class="!mt-4 text-sm text-secondary"
  >
    **
      See what moves into a plugin and what needs rebuilding.
    **

      See how a GPT’s instructions and reference files become a skill and
      connected apps remain part of the plugin. Custom actions do not transfer;
      plan to replace them with a supported app’s read or write actions, or a
      custom MCP server.

  </figcaption>
</figure>

<a id="plan-your-transition"></a>

## For admins: Prepare your workspace

Help your team carry its work forward: agree on migration owners, check their permissions, and plan access to the replacements.

- **Admin notice.** Admins receive an early heads-up and guidance to plan the transition and prepare their teams.
- **Migration.** GPT creators and workspace admins can migrate published GPTs to plugins.
- **Custom GPT retirement.** Custom GPTs stop working. Move the workflows you want to keep to plugins and test them before retirement.

### Choose priority migrations

Start with GPTs your team relies on most. Agree with their creators on what to keep, who will maintain it, and who needs access.

- Allow extra time for custom actions, which need to be rebuilt separately.
- Name an owner for each GPT and record its purpose, audience, instructions, reference files, and integrations.
- Ask owners to save a few familiar prompts and good results, including one harder case, so they can compare the replacement.
- Confirm which GPTs are published. Have creators publish needed drafts while GPT creation is still available; public sharing isn’t required.

<figure id="clip-prioritize-workflows" class="my-8 w-full scroll-mt-32">
  <h4 class="!mb-4 !mt-0 text-lg">Choose priority workflows</h4>

[Choose priority workflows](https://cdn.openai.com/devhub/docs/codex/migrate-custom-gpts/02-prioritize-workflows-hq.mp4)

  <figcaption
    id="02-prioritize-workflows-description"
    class="!mt-4 text-sm text-secondary"
  >
    **
      Use ownership and recent usage to prioritize your GPT migrations.
    **

      Identify the GPTs your team still relies on and consider leaving unused
      workflows behind. Admins with access to the ChatGPT admin plugin can
      request GPT names, owners, and message counts from the last 30 days to
      help prioritize.

  </figcaption>
</figure>

### Review workspace permissions

Before migrating, check that everyone has the access they need. Permissions control actions such as using, sharing, or publishing plugins; roles group permissions for similar responsibilities. With [role-based access control (RBAC)](https://help.openai.com/en/articles/11750701), workspace owners assign roles to people or groups.

Use this table to check access for migration and the replacement plugins.

| Action                                                               | What admins should check                                                                                                                                                                                                                                            |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Migrate their own custom GPTs to plugins                             | Enable plugins for the workspace. The person migrating must be the GPT’s creator or a workspace owner or admin, and the GPT must be published. Having access to someone else’s GPT is not enough.                                                                   |
| Share newly migrated GPTs (now plugins) with people or groups        | Give Share plugins to people who need to share replacements with individuals or groups. People who only use a plugin don’t need this permission.                                                                                                                    |
| Publish newly migrated GPTs (now plugins) to the workspace directory | Give Publish plugins to workspace to people who will publish replacements in the workspace plugin directory. This is separate from sharing directly.                                                                                                                |
| Install and use new plugins                                          | Allow Use plugins for the intended users or roles.                                                                                                                                                                                                                  |
| Use an included app                                                  | Enable required apps for the intended users or roles. Check that their connected accounts can access the needed information. Only supported, allowed actions can run, and required approvals still apply. Plugin installation does not add app or file permissions. |

**Built-in migration doesn't require upload permissions**

You do not need to enable **Upload plugins** or **Upload plugins with custom MCP servers** just for the built-in migration. Set any permissions for separately rebuilt integrations according to your workspace's policies.

For current settings, see [Plugin and app admin controls](https://help.openai.com/en/articles/11509118) and [Skill admin controls](https://help.openai.com/en/articles/20001066).

### Check installation and app access

Decide how teammates will get each replacement. Available lets eligible users install a plugin; Installed installs it for eligible users or roles. These settings do not change who the plugin is shared with.

Review required apps separately: check workspace and role access, account sign-in, and action approvals. Test access with an account that has the same permissions as a typical teammate.

<a id="admin-bulk-migration"></a>

#### For workspace admins: Migrate GPTs in bulk

In ChatGPT Work, type **@** and select [ChatGPT Admin](https://learn.chatgpt.com/docs/enterprise/admin-plugin). Check that its Admin app shows **Connected**. For Codex, use the open or copy button on a prompt below. Review the prompt and selected plugin before sending.

<a id="1-inventory-and-prioritize"></a>
<a id="1-choose-the-gpts"></a>

### 1. Run the GPT report

**Prompt:**

```text
[@ChatGPT Admin](plugin://admin-console@openai-curated-remote) Run the GPT report prioritizing by most recently used GPTs in the last 30 days.
```

The report is ordered by recent use and includes owners, usage, migration status, and custom actions.

#### Optional: Add report details

**Prompt:**

```text
[@ChatGPT Admin](plugin://admin-console@openai-curated-remote) Run the GPT report and include a summary of GPTs that haven’t been migrated.
```

**Prompt:**

```text
[@ChatGPT Admin](plugin://admin-console@openai-curated-remote) Run the GPT report and include which GPTs have knowledge files attached.
```

<a id="2-create-one-migration-tracker"></a>

### 2. Export and use the results

Ask for your preferred format, such as **Excel**, **CSV**, or **Google Sheets**. Sort, filter, share, or track migration your way.

**Prompt:**

```text
[@ChatGPT Admin](plugin://admin-console@openai-curated-remote) Run the GPT report and export it as [preferred format].
```

<a id="6-help-teams-switch-and-repeat"></a>

### 3. Schedule a recurring report

**Prompt:**

```text
[@ChatGPT Admin](plugin://admin-console@openai-curated-remote) Run the GPT report for [workspace] every [day] at [time and time zone]. Post the results here.
```

[Scheduled tasks](https://learn.chatgpt.com/docs/automations) must be enabled, with the Admin plugin available to the task. Review the schedule and first runs in **Scheduled**.

<a id="3-migrate-a-small-batch"></a>
<a id="2-migrate-a-small-batch"></a>

### 4. Migrate selected GPTs

Choose GPTs by ID or describe the group, such as all private GPTs. Replacements start private, and originals become read-only.

<WarningTip title="Sharing settings do not carry over in bulk">

Bulk migration **does not copy sharing settings**. Record who needs access, then **share each replacement manually** or ask the GPT creator to share it. We expect bulk sharing through the Admin plugin soon.

</WarningTip>

**Prompt:**

```text
[@ChatGPT Admin](plugin://admin-console@openai-curated-remote) Migrate [GPT IDs or a description of the GPTs] to plugins. Show me the selection and ask for confirmation before migrating.
```

<a id="4-test-and-refine"></a>
<a id="3-have-owners-test"></a>
<a id="5-share-and-check-access"></a>
<a id="4-share-and-confirm-access"></a>

Have owners [test the replacement plugins](#step-2-test-with-familiar-work) and verify access. Custom actions need to be rebuilt separately.

<a id="migration-email-template"></a>

#### Email template: Ask GPT creators to migrate

Make this your own: replace the placeholders before sending.

**Email template:**

```text
Subject: Please migrate your custom GPTs by [deadline]

Hi [name],

We’re moving our custom GPT workflows to plugins. Please migrate, test, and share these GPTs by [deadline]:

[GPT names/links]

If you no longer need one, let us know. For those you’re keeping:

1. Migrate. Save the intended audience and finish important edits first. Go to My GPTs > Created by me > Migrate to plugin. The GPT must be published; after migration, it becomes read-only.

2. Test. Try familiar tasks and one harder case. Check the instructions, attached files, results, and required apps or tools.

3. Share. Each replacement starts private. Share it with the intended people or groups, then ask a teammate to test access. Keep private workflows private.

Follow [migration guide link] for the steps. Custom actions need rebuilding; contact [admin contact] if yours uses them or you need help.

Please reply with each plugin’s link, testing status, and any blockers.

Thanks for helping your team make the switch,
[admin name/team]
```

<a id="identify-gpts-that-may-need-extra-attention"></a>

## For GPT creators: Prepare your GPT

Before migrating a GPT you created, save its intended audience and a few familiar prompts and results for testing. Check the table below for anything that needs extra attention. Admins migrating on a creator’s behalf should review these details with them.

| If your custom GPT…                                           | What to review                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Uses custom actions                                           | Custom actions don’t transfer. Rebuild needed integrations with a supported connector or custom MCP connection, then test them before your team switches.                                                                                                                                                                                                         |
| Depends on a model, detailed instructions, or a strict format | The selected model doesn’t carry over; Enterprise defaults apply. Compare familiar prompts and results. Check that the right skill is selected and follows your instructions and format, since behavior can differ.                                                                                                                                               |
| Relies on files, tools, or previous chat context              | Check that files, templates, and examples are present and used correctly; transfer and retrieval may differ. Test required tools, such as web search, images, data analysis, or file creation. GPT capability settings don’t guarantee the same setup. Conversation starters and previous chats may not copy, so save useful prompts and identify needed context. |
| Is shared with teammates or people outside your workspace     | Record the intended audience and verify they can install and use the replacement. Show users how to install or select it. Check the replacement’s sharing settings. Check access for external users: public GPTs in affected Enterprise workspaces are included, but public sharing and timelines for other plans may differ.                                     |
| Needs updates during the transition                           | The original GPT stays usable until retirement. Maintain and test the replacement plugin as your workflow changes.                                                                                                                                                                                                                                                |

<a id="migrate-test-and-share"></a>

## For GPT creators: Migrate, test, and share

Use these steps for a published GPT you created. Workspace admins can also use them to help creators migrate individual GPTs.

**Before you migrate:** The original GPT becomes read-only after migration. You can continue using it until retirement, but future edits must be made in the replacement plugin.

### Step 1: Convert your GPT

Go to **My GPTs**, find your GPT under **Created by me**, and select **Migrate to plugin**. You can also ask a workspace admin for help.

Migration turns your GPT’s instructions into a skill and brings over its knowledge files and connected apps. Rebuild custom actions separately. Save familiar prompts: conversation starters do not transfer one-to-one. The selected model does not carry over, and capability settings do not guarantee the same tools or behavior. Review migrated files and test required tools before sharing.

If you don’t see **Migrate to plugin**, see [Why don’t I see the migration option?](#why-dont-i-see-the-migration-option) in the Admin FAQ.

Your new plugin starts private. Test it, then share it with the people who need access—even if they could already use the original GPT.

<figure id="migration-preview" class="my-8 w-full scroll-mt-32">

[Watch the migration workflow](https://cdn.openai.com/devhub/docs/codex/migrate-custom-gpts/03-migration-walkthrough-hq.mp4)

  <figcaption
    id="03-migration-walkthrough-description"
    class="!mt-4 text-sm text-secondary"
  >
    **
      Follow the migration steps, then review and install your plugin.
    **
  </figcaption>
</figure>

### Step 2: Test with familiar work

Try the plugin on familiar tasks and one harder case. Check the following before sharing it.

- Is the right skill selected, and does it follow your instructions?
- Does it use the expected reference material and produce complete answers or files with the required structure, fields, and format?
- Does it handle the harder case correctly and respond in a workable amount of time?
- Are the tools and integrations it needs available?

**Switch after the workflow is ready**

If a required capability is missing, wait to switch that workflow until you have a tested alternative.

<figure id="clip-test-and-share" class="my-8 w-full scroll-mt-32">

[Test before sharing](https://cdn.openai.com/devhub/docs/codex/migrate-custom-gpts/04-test-and-share-hq.mp4)

  <figcaption
    id="04-test-and-share-description"
    class="!mt-4 text-sm text-secondary"
  >
    **
      Test familiar workflows and refine the plugin before sharing it.
    **
  </figcaption>
</figure>

### Step 3: Share and verify access

Review who can access the new plugin. To share with people or groups, you need Share plugins access. To publish to the workspace, you need Publish plugins to workspace. Have an intended user open and test the replacement.

**For people using the replacement:** After the creator or admin shares the plugin with you, install it before using it, unless your admin has installed it for you. Sharing access and installation are separate steps.

If you can’t share or publish the plugin, ask your admin to check your permissions before announcing the switch.

### Step 4: Help your team switch

Share the replacement link, explain key differences, and demonstrate a familiar task. Update onboarding, instructions, and saved resources, and name an owner for future changes and questions.

After migration, the plugin’s creator or a workspace owner or admin can [edit the replacement](https://learn.chatgpt.com/docs/build-plugins). Rerun your important tests after each change.

### What happens to the original GPT?

Until retirement, the original GPT stays usable, and you can continue editing an existing GPT that you have not migrated, even after new GPT creation stops. Once you migrate a GPT, the original becomes read-only. At retirement, custom GPTs stop running and leave the GPT directory.

<a id="troubleshoot-common-blockers"></a>
<a id="details-still-being-confirmed"></a>
<a id="additional-migration-questions"></a>
<a id="can-i-migrate-gpts-on-behalf-of-my-customers-or-users-including-in-bulk"></a>
<a id="can-we-migrate-or-recover-a-gpt-after-the-retirement-date"></a>

## Admin FAQ

Find answers to common questions about preparing your workspace and helping your team switch.

h3]:mb-5 [&>h3]:mt-12 [&>h3]:text-xl [&>h3:first-child]:mt-0 [&_summary]:gap-3 [&_summary]:px-5 [&_summary]:py-4 [&_.toggle-section-content]:px-5 [&_details[open]>.toggle-section-content]:border-t [&_details[open]>.toggle-section-content]:border-default [&_details[open]>.toggle-section-content]:pt-4 [&_details[open]>summary>span>svg]:rotate-90">

### Preparing your workspace

  <ToggleSection title="Can admins migrate many GPTs at once?">

Yes. Workspace admins can use the [ChatGPT Admin plugin](https://learn.chatgpt.com/docs/enterprise/admin-plugin) to migrate selected batches. Start with the GPTs your team needs most.

Use the [admin walkthrough](#admin-bulk-migration) to run a report and migrate selected GPTs. Sharing settings do not carry over in bulk; share each replacement manually.

  </ToggleSection>

  <ToggleSection title="Who can migrate a GPT, and how does the process work?">

The GPT’s creator or a workspace admin can start migration from a published GPT’s page. Admins can do this even if they did not create the GPT.

Plugins must be enabled, and shared access alone does not give someone permission to migrate.

  </ToggleSection>

  <ToggleSection title="Why don’t I see the migration option?">

You must be the GPT’s creator or a workspace admin, the GPT must be published, and plugins must be enabled for you.

Access to use someone else’s GPT does not give you permission to migrate it.

If these conditions are met and the option is still missing, contact OpenAI support with the GPT’s name, owner, and a description of what you’re seeing.

  </ToggleSection>

  <ToggleSection title="Which permissions should I review before people start migrating?">

Start by enabling plugins. The built-in migration workflow does not require Upload plugins or Upload plugins with custom MCP servers.

People who will share plugins with others in the workspace need Share plugins, and those who will publish them across the workspace need Publish plugins to workspace.

Rebuilding a custom integration is a separate task and may require additional permissions.

  </ToggleSection>

  <ToggleSection title="What do employees need to use a migrated plugin?">

Employees need:

- **Use plugins** permission.
- Access to the replacement plugin.
- A workspace policy that allows them to install it or installs it for them.

Any included apps still require the appropriate app access and authorization. Connecting an account through ChatGPT does not give someone additional permissions in that app.

  </ToggleSection>

  <ToggleSection title="Can employees use migrated plugins in Chat, or do they need Work?">

Migrated plugins can be used in Chat when plugins are enabled for the user, as well as in Work. Available tools still depend on the plugin, workspace settings, and where it is used. For the creation and editing workflow and its prerequisites, see [Build plugins](https://learn.chatgpt.com/docs/build-plugins).

Check access for each task separately: using the plugin, creating or editing it, and sharing or publishing it. Before assigning maintainers, ask your admin to confirm that they can access the creation and editing experience; the built-in migration requirements do not answer that question.

  </ToggleSection>

  <ToggleSection title="How should I manage access when we roll out the replacements?">

Review each plugin’s audience and [installation policy](https://help.openai.com/en/articles/11509118), then ask someone in the intended audience to test access.

An Available plugin lets eligible users install it, while an Installed plugin is installed for them by default. Role controls and app permissions still apply.

The replacement starts private. Access to the original GPT does not automatically give someone access to the plugin. Share it with the intended people or groups, then ask a recipient to install and test it, unless their admin has already installed it for them. Identify who will maintain the replacement and help teammates with access.

  </ToggleSection>

### Testing and ongoing administration

  <ToggleSection title="Will a migrated plugin behave exactly like the original GPT?">

A migrated plugin may respond differently from the original GPT. Compare the same prompts and reference files, including one difficult example, and check that answers use the right sources, include the expected facts, follow the requested format, and use the required tools. Test both explicit plugin selection and a normal task request, since automatic skill selection depends on the request and available capabilities. Ask owners to assess:

- The quality of the output.
- How well instructions are followed.
- How long the task takes.

The GPT’s selected model does not carry over; Enterprise defaults apply.

  </ToggleSection>

  <ToggleSection title="What should I do about GPTs that use custom actions?">

Custom actions do not transfer through the migration workflow. The person maintaining that workflow will need to rebuild the integration using a supported connector or a custom MCP server.

Identify these GPTs early so the appropriate technical and security teams have time to review the replacement and its permissions.

  </ToggleSection>

  <ToggleSection title="What happens to the original GPT after migration?">

The original GPT remains usable until retirement. At retirement, custom GPTs stop running and leave the GPT directory.

Owners should maintain the plugin going forward. See [What happens to the original GPT?](#what-happens-to-the-original-gpt).

  </ToggleSection>

  <ToggleSection title="Can we still migrate a GPT after retirement?">

Yes. You will still be able to migrate a GPT after retirement, although the GPT itself will no longer run.

  </ToggleSection>

  <ToggleSection title="Which admin controls apply after migration?">

Migrated plugins follow the workspace’s [plugin permissions](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex). Admins can control who uses and shares plugins, as well as who publishes them to the workspace. You can review role permissions and manage individual plugins.

Included apps retain their own access and action controls, so making a plugin available does not grant access to the data or actions in its apps.

  </ToggleSection>

  <ToggleSection title="How should admins plan for plugin usage and costs?">

Converting a custom GPT to a plugin does not consume credits. Under credit-based pricing, editing or updating a plugin does consume credits. Conversion is separate from using the replacement plugin, so review the usage and costs of the workflow before rolling it out.

Usage depends on whether the plugin runs in Chat or Work, the models and features involved, and your workspace’s agreement. Under credit-based pricing, Instant Chat is generally unlimited, but a request can switch to a reasoning model or use a feature that consumes credits. Work consumes credits based on the model and tokens used. Enterprise agreements billed in USD have different terms, including charges for Instant usage. Review your workspace’s [credit-based rate card](https://help.openai.com/en/articles/11481834) or [USD rate card](https://help.openai.com/en/articles/20001415) before rollout.

Review users’ effective usage limits and workspace spending controls separately. In a credit-based workspace, a zero overage limit prevents spending beyond the shared credit allocation; it does not prevent use of remaining credits. Usage alerts notify admins but do not stop usage. See [Manage usage limits and overages](https://help.openai.com/en/articles/20001001) for the controls that apply to your workspace.

  </ToggleSection>
