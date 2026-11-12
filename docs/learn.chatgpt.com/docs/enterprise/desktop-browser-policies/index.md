---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/desktop-browser-policies'
source_kind: 'learn_markdown'
---

# Desktop browser policies

Source: https://learn.chatgpt.com/docs/enterprise/desktop-browser-policies

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use mobile device management (MDM) to configure the built-in browser in the ChatGPT desktop app. Choose a policy from the [supported list](#support-policy-reference), then look up its name and value format in the [Chrome Enterprise policy reference](https://chromeenterprise.google/policies/) before deploying it. Check the platform and browser version for each policy.

If you already manage Chrome, the deployment process will be familiar. Chrome supports both device-based policy deployment and cloud browser management through Google Admin. ChatGPT desktop currently supports device-based deployment through MDM, Group Policy, or configuration-management tools; cloud management of these browser policies is not yet available.

For a given operating system, the policy contents and formats stay the same. The main change is **where you deploy them on the device**: use ChatGPT desktop's registry keys, preference domain, or policy directory instead of Chrome's.

## Policy locations by platform

| Platform | Policy format                                  | Chrome location                     | ChatGPT desktop location           |
| -------- | ---------------------------------------------- | ----------------------------------- | ---------------------------------- |
| Windows  | Registry values and keys                       | `SOFTWARE\Policies\Google\Chrome`   | `SOFTWARE\Policies\OpenAI\Codex`   |
| macOS    | Managed preferences in a configuration profile | `com.google.Chrome`                 | `com.openai.codex`                 |
| Linux    | JSON files in the mandatory-policy directory   | `/etc/opt/chrome/policies/managed/` | `/etc/opt/codex/policies/managed/` |

The ChatGPT desktop identifiers still contain `Codex` or `codex`. Use them exactly as shown.

- **Windows:** Use `HKEY_LOCAL_MACHINE` for all users on a device, or `HKEY_CURRENT_USER` for a specific user. Use Chrome’s Windows registry format for values and lists. Chrome's standard administrative templates (ADMX) target Chrome; use custom registry settings for ChatGPT desktop.
- **macOS:** Deploy the policy keys and their property list values as managed preferences under `com.openai.codex`. A profile targeting Chrome's domain does not target ChatGPT desktop.
- **Linux:** Deploy JSON files directly into `/etc/opt/codex/policies/managed/`. Use `/etc/opt/codex/policies/recommended/` for policies that support defaults that users can change.

## Admin guide

### Example policies

The examples below configure two policies:

| Policy                   | Example value             | Effect                                                                                     |
| ------------------------ | ------------------------- | ------------------------------------------------------------------------------------------ |
| `PasswordManagerEnabled` | `false`                   | Prevents saving new passwords. Existing saved passwords are not deleted.                   |
| `CookiesBlockedForUrls`  | `["https://example.com"]` | Prevents `https://example.com` from setting cookies. It does not block access to the site. |

Replace these examples with your organization's settings.

### Windows: Microsoft Intune or Group Policy

For **Microsoft Intune**, save the following as a PowerShell script and add it under **Platform scripts**. It writes mandatory policies for all users on the device:

```powershell
$ErrorActionPreference = 'Stop'
$policyRoot = 'HKLM:\SOFTWARE\Policies\OpenAI\Codex'
if (-not (Test-Path -LiteralPath $policyRoot)) {
  New-Item -Path $policyRoot -Force | Out-Null
}
New-ItemProperty -Path $policyRoot -Name PasswordManagerEnabled -PropertyType DWord -Value 0 -Force | Out-Null
$cookieKey = "$policyRoot\CookiesBlockedForUrls"
if (-not (Test-Path -LiteralPath $cookieKey)) {
  New-Item -Path $cookieKey -Force | Out-Null
}
New-ItemProperty -Path $cookieKey -Name '1' -PropertyType String -Value 'https://example.com' -Force | Out-Null
```

In [Microsoft Intune Platform scripts](https://learn.microsoft.com/en-us/intune/device-management/tools/run-powershell-scripts-windows), set **Run this script using the logged on credentials** to **No** and **Run script in 64-bit PowerShell host** to **Yes**, then assign it to your pilot group. After the script runs, restart ChatGPT desktop and [verify the policies](#verify-the-policies).

For **Group Policy**, create Registry preference items for the same keys, value names, types, and values shown in the script, and apply them to your pilot devices.

Registry value formats:

- **True or false:** `REG_DWORD`, with `0` for false and `1` for true.
- **String lists:** Create a child key named after the policy. Number its `REG_SZ` values starting at `1`. When updating a list, remove numbered values that no longer apply.
- **Structured policies:** Follow the policy reference's Windows encoding. For example, `ExtensionSettings` stores its dictionary as a JSON string in a `REG_SZ` value.

For per-user policies, use the same path under `HKEY_CURRENT_USER` and deploy in the intended user's context. A script running as SYSTEM does not write to the signed-in user's `HKEY_CURRENT_USER`. For policies that support recommended defaults, use a child key named `Recommended` beneath the ChatGPT desktop root.

### macOS configuration profiles

Create a configuration profile that sets **forced (mandatory) managed preferences** in the `com.openai.codex` domain. For `Jamf Pro`, first save the following as `com.openai.codex.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PasswordManagerEnabled</key>
  <false/>
  <key>CookiesBlockedForUrls</key>
  <array>
    <string>https://example.com</string>
  </array>
</dict>
</plist>
```

- `Jamf Pro`: Use a computer configuration profile's **Application & Custom Settings** payload, upload the property list, and set the preference domain to `com.openai.codex`. See [the custom settings instructions](https://learn.jamf.com/r/en-US/technical-articles/Deploying_Custom_Computer_Configuration_Profiles_Using_the_Application_and_Custom_Settings_Payload).
- **Microsoft Intune:** Create a macOS **Templates → Preference file** profile and set **Preference domain name** to `com.openai.codex`. For this profile, save only the key-value pairs inside the example's outer `<dict>`; omit the XML declaration, DOCTYPE, `<plist>`, and outer `<dict>` wrappers. Keep the nested `<array>` intact. See [Intune's preference-file instructions](https://learn.microsoft.com/en-us/intune/device-configuration/templates/configure-preference-file-macos).
- **Other MDM tools:** Use their custom managed-preferences workflow or deploy an equivalent `.mobileconfig` profile for this domain.

Assign the profile to your pilot devices and confirm installation. Restart ChatGPT desktop and [verify the policies](#verify-the-policies). Use managed preferences: a normal user preference written with `defaults write` does not make a policy mandatory.

### Linux configuration management

Use a tool such as `Ansible`, Puppet, or Chef to deliver a JSON policy file to your devices, just as you would for Chrome.

1. Create `/etc/opt/codex/policies/managed/` if needed.
2. Deploy a JSON file directly into that directory using your configuration-management tool, package, or device-management agent.
3. Make the directories and file owned by `root`, readable by ChatGPT desktop users, and writable only by trusted administrators. Typical permissions are `0755` for directories and `0644` for files.
4. Restart ChatGPT desktop and [verify the policies](#verify-the-policies).

Example `/etc/opt/codex/policies/managed/browser.json`:

```json
{
  "PasswordManagerEnabled": false,
  "CookiesBlockedForUrls": ["https://example.com"]
}
```

Use JSON boolean values, numbers, arrays, and objects as required by each policy. Place files directly in `managed/`; nested directories are not read. Avoid defining the same policy in multiple files.

## Verify the policies

1. Confirm that your deployment tool delivered the registry values, installed profile, or JSON file to a pilot device.
2. Quit and reopen ChatGPT desktop. Open an in-app browser tab and navigate to `chrome://policy` **inside ChatGPT desktop**.
3. Select **Reload policies**. Check each policy's value, source, scope, level, and status. For the mandatory examples, expect source **Platform**, level **Mandatory**, and no policy error.
4. Test the intended behavior in that browser. A policy appearing on this page confirms it was read; it does not by itself prove that the affected feature behaves as intended.

Some policies require a full app restart even after reloading policies. Complete the pilot checks before expanding the deployment.

If a policy is missing, check its spelling, target location, assignment, and read permissions. If a policy shows an error or is ignored, check the value type, supported platform and policy level, and any conflicting policy reported on `chrome://policy`.

To change or remove a policy, update the deployment that supplied it and remove obsolete registry entries or file keys. If you used a script, remove the values it wrote before you remove the script assignment. Restart ChatGPT desktop and verify again.

## Support policy reference

ChatGPT desktop’s in-app browser supports the 244 policies listed below. For each policy’s purpose, accepted values, and platform details, look up its name in Google’s [Chrome Enterprise policy list](https://chromeenterprise.google/policies/).

### A–C

- `AccessControlAllowMethodsInCORSPreflightSpecConformant`
- `AIModeSettings`
- `AllowDeletingBrowserHistory`
- `AllowedDomainsForApps`
- `AllowSystemNotifications`
- `AllowWebAuthnWithBrokenTlsCerts`
- `AlternateErrorPagesEnabled`
- `AlwaysOpenPdfExternally`
- `AudioCaptureAllowed`
- `AudioCaptureAllowedUrls`
- `AuthNegotiateDelegateAllowlist`
- `AuthServerAllowlist`
- `AutofillAddressEnabled`
- `AutofillCreditCardEnabled`
- `AutoFillEnabled`
- `AutofillSettings`
- `AutoLaunchProtocolsFromOrigins`
- `AutomaticDownloadsAllowedForUrls`
- `AutomaticDownloadsBlockedForUrls`
- `AutomaticFullscreenAllowedForUrls`
- `AutomaticFullscreenBlockedForUrls`
- `AutoOpenAllowedForURLs`
- `AutoOpenFileTypes`
- `AutoplayAllowed`
- `AutoplayAllowlist`
- `AutoSelectCertificateForUrls`
- `BlockExternalExtensions`
- `BlockThirdPartyCookies`
- `BoundSessionCredentialsEnabled`
- `CACertificates`
- `CACertificatesWithConstraints`
- `CacheEncryptionEnabled`
- `CADistrustedCertificates`
- `CAHintCertificates`
- `CAPlatformIntegrationEnabled`
- `CloudAPAuthEnabled`
- `ComponentUpdatesEnabled`
- `CompressionDictionaryTransportEnabled`
- `CookiesAllowedForUrls`
- `CookiesBlockedForUrls`
- `CORSNonWildcardRequestHeadersSupport`
- `CpuPerformanceTierOverride`

### D–F

- `DataUrlInSvgUseEnabled`
- `DataUrlInWebWorkerOpaqueOriginEnabled`
- `DefaultAutomaticDownloadsSetting`
- `DefaultIdleDetectionSetting`
- `DefaultImagesSetting`
- `DefaultJavaScriptJitSetting`
- `DefaultJavaScriptOptimizerSetting`
- `DefaultJavaScriptSetting`
- `DefaultLocalFontsSetting`
- `DefaultMediaStreamSetting`
- `DefaultNotificationsSetting`
- `DefaultPopupsSetting`
- `DefaultPrinterSelection`
- `DefaultSearchProviderAlternateURLs`
- `DefaultSearchProviderContextMenuAccessAllowed`
- `DefaultSearchProviderName`
- `DefaultSearchProviderNewTabURL`
- `DefaultSearchProviderSearchURLPostParams`
- `DefaultSearchProviderSuggestURL`
- `DefaultSearchProviderSuggestURLPostParams`
- `DefaultSensorsSetting`
- `DefaultSerialGuardSetting`
- `DefaultWebBluetoothGuardSetting`
- `DefaultWebHidGuardSetting`
- `DefaultWebUsbGuardSetting`
- `DefaultWindowManagementSetting`
- `DefaultWindowPlacementSetting`
- `Disable3DAPIs`
- `DisabledSchemes`
- `DisablePrintPreview`
- `DNSInterceptionChecksEnabled`
- `DownloadRestrictions`
- `EditBookmarksEnabled`
- `EnableMediaRouter`
- `EnableOnlineRevocationChecks`
- `EncryptedClientHelloEnabled`
- `EnterpriseHardwarePlatformAPIEnabled`
- `ExemptDomainFileTypePairsFromFileTypeDownloadWarnings`
- `ExtensionAllowedTypes`
- `ExtensionDeveloperModeSettings`
- `ExtensionExtendedBackgroundLifetimeForPortConnectionsToUrls`
- `ExtensionInstallAllowlist`
- `ExtensionInstallBlocklist`
- `ExtensionInstallForcelist`
- `ExtensionInstallSources`
- `ExtensionInstallTypeBlocklist`
- `ExtensionSettings`
- `ExtensionUnpublishedAvailability`
- `ExternalProtocolDialogShowAlwaysOpenCheckbox`
- `FileOrDirectoryPickerWithoutGestureAllowedForOrigins`
- `ForceForegroundPriorityForUrls`
- `ForceGoogleSafeSearch`
- `ForceSafeSearch`
- `ForceYouTubeRestrict`
- `ForceYouTubeSafetyMode`

### G–L

- `GeolocationBlockedForUrls`
- `HSTSPolicyBypassList`
- `HttpAllowlist`
- `HttpHeaderInjection`
- `HttpsUpgradesEnabled`
- `IdleDetectionAllowedForUrls`
- `IdleDetectionBlockedForUrls`
- `ImagesAllowedForUrls`
- `ImagesBlockedForUrls`
- `ImportHistory`
- `ImportSavedPasswords`
- `IsolateOrigins`
- `JavaScriptAllowedForUrls`
- `JavaScriptBlockedForUrls`
- `JavascriptEnabled`
- `JavaScriptJitAllowedForSites`
- `JavaScriptJitBlockedForSites`
- `JavaScriptOptimizerAllowedForSites`
- `JavaScriptOptimizerBlockedForSites`
- `LocalFontsAllowedForUrls`
- `LocalFontsBlockedForUrls`
- `LocalNetworkAccessAllowedForUrls`
- `LocalNetworkAccessBlockedForUrls`
- `LocalNetworkAccessIpAddressSpaceOverrides`
- `LocalNetworkAccessRestrictionsTemporaryOptOut`
- `LocalNetworkAllowedForUrls`
- `LocalNetworkBlockedForUrls`
- `LookalikeWarningAllowlistDomains`
- `LoopbackNetworkAllowedForUrls`
- `LoopbackNetworkBlockedForUrls`

### M–P

- `ManagedBookmarks`
- `ManagedConfigurationPerOrigin`
- `NativeHostsExecutablesLaunchDirectly`
- `NativeMessagingAllowlist`
- `NativeMessagingBlocklist`
- `NativeMessagingUserLevelHosts`
- `NetworkPredictionOptions`
- `NotificationsAllowedForUrls`
- `NotificationsBlockedForUrls`
- `OopPrintDriversAllowed`
- `OriginAgentClusterDefaultEnabled`
- `PartitionedBlobUrlUsage`
- `PasswordLeakDetectionEnabled`
- `PasswordManagerBlocklist`
- `PasswordManagerEnabled`
- `PaymentMethodQueryEnabled`
- `PdfAnnotationsEnabled`
- `PdfLocalFileAccessAllowedForDomains`
- `PdfUseSkiaRendererEnabled`
- `PdfViewerOutOfProcessIframeEnabled`
- `PolicyDictionaryMultipleSourceMergeList`
- `PopupsAllowedForUrls`
- `PopupsBlockedForUrls`
- `PreferSlowCiphers`
- `PreferSlowKexAlgorithms`
- `PrefetchWithServiceWorkerEnabled`
- `PrinterTypeDenyList`
- `PrintHeaderFooter`
- `PrintingAllowedBackgroundGraphicsModes`
- `PrintingBackgroundGraphicsDefault`
- `PrintingEnabled`
- `PrintingLPACSandboxEnabled`
- `PrintingPaperSizeDefault`
- `PrintPdfAsImageAvailability`
- `PrintPdfAsImageDefault`
- `PrintPostScriptMode`
- `PrintPreviewUseSystemDefaultPrinter`
- `PrintRasterizationMode`
- `PrintRasterizePdfDpi`
- `PromptOnMultipleMatchingCertificates`
- `ProxyBypassList`
- `ProxyMode`
- `ProxyPacUrl`
- `ProxyServer`
- `ProxyServerMode`
- `ProxySettings`

### Q–S

- `QuicAllowed`
- `ReduceAcceptLanguageEnabled`
- `RegisteredProtocolHandlers`
- `RelaunchFastIfOutdated`
- `RelaunchNotification`
- `RelaunchNotificationPeriod`
- `RelaunchWindow`
- `RemoteDebuggingAllowed`
- `RequireOnlineRevocationChecksForLocalAnchors`
- `RestrictYouTubeCookiesDeletion`
- `SameOriginTabCaptureAllowedByOrigins`
- `SandboxExternalProtocolBlocked`
- `ScreenCaptureAllowed`
- `ScreenCaptureAllowedByOrigins`
- `ScreenCaptureWithoutGestureAllowedForOrigins`
- `ScrollToTextFragmentEnabled`
- `SearchSuggestEnabled`
- `SecurityKeyPermitAttestation`
- `SensorsAllowedForUrls`
- `SensorsBlockedForUrls`
- `SerialAllowAllPortsForUrls`
- `SerialAllowUsbDevicesForUrls`
- `SerialAskForUrls`
- `SerialBlockedForUrls`
- `ServiceWorkerAutoPreloadEnabled`
- `ServiceWorkerToControlSrcdocIframeEnabled`
- `SharedArrayBufferUnrestrictedAccessAllowed`
- `SharedWorkerBlobURLFixEnabled`
- `SharedWorkerExtendedLifetimeEnabled`
- `SignedHTTPExchangeEnabled`
- `SilentPrintingEnabled`
- `SitePerProcess`
- `SpellcheckEnabled`
- `SpellcheckLanguage`
- `SpellcheckLanguageBlocklist`
- `SSLErrorOverrideAllowed`
- `SSLErrorOverrideAllowedForOrigins`
- `StandardizedBrowserZoomEnabled`
- `StaticStorageQuotaEnabled`
- `StrictMimetypeCheckForWorkerScriptsEnabled`
- `SuppressDifferentOriginSubframeDialogs`

### T–Z

- `TabCaptureAllowedByOrigins`
- `TranslatorAPIAllowed`
- `URLAllowlist`
- `URLBlocklist`
- `UrlKeyedAnonymizedDataCollectionEnabled`
- `VideoCaptureAllowed`
- `VideoCaptureAllowedUrls`
- `WebAudioOutputBufferingEnabled`
- `WebHidAllowAllDevicesForUrls`
- `WebHidAllowDevicesForUrls`
- `WebHidAllowDevicesWithHidUsagesForUrls`
- `WebHidAskForUrls`
- `WebHidBlockedForUrls`
- `WebRtcDiagnosticLogCollectionAllowedForOrigins`
- `WebRtcIPHandling`
- `WebRtcIPHandlingUrl`
- `WebRtcLocalIpsAllowedUrls`
- `WebRtcPostQuantumKeyAgreement`
- `WebRtcTextLogCollectionAllowed`
- `WebRtcUdpPortRange`
- `WebUsbAllowDevicesForUrls`
- `WebUsbAskForUrls`
- `WebUsbBlockedForUrls`
- `WindowCaptureAllowedByOrigins`
- `WindowManagementAllowedForUrls`
- `WindowManagementBlockedForUrls`
- `WindowPlacementAllowedForUrls`
- `WindowPlacementBlockedForUrls`
- `WPADQuickCheckEnabled`
- `XSLTEnabled`
