# Quickstart

Source: https://developers.openai.com/codex/quickstart

Start using Codex in your IDE, CLI, or the cloud

ChatGPT Plus, Pro, Business, Edu, and Enterprise plans include Codex. Using Codex with your ChatGPT subscription gives you access to the latest Codex models and features.

You can also use Codex with API credits by signing in with an OpenAI API key.

For a limited time, **try Codex for free in ChatGPT Free and Go**, or enjoy
**2x Codex rate limits** with Plus, Pro, Business and Enterprise
subscriptions.

## Setup

Choose an option

AppRecommended (macOS only)IDE extensionCodex in your IDECLICodex in your terminalCloudCodex in your browser

The Codex app is available on macOS (Apple Silicon).

1. Download and install the Codex app

   The Codex app is currently only available for macOS.

   [Download for macOS](https://persistent.oaistatic.com/codex-app-prod/Codex.dmg)

   [Get notified for Windows and Linux](https://openai.com/form/codex-app/)
2. Open Codex and sign in

   Once you downloaded and installed the Codex app, open it and sign in with your ChatGPT account or an OpenAI API key.

   If you sign in with an OpenAI API key, some functionality such as [cloud threads](/codex/prompting#threads) might not be available.
3. Select a project

   Choose a project folder that you want Codex to work in.

If you used the Codex app, CLI, or IDE Extension before you’ll see past projects that you worked on.

4. Send your first message

   After choosing the project, make sure **Local** is selected to have Codex work on your machine and send your first message to Codex.

   You can ask Codex anything about the project or your computer in general. Here are some examples:

   ![](/codex/colorcons/brain.png)Tell me about this projectCopied![](/codex/colorcons/gamepad.png)Build a classic Snake game in this repo.Copied![](/codex/colorcons/search.png)Find and fix bugs in my codebase with minimal, high-confidence changes.Copied

   If you need more inspiration, check out the [explore section](/codex/explore).

   [Learn more about the Codex app](/codex/app)

Install the Codex extension for your IDE.

1. Install the Codex extension

   Download it for your editor:

   - [Download for Visual Studio Code](vscode:extension/openai.chatgpt)
   - [Download for Cursor](cursor:extension/openai.chatgpt)
   - [Download for Windsurf](windsurf:extension/openai.chatgpt)
   - [Download for Visual Studio Code Insiders](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)
2. Open the Codex panel

   Once installed, the Codex extension appears in the sidebar alongside your other extensions. It may be hidden in the collapsed section. You can move the Codex panel to the right side of the editor if you prefer.
3. Sign in and start your first task

   Sign in with your ChatGPT account or an API key to get started.

   Codex starts in Agent mode by default, which lets it read files, run commands, and write changes in your project directory.

   ![](/codex/colorcons/brain.png)Tell me about this projectCopied![](/codex/colorcons/gamepad.png)Build a classic Snake game in this repo.Copied![](/codex/colorcons/search.png)Find and fix bugs in my codebase with minimal, high-confidence changes.Copied
4. Use Git checkpoints

   Codex can modify your codebase, so consider creating Git checkpoints before and after each task so you can easily revert changes if needed.

   [Learn more about the Codex IDE extension](/codex/ide)

The Codex CLI is supported on macOS, Windows, and Linux.

1. Install the Codex CLI

   Install with npm:

   ```
   npm install -g @openai/codex
   ```

   Install with Homebrew:

   ```
   brew install codex
   ```
2. Run `codex` and sign in

   Run `codex` in your terminal to get started. You’ll be prompted to sign in with your ChatGPT account or an API key.
3. Ask Codex to work in your current directory

   Once authenticated, you can ask Codex to perform tasks in the current directory.

   ![](/codex/colorcons/brain.png)Tell me about this projectCopied![](/codex/colorcons/gamepad.png)Build a classic Snake game in this repo.Copied![](/codex/colorcons/search.png)Find and fix bugs in my codebase with minimal, high-confidence changes.Copied
4. Use Git checkpoints

   Codex can modify your codebase, so consider creating Git checkpoints before and after each task so you can easily revert changes if needed.

[Learn more about the Codex CLI](/codex/cli)

Use Codex in the cloud at [chatgpt.com/codex](https://chatgpt.com/codex).

1. Open Codex in your browser

   Go to [chatgpt.com/codex](https://chatgpt.com/codex). You can also delegate a task to Codex by tagging `@codex` in a GitHub pull request comment (requires signing in to ChatGPT).
2. Set up an environment

   Before starting your first task, set up an environment for Codex. Open the environment settings at [chatgpt.com/codex](https://chatgpt.com/codex/settings/environments) and follow the steps to connect a GitHub repository.
3. Launch a task and monitor progress

   Once your environment is ready, launch coding tasks from the [Codex interface](https://chatgpt.com/codex). You can monitor progress in real time by viewing logs, or let tasks run in the background.

   ![](/codex/colorcons/brain.png)Tell me about this projectCopied![](/codex/colorcons/brain.png)Explain the top failure modes of my application's architecture.Copied![](/codex/colorcons/search.png)Find and fix bugs in my codebase with minimal, high-confidence changes.Copied
4. Review changes and create a pull request

   When a task completes, review the proposed changes in the diff view. You can iterate on the results or create a pull request directly in your GitHub repository.

   Codex also provides a preview of the changes. You can accept the PR as is, or check out the branch locally to test the changes:

   ```
   git fetch
   git checkout <branch-name>
   ```

   [Learn more about Codex cloud](/codex/cloud)

