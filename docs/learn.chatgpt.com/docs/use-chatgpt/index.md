---
source_type: 'learn'
source_area: 'learn_use_chatgpt'
source_url: 'https://learn.chatgpt.com/docs/use-chatgpt'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0"]
---

# Use ChatGPT

Source: https://learn.chatgpt.com/docs/use-chatgpt

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

{/* vale alex.Condescending = NO */}

## Go from idea to useful result

ChatGPT is an AI agent that you communicate with in natural language:

<WorkflowSteps>
1. Start with a question, an idea, rough notes, a file, or a task you need to
   complete.

2. Ask ChatGPT to explain information, develop ideas, draft content, research a
   topic, analyze materials, or create something new.

3. Add the context and tools it needs, such as files, web search, projects, or
   plugins.

4. Review the result, correct the direction, and ask for changes. You don't need
   a perfect first prompt or special commands.

</WorkflowSteps>

## Choose how you want to work

Use Chat for a question or back-and-forth. Turn on Work in the switcher when you
want ChatGPT to carry a larger task through to a reviewable result. Select Codex
when you want developer views or more technical detail, especially for software
development.

| Choose       | When you want to                              | Examples                                                                     |
| ------------ | --------------------------------------------- | ---------------------------------------------------------------------------- |
| Chat         | Work through something with ChatGPT           | Ask a question, search the web, brainstorm, draft a message, compare options |
| ChatGPT Work | Define an outcome and get a reviewable result | Create a deck, analyze files, draft a report, build a project plan           |
| Codex        | Use developer tools and see technical details | Debug code, run tests, review a PR, implement a feature                      |

Use Chat to ask questions, brainstorm, draft or revise text, summarize files,
compare options, or clarify a larger task. In Codex, point to **New chat**, then
select **Quick chat** when that option is available.

When you need a finished, reviewable result, switch to **Work** and describe
what it should include. See [Get started with ChatGPT
Work](https://learn.chatgpt.com/docs/get-started-with-work) for example tasks, prompts, and best
practices.

### What ChatGPT Work can do

ChatGPT Work can plan a task, gather context, use tools, and carry the work
through to a result you can review.

<Illustration description="ChatGPT Work comparing vendors and producing a spreadsheet you can review.">
  <CodexScreenshot
    alt="ChatGPT Work comparing vendors in a spreadsheet"
    lightSrc="/codex/get-started-with-work/comparison-spreadsheet.webp"
    darkSrc="/codex/get-started-with-work/comparison-spreadsheet.webp"
    maxHeight={520}
    class="my-6 p-4 md:p-8"
  />
</Illustration>

Ask it to:

- **Research and analyze information.** Search the web, browse websites,
  compare sources, read files, analyze data, and summarize findings.
- **Use your files and tools.** Bring in uploaded files,
  [projects](https://learn.chatgpt.com/docs/projects), memories, ChatGPT Library, and installed
  [plugins](https://learn.chatgpt.com/docs/plugins). Plugins can provide connected information, reusable
  workflows, and supported actions.
- **Create finished files.** Draft and refine [documents, presentations,
  spreadsheets, and PDF files](https://learn.chatgpt.com/docs/artifacts-viewer). Review the result, ask
  for specific changes, and download the completed file.
- **Create visual and interactive work.** Generate or edit
  [images](https://learn.chatgpt.com/docs/image-generation), make interactive
  [visualizations](https://learn.chatgpt.com/docs/visualizations), and build or share websites and apps
  with [Sites](https://learn.chatgpt.com/docs/sites).
- **Work across websites and apps.** Use the [browser](https://learn.chatgpt.com/docs/browser) to
  research and interact with websites. In the desktop app, use the
  [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension),
  [Computer Use](https://learn.chatgpt.com/docs/computer-use), and [appshots](https://learn.chatgpt.com/docs/appshots) when
  those features are available.
- **Run code and review technical work.** Run code and shell commands, analyze
  data, inspect files, [review code](https://learn.chatgpt.com/docs/code-review), and work with
  repositories your selected environment can access.
- **Delegate and continue longer tasks.** Split independent work across
  [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), follow their progress, and
  keep [long-running work](https://learn.chatgpt.com/docs/long-running-work) active.
- **Repeat useful workflows.** Set up [scheduled
  tasks](https://learn.chatgpt.com/docs/automations) for recurring work and use
  [skills](https://learn.chatgpt.com/docs/skills-and-plugins) to reuse a workflow.
- **Talk through a task.** On supported plans in the desktop app, use
  [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) to start work, check progress, or
  change direction.

Features depend on your plan, platform, region, rollout, and workspace
  settings. Your workspace administrator can control access to ChatGPT Work,
  plugins, browser use, and network access. ChatGPT Work and Codex share [usage
  limits](https://learn.chatgpt.com/docs/pricing).

### Choose cloud or local work

On the web, ChatGPT Work runs in a managed cloud environment. In the desktop
app, you may also be able to choose where a task runs:

- **Cloud:** Run work in an isolated hosted environment. A task can keep going
  after you close the desktop app and continue from the web or mobile app. Cloud
  work can use uploaded files, connected tools, and approved websites.
- **Work locally:** Use files, apps, or the browser on your computer. Local
  work is available in the desktop app when enabled for your account or
  workspace.

ChatGPT shows its progress and pauses when it needs information or approval.
Review consequential actions before approving them, and check the final result
before you use or share it.

<a id="compare-work-mode-and-codex-on-desktop"></a>

### Compare ChatGPT Work and Codex on desktop

ChatGPT Work and Codex have overlapping capabilities. If you
prefer Codex, you can keep using it for research, documents, presentations, and
other knowledge work. When both are available to you, the desktop app changes
the interface and how the agent presents its work.

<ToggleSection title="Detailed comparison">

| Difference          | ChatGPT in Desktop app                                                 | Codex in Desktop app                                              |
| ------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Where to start      | Select **ChatGPT**, then switch to **Work**                            | Select **Codex** in the product selector                          |
| Chats you see       | See chats started with Chat on web and mobile, plus ChatGPT Work chats | Focus on Codex chats and development projects                     |
| Quick chat          | Not available                                                          | When available, access ChatGPT chats from web and mobile in Codex |
| Technical detail    | Hide technical details like Git or shell commands                      | See developer details, including diff and review views            |
| Agent communication | Prefers nontechnical language and finished outputs                     | Can include technical and implementation details                  |
| Pull requests pane  | Not available when using ChatGPT Work                                  | Available when enabled                                            |

</ToggleSection>

### Talk to ChatGPT naturally

Write as if you were explaining the request to a helpful colleague. State what
you want to accomplish, add the details that change the answer, and describe the
format you need. Your first prompt is only a starting point—you can add context
or refine the result with follow-up messages.

**Start simple:**

```text
Help me plan a 30-minute team meeting about our new customer feedback process.
```

**Add context:**

```text
Help me plan a 30-minute team meeting about our new customer feedback process. The audience is a customer support team that hasn't seen the process before. Include five minutes for questions and end with clear next steps.
```

**Choose a format:**

```text
Create a 30-minute agenda for a customer support team that hasn't seen our new customer feedback process before. Include five minutes for questions, end with clear next steps, and format it so I can paste it into a calendar invitation.
```

You can continue with simple directions such as:

- “Make this shorter.”
- “Give me three different approaches.”
- “What assumptions are you making?”
- “Ask me questions before you continue.”

Learn more about [prompting](https://learn.chatgpt.com/docs/prompting), or take the
[AI Foundations course](https://academy.openai.com/home/courses/ai-foundations-juzjs)
for guided practice.

## Bring the right context into ChatGPT

Give ChatGPT the information, tools, and instructions that matter to the task.
You don't need to provide everything—include the context that changes what a
good result looks like.

### Keep related work in a project

Projects help you organize ChatGPT around a topic, goal, or ongoing body of
work. Keep related chats, files, and instructions in one project
when the work will continue over time or depend on the same context. [Learn more
about projects.](https://learn.chatgpt.com/docs/projects)

### Attach files

You can upload or attach documents, presentations, spreadsheets, PDF files, images,
and data exports. Use them when you want ChatGPT to:

- Summarize or compare them.
- Find patterns or inconsistencies.
- Extract, clean, or reorganize information.
- Use them as source material for a new file.

When ChatGPT creates a file, open the preview and check its contents. You can
then ask for changes without starting over. Learn more about
[working with files](https://learn.chatgpt.com/docs/artifacts-viewer).

### Connect tools with plugins

Plugins can connect ChatGPT to the tools and information you use for work, such
as Google Drive, SharePoint, Salesforce, or Gong. Use them when a task depends
on information outside the chat, actions in another system, or a
repeatable workflow.

<Illustration description="ChatGPT plugin directory showing connected tools such as Google Drive, Slack, and SharePoint.">
  <CodexScreenshot
    alt="ChatGPT plugin directory showing connected work tools"
    lightSrc="/codex/get-started-with-work/plugins.webp"
    darkSrc="/codex/get-started-with-work/plugins.webp"
    maxHeight={520}
    class="my-6 p-4 md:p-8"
  />
</Illustration>

Plugin availability depends on your plan, workspace settings, and the plugin
itself. Learn more about [skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins).

## Share a read-only snapshot of a Codex thread

On all Codex plans, you can create a read-only snapshot of a local Codex thread
in the ChatGPT desktop app for macOS. The snapshot doesn't give other people
access to your project or computer.

Before sharing, check who can open the link:

- **Personal account:** Anyone with the link can open the snapshot.
- **Workspace account:** Only authenticated members of the workspace that
  created the snapshot can open it. You can allow everyone in that workspace
  or restrict access to invited people and groups. A workspace administrator
  can turn off workspace share links.

1. Open the thread and select **Share**. You can also use `/share` where slash
   commands are available.
2. For a workspace account, use **Who has access** to choose everyone in your
   workspace or **Only people and groups invited**. For invited-only access,
   add existing workspace members by email or choose workspace groups.
3. Wait for the snapshot to finish uploading, then select **Copy link**.
   Opening the dialog starts the upload, but Codex publishes the snapshot only
   when you select **Copy link**, using your chosen audience and recipients.
4. Open the copied link and review the shared view before sending it to anyone.

A snapshot captures the supported thread content available when you share it.
Later messages and changes don't update the existing snapshot.

Shared snapshots can include user-visible messages, reasoning summaries, image
attachments, images viewed or generated by the agent, and file changes,
including paths and diffs. They don't include the original thread's tool calls,
shell commands, or tool input or output.

Codex redacts known secret patterns before uploading a snapshot. Review the
shared view before sending its link because sensitive content, including file
paths, may remain in messages, images, or diffs.

You can't fork the original thread from a shared snapshot. You can import the
snapshot as an attachment and refer to it in a new thread.

To view or revoke a shared link, open [ChatGPT data
controls](https://chatgpt.com/#settings/DataControls) and select **Shared links**.

## Make the result ready to use

Treat the first result as a draft you can inspect, challenge, and improve. A
polished response can still be incomplete or wrong, so review the details that
matter before you use or share it.

**Check the work:**

- Verify important numbers, names, dates, quotes, and claims.
- Open generated files and inspect every section, tab, slide, or page.
- Confirm that ChatGPT used the correct and most current source material.
- Look for missing information and unsupported assumptions.
- Ask for focused revisions when the result misses the goal.

Then ask ChatGPT to pressure-test the result:

- “What sources did you use for this?”
- “Cite the source for each major claim.”
- “What assumptions did you make?”
- “What information were you unable to access?”
- “What would change your recommendation?”
- “Check this result against the original files.”

If ChatGPT couldn't access a source or complete part of the task, ask it to say
so plainly. An explicit gap is easier to address than a confident guess.

Legal, financial, medical, security, and other high-stakes decisions require
  appropriate expert review. Use ChatGPT to support informed judgment, not
  replace it.

## Next steps

a]:min-w-0 [&>a]:no-underline">
  [Open the quickstart

        <OpenBook />

      Start using ChatGPT with a guided first task.](https://learn.chatgpt.com/docs/quickstart)

[Learn about prompting

      <Chat />

    Write useful prompts for questions, finished work, and coding tasks.](https://learn.chatgpt.com/docs/prompting)

  [Personalize ChatGPT

        <Settings />

      Set preferences and carry useful context across chats.](https://learn.chatgpt.com/docs/personalize)
