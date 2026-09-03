---
source_type: 'learn'
source_area: 'learn_webmcp'
source_url: 'https://learn.chatgpt.com/docs/webmcp'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0", "0.152.0", "0.152.1", "0.153.0"]
codex_cli_versions_raw: ["codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0"]
---

# Site tools

Source: https://learn.chatgpt.com/docs/webmcp

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Site tools are ChatGPT's implementation of the proposed
[WebMCP standard](https://webmachinelearning.github.io/webmcp/). With WebMCP,
a website can offer useful actions directly to an AI agent alongside the
interface people already use. You and the agent can work with the same live
page and signed-in session.

In the [built-in browser](https://learn.chatgpt.com/docs/browser) in the ChatGPT desktop app, ChatGPT
Work and Codex can discover and use these tools when they are available.

Use GPT-5.6 Sol or GPT-5.6 Terra for site tools. GPT-5.6 Luna currently has
  WebMCP disabled. Update the ChatGPT desktop app to the latest version. Site
  tools aren't available in Enterprise or Edu workspaces. Availability also
  depends on rollout and the tools provided by the current page.

## WebMCP vs. MCP

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/learn/architecture)
connects an AI application to a local or remote server. Its tools can work
independently of an open webpage, such as searching a service or managing
records through an API.

[WebMCP](https://github.com/webmachinelearning/webmcp) lets a website make its
capabilities available to an agent as a set of predefined tools. The agent can
discover them when it visits, so people don't need to install a separate MCP
server or set up another connection to use those capabilities.

This approach is useful when you and the agent need to see the same thing, such as
when editing a canvas or exploring a dashboard. A
[plugin with an MCP server](https://learn.chatgpt.com/docs/build-plugins) can provide an integration
that works independently of an open page. A website can support both.

## How it works in the browser

Open a website in the built-in browser and ask ChatGPT Work or Codex to help
with a task. If the page offers site tools, the agent can discover and use the
relevant actions in the website you're viewing. For example, a document
editor might let the agent find a section or leave a comment for you to review.

Select **Site tools** in the browser's address bar to see what the website
provides. Choose **Available site tools** to inspect the individual tools. The
browser checks each request before the website carries it out, and the agent
can inspect the page to see what changed. When recent activity is available,
choose **Recently used** to open **Sources** and review those calls.

In this example, expand **Available site tools** to inspect the tools provided
by [Margin](https://margin-local-docs.openai.chatgpt.site).

> Illustration: ChatGPT's built-in browser showing the Site tools menu for Margin, with 10 available tools.

Tools belong to the page that provides them. Closing or navigating away from a
page can make its tools unavailable. If no suitable tool is available, the
agent may still be able to use its regular browser capabilities.

## Example: Explore OpenAI documentation

ChatGPT Learn and OpenAI Developers offer site tools for finding and reading
documentation. Select **Open in ChatGPT** in the composer to open Learn in the
desktop app's browser beside a new chat with this prompt ready to send.

**Prompt:**

```text
Find the documentation for building reusable skills, open the relevant page, and explain when I should turn a skill into a plugin.
```

The agent can use these tools to search, read, and open the relevant page:

| Tool                    | What it does                                                             |
| ----------------------- | ------------------------------------------------------------------------ |
| `search_openai_docs`    | Searches OpenAI documentation.                                           |
| `lookup_page`           | Reads a documentation page by path or URL.                               |
| `lookup_context`        | Reads the current docs route and selected text.                          |
| `navigate_to_page`      | Opens a matching page on the current documentation site.                 |
| `generate_custom_guide` | Starts a custom build or learning guide and returns its status and link. |

Docs Agent generates a custom guide asynchronously. Receiving its link doesn't
mean generation has finished.

## Security and user controls

Website-provided tool definitions and results are untrusted content. A tool's
name or claim that it only reads data isn't proof of what it does. Website
instructions don't give the agent permission to share unrelated information or
take sensitive actions.

In the built-in browser, each tool invocation receives a safety review before
it runs. Normal website-access and confirmation policies still apply, including
for consequential actions such as sending messages, making purchases, deleting
data, or changing permissions. The browser ties each invocation to its
originating page and tool registration. These checks reduce risk; they don't
make a website or its output trustworthy.

You can turn off **Enable site tools** in **Settings > Browser > Permissions**.
Review the site, requested action, and result before sharing sensitive
information or relying on a change.

Report security vulnerabilities through OpenAI's
[Security Bug Bounty program](https://bugcrowd.com/engagements/openai). For AI
safety risks, see the
[Safety Bug Bounty program](https://openai.com/index/safety-bug-bounty/). Follow
each program's scope and submission instructions.

## Limitations

ChatGPT's built-in browser currently supports a subset of the WebMCP APIs.
The following features aren't supported:

- **Declarative API:** Tools defined through HTML form attributes aren't
  available as site tools.
- **Tools in iframes:** The browser doesn't discover tools registered inside
  iframes, including same-origin and cross-origin iframes.

Use JavaScript to register tools in the top-level page, as shown in the
[next section](#add-webmcp-to-your-website). ChatGPT Work and Codex may still
interact with forms using regular browser capabilities, but those interactions
aren't WebMCP tool calls.

The WebMCP specification and Chrome's developer guide describe the broader
APIs, including features that aren't currently supported in the built-in browser.

## Add WebMCP to your website

You can ask Codex to add WebMCP support to the web app or
[Site](https://learn.chatgpt.com/docs/sites) you're working on. Describe what an agent should be able
to do, and ask Codex to reuse the application's existing logic and permissions.

Start with an operation your application already supports. For example:

- A dashboard that lets the agent set a date range and inspect the data behind
  a chart.
- A document editor that lets the agent find a section, suggest an edit, or
  leave a comment for you to review.
- A travel planner that lets the agent compare options and update an itinerary
  while you inspect the map.

You can also write the code yourself. In your page's JavaScript module, check
for browser support and register a tool. This read-only example returns the
current page's title:

```javascript
if (typeof document.modelContext?.registerTool === "function") {
  await document.modelContext.registerTool({
    name: "get_page_title",
    description: "Read the title of the current page.",
    inputSchema: {
      type: "object",
      properties: {},
      additionalProperties: false,
    },
    annotations: { readOnlyHint: true },
    execute: async () => ({ title: document.title }),
  });
}
```

A compatible agent can discover `get_page_title` and receive the page's
current title. For a tool that accepts arguments, describe them in the input
schema and use them in the `execute` handler to call your application's
existing logic.

Keep inputs narrow, describe side effects, and return enough information to
verify the result. Use your application's existing authentication,
authorization, and input validation. Preserve the normal interface for people
and browsers that don't support WebMCP.

For API details and examples, see the
[WebMCP specification](https://webmachinelearning.github.io/webmcp/) and
[Chrome's developer guide](https://developer.chrome.com/docs/ai/webmcp).
