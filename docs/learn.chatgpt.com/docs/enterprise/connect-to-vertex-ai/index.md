---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/connect-to-vertex-ai'
source_kind: 'learn_markdown'
---

# Connect Codex to Google Cloud Vertex AI

Source: https://learn.chatgpt.com/docs/enterprise/connect-to-vertex-ai

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

{"OpenAI models on Google Cloud are in "}
    **private preview**
    {". To use them in your project, "}
    [{"request access"}](https://openai.com/form/openai-on-google-cloud/)
    {"."}

## Before you begin

Ask your administrator for the project ID, model name, and Vertex AI location to use with Codex. Your user or service account needs permission to invoke the model in that project. For help setting up billing, accepting a Marketplace private offer, and enabling the model, see the [Google Cloud prerequisites](https://developers.openai.com/api/docs/guides/google-cloud#before-you-begin).

With the default location, `global`, Google Cloud can process model requests in more than one region. If your organization requires regional processing, confirm which supported location to use with your administrator before you send a request.

## Authenticate on the Codex host

Install the Google Cloud CLI on the machine where Codex runs. For local development, run this command to sign in and set up Application Default Credentials (ADC).

```sh
gcloud auth application-default login
```

If your administrator has provided an ADC file, skip the interactive sign-in and use the file during setup. Codex runs `gcloud auth application-default print-access-token` to get an access token.

<a id="use-interactive-setup"></a>

## Set up Google Cloud in Codex

Use Codex CLI 0.167.0 or later, or Codex desktop app 26.1103.32239 or later.

If you’re already signed in to Codex or don’t see Google Cloud in the sign-in options, [authenticate on the Codex host](#authenticate-on-the-codex-host), then [configure the provider manually](#configure-the-provider). Start a new CLI session or desktop task and [verify a model request](#verify-a-model-request).

<Tabs
  id="gcp-client-setup"
  param="setup"
  ariaLabel="Google Cloud setup by client"
  tabs={[
    { id: "cli", label: "CLI" },
    { id: "desktop", label: "Desktop" },
  ]}
>

1. Start `codex`. Select **Sign in another way**, then **Use Google Cloud Vertex AI**.

![Codex CLI provider selection with Use Google Cloud Vertex AI selected.](https://developers.openai.com/images/codex/google-cloud/cli-provider-selection.webp)

2. Enter the Google Cloud project ID from your administrator.

![Codex CLI Google Cloud setup asking for the project ID.](https://developers.openai.com/images/codex/google-cloud/cli-project-setup.webp)

3. Enter the Vertex AI location, or press Enter to use `global`.
4. Enter the absolute path to your credential JSON file, or press Enter to use ADC on this computer. Codex checks that it can get a token before it saves your settings.
5. [Verify a model request](#verify-a-model-request).

1. On **Sign in another way**, select **Use Google Cloud**.

![Codex desktop provider selection with the Use Google Cloud option.](https://developers.openai.com/images/codex/google-cloud/desktop-provider-selection.webp)

2. On **Set up Google Cloud**, enter the **Project ID** from your administrator.

![Codex desktop Google Cloud setup with project, location, and credential file fields.](https://developers.openai.com/images/codex/google-cloud/desktop-setup.webp)

3. Enter a **Location**, or leave it blank to use `global`.
4. In **Credential file**, enter the absolute path to your credential JSON file or select **Browse…** to choose it. Leave the field blank to use ADC on this computer.
5. Select **Continue**, then [verify a model request](#verify-a-model-request).

</Tabs>

<a id="configure-the-provider"></a>

## Configure the provider manually

In `~/.codex/config.toml`, set `model_provider` to `"gcp"` above any table headers. Set your project ID and location under `[model_providers.gcp]`.

```toml
model_provider = "gcp"

[model_providers.gcp]
project_id = "my-project"
location = "global"
```

If you use an ADC file, add `credential_file = "/absolute/path/to/credentials.json"` under `[model_providers.gcp]`. Codex sets `GOOGLE_APPLICATION_CREDENTIALS` for the authentication command.

You can omit `project_id` if you set `GOOGLE_CLOUD_PROJECT` on the Codex host. If you omit `location`, Codex uses `GOOGLE_CLOUD_LOCATION` when set and otherwise uses `global`.

## Verify a model request

1. Start a new session with `codex` and enter `/model`, or start a new task in the desktop app and open the model picker.
2. Select a model your administrator has enabled for your project and ask it to reply with a short greeting. A reply confirms that Codex can authenticate and call that model.

If credential validation fails, check that the machine running Codex can run `gcloud` and read your credential file, if you specified one. To sign in again with local user credentials, run `gcloud auth application-default login` on that machine.

If authentication succeeds but the model request fails, check that your project ID and location match the model deployment. Ask your administrator to confirm that your user or group has access to the project and that the account running Codex can invoke the model.
