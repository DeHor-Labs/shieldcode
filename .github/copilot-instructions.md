# Copilot Instructions — shieldcode

## Project Overview
ShieldCode é uma **skill de segurança para Claude Code**, não um projeto de aplicação.
O repositório contém documentação, exemplos e regras de hardening para orientar código gerado por IA (principalmente JavaScript/TypeScript e Python).

## Stack
- **Markdown + SKILL.md** (`skills/shieldcode/SKILL.md`) como fonte de instruções de implementação segura
- **JavaScript/TypeScript** e **Python** (exemplos de referência no README, exemplos e skill)
- **Bash** (`install.sh`, `uninstall.sh`) para instalação/desinstalação
- **GitHub Actions** para validações

## Conventions
- Seguir **todas** as regras não negociáveis do `skills/shieldcode/SKILL.md`.
- Segurança por padrão: validação de input, prevenção de injeções, tratamento seguro de erros, autenticação/autorização, headers de segurança e logging sem PII/segredos.
- Preferir patterns de produção: validação allowlist, queries parametrizadas, erros tipados/mapeados, backoff/jitter para retries e circuit breaker quando aplicável.

## Folder Structure
- `skills/shieldcode/SKILL.md` — regras principais (obra viva da skill)
- `examples/` — cenários de vulnerabilidade e versões hardened/vulnerable
- `.github/workflows/` — CI e automações de validação
- `install.sh`, `uninstall.sh` — scripts de distribuição/remoção
- `README.md` — visão de produto, cobertura e uso

## Development
- Não execute build de app; este repositório é documentação e instruções de skill.
- Para mudanças locais: validar os arquivos alterados em Markdown e scripts de instalação.
- CLI de referência:
  - `bash -n install.sh`
  - `bash -n uninstall.sh`
  - `sed -n '1,260p' README.md` / `SKILL.md` para manter consistência de orientação

## CI / Plugin
- O CI inclui validação de `install.sh`, `uninstall.sh` e verificação de frontmatter no `SKILL.md`.
- `plugin.json` não está presente no repositório hoje; o workflow atual trata essa ausência como opcional.

## Critical Files
- `skills/shieldcode/SKILL.md` — regras obrigatórias
- `README.md` — fonte de verdade para o escopo público da skill
- `.github/copilot-instructions.md` — alinhamento de orientação para Copilot
