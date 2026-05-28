# Copilot Instructions — shieldcode

## Project Overview
Aplicação macOS em Swift (baseada em VibeTunnel xcworkspace).

## Stack
- **Swift 5.9+**
- **SwiftUI** ou **AppKit** (verificar)
- **Xcode** workspace
- macOS target

## Conventions
- Swift Concurrency: `async/await`, `actor` para estado compartilhado
- Memória: sem retain cycles; `[weak self]` em closures que capturam self
- Sem force unwrap (`!`) exceto em IBOutlets ou casos com invariante claro
- `os.Logger` em vez de `print` em release
- Erros via `throws` + `Result` quando assíncrono
- Entitlements mínimos necessários; sandbox respeitado

## Folder Structure
- `<Module>.xcworkspace` / `<Module>.xcodeproj` — workspace
- `Sources/` ou `<Module>/` — código Swift
- `*.entitlements` — entitlements

## Development
- Abrir workspace no Xcode
- ⌘B build, ⌘R run, ⌘U test
- CLI: `xcodebuild` se houver script

## Critical Files
- `<Module>.xcworkspace` — workspace principal
- `*.entitlements` — capabilities
- `Info.plist` — bundle config
