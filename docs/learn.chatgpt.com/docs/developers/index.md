---
source_type: 'learn'
source_area: 'learn_developers'
source_url: 'https://learn.chatgpt.com/docs/developers'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Developers

Source: https://learn.chatgpt.com/docs/developers

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<CodexDocsOverviewLanding
  title="Developers"
  description="Use Codex with codebases, development environments, automation, and your team's tools."
  intro="Codex supports everyday code work and deeper integrations across local and cloud environments. Its developer workflows span code review, the integrated terminal, reusable skills and plugins, automation with the SDK and App Server, team tools, and reference material for each surface."
  video={{
    title: "What's new in Codex for engineers",
    videoId: "eiQgljOrkWU",
  }}
  primaryCta={{
    label: "Explore workflows",
    href: "/codex/code-review?surface=app",
  }}
  hero={{
    illustration: "developers",
    backgroundImage: "/images/codex/codex-wallpaper-1.webp",
    alt: "Codex outputs, integrated terminal, and code review for a web application",
  }}
  sections={[
    {
      title: "Development workflows",
      description: "Review changes and work with development tools in ChatGPT.",
      pages: [
        {
          title: "Code review",
          description: "Review changes and address feedback before you ship.",
          href: "/codex/code-review",
          icon: "shieldCheck",
        },
        {
          title: "Integrated terminal",
          description:
            "Run commands and inspect output inside the ChatGPT desktop app.",
          href: "/codex/integrated-terminal",
          icon: "terminal",
        },
      ],
    },
    {
      title: "Extend and automate",
      description:
        "Package development workflows and run deterministic automation.",
      pages: [
        {
          title: "Build skills",
          description:
            "Package instructions and resources for repeatable tasks in ChatGPT and Codex.",
          href: "/codex/build-skills",
          icon: "tools",
        },
        {
          title: "Build plugins",
          description: "Package skills and MCP servers for ChatGPT and Codex.",
          href: "/codex/build-plugins",
          icon: "connect",
        },
        {
          title: "Hooks",
          description: "Run custom commands when Codex emits lifecycle events.",
          href: "/codex/hooks",
          icon: "terminal",
        },
      ],
    },
    {
      title: "Environments",
      description: "Choose where development work runs and how it is isolated.",
      pages: [
        {
          title: "Environments",
          description: "Compare local, cloud, and other ways to run a task.",
          href: "/codex/environments/modes",
          icon: "workspace",
        },
        {
          title: "Local environments",
          description:
            "Configure setup scripts and actions for projects and worktrees.",
          href: "/codex/environments/local-environment",
          icon: "terminal",
        },
        {
          title: "Cloud environment",
          description: "Delegate work to a configured cloud environment.",
          href: "/codex/environments/cloud-environment",
          icon: "storage",
        },
        {
          title: "Git worktrees",
          description: "Isolate parallel changes in separate working trees.",
          href: "/codex/environments/git-worktrees",
          icon: "folder",
        },
      ],
    },
    {
      title: "Build with Codex",
      description: "Add Codex to products, systems, and automated workflows.",
      pages: [
        {
          title: "Codex SDK",
          description: "Control Codex programmatically from your application.",
          href: "/codex/codex-sdk",
          icon: "code",
        },
        {
          title: "App Server",
          description: "Integrate with the protocol that powers Codex clients.",
          href: "/codex/app-server",
          icon: "storage",
        },
        {
          title: "MCP Server",
          description:
            "Expose Codex capabilities through Model Context Protocol.",
          href: "/codex/mcp-server",
          icon: "connect",
        },
        {
          title: "GitHub Action",
          description: "Run Codex from GitHub Actions workflows.",
          href: "/codex/github-action",
          icon: "github",
        },
        {
          title: "Non-interactive mode",
          description: "Run Codex from scripts and other automated systems.",
          href: "/codex/non-interactive-mode",
          icon: "terminal",
        },
      ],
    },
    {
      title: "Third-party integrations",
      description: "Delegate and track work from tools your team already uses.",
      pages: [
        {
          title: "GitHub",
          description:
            "Assign work, review changes, and move toward a pull request.",
          href: "/codex/third-party/github",
          icon: "github",
        },
        {
          title: "Slack",
          description:
            "Start Codex chats from external discussions and return results.",
          href: "/codex/third-party/slack",
          icon: "chat",
        },
        {
          title: "Linear",
          description:
            "Assign issues to Codex and follow work through delivery.",
          href: "/codex/third-party/linear",
          icon: "threads",
        },
      ],
    },
    {
      title: "Reference",
      description:
        "Find commands, settings, and plugin submission errors for developer surfaces.",
      pages: [
        {
          title: "CLI customization",
          description:
            "Adjust syntax highlighting, themes, and shell behavior.",
          href: "/codex/cli-customization",
          icon: "terminal",
        },
        {
          title: "Developer commands",
          description:
            "Use commands and slash commands in the desktop app, Codex CLI, and IDE extension.",
          href: "/codex/developer-commands?surface=app",
          icon: "terminal",
        },
        {
          title: "Developer settings",
          description:
            "Configure the desktop app, Codex CLI, and IDE extension for development.",
          href: "/codex/developer-settings?surface=app",
          icon: "settings",
        },
      ],
    },
  ]}
/>
