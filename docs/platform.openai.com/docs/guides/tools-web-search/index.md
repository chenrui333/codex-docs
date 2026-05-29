---
source_type: 'platform_tool_guide'
source_area: 'tool_guide_web_search'
source_url: 'https://platform.openai.com/docs/guides/tools-web-search'
source_last_modified: '2026-05-11T18:44:02Z'
source_etag: 'W/"c949ffebf2a8619dfde1bde5718b9407"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0"]
---

# Web search

Source: https://platform.openai.com/docs/guides/tools-web-search

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

Using the [Responses API](https://developers.openai.com/api/docs/api-reference/responses), you can enable web search by configuring it in the `tools` array in an API request to generate content. Like any other tool, the model can choose to search the web or not based on the content of the input prompt.

For new Responses API integrations, use `{ "type": "web_search" }`. The earlier `web_search_preview` tool remains available for legacy integrations, but it does not support newer controls such as `filters`, `external_web_access`, and `return_token_budget`.

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

## Run longer web research

`return_token_budget` controls how much web search result content the tool can return during a Responses API search run with GPT-5+ reasoning models. Keep the default for most requests. Set it to `unlimited` only for high-effort research or evaluation runs that need to inspect many pages and might otherwise stop at the standard returned-token cap.

Use `unlimited` selectively because it can increase latency and cost. For long-running multi-search tasks, use background mode (`background: true`) so the request can keep running asynchronously and you can retrieve the final response later.

| Value       | Behavior                                                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `default`   | Uses the standard returned-token budget for web search results. This is the same behavior as omitting `return_token_budget`. |
| `unlimited` | Removes the default returned-token budget for the web search run.                                                            |

This parameter applies only to the hosted Responses API `web_search` tool with GPT-5+ reasoning web search. It does not change the search context window, and it does not apply to non-reasoning web search, legacy Search API paths, container web search, Chat Completions search models, or `web_search_preview`. Only `default` and `unlimited` are supported values; `null`, numbers, and other strings are rejected.

## Domain filtering

Domain filtering in web search lets you limit results to a specific set of domains. With the `filters` parameter you can configure up to 100 `allowed_domains` or up to 100 `blocked_domains`. When formatting domains, omit the HTTP or HTTPS prefix. For example, use `openai.com` instead of `https://openai.com/`. This approach also includes subdomains in the search. Note that domain filtering is only available in the Responses API with the `web_search` tool.

## Sources

To view all URLs retrieved during a web search, use the `sources` field. Unlike inline citations, which show only the most relevant references, sources returns the complete list of URLs the model consulted when forming its response.
The number of sources is often greater than the number of citations. Real-time third-party feeds are also surfaced here and are labeled as `oai-sports`, `oai-weather`, or `oai-finance`. The sources field is available with both the `web_search` and `web_search_preview` tools.

## User location

To refine search results based on geography, you can specify an approximate user location using country, city, region, and/or timezone.

- The `city` and `region` fields are free text strings, like `Minneapolis` and `Minnesota` respectively.
- The `country` field is a two-letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1), like `US`.
- The `timezone` field is an [IANA timezone](https://timeapi.io/documentation/iana-timezones) like `America/Chicago`.

Note that user location is not supported for deep research models using web
  search.

## Live internet access

Control whether the web search tool fetches live content or uses only cached/indexed results in the Responses API.

- Set `external_web_access: false` on the `web_search` tool to run in offline/cache‑only mode.
- Default is `true` (live access) if you do not set it.
- Preview variants (`web_search_preview`) ignore this parameter and behave as if `external_web_access` is `true`.

## Limitations

#### Chat Completions API

The Chat Completions API supports only specialized search models for web search. These models do not support Responses API `web_search` features such as domain filters, complete source lists, live-access control, and returned-token budget control.

| Model                        | Context window | Limitation                                                                                                                                   |
| ---------------------------- | -------------: | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `gpt-5-search-api`           |           200k | Uses the Chat Completions search model path                                                                                                  |
| `gpt-4o-search-preview`      |           128k | Uses the Chat Completions search model path; [deprecated, shutdown 2026-07-23](https://developers.openai.com/api/docs/deprecations#2026-04-22-legacy-gpt-model-snapshots) |
| `gpt-4o-mini-search-preview` |           128k | Uses the Chat Completions search model path; [deprecated, shutdown 2026-07-23](https://developers.openai.com/api/docs/deprecations#2026-04-22-legacy-gpt-model-snapshots) |

#### Responses API

Use the hosted `web_search` tool. The Responses API still accepts `web_search_preview` for legacy integrations, but use `web_search` for new integrations.

For a larger model context window, use `gpt-5.5`. The web search context window remains 128k.

| Model          | Model context window | Limitation                                                                                                                         |
| -------------- | -------------------: | ---------------------------------------------------------------------------------------------------------------------------------- |
| `gpt-4.1`      |                   1M | Search context is limited to 128k                                                                                                  |
| `gpt-4.1-mini` |                   1M | Search context is limited to 128k                                                                                                  |
| `o4-mini`      |                 200k | Search context is limited to 128k; [deprecated, shutdown 2026-10-23](https://developers.openai.com/api/docs/deprecations#2026-04-22-legacy-gpt-model-snapshots) |

For Responses API web search, the search context window is limited to 128k, even when the model context window is larger.

- Web search does not support [`gpt-5`](https://developers.openai.com/api/docs/models/gpt-5) with `minimal` reasoning.
- [`gpt-5.4`](https://developers.openai.com/api/docs/models/gpt-5.4) with reasoning effort set to `none` may produce lower-quality results.
- Responses API web search uses the underlying model's tiered rate limits.
- `web_search_preview` does not support `filters` or `return_token_budget`, and ignores `external_web_access`.
- With `tool_choice: "auto"`, search is optional. Use `tool_choice: "required"` or a specific web search tool choice when search must run.

## Usage notes

<table>
<tbody>

<tr>
  <th>API Availability</th>
  <th>Rate limits</th>
  <th>Notes</th>
</tr>

<tr>
  <td>
    <div className="mb-1 flex items-center gap-2">
      [Responses](https://developers.openai.com/api/docs/api-reference/responses)
    </div>
    <div className="mb-1 flex items-center gap-2">
      [Chat Completions](https://developers.openai.com/api/docs/api-reference/chat)
    </div>
    <div className="mb-1 flex items-center gap-2">
      [Assistants](https://developers.openai.com/api/docs/api-reference/assistants)
    </div>
  </td>
  <td style={{ maxWidth: "150px" }}>
    Same as tiered rate limits for underlying [model](https://developers.openai.com/api/docs/models) used
    with the tool.
  </td>
  <td style={{ maxWidth: "150px" }}>
    [Pricing](https://developers.openai.com/api/docs/pricing#built-in-tools) <br />
    [ZDR and data residency](https://developers.openai.com/api/docs/guides/your-data)
  </td>
</tr>

</tbody>
</table>
