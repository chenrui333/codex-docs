---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/ios-swiftui-view-refactor'
source_last_modified: '2026-04-25T06:49:17Z'
source_etag: 'W/"57eecd6d44c7ae331b284471aa30b6cd"'
codex_cli_versions: ["0.125.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0"]
---

# Refactor SwiftUI screens | Codex use cases

Source: https://developers.openai.com/codex/use-cases/ios-swiftui-view-refactor

Need

UI architecture

Default options

SwiftUI with an MV-first split across `@State`, `@Environment`, and small dedicated `View` types

Why it's needed

Large screens usually get easier to maintain when Codex simplifies the view tree and state flow before introducing another view model layer.

