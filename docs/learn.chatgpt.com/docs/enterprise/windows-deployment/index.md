---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/windows-deployment'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Deploy the Windows app

Source: https://learn.chatgpt.com/docs/enterprise/windows-deployment

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Choose how your organization installs apps.

<a id="deploy-the-app-with-an-enterprise-management-tool"></a>

{/* prettier-ignore */}
<Tabs
  id="windows-deployment"
  ariaLabel="Deployment method"
  param="deployment"
  defaultTab="intune"
  block
  tabs={[
    { id: "intune", label: "Intune" },
    { id: "sccm", label: "SCCM" },
    { id: "user", label: "Self-install" },
    { id: "other", label: "Other" },
  ]}
>

Package source

<Tabs
  id="windows-intune-source"
  ariaLabel="Intune package source"
  param="intune-source"
  defaultTab="store"
  selector="dropdown"
  tabs={[
    { id: "store", label: "Microsoft Store (recommended)" },
    { id: "offline", label: "Offline MSIX" },
  ]}
>

### Deploy through Microsoft Store

Use Intune's Microsoft Store integration to install and update the app.

<WorkflowSteps>

1. In the Intune admin center, go to **Apps** > **All apps** >
   **Create**. Select **Microsoft Store app (new)**.
2. Search for **ChatGPT** from **OpenAI**, or enter the Store
   product ID `9PLM9XGG6VKS`. Select the app and review its installation settings.
3. On **App information**, set **Install behavior** to **System**.
4. Under **Required**, add your target group so Intune installs the app
   automatically, then select **Create**.

</WorkflowSteps>

For optional installation through Company Portal, use **Available for enrolled
devices** instead.

Devices need access to the Microsoft Store and Windows Update endpoints in
Microsoft's [network requirements](https://learn.microsoft.com/en-us/intune/fundamentals/endpoints#microsoft-store).
If your network blocks these endpoints, select **Offline MSIX**.

For installation context, network requirements, and deployment monitoring, see
Microsoft's [Intune Store app guide](https://learn.microsoft.com/en-us/intune/app-management/deployment/add-microsoft-store).

### Deploy an offline package with Intune

Use a downloaded MSIX when devices can't use Microsoft's distribution services
or you need to deploy a specific approved version. Choose a **Required**
assignment so Intune installs the app automatically.

<WarningTip>
  If you've only blocked access to the Microsoft Store app, you can still deploy
  through Intune's Microsoft Store integration. Select **Microsoft Store
  (recommended)** above.
</WarningTip>

Assignment

<Tabs
  id="windows-intune-assignment"
  ariaLabel="Intune assignment"
  param="intune-assignment"
  defaultTab="required"
  selector="dropdown"
  tabs={[
    { id: "required", label: "Required (recommended)" },
    { id: "available", label: "Available in Company Portal" },
  ]}
>

<WorkflowSteps>

1. Download the [x64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix) or [Arm64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix) for your devices.
2. In the Intune admin center, go to **Apps** > **All apps** > **Create**.
   Select **Line-of-business app**, upload the MSIX, and review the package
   information.
3. On **Assignments**, add your target device group under **Required**.
4. In that assignment's **Install Context** column, select **User context**,
   change it to **Device context**, and save.
5. Review and create the app. Confirm successful installation in **Device
   install status**, then have employees launch ChatGPT normally.

</WorkflowSteps>

If the app doesn't appear, have users sign out and back in.

For more information, see Microsoft's [LOB app deployment guide](https://learn.microsoft.com/en-us/intune/app-management/deployment/add-lob-windows).

To let users choose when to install the offline package, use a **Windows app
(Win32)** with an **Available for enrolled devices** assignment:

<WorkflowSteps>

1. Download the [x64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix) or [Arm64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix), plus the [offline license](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-License.xml). Rename the package to `ChatGPT.msix` and keep both files in the same
   folder.
2. Save the following as `Install-ChatGPT.ps1`
   beside the downloaded files:

```powershell
   #Requires -RunAsAdministrator
   $ErrorActionPreference = 'Stop'

   Add-AppxProvisionedPackage -Online `
     -PackagePath "$PSScriptRoot\ChatGPT.msix" `
     -LicensePath "$PSScriptRoot\ChatGPT-License.xml" `
     -Regions all
```

3. Use Microsoft's [Win32 app workflow](https://learn.microsoft.com/en-us/intune/app-management/deployment/add-win32) to package these files and add a **Windows app (Win32)** in Intune. Set
   **Install behavior** to **System**, target the package's architecture, and
   run the script with 64-bit Windows PowerShell. Assign it as
   **Available for enrolled devices**.

</WorkflowSteps>

<details>
<summary>Win32 installation and detection settings</summary>

Use this install command:

```text
%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe -NoProfile -File .\Install-ChatGPT.ps1
```

For the custom detection rule, run the following script in 64-bit PowerShell.
It reports success when Windows has provisioned the app on the device. If you deploy a
specific version, also compare its `Version` with your approved version.

```powershell
$package = Get-AppxProvisionedPackage -Online -ErrorAction Stop |
  Where-Object DisplayName -eq 'OpenAI.Codex'

if ($package) {
  Write-Output $package.PackageName
  exit 0
}
exit 1
```

For the uninstall command, package an `Uninstall-ChatGPT.ps1` script with these
commands and run it in the same System context. This removes the provisioned
package and the app registrations for all users on the device.

```powershell
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

Get-AppxProvisionedPackage -Online |
  Where-Object DisplayName -eq 'OpenAI.Codex' |
  Remove-AppxProvisionedPackage -Online -AllUsers

Get-AppxPackage -AllUsers -Name 'OpenAI.Codex' |
  Remove-AppxPackage -AllUsers
```

Follow your organization's PowerShell script-signing policy for both scripts.

The app becomes available to users when Windows registers the provisioned
package at sign-in. Have users sign out and back in if it doesn't appear.

</details>

</Tabs>

</Tabs>

### Deploy with Microsoft Configuration Manager (SCCM)

Deploy the downloaded MSIX through Configuration Manager and Software Center.

<WorkflowSteps>

1. Download the [x64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix) or [Arm64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix) for your devices. Put it on a network share accessible to Configuration
   Manager.
2. Go to **Software Library** > **Application
   Management** > **Applications** > **Create Application**. Select **Windows app
   package** and enter the MSIX path. Review the detected package information and
   enable **Provision this application for all users on the device**.
3. Distribute the content to your distribution points
   and deploy to a device collection. Choose **Required** to install
   automatically, or **Available** to let users install from Software Center.

</WorkflowSteps>

Use the Windows app package deployment type, rather than the Store-link
deployment type. For package requirements and all-user provisioning, see
Microsoft's [Configuration Manager guide](https://learn.microsoft.com/en-us/intune/configmgr/apps/get-started/creating-windows-applications).

If your deployment workflow requires it, download the [offline license](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-License.xml) alongside the package.

### Deploy with another management tool

Use your management tool's MSIX deployment workflow to install the app on managed
Windows devices.

<WorkflowSteps>

1. Download the [x64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix) or [Arm64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix) for your devices.
2. Add the MSIX to your deployment tool. Configure installation for the device,
   using Local System or administrator privileges.
3. Assign automatic installation to a pilot device group. Confirm that employees
   can open ChatGPT under their normal Windows accounts before expanding deployment.

</WorkflowSteps>

If the app doesn't appear, have users sign out and back in.

<details>
<summary>Install with a PowerShell script</summary>

If your tool requires an installation command, download the [offline license](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-License.xml) alongside the MSIX.
Rename the package to `ChatGPT.msix` and save this script as
`Install-ChatGPT.ps1` in the same folder:

```powershell
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

Add-AppxProvisionedPackage -Online `
  -PackagePath "$PSScriptRoot\ChatGPT.msix" `
  -LicensePath "$PSScriptRoot\ChatGPT-License.xml" `
  -Regions all
```

Package the script and both files together. Configure your tool to run the script
with 64-bit Windows PowerShell as Local System or an administrator.

</details>

<a id="let-users-install-and-update-the-app"></a>

Package source

<Tabs
  id="windows-user-source"
  ariaLabel="User installation package source"
  param="user-source"
  defaultTab="store"
  selector="dropdown"
  tabs={[
    { id: "store", label: "Web installer (recommended)" },
    { id: "offline", label: "Offline MSIX" },
  ]}
>

### Let users install the app

Use this option when users can install applications themselves or get help
from an administrator.

<WorkflowSteps>

1. Direct users to the [ChatGPT Windows installer](https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi).
2. Run the installer and follow the Windows installation
   prompts. An administrator must approve the installation.
3. Open ChatGPT and sign in with a work account to get started.

</WorkflowSteps>

Users can also install from the command line:

```powershell
winget install --id 9PLM9XGG6VKS -s msstore
```

The installer provides automatic updates. Microsoft Store components may appear
during installation or updates, but users don't need to browse the Store.

<a id="install-without-microsoft-distribution-services"></a>

### Install from an offline package

Download the files on a connected machine, then copy them to the target device.
An administrator must perform the installation.

<WorkflowSteps>

1. Download the [x64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix) or [Arm64 MSIX](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix), plus the [offline license](https://persistent.oaistatic.com/codex-app-prod/ChatGPT-License.xml). Rename the package to `ChatGPT.msix` and keep both files in the same
   folder.
2. Open Windows PowerShell as an administrator in that
   folder and run:

```powershell
   Add-AppxProvisionedPackage -Online `
     -PackagePath .\ChatGPT.msix `
     -LicensePath .\ChatGPT-License.xml `
     -Regions all
```

3. Sign out and back in if the app doesn't appear, then open
   ChatGPT and sign in with a work account.

</WorkflowSteps>

These links provide the latest Store-signed package for each architecture.
Offline installation doesn't provide offline access to ChatGPT. Standalone
MSI and non-Store EXE packages aren't available.

</Tabs>

</Tabs>

<a id="manage-in-app-updates"></a>

## Manage app updates

The app checks for updates by default, including after an offline
installation. To enable automatic updates, allow devices to reach
`persistent.oaistatic.com`. If you disable automatic updates, deploy newer
packages through your management tool.

For update policy and rollout guidance, see
[Manage app updates](https://learn.chatgpt.com/docs/enterprise/manage-app-updates). Disabling the built-in
updater doesn't disable updates from the Microsoft Store or your management tool.

## Troubleshooting

<details>
<summary>Users are prompted for administrator credentials when installing</summary>

For self-install, this is expected. An administrator must approve the installation.

For an Intune deployment through the Microsoft Store:

1. In the Intune admin center, go to **Apps** > **All apps** and select ChatGPT.
2. Check **Install behavior** in the app's **Properties**. If it's **User**, add
   the app again as a **Microsoft Store app (new)** and select **System** on
   **App information**.
3. Assign the app to your target group under **Required** or **Available for
   enrolled devices**. If you added a new app, remove that group's assignment
   from the original app.
4. Sync the affected device with Intune, then check **Device install status**.
   For an available assignment, retry the installation in Company Portal.

If the app is already installed, deploying it with **System** install behavior may
cause Intune to report `0x87D1041C`. Installation still succeeds in this scenario.
Verify the app on the affected device.

</details>

<details>
<summary>Installation fails with error `0x80073D28`</summary>

Windows returns `0x80073D28` (`ERROR_PACKAGED_SERVICE_REQUIRES_ADMIN_PRIVILEGES`)
when it can't install a packaged service without administrator privileges.
Run the installation as an administrator, or configure your deployment tool to
install in device or System context.

For an existing SCCM deployment:

1. Open the application's **Properties** > **Deployment Types**.
2. Edit the **Windows app package** deployment type and open **User Experience**.
3. Enable **Provision this application for all users on the device** and save.
4. Refresh the client's machine policy, then retry the installation in Software
   Center.

For more information about the provisioning setting, see Microsoft's [application deployment settings](https://learn.microsoft.com/en-us/intune/configmgr/apps/deploy-use/create-applications#automatically-detect-application-information).

</details>

## Related resources

- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
- [ChatGPT desktop app for Windows](https://learn.chatgpt.com/docs/windows/windows-app)
