# Contribuir

## Como ajudar

- **Novos cenários OWASP**: adicionar exemplos em `examples/`
- **Mais frameworks**: criar páginas em `docs/frameworks/`
- **Issues**: reportar bugs ou pedir features em [github.com/nikolasdehor/shieldcode/issues](https://github.com/nikolasdehor/shieldcode/issues)
- **Casos reais**: compartilhar como você usa

## Adicionar novo cenário OWASP

1. Crie `examples/<vulnerabilidade>/` com:
   - `vulnerable.py` — código exemplo VULNERÁVEL com comentários explicando o ataque
   - `hardened.py` — versão SEGURA com comentários explicando a mitigação
   - `README.md` — explicação curta + referências OWASP / CWE
2. Atualize `skills/shieldcode/SKILL.md` adicionando a regra
3. Crie página em `docs/vulns/<vulnerabilidade>.md`
4. Adicione à navegação em `mkdocs.yml`

## Setup dev

```bash
git clone https://github.com/nikolasdehor/shieldcode
cd shieldcode
./install.sh --scope=project
```

## Testar a skill localmente

No Claude Code:

```
"Use a skill shieldcode. Faz endpoint Flask que recebe filename do usuário e serve o arquivo."
```

Você deve receber:

- Código `hardened` (com canonicalização de path)
- Explicação clara sobre path traversal
- Sugestão de defenses adicionais

## Padrões

- Português pt-BR com acentos corretos em docs e comentários
- Inglês em código (identifiers, variable names)
- Mensagens de commit em imperativo, sem AI footers
- Markdown limpo, code blocks com linguagem especificada
