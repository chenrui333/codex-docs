---
source_type: 'learn'
source_area: 'learn_administration'
source_url: 'https://learn.chatgpt.com/docs/administration'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Administration

Source: https://learn.chatgpt.com/docs/administration

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<CodexDocsOverviewLanding
  title="Administration"
  description="Set access and policy boundaries for ChatGPT, Codex developer tools, APIs, plugins, and connected systems."
  intro="Start with workspace identity and access. Then configure local runtime policy for supported capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension; Codex cloud eligibility; Platform API access; plugins and connectors; and permissions in connected systems."
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
        "Plan your rollout and explore tools for routine administration.",
      pages: [
        {
          title: "Admin rollout guide",
          description:
            "Plan access, assign owners, configure controls, and verify the rollout.",
          href: "/codex/enterprise/admin-setup",
          icon: "users",
        },
        {
          title: "Admin plugin",
          description:
            "Use the Admin plugin for permissions, approvals, and supported administrative workflows.",
          href: "/codex/enterprise/admin-plugin",
          icon: "tools",
        },
      ],
    },
    {
      title: "Feature setup",
      description:
        "Choose a setup task, then review its access and security requirements.",
      pages: [
        {
          title: "Configure dots permissions",
          description:
            "Manage dots access, communication, computers, and custom rules.",
          href: "/codex/dots/controls#for-workspace-admins",
          icon: "shieldCheck",
        },
        {
          title: "Manage Space sharing and access",
          description:
            "Control Library sharing permissions and help members share pages.",
          href: "/codex/space/collaboration#for-workspace-admins",
          icon: "userLock",
        },
        {
          title: "Set up teams and Team Tasks",
          description:
            "Set team permissions, connect shared accounts, and create recurring tasks.",
          href: "/codex/enterprise/teams#for-workspace-admins",
          icon: "users",
        },
        {
          title: "Set up @ChatGPT in Slack or Teams",
          description:
            "Review administrator responsibilities and deployment prerequisites.",
          href: "/codex/enterprise/chatgpt-slack-and-teams",
          icon: "chat",
        },
        {
          title: "Set up a workspace connection",
          description:
            "Prepare company-managed accounts and configure a workspace connection.",
          href: "/codex/enterprise/shared-connections#set-up-a-connection",
          icon: "connect",
        },
        {
          title: "Local computer access for Work Cloud and dots",
          description:
            "Review shared policies and compatibility, then enable local computer access separately for Work and dots.",
          href: "/codex/enterprise/cloud-local-access#how-to-set-up-local-computer-access",
          icon: "settings",
        },
        {
          title: "Set up Sites and connected plugins",
          description:
            "Enable tenant and plugin access so Sites can use visitors' connected accounts.",
          href: "/codex/enterprise/sites#enable-plugin-use-in-sites",
          icon: "connect",
        },
      ],
    },
    {
      title: "Identity and access",
      description: "Manage sign-in, provisioning, roles, and credentials.",
      pages: [
        {
          title: "Authentication overview",
          description:
            "Compare sign-in methods, credential storage, and enforcement controls.",
          href: "/codex/auth",
          icon: "key",
        },
        {
          title: "Groups and provisioning",
          description:
            "Manage manual and SCIM groups, provisioning, and rollout cohorts.",
          href: "/codex/enterprise/groups-and-provisioning",
          icon: "users",
        },
        {
          title: "User lifecycle management",
          description:
            "Provision employees, update group access, and revoke departing users' credentials.",
          href: "/codex/enterprise/user-lifecycle",
          icon: "userLock",
        },
        {
          title: "Roles and workspace permissions",
          description:
            "Find workspace, runtime, API, plugin, and source-system controls.",
          href: "/codex/enterprise/roles-and-workspace-permissions",
          icon: "userLock",
        },
        {
          title: "Personal access tokens",
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
      title: "Deployment and configuration",
      description:
        "Deploy apps and configure updates, runtime settings, remote connections, and model access.",
      pages: [
        {
          title: "Windows app deployment",
          description:
            "Choose an installation and update path for managed Windows devices.",
          href: "/codex/enterprise/windows-deployment",
          icon: "settings",
        },
        {
          title: "Manage app updates",
          description:
            "Control desktop app updates and deploy approved versions through your device management platform.",
          href: "/codex/enterprise/manage-app-updates",
          icon: "settings",
        },
        {
          title: "Managed configuration",
          description:
            "Review the global baseline in Agent Security, policy precedence for this feature, and supported runtime requirements.",
          href: "/codex/enterprise/managed-configuration",
          icon: "dataControls",
        },
        {
          title: "Remote connections",
          description: "Start and control work on connected computers.",
          href: "/codex/remote-connections",
          icon: "connect",
        },
        {
          title: "Workspace model availability",
          description:
            "Separate model access for ChatGPT, Codex in the ChatGPT desktop app, Codex CLI, the IDE extension, Codex cloud, and the Platform API.",
          href: "/codex/enterprise/workspace-model-availability",
          icon: "settings",
        },
        {
          title: "Amazon Bedrock",
          description:
            "Configure supported local clients to use models available through Bedrock.",
          href: "/codex/amazon-bedrock",
          icon: "storage",
        },
        {
          title: "Bedrock GovCloud configuration",
          description:
            "Configure local Codex workflows with Amazon Bedrock in AWS GovCloud.",
          href: "/codex/enterprise/govcloud-configuration",
          icon: "storage",
        },
        {
          title: "Sign in with ChatGPT through a gateway",
          description:
            "Keep your gateway for model requests while using your ChatGPT workspace identity.",
          href: "/codex/enterprise/sign-in-with-chatgpt-through-a-gateway",
          icon: "connect",
        },
        {
          title: "Use API/provider credentials",
          description:
            "Configure one Codex client to use your organization's model gateway and verify the connection.",
          href: "/codex/enterprise/connect-to-a-gateway",
          icon: "connect",
        },
        {
          title: "Roll out a gateway",
          description:
            "Configure model routes, issue credentials, and deploy Codex through your organization’s gateway.",
          href: "/codex/enterprise/roll-out-a-gateway",
          icon: "settings",
        },
        {
          title: "Gateway compatibility",
          description:
            "Check the Responses API behavior required for model requests, streaming, and tool calls.",
          href: "/codex/enterprise/gateway-compatibility",
          icon: "code",
        },
        {
          title: "Bedrock through LiteLLM",
          description:
            "Configure a LiteLLM gateway to route Codex model requests to Amazon Bedrock.",
          href: "/codex/enterprise/bedrock-through-litellm",
          icon: "storage",
        },
      ],
    },
    {
      title: "ChatGPT Work",
      description:
        "Review the ChatGPT Work overview and administration reference.",
      pages: [
        {
          title: "Overview",
          description:
            "Understand local and cloud execution, Local computer access with Work Cloud, network controls, and data boundaries.",
          href: "/codex/enterprise/chatgpt-work-overview",
          icon: "shieldCheck",
        },
        {
          title: "Cloud security",
          description:
            "Review hosted execution, connected accounts, access controls, retention, and audit visibility.",
          href: "/codex/enterprise/chatgpt-work-cloud-security",
          icon: "shieldCheck",
        },
        {
          title: "Local security",
          description:
            "Review local execution, device and browser access, managed policies, data handling, and audit limitations.",
          href: "/codex/enterprise/chatgpt-work-local-security",
          icon: "shieldCheck",
        },
        {
          title: "Usage and cost",
          description:
            "Understand shared credits, billing impact, spending controls, and adoption planning.",
          href: "/codex/enterprise/chatgpt-work-usage-and-cost",
          icon: "dataControls",
        },
        {
          title: "Admin FAQ",
          description:
            "Review access, data, governance, usage, and incident controls for ChatGPT Work.",
          href: "/codex/enterprise/work-admin-faq",
          icon: "userLock",
        },
      ],
    },
    {
      title: "Collaboration and sharing",
      description: "Manage GPT sharing and ownership.",
      pages: [
        {
          title: "GPTs and sharing",
          description:
            "Manage GPT sharing, ownership, connected apps, and third-party actions across your workspace.",
          href: "/codex/enterprise/gpts-and-sharing",
          icon: "userLock",
        },
      ],
    },
    {
      title: "Plugins and connections",
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
        {
          title: "Migrate custom GPTs to plugins",
          description:
            "Plan your workspace transition, migrate individual GPTs or eligible batches, and test and share replacement plugins.",
          href: "/codex/migrate-custom-gpts",
          icon: "tools",
        },
      ],
    },
    {
      title: "Usage and analytics",
      description:
        "Review workspace usage and adoption, and automate reporting.",
      pages: [
        {
          title: "Workspace analytics",
          description:
            "Review workspace-level ChatGPT adoption and Codex usage.",
          href: "/codex/enterprise/workspace-analytics",
          icon: "dataControls",
        },
        {
          title: "Usage Insights",
          description:
            "Explore usage across ChatGPT Work and Codex and assess workflow results with your team.",
          href: "/codex/enterprise/usage-insights",
          icon: "dataControls",
        },
        {
          title: "Analytics API",
          description:
            "Automate developer activity and code review reporting with the Codex Analytics API.",
          href: "/codex/enterprise/analytics-api",
          icon: "code",
        },
      ],
    },
    {
      title: "Security and compliance",
      description:
        "Review workspace security policies, governance, and audit controls.",
      pages: [
        {
          title: "Governance",
          description:
            "Choose the right analytics, spend, and audit surface for each question.",
          href: "/codex/enterprise/governance",
          icon: "shieldCheck",
        },
        {
          title: "Agent security",
          description:
            "Manage the Global policy baseline and supported Local and Codex Cloud environment settings.",
          href: "/codex/enterprise/agent-security",
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
          title: "Compliance API and audit events",
          description:
            "Export activity records for audit and investigation workflows.",
          href: "/codex/enterprise/compliance-api",
          icon: "userLock",
        },
      ],
    },
  ]}
/>
