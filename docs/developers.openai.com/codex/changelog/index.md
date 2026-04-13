# Changelog – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/changelog

#### Agent internet access

![](/images/codex/changelog/internet_access.png)

Now you can give Codex access to the internet during task execution to install dependencies, upgrade packages, run tests that need external resources, and more.

Internet access is off by default. Plus, Pro, and Business users can enable it for specific environments, with granular control of which domains and HTTP methods Codex can access. Internet access for Enterprise users is coming soon.

Learn more about usage and risks in the [docs](/codex/cloud/agent-internet).

#### Update existing PRs

![](/images/codex/changelog/update_prs.png)

Now you can update existing pull requests when following up on a task.

#### Voice dictation

![](/images/codex/changelog/voice_dictation.gif)

Now you can dictate tasks to Codex.

#### Fixes & improvements

- Added a link to this changelog from the profile menu.
- Added support for binary files: When applying patches, all file operations are supported. When using PRs, only deleting or renaming binary files is supported for now.
- Fixed an issue on iOS where follow up tasks where shown duplicated in the task list.
- Fixed an issue on iOS where pull request statuses were out of date.
- Fixed an issue with follow ups where the environments were incorrectly started with the state from the first turn, rather than the most recent state.
- Fixed internationalization of task events and logs.
- Improved error messages for setup scripts.
- Increased the limit on task diffs from 1 MB to 5 MB.
- Increased the limit for setup script duration from 5 to 10 minutes.
- Polished GitHub connection flow.
- Re-enabled Live Activities on iOS after resolving an issue with missed notifications.
- Removed the mandatory two-factor authentication requirement for users using SSO or social logins.

