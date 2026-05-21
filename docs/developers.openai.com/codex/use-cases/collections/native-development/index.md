---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/collections/native-development'
source_last_modified: '2026-05-20T00:58:22Z'
source_etag: 'W/"53abdf991ebb76645d5aac1e062d987d"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0"]
---

# Native development – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/use-cases/collections/native-development

Codex works great on Apple platform projects when each pass has a build, run, or simulator loop attached to it.
These use cases are helpful when you are building new or existing iOS and macOS apps and need to iterate on the UI and debug issues.

## Build the app shell

Ask Codex to scaffold iOS and macOS apps with repeatable build loops. The Mac shell use case goes deeper on sidebar-detail-inspector layouts, commands, settings, and other desktop-native structure.

[![](/codex/use-cases/native-ios-apps.webp)

### Build for iOS

Use Codex to scaffold iOS SwiftUI projects, keep the build loop CLI-first with `xcodebuild`...

iOS  Code](/codex/use-cases/native-ios-apps)[![](/codex/use-cases/native-macos-apps.webp)

### Build for macOS

Use Codex to build macOS SwiftUI apps, wire a shell-first build-and-run loop, and add...

macOS  Code](/codex/use-cases/native-macos-apps)[![](/codex/use-cases/macos-sidebar-detail-inspector.webp)

### Build a Mac app shell

Use Codex and the Build macOS Apps plugin to turn an app idea into a desktop-native...

macOS  Code](/codex/use-cases/macos-sidebar-detail-inspector)

## Refactor iOS SwiftUI screens

Use Codex to split large SwiftUI views without changing behavior, then move selected iOS flows to Liquid Glass when the app is ready.

[![](/codex/use-cases/ios-swiftui-view-refactor.webp)

### Refactor SwiftUI screens

Use Codex and the Build iOS Apps plugin to break a long SwiftUI view into dedicated section...

iOS  Code](/codex/use-cases/ios-swiftui-view-refactor)[![](/codex/use-cases/ios-liquid-glass.webp)

### Adopt liquid glass

Use Codex and the Build iOS Apps plugin to audit existing iPhone and iPad UI, replace custom...

iOS  Code](/codex/use-cases/ios-liquid-glass)

## Expose iOS actions to the system

Leverage Codex to identify the actions and entities your app should expose through App Intents, so users can reach app behavior from system surfaces.

[![](/codex/use-cases/ios-app-intents.webp)

### Add iOS app intents

Use Codex and the Build iOS Apps plugin to identify the actions and entities your app should...

iOS  Code](/codex/use-cases/ios-app-intents)

## Debug your app

Have Codex reproduce bugs in Simulator or add telemetry to your macOS app to help you debug and fix issues.

[![](/codex/use-cases/ios-simulator-bug-debugging.webp)

### Debug in iOS simulator

Use Codex to discover the right Xcode scheme and simulator, launch the app, inspect the UI...

iOS  Code](/codex/use-cases/ios-simulator-bug-debugging)[![](/codex/use-cases/macos-telemetry-logs.webp)

### Add Mac telemetry

Use Codex and the Build macOS Apps plugin to add a few high-signal `Logger` events around...

macOS  Code](/codex/use-cases/macos-telemetry-logs)

