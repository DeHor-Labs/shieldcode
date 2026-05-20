# Comparativo

ShieldCode vs outras formas de hardening de código.

## Snyk Code, GitHub Advanced Security, Sonar

| Aspecto | ShieldCode | SAST tools |
|---------|-----------|------------|
| Quando age | Durante geração | Após código escrito |
| Granularidade | Padrão por padrão | Vulnerabilidade por vulnerabilidade |
| Custo | $0 | Pago (SaaS) |
| Cobertura | Padrões comuns (4 hoje, mais vindo) | Bibliotecas grandes de CVEs |
| Falsos positivos | Zero (não detecta, previne) | Médio-alto |
| Educação | Alta (explica cada padrão) | Baixa (só aponta) |

**Combine ambos**: ShieldCode previne os 80% mais comuns durante a geração, SAST cobre os 20% restantes e CVEs específicos de libs.

## Bandit / Semgrep

Linters de segurança open source. ShieldCode complementa:

- **Bandit/Semgrep**: detectam após escrita
- **ShieldCode**: previne durante geração

Bandit pode rodar em CI verificando que ShieldCode foi aplicado. Defense-in-depth.

## OWASP Cheat Sheets

OWASP mantém cheat sheets pra cada vulnerabilidade. ShieldCode é a **versão acionável** dessas cheat sheets pra agentes de IA:

- OWASP cheat sheet diz "use parametrização em SQL"
- ShieldCode FAZ o Claude usar parametrização toda vez

## Por que skill é melhor que prompt engineering manual

Sem ShieldCode, você teria que lembrar de pedir:

> "Faz endpoint Y mas usa parametrização SQL pra prevenir injection, escape HTML do input do usuário, valida URL antes de fazer request, canonicaliza path antes de salvar..."

Com ShieldCode, você só pede:

> "Faz endpoint Y"

E a skill garante todos os padrões. Você não precisa lembrar — o sistema lembra por você.

## Por que skill em vez de fine-tuning

Fine-tuning seria a melhor solução em teoria. Mas:

- Caro (precisa de dataset grande, GPU, tempo)
- Específico de modelo (não funciona em todos os Claude / GPT / Gemini)
- Não é atualizável rápido (padrões de segurança evoluem)

Skill em markdown é hackável, gratuita, atualizável em segundos.

## Limitações

ShieldCode reduz risco de classes comuns de vulnerabilidade. NÃO substitui:

- **Pentesting** (encontra problemas que escapam de SAST e generators)
- **Code review** humano (julgamento contextual)
- **Threat modeling** (decisões arquiteturais)
- **Dependency scanning** (CVEs em libs)
- **Runtime protection** (WAF, RASP)

É uma layer adicional, não a única.
