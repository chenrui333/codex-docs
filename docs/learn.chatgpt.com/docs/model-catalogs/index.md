---
source_type: 'learn'
source_area: 'learn_model_catalogs'
source_url: 'https://learn.chatgpt.com/docs/model-catalogs'
source_kind: 'learn_markdown'
---

# Implementing model catalogs for gateways and clouds

Source: https://learn.chatgpt.com/docs/model-catalogs

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

This page is for developers implementing the Codex Models format, which defines
the model catalog and powers the model picker. If you build an inference
provider, such as a gateway or cloud service, use this specification to let the
Codex desktop app and CLI discover your models and use their instructions and
capability settings.

If you administer an enterprise and want to control the model catalog, see the
[`model_catalog_url` configuration guidance](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway#serve-a-remote-catalog).

To support the format, implement an authenticated catalog endpoint. Fetch your
upstream provider's current defaults for the requesting Codex version, apply
your overrides, and return the resulting catalog.

> Illustration: Cloud providers fetch OpenAI model defaults for the requesting Codex version. Gateways read catalogs from their cloud or upstream providers, then apply caller filtering, aliases, and supported settings. Codex reads the gateway catalog to show available models and use compatible settings. Reads are authenticated at each step, and catalog responses return toward Codex. Optional enterprise or custom model definitions can feed the gateway and need not originate from OpenAI.

## Implement the catalog endpoint

The default catalog endpoint is `/models` under the provider's `base_url`.
For example, with `base_url = "https://gateway.example.com/v1"`, Codex requests:

```http
GET /v1/models?client_version=0.162.1
Authorization: Bearer <PROVIDER_ACCESS_TOKEN>
```

Default discovery supports command-backed authentication and Codex-backend
authentication, such as ChatGPT. For a custom provider using API-key authentication
without command-backed authentication, set `model_providers.<id>.model_catalog_url`
explicitly to enable remote discovery. An API key alone doesn't trigger discovery
at the default path.

Use `model_catalog_url` to choose a full catalog URL, such as
`https://gateway.example.com/codex/models`. It can also point to the default
`/v1/models` endpoint. Codex uses this URL directly without appending `/models`.
For API-key discovery, keep `features.api_key_model_discovery` enabled; it is on
by default. Custom headers alone don't enable discovery.

Codex sends the selected provider's authentication and configured headers, and
appends `client_version` and any provider `query_params`. Host the catalog on a
service authorized to receive those credentials.

Authenticate the caller, fetch the corresponding upstream defaults, apply your
overrides, and return the complete `ModelsResponse` JSON directly. Give every
entry a unique, nonempty `slug`. For an explicit `model_catalog_url`, Codex rejects
redirects and responses larger than 1 MiB. Continue enforcing model access on
inference requests.

Remove any effective `model_catalog_json` setting from clients using the endpoint:
the local file takes precedence and prevents remote fetching.

## Match the client's schema

Read the `client_version` query parameter on the catalog request. Codex sends its
CLI version as `major.minor.patch`, with any prerelease suffix removed. For desktop
clients, this is the bundled CLI version.

Use the matching `rust-v<version>` tag in the public Codex repository, or the
exact source commit for a custom build. These links use `rust-v0.162.1`; select
the revision matching your client:

- Read the [`ModelsResponse` and `ModelInfo` response types](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/protocol/src/openai_models.rs) for the schema.
- Inspect the [bundled `models.json`](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/models-manager/models.json) for a complete example. This is catalog data, not a JSON Schema document.

The bundled file is a release snapshot. Fetch current defaults before producing
your catalog.

## Fetch current upstream defaults

Cloud providers serving OpenAI models fetch defaults from OpenAI. Gateways read
their cloud or upstream provider's catalog so they retain the deployed model's
settings and account and region availability. Pass the requesting Codex version
at each step, and authenticate separately to each endpoint.

To fetch defaults directly from OpenAI, call the Codex models endpoint with the
same `client_version`. For example, with an OpenAI API key:

```bash
curl --fail --silent --show-error \
  'https://chatgpt.com/backend-api/codex/models?client_version=0.162.1' \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

For a ChatGPT integration, use the caller's ChatGPT access token and
`ChatGPT-Account-ID` header when applicable. Use credentials authorized for the
upstream endpoint; your gateway's own API key doesn't authenticate to OpenAI.

Parse the full response, including its top-level `models` array. This endpoint
returns Codex metadata such as instructions, reasoning defaults, tool settings,
context limits, and service tiers. The public `/v1/models` endpoint doesn't
supply this catalog.

Refresh these defaults even when the Codex version hasn't changed. Keep requests
scoped to the intended upstream identity and honor response cache controls:
catalogs can depend on the caller's access. Keep your overrides separate so you
can reapply them to fresh defaults.

## Apply provider overrides

Change field values while preserving the version's response structure:

- Filter models to those the caller can use. Map each `slug` to a supported
  inference route, and adjust `display_name`, `description`, or `priority`.
  For an alias without a model migration, set `upgrade` to `null`.
- Set reasoning options, context limits, input modalities, and service tiers to
  values your model and route support. Keep defaults within the supported
  choices. For a route without service tiers, clear `service_tiers` and
  `additional_speed_tiers`, and set `default_service_tier` to `null`.
- Preserve upstream instructions and tool settings unless you have tested a
  replacement. Metadata doesn't add model capabilities or grant inference access.

For Bedrock through LiteLLM, apply the
[required catalog edits](https://learn.chatgpt.com/docs/enterprise/bedrock-through-litellm#prepare-the-client-catalog).
Test the resulting catalog with each supported Codex version.

## Use the public Rust types

Use crates from the same public Git tag or commit as the client's schema:

- Use [`codex-protocol`](https://github.com/openai/codex/tree/rust-v0.162.1/codex-rs/protocol) for `codex_protocol::openai_models::{ModelsResponse, ModelInfo}`. Parse with `serde_json::from_slice::<ModelsResponse>()`, edit `catalog.models`, and serialize the whole wrapper with `serde_json::to_vec()`. The wrapper handles compatibility fields for model instructions.
- Use [`codex-models-manager::bundled_models_response()`](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/models-manager/src/lib.rs) to load that revision's static bundled catalog as a `ModelsResponse`. It doesn't fetch current upstream defaults.
