---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/windows-deployment'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0"]
---

# Deploy the Windows app

Source: https://learn.chatgpt.com/docs/enterprise/windows-deployment

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Users can install the ChatGPT desktop app themselves, or your IT team can
deploy it with an enterprise management tool. The app is Store-signed, but
users don't need to open the Microsoft Store to install or update it.

## Let users install and update the app

If users can manage their own applications, direct them to the
[web installer](https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi).
The installer provides the standard installation and automatic-update
experience. Microsoft Store components may appear during installation or
updates, but users don't need to browse the Store themselves.

You can also install the app from the command line:

```powershell
winget install --id 9PLM9XGG6VKS -s msstore
```

## Deploy the app with an enterprise management tool

If your organization centrally manages software, use Microsoft Intune or
another compatible mobile device management (MDM) or software-deployment
platform. If your platform supports Microsoft Store app deployment, search for
ChatGPT from OpenAI in the Store app flow, or use this Store product ID:

```text
9PLM9XGG6VKS
```

For setup details, see the following Microsoft documentation:

- [Enterprise deployment guide](https://1drv.ms/b/c/123ec1ed6c72a14a/IQDVdo5pE5P3QKg5r0eieSvfAeE7cW0yy58ncBFW7OYajwU?e=dGH94F)
- [Intune deployment guide](https://1drv.ms/b/c/123ec1ed6c72a14a/IQDh_5o31T6XT7bUn5RPldEJAZX58gEuRr8YnJD7d2IMpec?e=nByKw6)
- [MECM deployment guide](https://1drv.ms/b/c/123ec1ed6c72a14a/IQB829f_TSbkR7-H9qA4Q9ntAa9D2He3qMjXksWi2ozdeg8?e=GTKgAl)
- [Add Microsoft Store apps to Microsoft Intune](https://learn.microsoft.com/en-us/intune/app-management/deployment/add-microsoft-store)

<a id="manage-in-app-updates"></a>

### Manage app updates

For setup instructions and rollout guidance, see
[Manage app updates](https://learn.chatgpt.com/docs/enterprise/manage-app-updates).

## Install without Microsoft distribution services

If your environment can't use Microsoft app-distribution services for the
initial installation, download the Store-signed MSIX package for each device
architecture:

| Device architecture | Package                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------- |
| x64                 | [ChatGPT-x64.msix](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix)     |
| Arm64               | [ChatGPT-arm64.msix](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix) |

These stable links point to the latest published Store-signed package for each
architecture. For offline deployment workflows that require a license file,
also download the
[offline license (`ChatGPT-License.xml`)](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-License.xml).
Ingest the appropriate MSIX and, when required, the license file into your MDM
or software-deployment platform.

After the initial installation, devices that can reach
`persistent.oaistatic.com` can install updates automatically unless managed
configuration disables the app's built-in updater. If you disable in-app
updates, deploy newer packages through your MDM or software-deployment tool.

This deployment path:

- Supports initial installation in restricted environments.
- Supports x64 and Arm64 devices.
- Doesn't provide a standalone MSI or non-Store EXE.

## Related resources

- [Manage app updates](https://learn.chatgpt.com/docs/enterprise/manage-app-updates)
- [ChatGPT desktop app for Windows](https://learn.chatgpt.com/docs/windows/windows-app)
