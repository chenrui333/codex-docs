---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/ios-swiftui-view-refactor'
source_last_modified: '2026-04-25T06:49:17Z'
source_etag: 'W/"57eecd6d44c7ae331b284471aa30b6cd"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0"]
---

# Refactor SwiftUI screens | Codex use cases

Source: https://developers.openai.com/codex/use-cases/ios-swiftui-view-refactor

Need

UI architecture

Default options

SwiftUI with an MV-first split across `@State`, `@Environment`, and small dedicated `View` types

Why it's needed

Large screens usually get easier to maintain when Codex simplifies the view tree and state flow before introducing another view model layer.

