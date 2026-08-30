---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/plugin-management'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.151.0"]
---

# Plugin management

Source: https://learn.chatgpt.com/docs/enterprise/plugin-management

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Before you begin

Workspace admins can import a plugin marketplace from GitHub and keep its plugins up to date from the repository. A marketplace is a JSON catalog that lists the plugins to import.

Use a GitHub account that can read the marketplace repository and any other repositories it references. Public and private GitHub repositories are supported. Complete any GitHub organization approval required for your repository access before importing.

Review the repository content before importing. New plugins start with **Available** installation and authentication on install. New marketplaces have automatic daily sync enabled. Import processes all valid entries, and future syncs automatically add any new plugins in the repository.

## Configure a marketplace sync

1. Open **Admin** > **Plugins** and select **Add** > **Import marketplace**.
2. In **Source**, enter the repository URL, such as `https://github.com/example/team-plugins`. Use the repository URL only, without a branch or folder URL.
3. If the marketplace is in a subdirectory, enter that directory in **Path**. For example, use `team-tools` for `team-tools/.agents/plugins/marketplace.json`. Leave **Path** empty for the repository root. Do not enter the manifest filename.
4. Optionally enter a **Branch, tag, or commit**. Leave this empty to use the repository's default branch. Use a branch to receive future commits; a fixed commit stays at that revision.
5. Select **Import marketplace** and authorize GitHub access when prompted. The initial import can take up to an hour for very large marketplaces. Subsequent daily syncs typically take a few minutes.
6. Review **Import results**, then open each imported plugin to configure its installation policy and any required apps.

To request an update without waiting for the daily sync, open the marketplace under **Admin** > **Plugins** > **Marketplaces** and select **Sync now**.

## Supported formats

The selected directory must contain one of these files:

| File                               | Format                                                               |
| ---------------------------------- | -------------------------------------------------------------------- |
| `.agents/plugins/marketplace.json` | A Codex marketplace with a `plugins` array.                          |
| `.claude-plugin/marketplace.json`  | A Claude-compatible marketplace with a `plugins` array.              |
| `.claude-plugin/plugin.json`       | A standalone Claude plugin, when no marketplace manifest is present. |

In a marketplace, entries can reference native plugins with `.codex-plugin/plugin.json`, Claude-compatible plugins, Agent Plugins 1.0 packages, or supported skill packages.

For a Codex marketplace, use local paths for plugins in the same repository:

```json
{
  "name": "team-plugins",
  "interface": {
    "displayName": "Team plugins"
  },
  "plugins": [
    {
      "name": "team-tools",
      "source": {
        "source": "local",
        "path": "./plugins/team-tools"
      }
    }
  ]
}
```

The path is relative to the selected marketplace root, not to `.agents/plugins/`.

A Claude-compatible marketplace can use a path string for each local plugin:

```json
{
  "name": "team-plugins",
  "plugins": [
    {
      "name": "team-tools",
      "source": "./plugins/team-tools"
    }
  ]
}
```

Codex marketplace entries also support `source: "url"` for a plugin at a GitHub repository root and `source: "git-subdir"` for a plugin in a GitHub subdirectory. For example:

```json
{
  "name": "team-tools",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/example/team-tools.git",
    "path": "./plugins/team-tools",
    "ref": "main"
  }
}
```

Git sources can select a `ref` or a full 40-character commit `sha`. The authorizing GitHub account must be able to read every referenced repository. Workspace import currently only supports GitHub repositories.

## Configure workspace access

GitHub import and sync do not apply repository installation or authentication policies, including `AVAILABLE`, `INSTALLED_BY_DEFAULT`, `NOT_AVAILABLE`, `ON_INSTALL`, and `ON_USE`. Workspace admins configure these settings for each plugin. Syncing an update or moving an existing plugin to GitHub management preserves its workspace policies.

Use **Installation policy** to choose **Available** or **Installed** for each eligible role. Required apps must also be enabled, and members must have access to the connected service. Importing a plugin does not grant app access or connect members' accounts. See [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors) for role, app, and action controls.

## Move an existing plugin to GitHub management

Add `pluginId` to the existing plugin's marketplace entry:

```json
{
  "name": "team-tools",
  "pluginId": "plugin_0123456789abcdef0123456789abcdef",
  "source": {
    "source": "local",
    "path": "./plugins/team-tools"
  }
}
```

Open the plugin from **Admin** > **Plugins** and copy the ID after `/admin/plugins/` in its URL. Put `pluginId` beside `name` and `source` in the marketplace entry. The existing plugin must be in the same workspace.

This moves an uploaded or otherwise unmanaged workspace plugin to GitHub management. The plugin keeps its ID, sharing, and workspace policies. Future updates come from GitHub; archive uploads can no longer replace the managed plugin. A plugin already managed by another GitHub source cannot be taken over this way.

## Desktop-only plugins

Any imported plugin that declares MCP servers in `mcp.json` or `.mcp.json` is marked **Desktop only** and works only in the ChatGPT desktop app. This includes servers that use a remote HTTPS URL. The same restriction applies to other supported MCP configuration forms, such as inline server declarations.

## Reference an existing app with `.app.json`

Add `.app.json` at the plugin root. The filename includes a leading dot; `app.json` without the dot is not supported.

```json
{
  "apps": {
    "team-tools": {
      "id": "asdk_app_example",
      "required": true
    }
  }
}
```

Replace `asdk_app_example` with the existing app's ID. Supported app IDs start with `asdk_app_`, `connector_`, or `templated_apps_`. Use the app ID, not a `plugin_...` ID. For example, a plugin URL containing `plugin_asdk_app_example` represents the app `asdk_app_example`.

The key `team-tools` names the reference within this file. Set `required` to `true` when the plugin depends on the app. You can add more entries to reference other existing apps.

For a native plugin, set `apps` to `./.app.json` in `.codex-plugin/plugin.json`. Here is a complete manifest for this example:

```json
{
  "name": "team-tools",
  "version": "1.0.0",
  "description": "Use the team's approved tools.",
  "author": {
    "name": "Example team"
  },
  "apps": "./.app.json",
  "interface": {
    "displayName": "Team tools",
    "shortDescription": "Use approved team tools",
    "longDescription": "Connect to the team's existing app.",
    "developerName": "Example team",
    "category": "Productivity",
    "capabilities": ["Read"]
  }
}
```

Keep the files in this layout:

```text
team-plugins/
├── .agents/plugins/marketplace.json
└── plugins/team-tools/
    ├── .codex-plugin/plugin.json
    └── .app.json
```

The reference does not create an app or grant permissions. Admins must make the app available to the intended roles, and members must complete any required authentication. Existing app permissions, action controls, and service access still apply.

## Keep plugins up to date

New marketplaces check for updates daily. Open **Admin** > **Plugins** > **Marketplaces**, select the marketplace, and choose **Sync now** to request an update without waiting for automatic sync.

Sync can add new marketplace entries and update existing plugins. Review changes to the repository before merging them, because automatic sync will import any new plugins.

After a sync, review the status and saved report. **Completed — N errors** means the pass finished but some plugins could not be processed. If an update to an existing plugin is invalid, its last working version is retained. Fix the reported problem in GitHub, then select **Sync now** to retry.

Removing an entry from the repository does not delete its imported workspace copy. It is marked **No longer in source**. Deleting the marketplace in ChatGPT deletes all plugins imported from it.

## Reconnect or change GitHub access

To **reconnect GitHub access**, first confirm that the GitHub account used for the import still has access to the repository and any referenced repositories. The admin who originally imported the marketplace should then open the GitHub plugin in ChatGPT and reconnect their account, since marketplace sync uses that admin’s GitHub connection.

To **transfer to a new owner**, the new workspace admin should open **Admin** > **Plugins** > **Add** > **Import marketplace** and import the same marketplace using the same **Source**, **Path**, and **Branch, tag, or commit** values. Future syncs will use their GitHub connection.

Do not delete the marketplace just to reconnect it or change ownership: deletion also removes its imported plugins.
