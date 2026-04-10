# Refactor SwiftUI screens | Codex use cases

Source: https://developers.openai.com/codex/use-cases/ios-swiftui-view-refactor

Need

UI architecture

Default options

SwiftUI with an MV-first split across `@State`, `@Environment`, and small dedicated `View` types

Why it's needed

Large screens usually get easier to maintain when Codex simplifies the view tree and state flow before introducing another view model layer.

