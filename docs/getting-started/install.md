# Instalação

## Pré-requisitos

- **Claude Code** ([docs](https://docs.claude.com/en/docs/claude-code))
- **Bash** ou shell POSIX

## Instalação

=== "Clone do repo"

    ```bash
    git clone https://github.com/nikolasdehor/shieldcode
    cd shieldcode
    ./install.sh --scope=user      # global
    # ou
    ./install.sh --scope=project   # só nesse projeto
    ```

=== "One-liner"

    ```bash
    curl -sSL https://raw.githubusercontent.com/nikolasdehor/shieldcode/main/install.sh | bash -s -- --scope=user
    ```

## Verificar

No Claude Code:

```
/skills
```

Deve listar `shieldcode`.

## Desinstalar

```bash
./uninstall.sh --scope=user
# ou
./uninstall.sh --scope=project
```

## Próximos passos

- [Quickstart](quickstart.md)
- [Como a skill funciona](how.md)
