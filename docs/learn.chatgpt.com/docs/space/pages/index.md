---
source_type: 'learn'
source_area: 'learn_space'
source_url: 'https://learn.chatgpt.com/docs/space/pages'
source_kind: 'learn_markdown'
---

# Work with pages

Source: https://learn.chatgpt.com/docs/space/pages

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

A page is a document you can edit directly or with ChatGPT. Use it for notes,
plans, research, or a shared reference you want to return to.

<a id="create-a-focused-page"></a>

## Create a page

Select **New page** in the Space sidebar, or ask ChatGPT to create a page from
an existing conversation. Select **Pages** to find pages you've created or can
access.

Give the page a title, then type or paste your content. Add headings, lists,
images, files, and tables as needed.

> Illustration: The Space sidebar, with New page highlighted and navigation for All, Pages, Sites, Images, and Google Drive.

## Add content with the insert menu

Pages organize content into blocks, such as headings, paragraphs, and tables.
Type `/` while editing to open the insert menu and add a new block. Search for the content
you want to add, then choose an option. Alongside headings, lists, and checklists,
the menu offers ways to combine supporting material and interactive content:

- **Table, Code, and Highlight:** Compare information, share code, or call attention to a note.
- **Image and File:** Generate or upload images, or attach files readers can download.
- **Page and Link to page:** Create a subpage or link to an existing page.
- **Files, Pages, and Chats:** Reference existing material without copying it.
- [**Visualize**](https://learn.chatgpt.com/docs/visualizations): Create interactive calculators, diagrams, or screen designs.
- **Prompt, Task, and Agent Instructions:** Add reusable prompts, actions for Codex, or guidance for agents.

> Illustration: Typing adds a heading, generated introduction, table, and image to one page. All content is selected and deleted together before the sequence restarts.

## Work with selected text

Select text on a page to open the floating toolbar. Use **Ask for change** to
describe a revision to the selection, or **Comment** to start a discussion about
that passage.

You can also apply bold, italic, underline, or strikethrough formatting, mark
inline code, and add a link. Open **Text** to change the block style, such as a
heading, list, checklist, or quote.

<PageSelectionIllustration
  askLabel="Ask for change"
  textLabel="Text"
  commentLabel="Comment"
  before="The launch date is"
  selected="September 29."
  ariaLabel="Selected text with a floating toolbar containing Ask for change, bold, italic, underline, strikethrough, inline code, link, Text styles, and Comment."
/>

## Rearrange blocks

Move blocks as your page takes shape. For example, bring a decision above its
supporting research, or move an image next to the explanation it illustrates.

Use the handle beside a block to drag it to a new position in the page. Select
the handle to open the block's options. The handle can also move a list or a
heading's section, so check which content you're moving before dropping it.

## Draft content with Generate

Use **Generate** to write a first draft directly in your page. Open the `/` menu,
choose **Generate**, and describe what you want to add. Include the purpose,
format, and details the draft should preserve. For example:

<PageComposerIllustration
  kind="generate"
  prompt="Write a short introduction for this launch plan. Summarize its goal, name the intended audience, and leave dates that are not confirmed as open questions."
  ariaLabel="Generate composer with a request to draft a launch introduction."
/>

Review the generated text in place. You can accept it, ask for a change, or undo
it. Use Generate when you want new page content; use a Prompt block when you want
to leave a reusable request for readers.

## Generate images

Add an **Image** block from the `/` menu, then choose **Generate** and describe
the image you want. Include the subject, style, and details that matter for your
page. For example: “Create a mountain lake at dusk for a team retreat plan.”

To use an existing image, choose **Attach** instead. See [Image generation](https://learn.chatgpt.com/docs/image-generation)
for more ways to create and refine images.

## Add interactive visualizations

Visualizations let readers explore generated content inside the page.
Use one to explain a process with a diagram, try a screen design, or let readers
adjust inputs in a small calculator. Describe both what to show and how readers
should interact with it.

Type `/visualize` followed by your request, then choose the matching menu option.
For example:

<PageComposerIllustration
  kind="visualize"
  prompt="Create a project budget calculator. Let readers change the team size, number of weeks, and weekly cost per person, and show the total cost."
  ariaLabel="Visualization placeholder with a floating composer requesting a project budget calculator."
/>

The menu also offers starting points for an app, screen design, widget, or
diagram. Review the generated result and try its controls before sharing the
page. To request a revision, describe the visualization and the change you want
in ChatGPT alongside the page.

See [Visualizations](https://learn.chatgpt.com/docs/visualizations) for more examples, prompting tips,
and guidance on refining and sharing a result.

## Add prompts readers can run

A **Prompt** block stores a request that readers can use to start a chat. Add one
from the `/` menu and write the request in the block. For example, a project
page could include:

> Summarize the open decisions on this page and suggest the next three steps.

Use prompts to give readers a starting point for exploring the work, asking
questions, or planning a follow-up. Choose **Chat about this** to run the prompt
while editing, or select the prompt when reading the page.

<a id="mention-people-and-agents"></a>

## Mention people, agents, files, and chats

Type `@` and start a name to mention a person or one of your agents. Use a person
mention to identify an owner or collaborator, and an agent mention to refer to
the agent involved in the work. In a comment, mention **ChatGPT** with a specific
request to ask it to help. See [Collaborate in Space](https://learn.chatgpt.com/docs/space/collaboration)
for working with people and [Work with the agent in Space](https://learn.chatgpt.com/docs/space/agents)
for asking an agent to draft, research, or revise content.

You can also type `@` to find and mention files in Space and your ChatGPT chats.
Use a file mention to connect a plan to its supporting material, or a chat mention
to point readers to a discussion behind a decision. These references keep the
source close to the work without copying its contents into the page.

## Organize related work

Create child pages to group details under a parent page, or keep related pages
in a space for a topic or team. Link to another page when you want to reference
it without moving it.

> Illustration: A cursor drags the Launch checklist heading and its checklist above the Launch overview heading and paragraph. Each section moves together.

### Create subpages

A subpage is a page inside another page. Use subpages to keep a project overview
short while giving research, meeting notes, or detailed plans their own space.
For example, a launch page could contain subpages for customer research and a
communications plan.

In the parent page, type `/` and choose **Page** to create a subpage. Give the
new page a descriptive title so readers can tell what belongs there. To refer
to a page that already exists, choose **Link to page** instead.

Review access as you organize the work. A page can inherit access from its
shared Space or a parent page. See
[Understand inherited access](https://learn.chatgpt.com/docs/space/collaboration#understand-inherited-access).

## Revise the content

<WorkflowSteps>

1. Open the page and ChatGPT alongside it.
2. Describe the change and identify the text to revise. You can ask for a new
   section, a shorter draft, or an update based on a source.
3. Read the updated page. Edit it directly or ask for another change.

</WorkflowSteps>

**Prompt:**

```text
Rewrite the introduction for a reader who is new to this project. Preserve the scope, dates, decisions, and source links. Leave the rest of the page unchanged.
```

## Give wide content more room

Open a table's block handle menu and select **Width**. Choose **Normal**,
**Flexible**, or **Full width** to change how much of the page it uses.

> Illustration: A cursor opens a Space table's block menu, opens Width, and selects Full width. The same table expands from the normal reading column into the page margins.

The table's **Fit** menu offers ways to size its columns. When
offered, try **For readability** to give the content room or **Distribute
columns evenly** for equally sized columns. Review the result on the screen
where you'll use the page.

<a id="review-changes-with-collaborators"></a>

## Comment and collaborate

Share the page with edit access to write together in real time. Use comments
for questions or feedback on a passage. You can also mention ChatGPT in a
comment to ask for help with that part of the page.

When available, select **Show attribution** to see who contributed. See
[Collaboration](https://learn.chatgpt.com/docs/space/collaboration) for sharing and access controls.

> Illustration: A highlighted launch date has a comment thread. Alex asks Sam to confirm the date, and Sam replies that approval is still pending.
