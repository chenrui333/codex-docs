---
source_type: 'platform_tool_guide'
source_area: 'tool_guide_web_search'
source_url: 'https://platform.openai.com/docs/guides/tools-web-search'
source_last_modified: '2026-08-05T18:39:37Z'
source_etag: 'W/"593aa8167ab961879d497974cc752ff7"'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
---

# Web search

Source: https://platform.openai.com/docs/guides/tools-web-search

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Web search allows models to access up-to-date information from the internet and provide answers with sourced citations. To enable this, use the web search tool in the Responses API or, in some cases, Chat Completions.

There are three main types of web search available with OpenAI models:

1. Non‑reasoning web search: The non-reasoning model sends the user’s query to the web search tool, which returns the response based on top results. There’s no internal planning and the model simply passes along the search tool’s responses. This method is fast and ideal for quick lookups.
2. Agentic search with reasoning models is an approach where the model actively manages the search process. It can perform web searches as part of its chain of thought, analyze results, and decide whether to keep searching. This flexibility makes agentic search well suited to complex workflows, but it also means searches take longer than quick lookups. For example, you can adjust reasoning levels on models like `gpt-5.5` to change both the depth and latency of the search.
3. Deep research is a specialized, agent-driven method for in-depth, extended investigations by reasoning models. The model conducts web searches as part of its chain of thought, often tapping into hundreds of sources. Deep research can run for several minutes and is best used with background mode. Use `gpt-5.5` with reasoning set to `high` or `xhigh`.

## Choose an integration

| Use case                                      | Recommended path                              | Notes                                                                                                       |
| --------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| New web search integration                    | Responses API with `web_search` and `gpt-5.5` | Supports hosted web search controls such as filters, sources, live-access control, and longer research runs |
| Existing Chat Completions search integration  | Chat Completions with `gpt-5-search-api`      | Use this only when you need to preserve a Chat Completions integration                                      |
| Multi-step research or long-running reporting | `gpt-5.5` with `high` or `xhigh` reasoning    | Use background mode for reports that can take several minutes                                               |

Using the [Responses API](https://developers.openai.com/api/reference/resources/responses), you can enable web search by configuring it in the `tools` array in an API request to generate content. Like any other tool, the model can choose to search the web or not based on the content of the input prompt.

For new Responses API integrations, use `{ "type": "web_search" }`. The earlier `web_search_preview` tool remains available for legacy integrations, but it does not support newer controls such as `filters`, `external_web_access`, and `return_token_budget`.

Web search tool example

```javascript
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.6",
  tools: [{ type: "web_search" }],
  input: "What was a positive news story from today?",
});

console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    tools=[{"type": "web_search"}],
    input="What was a positive news story from today?",
)

print(response.output_text)
```

```go
package main

#pragma warning disable OPENAI001

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
ResponsesClient client = new(key);

CreateResponseOptions options = new() { Model = "gpt-5.6" };
options.Tools.Add(ResponseTool.CreateWebSearchTool());
options.InputItems.Add(
    ResponseItem.CreateUserMessageItem("What was a positive news story from today?")
);

ResponseResult response = await client.CreateResponseAsync(options);

Console.WriteLine(response.GetOutputText());
```

```ruby
require "openai"

openai = OpenAI::Client.new

response = openai.responses.create(
  model: "gpt-5.6",
  tools: [{type: "web_search"}],
  input: "What was a positive news story from today?"
)

puts(response.output_text)
```

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5.6",
        "tools": [{"type": "web_search"}],
        "input": "what was a positive news story from today?"
}'
```

```bash
openai responses create \
  --model gpt-5.6 \
  --raw-output \
  --transform 'output.#(type=="message").content.0.text' <<'YAML'
tools:
  - type: web_search
input: What was a positive news story from today?
YAML
```

## Output and citations

Model responses that use the web search tool will include two parts:

- A `web_search_call` output item with the ID of the search call, along with the action taken in `web_search_call.action`. The action is one of:
  - `search`, which represents a web search. It will usually (but not always) includes the search `queries` which were searched. Search actions incur a tool call cost (see [pricing](https://developers.openai.com/api/docs/pricing#built-in-tools)).
  - `open_page`, which represents a page being opened. Supported in reasoning models.
  - `find_in_page`, which represents searching within a page. Supported in reasoning models.
- A `message` output item containing:
  - The text result in `message.content[0].text`
  - Annotations `message.content[0].annotations` for the cited URLs

By default, the model's response will include inline citations for URLs found in the web search results. In addition to this, the `url_citation` annotation object will contain the URL, title and location of the cited source.

When displaying web results or information contained in web results to end
  users, inline citations must be made clearly visible and clickable in your
  user interface.

```json
[
  {
    "type": "web_search_call",
    "id": "ws_67c9fa0502748190b7dd390736892e100be649c1a5ff9609",
    "status": "completed",
    "action": {
      "type": "search",
      "query": "latest news about AI"
    }
  },
  {
    "id": "msg_67c9fa077e288190af08fdffda2e34f20be649c1a5ff9609",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "output_text",
        "text": "On March 6, 2025, several news...",
        "annotations": [
          {
            "type": "url_citation",
            "start_index": 2606,
            "end_index": 2758,
            "url": "https://...",
            "title": "Title..."
          }
        ]
      }
    ]
  }
]
```

## Migrating from legacy web search

| If you use                                              | Recommended path                                                                                        | Notes                                                                                                    |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `web_search_preview` in Responses                       | Migrate to `web_search`                                                                                 | `web_search` supports newer controls such as `filters`, `external_web_access`, and `return_token_budget` |
| `gpt-4o-search-preview` or `gpt-4o-mini-search-preview` | Migrate to Responses `web_search`, or use `gpt-5-search-api` if you must stay on Chat Completions       | The preview search models are deprecated and shut down on 2026-07-23                                     |
| Chat Completions search integrations                    | Use `gpt-5-search-api`, or migrate to Responses `web_search` for more tool controls and optional search | Chat Completions search models always search before responding; Responses search is a tool               |

## Search context size

`search_context_size` controls how much context from web search results is made available to the model before it generates a response. Use `low` for simple lookups, `medium` for a balanced default, and `high` when the answer may require more detail from search results. This setting does not set an exact token count or guarantee a specific number of sources or citations.

Set search context size

```javascript
const openai = new OpenAI();

const response = await openai.responses.create({
  model: "gpt-5.6",
  tools: [
    {
      type: "web_search",
      search_context_size: "low",
    },
  ],
  input: "What movie won best picture in 2025?",
});
console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    tools=[
        {
            "type": "web_search",
            "search_context_size": "low",
        }
    ],
    input="What movie won best picture in 2025?",
)

print(response.output_text)
```

```go
package main

#pragma warning disable OPENAI001

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
ResponsesClient client = new(key);

CreateResponseOptions options = new() { Model = "gpt-5.6" };
options.Tools.Add(
    ResponseTool.CreateWebSearchTool(
        searchContextSize: WebSearchToolContextSize.Low
    )
);
options.InputItems.Add(
    ResponseItem.CreateUserMessageItem("What movie won best picture in 2025?")
);

ResponseResult response = await client.CreateResponseAsync(options);

Console.WriteLine(response.GetOutputText());
```

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5.6",
        "tools": [{
            "type": "web_search",
            "search_context_size": "low"
        }],
        "input": "What movie won best picture in 2025?"
    }'
```

## Run longer web research

`return_token_budget` controls how much web search result content the tool can return during a Responses API search run with GPT-5+ reasoning models. Keep the default for most requests. Set it to `unlimited` only for high-effort research or evaluation runs that need to inspect many pages and might otherwise stop at the standard returned-token cap.

Use `unlimited` selectively because it can increase latency and cost. For long-running multi-search tasks, use background mode (`background: true`) so the request can keep running asynchronously and you can retrieve the final response later.

| Value       | Behavior                                                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `default`   | Uses the standard returned-token budget for web search results. This is the same behavior as omitting `return_token_budget`. |
| `unlimited` | Removes the default returned-token budget for the web search run.                                                            |

This parameter applies only to the hosted Responses API `web_search` tool with GPT-5+ reasoning web search. It does not change the search context window, and it does not apply to non-reasoning web search, legacy Search API paths, container web search, Chat Completions search models, or `web_search_preview`. Only `default` and `unlimited` are supported values; `null`, numbers, and other strings are rejected.

Run longer web searches

```javascript
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.6",
  reasoning: { effort: "xhigh" },
  tools: [
    {
      type: "web_search",
      return_token_budget: "unlimited",
    },
  ],
  input: [
    "Research the economic impact of semaglutide on global healthcare systems.",
    "",
    "Do:",
    "- Include specific figures, trends, statistics, and measurable outcomes.",
    "- Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports.",
    "- Include inline citations and return all source metadata.",
    "",
    "Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling.",
  ].join("\n"),
});

console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    reasoning={"effort": "xhigh"},
    tools=[
        {
            "type": "web_search",
            "return_token_budget": "unlimited",
        }
    ],
    input="""Research the economic impact of semaglutide on global healthcare systems.

Do:
- Include specific figures, trends, statistics, and measurable outcomes.
- Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports.
- Include inline citations and return all source metadata.

Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling.""",
)

print(response.output_text)
```

```go
package main

const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.6",
  reasoning: { effort: "low" },
  tools: [
    {
      type: "web_search",
      filters: {
        allowed_domains: [
          "pubmed.ncbi.nlm.nih.gov",
          "clinicaltrials.gov",
          "www.who.int",
          "www.cdc.gov",
          "www.fda.gov",
        ],
        blocked_domains: ["reddit.com", "quora.com", "wikipedia.org"],
      },
    },
  ],
  tool_choice: "auto",
  include: ["web_search_call.action.sources"],
  input:
    "Please perform a web search on how semaglutide is used in the treatment of diabetes.",
});

console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    reasoning={"effort": "low"},
    tools=[
        {
            "type": "web_search",
            "filters": {
                "allowed_domains": [
                    "pubmed.ncbi.nlm.nih.gov",
                    "clinicaltrials.gov",
                    "www.who.int",
                    "www.cdc.gov",
                    "www.fda.gov",
                ],
                "blocked_domains": [
                    "reddit.com",
                    "quora.com",
                    "wikipedia.org",
                ],
            },
        }
    ],
    tool_choice="auto",
    include=["web_search_call.action.sources"],
    input="Please perform a web search on how semaglutide is used in the treatment of diabetes.",
)

print(response.output_text)
```

```go
package main

const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.6",
  reasoning: { effort: "low" },
  tools: [
    {
      type: "web_search",
      search_content_types: ["image", "text"],
      image_settings: {
        max_results: 3,
        caption: true,
      },
    },
  ],
  include: ["web_search_call.results"],
  input:
    "Search for recent images and supporting text sources about the Golden Gate Bridge at sunset.",
});

console.log(response.output);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    reasoning={"effort": "low"},
    tools=[
        {
            "type": "web_search",
            "search_content_types": ["image", "text"],
            "image_settings": {
                "max_results": 3,
                "caption": True,
            },
        }
    ],
    include=["web_search_call.results"],
    input="Search for recent images and supporting text sources about the Golden Gate Bridge at sunset.",
)

print(response.output)
```

```go
package main

const openai = new OpenAI();

const response = await openai.responses.create({
  model: "gpt-5.6",
  tools: [
    {
      type: "web_search",
      user_location: {
        type: "approximate",
        country: "GB",
        city: "London",
        region: "London",
      },
    },
  ],
  input: "What are the best restaurants near me?",
});
console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    tools=[
        {
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "GB",
                "city": "London",
                "region": "London",
            },
        }
    ],
    input="What are the best restaurants near me?",
)

print(response.output_text)
```

```go
package main

#pragma warning disable OPENAI001

string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
ResponsesClient client = new(key);

CreateResponseOptions options = new() { Model = "gpt-5.6" };
options.Tools.Add(
    ResponseTool.CreateWebSearchTool(
        userLocation: WebSearchToolLocation.CreateApproximateLocation(
            country: "GB",
            city: "London",
            region: "London"
        )
    )
);
options.InputItems.Add(
    ResponseItem.CreateUserMessageItem("What are the best restaurants near me?")
);

ResponseResult response = await client.CreateResponseAsync(options);

Console.WriteLine(response.GetOutputText());
```

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5.6",
        "tools": [{
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "GB",
                "city": "London",
                "region": "London"
            }
        }],
        "input": "What are the best restaurants near me?"
    }'
```

## Live internet access

Control whether the web search tool fetches live content or uses only cached/indexed results in the Responses API.

- Set `external_web_access: false` on the `web_search` tool to run in offline/cache‑only mode.
- Default is `true` (live access) if you do not set it.
- Preview variants (`web_search_preview`) ignore this parameter and behave as if `external_web_access` is `true`.

Control live internet access

```bash
curl "https://api.openai.com/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.6",
    "tools": [
      { "type": "web_search", "external_web_access": false }
    ],
    "tool_choice": "auto",
    "input": "Find when the Eiffel Tower opened to the public and cite the source."
  }'
```

```javascript
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.6",
  tools: [{ type: "web_search", external_web_access: false }],
  tool_choice: "auto",
  input: "Find when the Eiffel Tower opened to the public and cite the source.",
});

console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-5.6",
    tools=[{"type": "web_search", "external_web_access": False}],
    tool_choice="auto",
    input="Find when the Eiffel Tower opened to the public and cite the source.",
)
print(resp.output_text)
```

```go
package main
