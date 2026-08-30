---
source_type: 'learn'
source_area: 'learn_administration'
source_url: 'https://learn.chatgpt.com/docs/administration'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0"]
---

# Administration

Source: https://learn.chatgpt.com/docs/administration

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<CodexDocsOverviewLanding
  title="Administration"
  description="Set access and policy boundaries for ChatGPT, Codex developer tools, APIs, plugins, and connected systems."
  intro="Administration covers six related boundaries: ChatGPT workspace access; local runtime policy for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension; Codex cloud eligibility; Platform API access; plugin availability and connector permissions; and permissions in connected systems. Start with workspace identity and access, then apply the runtime and source-system controls required for each deployment."
  primaryCta={{
    label: "Explore authentication",
    href: "/codex/auth?surface=app",
  }}
  hero={{
    illustration: "administration",
    backgroundImage: "/images/codex/codex-wallpaper-1.webp",
    alt: "ChatGPT workspace members, groups, access tokens, and role controls",
  }}
  sections={[
    {
      title: "Getting started",
      description:
        "Start with the rollout guide, then use the reference pages for each control boundary.",
      pages: [
        {
          title: "Admin rollout guide",
          description:
            "Plan access, assign owners, configure controls, and verify the rollout.",
          href: "/codex/enterprise/admin-setup",
          icon: "users",
        },
        {
          title: "ChatGPT Work Overview",
          description:
            "Understand hosted execution, network controls, data boundaries, and audit visibility.",
          href: "/codex/enterprise/chatgpt-work-overview",
          icon: "shieldCheck",
        },
        {
          title: "ChatGPT Work cloud security",
          description:
            "Review hosted execution, connected accounts, access controls, retention, and audit visibility.",
          href: "/codex/enterprise/chatgpt-work-cloud-security",
          icon: "shieldCheck",
        },
        {
          title: "ChatGPT Work local security",
          description:
            "Review local execution, device and browser access, managed policies, data handling, and audit limitations.",
          href: "/codex/enterprise/chatgpt-work-local-security",
          icon: "shieldCheck",
        },
        {
          title: "ChatGPT Work admin FAQ",
          description:
            "Review access, data, governance, usage, and incident controls for ChatGPT Work.",
          href: "/codex/enterprise/work-admin-faq",
          icon: "userLock",
        },
        {
          title: "ChatGPT Work: usage and cost",
          description:
            "Understand shared credits, billing impact, spending controls, and adoption planning.",
          href: "/codex/enterprise/chatgpt-work-usage-and-cost",
          icon: "dataControls",
        },
      ],
    },
    {
      title: "Identity and authentication",
      description:
        "Choose how people sign in and issue credentials for programmatic workflows.",
      pages: [
        {
          title: "Authentication overview",
          description:
            "Compare sign-in methods, credential storage, and enforcement controls.",
          href: "/codex/auth",
          icon: "key",
        },
        {
          title: "Workload identity",
          description:
            "Let trusted workloads use Codex without long-lived credentials.",
          href: "/codex/enterprise/workload-identity",
          icon: "key",
        },
        {
          title: "Personal Access Tokens",
          description: "Create and manage tokens for programmatic access.",
          href: "/codex/enterprise/access-tokens",
          icon: "lock",
        },
        {
          title: "Service accounts",
          description:
            "Create and manage workspace identities for automated workflows.",
          href: "/codex/enterprise/service-accounts",
          icon: "robot",
        },
      ],
    },
    {
      title: "Workspace access, policy, and models",
      description:
        "Assign ChatGPT workspace access and keep it separate from local runtime policy, Codex cloud access, and Platform API access.",
      pages: [
        {
          title: "Groups and provisioning",
          description:
            "Manage manual and SCIM groups, provisioning, and rollout cohorts.",
          href: "/codex/enterprise/groups-and-provisioning",
          icon: "users",
        },
        {
          title: "Roles and workspace permissions",
          description:
            "Use the canonical map of workspace, runtime, API, plugin, and source-system controls.",
          href: "/codex/enterprise/roles-and-workspace-permissions",
          icon: "userLock",
        },
        {
          title: "GPTs and Sharing",
          description:
            "Manage GPT sharing, ownership, connected apps, and third-party actions across your workspace.",
          href: "/codex/enterprise/gpts-and-sharing",
          icon: "userLock",
        },
        {
          title: "Managed configuration",
          description:
            "Distribute managed settings where supported and enforce runtime requirements for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension.",
          href: "/codex/enterprise/managed-configuration",
          icon: "dataControls",
        },
        {
          title: "Prisma AIRS",
          description:
            "Apply workspace-wide security policies to Codex prompts.",
          href: "/codex/enterprise/prisma-airs",
          icon: "shieldCheck",
        },
        {
          title: "HIPAA configuration",
          description:
            "Configure local runtime safeguards for workflows that may handle protected health information.",
          href: "/codex/hipaa-configuration",
          icon: "shieldCheck",
        },
        {
          title: "Workspace model availability",
          description:
            "Separate model access for ChatGPT, Codex in the ChatGPT desktop app, Codex CLI, the IDE extension, Codex cloud, and the Platform API.",
          href: "/codex/enterprise/workspace-model-availability",
          icon: "settings",
        },
      ],
    },
    {
      title: "Plugin and connector controls",
      description:
        "Control plugin installation, bundled skills, connector-backed capabilities, and connected-service access.",
      pages: [
        {
          title: "Plugin controls",
          description:
            "Manage plugin availability, connector access and actions, and source-system permissions.",
          href: "/codex/enterprise/apps-and-connectors",
          icon: "connect",
        },
        {
          title: "Plugin management",
          description: "Import and sync workspace plugins from GitHub.",
          href: "/codex/enterprise/plugin-management",
          icon: "connect",
        },
        {
          title: "Skill controls",
          description:
            "Compare ChatGPT workspace, local filesystem, and plugin skill controls.",
          href: "/codex/enterprise/skills",
          icon: "tools",
        },
      ],
    },
    {
      title: "Usage, governance, and compliance",
      description:
        "Measure adoption and route reporting or audit data to the system that owns it.",
      pages: [
        {
          title: "Governance",
          description:
            "Choose the right analytics, spend, and audit surface for each question.",
          href: "/codex/enterprise/governance",
          icon: "shieldCheck",
        },
        {
          title: "Admin plugin",
          description:
            "Use the Admin plugin for permissions, approvals, and supported administrative workflows.",
          href: "/codex/enterprise/admin-plugin",
          icon: "tools",
        },
        {
          title: "Workspace analytics",
          description:
            "Review workspace-level ChatGPT adoption and Codex usage.",
          href: "/codex/enterprise/workspace-analytics",
          icon: "dataControls",
        },
        {
          title: "Analytics API",
          description:
            "Automate developer activity and code review reporting with the Codex Analytics API.",
          href: "/codex/enterprise/analytics-api",
          icon: "code",
        },
        {
          title: "Compliance API and audit events",
          description:
            "Export activity records for audit and investigation workflows.",
          href: "/codex/enterprise/compliance-api",
          icon: "userLock",
        },
      ],
    },
    {
      title: "Deployment and model providers",
      description:
        "Deploy and update desktop apps, connect managed hosts, or configure a supported external model provider.",
      pages: [
        {
          title: "Manage app updates",
          description:
            "Control desktop app updates and deploy approved versions through your device management platform.",
          href: "/codex/enterprise/manage-app-updates",
          icon: "settings",
        },
        {
          title: "Windows app deployment",
          description:
            "Choose an installation and update path for managed Windows devices.",
          href: "/codex/enterprise/windows-deployment",
          icon: "settings",
        },
        {
          title: "Remote connections",
          description: "Start and control work on connected computers.",
          href: "/codex/remote-connections",
          icon: "connect",
        },
        {
          title: "Amazon Bedrock",
          description:
            "Configure supported local clients to use models available through Bedrock.",
          href: "/codex/amazon-bedrock",
          icon: "storage",
        },
      ],
    },
  ]}
/>
