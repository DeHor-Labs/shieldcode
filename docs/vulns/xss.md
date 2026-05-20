# XSS (Cross-Site Scripting)

OWASP A03:2021 (Injection). Atacante injeta JavaScript que executa no browser de outros usuários.

## Tipos

- **Reflected**: input vai direto na resposta sem sanitização
- **Stored**: input vai pro DB e depois é renderizado pra todos
- **DOM-based**: JavaScript do próprio app constrói HTML inseguro

## Vulnerável

```python
# Reflected XSS
@app.route("/search")
def search():
    q = request.args.get("q")
    return f"<h1>Você buscou por: {q}</h1>"
```

Input `<script>fetch('/api/me/token')</script>` rouba token de qualquer usuário que clique no link.

## Padrão seguro: auto-escape

Use template engine que escapa por padrão:

```python
# Flask + Jinja2 (auto-escape ON por default)
@app.route("/search")
def search():
    q = request.args.get("q")
    return render_template("search.html", q=q)
```

Template:

```html
<h1>Você buscou por: {{ q }}</h1>
```

Jinja escapa `<`, `>`, `&`, `"` por padrão.

## Client-side: nunca usar HTML cru com input

```javascript
// VULNERÁVEL
element.innerHTML = userInput;

// SEGURO
element.textContent = userInput;
```

Em React, Vue, Svelte: passe como prop normal, framework escapa automaticamente.

## Quando precisa renderizar HTML do usuário

Caso real: editor de markdown. Use sanitizer:

```python
import bleach

safe_html = bleach.clean(
    user_html,
    tags=["p", "strong", "em", "a", "ul", "ol", "li", "code", "pre"],
    attributes={"a": ["href", "title"]},
    protocols=["http", "https", "mailto"],
)
```

Em JS, use DOMPurify com allowlist conservadora.

## Content Security Policy

Layer adicional. Mesmo se XSS acontecer, CSP bloqueia execução:

```text
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-RANDOM';
  style-src 'self' 'unsafe-inline';
```

Sem inline scripts arbitrários, payloads injetados não rodam.

## Exemplo no repo

[examples/xss/](https://github.com/nikolasdehor/shieldcode/tree/main/examples/xss)

## Como ShieldCode previne

Skill instrui Claude a:

1. SEMPRE usar template engine com auto-escape
2. NUNCA usar atribuição direta de HTML cru com input
3. Para HTML do usuário, sugerir sanitizer com whitelist conservadora
4. Sugerir CSP no servidor
