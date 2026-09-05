---
source_type: 'learn'
source_area: 'learn_whats_new'
source_url: 'https://learn.chatgpt.com/docs/whats-new'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# What's new

Source: https://learn.chatgpt.com/docs/whats-new

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

This weekly digest highlights ChatGPT and Codex features that can change how you
work, with examples and links to learn more. For every versioned update, bug fix,
and minor improvement, see the [Codex changelog](https://learn.chatgpt.com/docs/changelog).

## August 31–September 4, 2026

### Take on demanding work with GPT-6 Astra

[GPT-6 Astra](https://learn.chatgpt.com/docs/models#gpt-6-astra) combines advanced reasoning, computer
use, and stronger judgment for complex work across code, apps, and research in
Codex and ChatGPT Work. Use it to carry out a workflow, check the result, and
produce a document, spreadsheet, or presentation that fits your templates and
task.

Once Astra is available to your account, choose it from the model selector.
See [usage and pricing](https://learn.chatgpt.com/docs/pricing) before starting a large task.
Enterprise access requires both rollout eligibility and an administrator to
enable it.

## August 24–28, 2026

### Work with more websites

- **Use your browser:** Work in [Edge, Brave, Opera, or Vivaldi](https://learn.chatgpt.com/docs/chrome-extension)
  as well as Chrome from the ChatGPT desktop app. Bring an open tab into a
  ChatGPT Work or Codex chat and work with the website where you're already
  signed in. Opera supports browser control but doesn't have side chat.

- **Use a website's tools:** With [Site tools (WebMCP)](https://learn.chatgpt.com/docs/webmcp), ChatGPT
  Work and Codex can use actions offered by a website in the desktop app's
  built-in browser. For example, a document editor can provide tools to find
  a section or add a comment. Update the desktop app and use GPT-5.6 Sol or
  GPT-5.6 Terra. Site tools aren't available with GPT-5.6 Luna or in Enterprise
  or Edu workspaces.

- **Sign in through the cloud browser:** On eligible plans, continue a task
  that needs a website account in ChatGPT Work on the web, iOS, or Android.
  Follow the [sign-in request](https://learn.chatgpt.com/docs/browser?surface=web#web-sign-in-to-a-website)
  and enter your details in the sign-in flow, not in the chat. This doesn't
  connect your local browser profile. Website sign-in isn't available for
  Enterprise or Edu workspaces.

Availability depends on rollout and workspace settings.

**Prompt:**

```text
Use @Edge to read the current page and turn it into a concise checklist.
```

[Read the August 25 browser release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-08-25-browser).

### Run scheduled tasks from app events

[Scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=web#web-trigger-tasks-from-app-events) can now
start when a supported event occurs in Gmail, Slack, or GitHub. Use an event
trigger to triage new email, summarize channel activity, or act on pull request
feedback without polling on a fixed cadence.

Event-triggered tasks are available in ChatGPT on the web and mobile for
eligible plans. Connect the relevant app and approve its requested access first. In managed
workspaces, administrators can control access.

**Prompt:**

```text
When one of my pull requests in <owner>/<repository> receives new review feedback, summarize the feedback and prepare a revision plan.
```

[Read the August 25 release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-08-25-event-triggers).

## August 17–21, 2026

### Work with more of your apps and content

- **Apple Messages:** [Find chats, summarize messages, prepare replies, and send through Messages on your Mac](https://learn.chatgpt.com/docs/plugins?surface=app#app-use-apple-messages-from-codex). The plugin is available on all plans in the ChatGPT desktop app for macOS. Use it in ChatGPT Work and Codex, not in regular ChatGPT chats. By default, ChatGPT sends messages only after you approve the message and its recipients.

- **Site co-editing:** Where available, [invite active members of your workspace as editors](https://learn.chatgpt.com/docs/sites#collaborate-on-a-site). Editors can refine the Site and publish updates after its owner publishes it for the first time. Invited editors can read the Site's live database data; owners retain control of sharing and settings.

- **Editable Site URLs:** Where available, [choose a new ChatGPT-hosted address for an existing Site](https://learn.chatgpt.com/docs/sites#change-a-site-url) without redeploying it. The previous address redirects to the new one.

- **Computer History in Europe:** Use [Computer History](https://learn.chatgpt.com/docs/customization/computer-history) in the EEA, Switzerland, and the United Kingdom. It remains off by default for ChatGPT Pro, Business, and Enterprise users on macOS. Business and Enterprise administrators must enable access first.

- **Shared thread snapshots:** [Share a read-only snapshot of a local Codex thread](https://learn.chatgpt.com/docs/use-chatgpt#share-a-read-only-snapshot-of-a-codex-thread) from the ChatGPT desktop app for macOS. Personal-account links are viewable by anyone with the link; workspace-account links are limited to the originating workspace. Codex redacts known secret patterns, but review the snapshot before sharing because sensitive content may remain.

- **Unified pinned threads:** Keep your [pinned chats](https://learn.chatgpt.com/docs/projects?surface=app#app-organize-projects-and-chats) in sync between desktop and iOS.

**Prompt:**

```text
Find the latest Messages conversation about tomorrow's launch, summarize the open questions, and draft a reply without sending it.
```

[Read the August 20 release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-08-20-app).

> Shared threads in Codex and ChatGPT Work let you show the process behind your build with a read-only link

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2090555241343418814) (2026-08-20)

### Work with GitLab projects in Codex cloud

[GitLab support](https://learn.chatgpt.com/docs/third-party/gitlab) is available in beta on all ChatGPT
plans. Connect a project, create a cloud environment, start tasks from issues
or merge requests with `@codex`, and request one-off or automatic merge request
reviews.

The integration runs in Codex cloud, and a managed workspace admin can disable
it. GitLab-triggered activity requires permission to configure the applicable
webhook. GitLab Self-Managed and GitLab Dedicated connections require
workspace admin setup; webhook activity requires GitLab 19.0 or later.

[Read the August 19 GitLab release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-08-19-gitlab).

### Export public plugin metadata for review

Eligible ChatGPT Enterprise workspace owners and admins can download a CSV of
the public plugins visible to their workspace. In
[Admin > Plugins](https://chatgpt.com/admin/plugins), select **Public**, then
select the download icon (**Export CSV**).

The export lists plugin, app, and Chat skill names and descriptions, together
with developer, version, date added in UTC, and OpenAI verification metadata.
It uses a public-catalog snapshot that can be up to 48 hours old and excludes
plugins created for the workspace. The export isn't available in FedRAMP
workspaces.

[Read the August 17 admin export release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-08-17-admin-csv).

## August 10–14, 2026

### Find earlier work with Computer History

[Computer History](https://learn.chatgpt.com/docs/customization/computer-history) turns activity across
your apps and websites into a searchable timeline and memories that ChatGPT
and Codex can use. Turn it on only if you want to share that context, then
choose which apps and websites contribute, pause collection, and review or
delete your history at any time.

Computer History is available in the ChatGPT desktop app on macOS for ChatGPT
Pro, Business, and Enterprise customers. Business and Enterprise
administrators must first enable access. Initial availability excludes the
European Union, Switzerland, and the United Kingdom.

**Prompt:**

```text
Find the document and Slack thread I was reviewing earlier, then summarize the decisions I still need to act on.
```

[Watch: Computer History in ChatGPT](https://www.youtube.com/watch?v=W-HhMUe9hOg)

### Use the ChatGPT desktop app on Linux

The [ChatGPT desktop app for Linux](https://learn.chatgpt.com/docs/linux/linux-app) is now available in
preview. Install a `.deb` package on supported Ubuntu or Debian distributions,
or an `.rpm` package on Fedora. Packages are available for both x64 and ARM64
processors.

Sign in with your ChatGPT account to work with projects, local files, and
Codex. Some features, including Computer Use, aren't yet available in the
Linux preview.

> Now in preview: The ChatGPT desktop app for Linux.

[View @OpenAI on X](https://x.com/OpenAI/status/2087231350134980830) (2026-08-11)

### Bring your existing agent setup and work with you

[Import instructions, settings, skills, plugins, projects, and recent
work](https://learn.chatgpt.com/docs/import) from **Claude Code**, **Claude Cowork**, or
**Cursor** into the ChatGPT desktop app. Turn on automatic updates in
**Settings > Import** to keep your imported work in sync.

In Codex CLI, use `/import` to bring supported setup and recent chats from
Claude Code or Cursor into your local session.

[Read the August 11 desktop and CLI release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-08-11-app).

> You can now keep your work from other agents in sync with ChatGPT Work and Codex.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2087242829076791392) (2026-08-11)

### Choose the right access for defensive security work

Daybreak now offers two tiers for approved defenders. **Daybreak Blue** supports
general defensive work, such as secure code review, incident response, and
patch validation. **Daybreak Red** requires its own approval and provides
access to purpose-trained models for authorized security assessments.

Access requires [Trusted Access for
Cyber](https://learn.chatgpt.com/docs/cyber-safety#trusted-access-for-cyber) and applies only to the
approved identity, workspace or organization, model, and product surface.

[Read the August 10 Daybreak
announcement](https://learn.chatgpt.com/docs/changelog#codex-2026-08-10-daybreak).

> We’re expanding our cybersecurity initiative Daybreak

[View @OpenAI on X](https://x.com/OpenAI/status/2086864365379010729) (2026-08-10)

## August 3–7, 2026

### Talk through files and projects with ChatGPT Voice

[ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) now supports uploaded files and
[ChatGPT Projects](https://learn.chatgpt.com/docs/projects). Ask questions about a document during a
voice conversation, or continue a project using its recent chats, sources, and
instructions.

**Prompt:**

```text
Review the research brief I uploaded, explain the main tradeoffs out loud, and compare them with the sources already in this project.
```

### Study and teach with dedicated education plugins

Three new [plugins](https://learn.chatgpt.com/docs/plugins) bring classroom-specific workflows to
ChatGPT Work and Codex. **College Student** creates study guides, practice
quizzes, flashcards, and interactive explanations. **College Educator** helps
develop course plans, materials, and assessments. **K–12 Educator** supports
lesson planning, classroom resources, and materials adapted for different
learners.

The plugins are available through ChatGPT Edu and ChatGPT for Teachers district
deployments. Schools control which tools and permissions are available. Read
the [education plugins
announcement](https://openai.com/index/learn-teach-chatgpt-work-codex/).

### Reuse saved files and find past work faster

On the web, add a saved Library file to a conversation without uploading it
again, search within Library, and paste formatted text without losing headings,
links, or lists. Search also matches folders and conversation titles across the
web, iOS, and Android.

Pastes longer than 10,000 characters now become attachments on every ChatGPT
plan, including Enterprise and Edu. Select **Show in text field** if you want
to move the content back into your message.

Read the [ChatGPT release
notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes).

### See your remaining ChatGPT Work usage

Eligible users on personal plans and ChatGPT Business can check their remaining
ChatGPT Work usage directly in the web sidebar. Available credit options depend
on your account and workspace permissions. ChatGPT Work and Codex continue to
share the same [usage limits and credits](https://learn.chatgpt.com/docs/pricing).

### Choose how GPT-5.6 responds in ChatGPT

ChatGPT Plus and Pro users can adjust how much thought GPT-5.6 Sol puts into a
response with a new slider. The updated model also provides more reliable facts
and focused answers. GPT-5.6 Luna becomes the default ChatGPT model on the Free
and Go plans.

These changes apply to ChatGPT conversations. They don't change model behavior
in ChatGPT Work or Codex. Read the [ChatGPT release
notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes).

### Organize work and switch agents in Codex CLI 0.147.0

[Codex CLI 0.147.0](https://github.com/openai/codex/releases/tag/rust-v0.147.0)
adds persistent, manually ordered chat sections and portable Agent Plugins.
Search across local, personal, workspace, and remote plugin catalogs, or
[import Cursor and Claude Code setup](https://learn.chatgpt.com/docs/import) without duplicating
synced conversations.

Use `--approve-for-me` to enable [automatic approval
review](https://learn.chatgpt.com/docs/sandboxing/auto-review) for eligible requests without expanding
filesystem or network permissions. Amazon Bedrock sessions also gain cached
web search and remote conversation compaction.

[Watch: Introducing Agent Plugins](https://www.youtube.com/watch?v=UaeWJK_vv-Y)

### Follow and resume deeper security scans

Hosted Codex Security plugin versions `0.1.16` through `0.1.18` add live scan
progress, measured token usage, resumable deep scans, and configurable
discovery limits. The latest release also supports Amazon Bedrock
authentication for repository scans and their delegated workers.

Use the [Codex Security workbench](https://learn.chatgpt.com/docs/security/plugin/workbench) to review
scan progress and findings, or [configure a deep
scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans) when you need a more thorough
assessment. Check the [plugin changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) to
confirm which features your installed version supports.

### Review GitHub pull requests for security risks

[Codex Security Review](https://learn.chatgpt.com/docs/security/security-review) analyzes pull-request
changes alongside repository context, threat models, and security guidance.
Configure automatic reviews when a pull request opens or receives new
commits, or request one directly with `@codex security review`.

The feature is available in research preview to eligible ChatGPT Enterprise,
Business, Edu, and Pro customers. It isn't available on Plus, and usage limits
can apply.

> Now in research preview: Codex Security Review

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2085482310636560830) (2026-08-06)

## July 27–31, 2026

### Use GPT-5.6 Terra and Luna at lower rates

GPT-5.6 Terra now costs 20% less, and GPT-5.6 Luna costs 80% less. Input,
cached input, and output rates decreased by the same proportions. The updated
[usage limits and rates](https://learn.chatgpt.com/docs/pricing) make Terra a stronger fit for everyday
work and Luna especially useful for focused coding and high-volume tasks.

> Starting today, we are reducing prices for GPT-5.6 Luna by 80% and GPT-5.6 Terra by 20%

[View @OpenAI on X](https://x.com/OpenAI/status/2082878156483219672) (2026-07-30)

### Find useful context across your browser and open tabs

In the ChatGPT desktop app, the [built-in browser](https://learn.chatgpt.com/docs/browser) can find
pages from your browsing history or search Google directly from its address
bar. ChatGPT can also search your browsing history when a task needs earlier
context.

The [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension) lets you mention open tabs,
bring selected page text into a side chat, ask questions about YouTube videos,
or select **Ask ChatGPT** from a page's context menu. Review and approve
requests to use browser history before ChatGPT includes that information in a
task.

> In Side Chat, ask about a YouTube video, reference your open tabs, or highlight text on a page and ask away.

[View @ChatGPT on X](https://x.com/ChatGPT/status/2082970812584432115) (2026-07-30)

### Review changes across repositories

When a [local project contains more than one
folder](https://learn.chatgpt.com/docs/projects#use-local-projects-for-folders-and-codebases), the
desktop app shows every repository and the lines changed in each one. Select
**Review** to inspect their diffs together without switching between separate
review views.

**Prompt:**

```text
Review the changes across every repository in this project, identify integration risks, and summarize the fixes needed before I open a pull request.
```

### Refine generated images in your conversation

Open a generated image in the expanded viewer, then switch between
**Focused view** and **Canvas view**. Add comments across images, select the
versions you want to keep, and ask for targeted edits without leaving the chat.
Learn more about [image generation](https://learn.chatgpt.com/docs/image-generation).

> ImageGen in Codex just got a new lightbox and canvas.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2082944138635595782) (2026-07-30)

### Find chats that need your attention

The desktop app's new **Activity view** brings together chats you recently
engaged with and work that needs your attention. Select the bell in the sidebar
to open the view.

[Read the July 30 desktop release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-07-30-app).

> The new Activity view in the ChatGPT desktop app brings together conversations that need your attention

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2083288643310133716) (2026-07-31)

### Connect partner tools with Sign in with ChatGPT

**Sign in with ChatGPT** is rolling out in beta to supported plugins and
partner sites, beginning with Airtable, GitLab, HubSpot, Notion, Supabase, and
Vercel. Use it to create or link a partner account with fewer steps, then start
working with that service in ChatGPT or Codex.

Partners receive only your name, email address, and profile picture when
available. Each plugin's requested access still requires a separate review
and approval. Read the [July 29 sign-in
announcement](https://learn.chatgpt.com/docs/changelog#codex-2026-07-29).

### Collaborate in a dedicated academic research workspace

[ChatGPT for Academic Researchers](https://openai.com/index/chatgpt-for-academic-researchers/)
offers eligible faculty and postdoctoral researchers 12 months of complimentary
access to a dedicated ChatGPT workspace. Approved teams can include up to five
verified researchers from the same institution and receive business data
protections and ChatGPT Pro-level usage limits. Participants can use GPT-5.6
across ChatGPT, ChatGPT Work, and Codex for research and coding workflows.

The program covers ChatGPT access, not OpenAI API credits. Eligibility requires
[institutional verification and a qualifying research
paper](https://help.openai.com/en/articles/20001406).

[Watch: We're giving 100,000 academic researchers free access to our frontier models](https://www.youtube.com/watch?v=MLehRytu9Zo)

### Continue Codex tasks more reliably on iOS

ChatGPT for iOS 1.2026.202 reconnects to tasks more reliably when you return to
the app or unlock your device with Face ID. Voice conversations use your chosen
ChatGPT voice and show usage-limit warnings, while the composer now suggests
installed plugins and their skills consistently with the desktop app.

The release also improves pause and resume controls for goals, inline tables
and visual themes, large workspace diffs, selected-text references, and model
restoration. Read the [July 27 iOS release
notes](https://learn.chatgpt.com/docs/changelog#codex-2026-07-27-mobile).

### Compare security scans and manage findings

Hosted Codex Security plugin releases `0.1.14` and `0.1.15` add scan comparisons,
false-positive feedback, scoped `SECURITY.md` policies, and clearer repository
and finding histories. You can select findings for tracking in Linear or GitHub
Issues, with Codex reviewing the proposed action before you approve it.

Use the existing [Codex Security
workbench](https://learn.chatgpt.com/docs/security/plugin/workbench) to review saved scans, findings,
repository history, and remediation in the desktop app. The hosted plugin
catalog offers version `0.1.15`, while the public CLI plugin marketplace
offers version `0.1.11`. Check the [Codex Security plugin
changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) before relying on a new feature.

### Run security scans from the terminal, CI, or TypeScript

The public `@openai/codex-security` CLI and TypeScript SDK reached version
`0.1.5`, with release numbers separate from the Codex Security plugin. Use the
package to [run scans from the CLI](https://learn.chatgpt.com/docs/security/cli), review pull-request
changes and upload SARIF results in [CI](https://learn.chatgpt.com/docs/security/cli/ci), or run
resumable [bulk scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans) across GitHub
repositories or a pinned CSV inventory.

The [Codex Security TypeScript SDK](https://learn.chatgpt.com/docs/security/sdk) also lets you build
scanning, progress reporting, cost controls, and cancellation into your own
tools. The package is public, but running scans still requires Codex Security
access. Some full-repository scans also require Trusted Access for Cyber.

> You can now use it to scan repositories, track findings across runs, verify fixes, and add security checks to CI/CD.

[View @OpenAI on X](https://x.com/OpenAI/status/2082263717916586117) (2026-07-29)

### Organize sessions and extend Codex CLI 0.146.0

[Codex CLI 0.146.0](https://github.com/openai/codex/releases/tag/rust-v0.146.0)
lets you name a new chat with `/new release prep` or `/clear bug bash`, pin
important threads, and switch between side conversations without closing them.
It also adds temporary conversation forks, standalone web search for compatible
custom model providers, executor-provided skills, and support for Agent Plugins
manifests, workspace plugin publishing, and other plugin marketplaces.

For custom clients, the [app server](https://learn.chatgpt.com/docs/app-server) can filter pinned
threads, create in-memory forks, inspect installed connector state, and read
connector metadata. Experimental WebSocket support also connects app-server to
remote Code Mode hosts. Review the
[app-server security requirements](https://learn.chatgpt.com/docs/app-server#connect-the-cli-terminal-ui)
before exposing a remote connection. The release also improves proxy support,
MCP reconnection, terminal responsiveness, and Windows sandbox reliability.

### Use GPT-5.6 Sol for hosted Codex work

[GPT-5.6 Sol](https://learn.chatgpt.com/docs/models#recommended-models) now powers Codex cloud code
review and quality assurance for eligible customers. Sol is the flagship
GPT-5.6 model for complex coding, research, computer use, and security work.
Codex cloud selects its model automatically; Terra and Luna remain available on
supported local and web surfaces.

### Prepare for the GPT-5.4 model retirement

On August 31, GPT-5.4 and GPT-5.4 mini will retire from Codex for users signed
in with ChatGPT. Replace `gpt-5.4` with `gpt-5.6-terra` and `gpt-5.4-mini`
with `gpt-5.6-luna` in workspace defaults, saved model settings, managed
configurations, custom agents, and scheduled tasks.

The OpenAI API and Codex sessions authenticated with an API key are not
affected. Review the [deprecated Codex models](https://learn.chatgpt.com/docs/models#deprecated-codex-models)
and [workspace model
availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability) before the
cutoff.

## July 20–24, 2026

### Talk through work with ChatGPT Voice

[ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice), powered by GPT-Live, lets you talk
through work and coordinate tasks in Chat, Work, and Codex in the ChatGPT desktop
app. Start a new chat or task in voice mode, then ask ChatGPT to start, check, or
steer work in other threads.

On macOS, say, “Take a look at this” to share an [appshot](https://learn.chatgpt.com/docs/appshots) of
your frontmost window when **Screen context** is on.

Voice is available with Plus, Pro, Business, Edu, and Enterprise plans in the
desktop app and through [Remote on iOS](https://learn.chatgpt.com/docs/remote-connections#set-up-mobile-access).

[Watch: Building with ChatGPT Voice](https://www.youtube.com/watch?v=E0ZMOschrTU)

### Work across multiple folders in one local project

Local projects in the ChatGPT desktop app can now include multiple related
folders. Choose a primary folder for new chats, Git operations, and automatic
discovery of `AGENTS.md`, skills, and `config.toml`. Secondary folders remain
available for file search, reading, and editing.

Open **Edit project** to [add folders and choose the primary
folder](https://learn.chatgpt.com/docs/projects#use-local-projects-for-folders-and-codebases).

[Read the July 23 release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-07-23-app).

> Local projects can now include related code, docs, and reference files from multiple folders.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2080390328880951299) (2026-07-23)

## July 13–17, 2026

### Keep Work conversations and Projects together on desktop

The ChatGPT desktop app now keeps Chat and Work conversations together in the
ChatGPT view. Cloud Work conversations sync across web, mobile, and desktop;
local Work conversations stay on your computer. ChatGPT Projects are available
in the desktop app. Codex keeps its dedicated view and separate history for
developer workflows.

[Compare ChatGPT Work and Codex on
desktop](https://learn.chatgpt.com/docs/use-chatgpt#compare-chatgpt-work-and-codex-on-desktop) to choose the
view that fits your task.

**Prompt:**

```text
Open the Launch project, review its files and recent conversations, and continue the launch plan from the latest Work conversation.
```

### Control parallel Codex work with Codex Micro

On July 15, OpenAI and Work Louder launched
[Codex Micro](https://learn.chatgpt.com/docs/features/codex-micro), a limited-run physical control
surface for Codex in the ChatGPT desktop app. Its Agent Keys show the status of
up to six chats and switch between them. Customizable Command Keys, an analog
stick, and a dial can trigger common actions or skills, start push-to-talk, and
adjust reasoning effort without leaving the keyboard.

[Watch: Introducing the Codex Micro](https://www.youtube.com/watch?v=m8uUUUsMD3Y)

### Use GPT-5.6 through Amazon Bedrock

GPT-5.6 Sol, Terra, and Luna reached general availability through Amazon
Bedrock. Local ChatGPT Work and Codex surfaces can use the built-in
[`amazon-bedrock` provider](https://learn.chatgpt.com/docs/amazon-bedrock) with a Bedrock API key or the
AWS SDK credential chain. This includes Work and Codex in the ChatGPT desktop
app, Codex CLI, the IDE extension, and the Codex SDK.

### Inspect Codex task visualizations on iOS

ChatGPT for iOS 1.2026.188 added inline visualizations to Codex tasks and
improved creating and managing tasks from conversations, including reliable
links to newly created tasks. Read the
[July 13 iOS release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-07-13-mobile).

## July 6–10, 2026

<a id="take-on-ambitious-work-with-chatgpt-work"></a>

### Take on ambitious work in ChatGPT

[ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work) in ChatGPT can gather context from
your files and [plugins](https://learn.chatgpt.com/docs/plugins),
take action across workflows, and create reviewable documents, presentations,
spreadsheets, Sites, and other finished work. Powered by
[GPT-5.6](https://learn.chatgpt.com/docs/models), it can break a goal into steps and work for hours while
you follow its progress, answer questions, change direction, and approve
important actions.

[Scheduled tasks](https://learn.chatgpt.com/docs/automations) can keep that work moving when you're away
by running once, on a schedule, when an event occurs, or while monitoring for
changes.

**Prompt:**

```text
Create a launch brief from the attached research and campaign template. Show me the plan and flag missing information before you build the final document, then adapt the approved brief into assets for three markets.
```

[Watch: Meet ChatGPT Work](https://www.youtube.com/watch?v=yRc5HcGJ-Cs)

### Choose the right GPT-5.6 model

The [GPT-5.6 family](https://learn.chatgpt.com/docs/models#recommended-models) offers three recommended
models across ChatGPT Work, the ChatGPT desktop app, Codex CLI, and the Codex IDE
extension. Sol is the flagship for complex coding, computer use, research, and
security work. Terra balances capability and cost for everyday work, while Luna
is the fastest, lowest-cost option. The default **Power** setting uses Sol with
medium reasoning.

[Watch: Meet GPT-5.6](https://www.youtube.com/watch?v=-MPGU2a67Ls)

### Use Codex in the ChatGPT desktop app

On July 9, the Codex app merged into the
[ChatGPT desktop app](https://learn.chatgpt.com/docs/app) for macOS and Windows. Codex keeps its
dedicated coding experience alongside ChatGPT's Chat and Work. The Codex
experience includes inline editing in diffs, pull request review in the side panel, faster
[Computer Use](https://learn.chatgpt.com/docs/computer-use) powered by GPT-5.6, and multi-repository
projects.

Existing Codex app users can update as usual. You can make Codex the default
view, use the Codex logo as the app icon, and access desktop Codex projects from
the ChatGPT mobile app. The updated desktop app is available globally on every
ChatGPT plan, including Free.

[Watch: Codex for Engineering teams](https://www.youtube.com/watch?v=Ga792ftrBu4)

## June 15–19, 2026

### Turn demonstrated workflows into reusable skills

[Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay) lets you show ChatGPT or
Codex a workflow on macOS and turn the demonstration into a reusable skill. Use
it for repetitive tasks that are easier to show than describe, then refine the
generated skill and replay it with new inputs. Initial availability excludes
the EEA, the United Kingdom, and Switzerland, and requires Computer Use.

[Watch: Record & Replay in Codex](https://www.youtube.com/watch?v=ZK3JhU73W18)

<a id="continue-a-task-on-another-host"></a>

### Continue a chat on another host

[Chat handoff](https://learn.chatgpt.com/docs/remote-connections#hand-off-a-chat-between-hosts)
moves a chat and its Git state between your local computer and a connected
remote host. Codex can create or reuse a worktree on the destination, transfer
the chat, and continue from the matching project.

The same desktop release adds bulk actions to scheduled run history, so
you can mark every run as read or archive eligible runs together.

### Browse and review workspaces from iOS

In the ChatGPT mobile app, **Remote** added a workspace file browser, a
directory picker for new chats, expand-and-collapse controls for diffs, and
per-chat or cross-chat MCP approval choices on iOS.

Computer Use, the Chrome extension, Memories, and Chronicle also began
rolling out to the EEA, the United Kingdom, and Switzerland. Memories remain
off by default in those regions, and Chronicle is an opt-in research preview
for ChatGPT Pro subscribers on macOS.

Read the [June 15 iOS](https://learn.chatgpt.com/docs/changelog#codex-2026-06-15-mobile),
[June 16 availability](https://learn.chatgpt.com/docs/changelog#codex-2026-06-16-app), and
[June 18 app](https://learn.chatgpt.com/docs/changelog#codex-2026-06-18-app) release notes.

## June 8–12, 2026

### Debug web apps with Browser Developer mode

[Developer mode](https://learn.chatgpt.com/docs/browser?surface=app#app-developer-mode) gives Codex controlled
access to Chrome DevTools Protocol capabilities in Chrome and the built-in
browser. Codex can inspect network traffic, console output, runtime errors, and
page state while it profiles or debugs your app. Under **Developer mode** in
**Settings** > **Browser**, turn on **Enable full CDP access**. Codex asks for
explicit approval before it uses that access on a website.

Browser use is also up to twice as fast because CDP and DOM snapshot
optimizations reduce browser round trips.

> Illustration: Codex Browser settings with Developer mode enabled

**Prompt:**

```text
Use @Browser to reproduce the slow checkout. Inspect the network timing and console errors, fix the cause, and verify the result.
```

[Watch: Debug web apps with browser use in Codex](https://www.youtube.com/watch?v=bhgYFRZLyKI)

### Bring your setup to Codex

New migration flows can import supported setup from other coding agents during
onboarding. The Codex app also added `/init` for creating project instructions,
plus improved plugin management, browser diagnostics, and completed-chat
summaries.

<a id="set-up-codex-tasks-from-ios"></a>

### Set up Codex chats from iOS

Remote on iOS can now choose a branch, create a worktree, run an environment
setup script, manage goals, and add inline review comments.

Read the [June 9 app](https://learn.chatgpt.com/docs/changelog#codex-2026-06-09-app),
[June 9 iOS](https://learn.chatgpt.com/docs/changelog#codex-2026-06-09-mobile), and
[June 11 app](https://learn.chatgpt.com/docs/changelog#codex-2026-06-11-app) release notes.

## June 1–5, 2026

### Build and deploy websites with Sites

[Sites](https://learn.chatgpt.com/docs/sites) lets ChatGPT create, save, deploy, and inspect websites,
dashboards, internal tools, web apps, and games hosted by OpenAI. Sites has a
dedicated entry point in ChatGPT on the web and desktop, where you can return to
projects and manage hosted environment values and secrets without assembling a
separate deployment stack.

**Prompt:**

```text
Build a responsive launch dashboard from this project with Sites. Validate it at mobile and desktop sizes, then save a version for review. Do not deploy it until I approve the saved version.
```

[Watch: Introducing Sites in Codex](https://www.youtube.com/watch?v=VRvC5smyzso)

### Use Codex with Amazon Bedrock

You can [use Codex with Amazon Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock) for local
workflows with AWS-managed authentication, account controls, and billing.
Remote on iOS also added an optional in-app lock, follow-up behavior settings,
line wrapping for diffs, and SSH connections to Windows machines. The desktop
app added terminal placement controls and activity insights in the profile
view.

[Read all June 2026 release notes](https://learn.chatgpt.com/docs/changelog#month-2026-06).

> OpenAI models and Codex, now in your AWS workflows.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2061564710173224985) (2026-06-01)

## May 25–29, 2026

### Use Windows apps and control Codex remotely

[Computer use](https://learn.chatgpt.com/docs/computer-use#windows-foreground-use) added support for
seeing, clicking, and typing in Windows desktop apps. Install the Computer Use
plugin before starting. On Windows, Codex uses the active desktop and takes
over the foreground while the task runs. Remote connections also support
Windows. In the ChatGPT mobile app, open **Remote** to start work on a Windows
device, or use a Mac running the ChatGPT desktop app and check progress from
elsewhere.

**Prompt:**

```text
Use @Computer to open the Windows app, reproduce the export failure, save a diagnostic file, and summarize the exact steps that trigger the problem.
```

Remote on iOS also added Spotlight and Shortcuts entry points, archived-chat
browsing, `/side`, and options to save or copy rendered images. The desktop app
added chat coordination for local projects and worktrees, content and
branch-name search for past chats, and consistent visual identifiers for
background subagents.

Read the [May 25 iOS](https://learn.chatgpt.com/docs/changelog#codex-2026-05-25-mobile) and
[May 29 app](https://learn.chatgpt.com/docs/changelog#codex-2026-05-28-app) release notes.

[Watch: Windows Computer Use and mobile access for Codex](https://www.youtube.com/watch?v=MPIAB-8VmCo)

## May 18–22, 2026

### Give Codex context from any Mac app with Appshots

[Appshots](https://learn.chatgpt.com/docs/appshots) send the frontmost app window to Codex with a
screenshot and available text when you press both Command keys. Codex gets
working context from design tools, dashboards, documents, and other apps
without requiring you to copy, paste, or describe what's on screen.

**Prompt:**

```text
Use this appshot as the visual reference. Match the selected screen in the app, then open a preview and compare spacing, typography, and color.
```

[Watch: Introducing Appshots in Codex](https://www.youtube.com/watch?v=QKYbGCvNpFo)

### Follow long-running goals

[Goal mode](https://learn.chatgpt.com/docs/prompting#goal-mode) left experimental status and is
available in the Codex app, IDE extension, and CLI for objectives that can take
hours or days. [Locked use](https://learn.chatgpt.com/docs/computer-use#locked-use) lets Codex
continue approved computer-use work after a Mac locks, including through
**Remote** in the ChatGPT mobile app. ChatGPT Business workspaces can also
[share reusable plugin bundles with workspace members](https://developers.openai.com/plugins/build/plugins#share-a-local-plugin-with-your-workspace).

[Read the May 21 launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-05-21).

[Watch: Run long tasks in Codex using goals](https://www.youtube.com/watch?v=rgh0hMYPcd0)

## May 11–15, 2026

### Continue desktop work from mobile

In the ChatGPT mobile app, **Remote** connects to a Mac running the ChatGPT
desktop app. Because work runs on the connected host, your projects, files,
credentials, plugins, skills, and configuration remain available when you
continue from your phone. See [Remote connections](https://learn.chatgpt.com/docs/remote-connections)
to set up a host and pick up work from another device.

> Now in preview: Codex in the ChatGPT mobile app.

[View @OpenAI on X](https://x.com/OpenAI/status/2055016850849993072) (2026-05-14)

### Automate trusted workflows

Hooks reached general availability for running custom commands at key points in
the agent lifecycle. ChatGPT Enterprise admins can also enable
[Codex access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens) for trusted scripts,
schedulers, and private CI runners. Enterprise guidance expanded to cover
managed setup and controls for Codex.

[Read the May 14 launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-05-13-app).

> Codex is getting easier to automate and customize around your code.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2055032115964870838) (2026-05-14)

## May 4–8, 2026

### Work across browser tabs with the Chrome extension

The [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension) can work in
parallel across tabs in the background without taking over your browser. You
control which websites Codex can use, making it practical to combine research,
data entry, and verification across web apps in one task.

**Prompt:**

```text
Compare the open product pages, collect the plan limits in a table, cite each source tab, and flag any differences that need a manual check.
```

The Codex app also added dictation cleanup and a custom dictionary for names,
file paths, and code symbols. ChatGPT Enterprise workspace owners can allow
members to create [Codex access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens) for
trusted, non-interactive local workflows.

Read the [May 5 app](https://learn.chatgpt.com/docs/changelog#codex-2026-05-05-app),
[May 5 access-token](https://learn.chatgpt.com/docs/changelog#codex-2026-05-05), and
[Codex for Chrome](https://learn.chatgpt.com/docs/changelog#codex-2026-05-07) launch notes.

[Watch: Codex can now use Chrome directly on macOS and Windows](https://www.youtube.com/watch?v=b6Mxcv1pyBU)

## April 20–24, 2026

### Use GPT-5.5 for complex work

[GPT-5.5](https://learn.chatgpt.com/docs/models) arrived in Codex as the recommended model for most
tasks, with strengths across implementation, debugging, testing, computer use,
research, and finished knowledge-work outputs.

[Watch: Introducing GPT-5.5](https://www.youtube.com/watch?v=blGtYq9mL18)

### Let Codex operate the browser and review approvals

[Computer Use in the built-in browser](https://learn.chatgpt.com/docs/browser?surface=app#app-computer-use-in-the-browser)
lets Codex click through local development servers and file-backed pages to
reproduce issues and verify fixes. Eligible approval requests can also go
through [automatic approval review](https://learn.chatgpt.com/docs/sandboxing/auto-review),
which shows the review status and risk before the action runs.

**Prompt:**

```text
Use @Browser to open the local app, reproduce the checkout failure, fix it, and verify the flow end to end.
```

[Read the April 23 launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-04-23).

> With GPT-5.5, Codex now gets more of the job done across the browser, files, docs, and your computer.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2047381283358355706) (2026-04-23)

## April 13–17, 2026

### Preview and operate work in one place

The [built-in browser](https://learn.chatgpt.com/docs/browser?surface=app) added live previews and page
comments, while [Computer Use](https://learn.chatgpt.com/docs/computer-use) let Codex see and
operate macOS apps. Together, they made visual implementation and end-to-end
verification part of the same task as the code change.

> Illustration: ChatGPT desktop app with a local web page open in the built-in browser

[Watch: Codex for (almost) everything](https://www.youtube.com/watch?v=Lm7-yFZ5fZQ)

<a id="start-with-a-task-and-keep-it-moving"></a>

### Start with a chat and keep it moving

[Standalone chats](https://learn.chatgpt.com/docs/projects#start-without-a-project) made it
possible to begin without choosing a project folder. The same release added
[scheduled tasks inside a chat](https://learn.chatgpt.com/docs/automations#schedule-a-task-inside-a-chat),
pull-request context, richer file previews, and [Memories](https://learn.chatgpt.com/docs/customization/memories) for
work that spans chats.

[Read the April 16 Codex app release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-04-16-app).

> Automations can now run in the same thread, so Codex can pick up where it left off

[View @OpenAI on X](https://x.com/OpenAI/status/2044828148890812538) (2026-04-16)

## April 6–10, 2026

### Review and ship pull requests in the app

The review experience added collapsible inline comments, inline and detached
review modes, and clearer Git and source context. Pull-request activity,
comments, and push choices then moved into the app alongside workspace file
tabs, so you could inspect a change and respond without switching tools.

Read the [April 9](https://learn.chatgpt.com/docs/changelog#codex-2026-04-09-app) and
[April 10](https://learn.chatgpt.com/docs/changelog#codex-2026-04-10-app) Codex app release notes, or
learn how to [review changes in the app](https://learn.chatgpt.com/docs/code-review?surface=app).

## March 23–27, 2026

### Package workflows as plugins

[Plugins](https://learn.chatgpt.com/docs/plugins) launched as installable bundles of skills,
connectors, and MCP servers. They made complete workflows easier to discover,
install, and share, while redesigned plugin and skill pages made their contents
and status clearer. Search for past chats also arrived that week.

Read the [task search](https://learn.chatgpt.com/docs/changelog#codex-2026-03-24-app),
[plugins launch](https://learn.chatgpt.com/docs/changelog#codex-2026-03-25), and
[Codex app](https://learn.chatgpt.com/docs/changelog#codex-2026-03-25-app) release notes.

> Plugins in Codex? We got you.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2037604273434018259) (2026-03-27)

## March 16–20, 2026

### Branch earlier and choose tools from the composer

You could fork a chat from an earlier message, making it easier to try a new
approach without losing the original path. Model and reasoning commands became
available while drafting, enabled skills appeared in the `@` menu, and GPT-5.4
mini added a faster option for lighter tasks and subagents.

Read the [GPT-5.4 mini](https://learn.chatgpt.com/docs/changelog#codex-2026-03-17),
[chat control](https://learn.chatgpt.com/docs/changelog#codex-2026-03-18-app), and
[skill menu](https://learn.chatgpt.com/docs/changelog#codex-2026-03-19-app) release notes.

> GPT-5.4 mini is more than 2x faster than GPT-5 mini. Optimized for coding, computer use, multimodal understanding, and subagents.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2033953815834333608) (2026-03-17)

## March 9–13, 2026

### Schedule work with the right environment

[Scheduled tasks](https://learn.chatgpt.com/docs/automations) could run locally or in a worktree
with an explicit model and reasoning level. Reusable templates made common
tasks faster to configure, and custom themes made the workspace easier to
personalize.

> Illustration: Scheduled task settings in the ChatGPT desktop app

> Automations are now GA.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2032222711032971548) (2026-03-12)

### Let Codex inspect terminal output

Codex also learned to read the [integrated terminal](https://learn.chatgpt.com/docs/integrated-terminal#run-and-validate-your-project)
for the current chat. It could inspect a running development server or build
output directly instead of asking you to paste it.

**Prompt:**

```text
Every weekday, inspect changes from the last 24 hours, find one likely regression, fix it in a worktree, run the smallest relevant tests, and report the evidence.
```

Read the [March 11](https://learn.chatgpt.com/docs/changelog#codex-2026-03-11-app) and
[March 12](https://learn.chatgpt.com/docs/changelog#codex-2026-03-12-app) Codex app release notes.

## March 2–6, 2026

### Run Codex natively on Windows

The Codex app launched on [Windows](https://learn.chatgpt.com/docs/windows/windows-app) with native PowerShell
and sandbox support, plus worktrees, scheduled tasks, and skills. WSL remained
available for developers who preferred a Linux environment.

> Illustration: Codex app running natively on Windows

[Watch: The Codex app is now on Windows](https://www.youtube.com/watch?v=8hNcRChDrNk)

<a id="move-tasks-between-local-and-worktree"></a>

### Move chats between Local and Worktree

[Local and Worktree handoff](https://learn.chatgpt.com/docs/environments/git-worktrees#working-between-local-and-worktree)
made it possible to move an active chat while preserving its context. GPT-5.4
also arrived in Codex that week for coding, computer use, and longer-context
workflows.

Read the [Windows launch](https://learn.chatgpt.com/docs/changelog#codex-2026-03-04-app),
[worktree handoff](https://learn.chatgpt.com/docs/changelog#codex-2026-03-03-app), and
[GPT-5.4](https://learn.chatgpt.com/docs/changelog#codex-2026-03-05) release notes.

## February 9–13, 2026

### Iterate in real time and branch an approach

GPT-5.3-Codex-Spark entered research preview as a near-instant model for
real-time coding iteration. The app also added chat forking and a
floating, always-on-top chat window, so you could explore another approach or
keep Codex beside an editor or browser.

Read the [Spark](https://learn.chatgpt.com/docs/changelog#codex-2026-02-12) and
[Codex app](https://learn.chatgpt.com/docs/changelog#codex-2026-02-12-app) release notes, or see the
current [model guide](https://learn.chatgpt.com/docs/models).

> Introducing GPT-5.3-Codex-Spark, our ultra-fast model purpose built for real-time coding.

[View @OpenAIDevs on X](https://x.com/OpenAIDevs/status/2022009906329739681) (2026-02-12)

## February 2–6, 2026

### The Codex app launches on macOS

The Codex app launched as a desktop workspace for parallel project chats,
built-in Git review, worktrees, skills, scheduled tasks, and voice dictation.
Those capabilities now live in Codex in the [ChatGPT desktop app](https://learn.chatgpt.com/docs/app).

> Illustration: The original Codex app showing parallel project chats on macOS

[Watch: Introducing the Codex app](https://www.youtube.com/watch?v=HFM3se4lNiw)

### Steer active work and add files

Mid-turn steering made it possible to redirect Codex without stopping an
active response, and file attachments expanded beyond images. These patterns
became the foundation for [steering and queuing](https://learn.chatgpt.com/docs/prompting#steering-and-queuing)
follow-ups with the context Codex needs.

Read the [Codex app launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-02-02) and
[February 5 app release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-02-05-app).
