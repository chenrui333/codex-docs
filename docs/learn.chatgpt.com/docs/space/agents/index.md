---
source_type: 'learn'
source_area: 'learn_space'
source_url: 'https://learn.chatgpt.com/docs/space/agents'
source_kind: 'learn_markdown'
---

# Work with agents in Space

Source: https://learn.chatgpt.com/docs/space/agents

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Work with ChatGPT or a dot in Space to draft, research, or revise a page.
Available agents and connected tools depend on your access.

> Illustration: The page mention menu after typing @, with All, People, Pages, and Chats tabs, ChatGPT to start a task, and My dot to send a prompt to your dot.

<a id="start-with-a-bounded-request"></a>

## Choose how to ask for help

Use the conversation alongside a page for questions, planning, or a revision that
needs discussion. For a small change, select the relevant text, ask ChatGPT or a dot inline,
or add a comment. The controls offered depend on your access.

| Your goal                                        | Where to ask                                                                           | What to review                                 |
| ------------------------------------------------ | -------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Explore a question or discuss a larger revision. | The conversation alongside the page. State whether to answer in chat or edit the page. | The conversation and any requested page edits. |
| Rewrite selected text.                           | Select the text and use **Ask for change**, when offered.                              | The proposed edit before accepting it.         |
| Ask ChatGPT or a dot directly in the page.       | Type `@ChatGPT` or `@dot` followed by your prompt inline.                              | The reply and any changes to the page.         |
| Keep a specific request in a comment discussion. | Mention `@ChatGPT` or `@dot` followed by your prompt.                                  | The reply and any changes to the page.         |

Mentioning ChatGPT or a dot asks that agent to act on your request. A comment to
another person leaves feedback for them. Check the recipient before sending.

> Illustration: A selected sentence in an offsite plan has a comment mentioning @ChatGPT to change its start date. The comment includes the author, timestamp, and an empty Reply composer.

## Use slash commands

Type `/` in a page to open the slash menu. Choose **Generate** to generate text
inline, **Visualize** to create an interactive visualization, or **Image** to add
an image block. In the image block, choose **Generate** and describe the image
you want. See [Add content to a page](https://learn.chatgpt.com/docs/space/pages#add-content-with-the-insert-menu)
and [Generate images](https://learn.chatgpt.com/docs/space/pages#generate-images) for more examples.

> Illustration: The page slash menu after typing /, with Generate to describe what you want to write, Visualize to create an interactive visualization, and Image to upload or generate an image.

## Use dots in Space

You can work with [dots](https://learn.chatgpt.com/docs/dots) directly in ChatGPT Space. Type `@` in a
page to open the mention menu and choose your dot.

Type `@dot` followed by your prompt inline or in a page comment. For example:

<SpaceDotPrompt
  mention="@dot"
  prompt="Summarize the open questions in this page and suggest next steps."
  description="A page paragraph mentions @dot and asks it to summarize the open questions and suggest next steps."
/>

Review your dot's reply and any changes to the page before continuing.

## Revise a launch brief

If a brief names a launch date but the linked plan says it still needs approval,
check the source, then select the sentence and use **Ask for change**, when offered:

> Describe the date as proposed and awaiting approval. Keep the date and
> source link unchanged.

Review the proposed wording before accepting it.

## Verify recurring work separately

Keep Updated isn’t available at launch.

To set up recurring work, ask ChatGPT in chat and review the saved schedule.
Writing a cadence in a page or its instructions doesn't by itself confirm that
a task is scheduled.

After setup, review the saved task, its timing, and whether it's enabled. Then
check an actual run and the resulting page update. These controls depend on
what's available in your account.

For schedule management and execution requirements, see
[Scheduled tasks](https://learn.chatgpt.com/docs/automations).

## Work with others

Collaborators share the page content, but may use different agents, connected
tools, or instructions. Agree on who is changing what and review the result.

See [Collaboration](https://learn.chatgpt.com/docs/space/collaboration) for access and review guidance.
