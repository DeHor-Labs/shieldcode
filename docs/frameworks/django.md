# Django

ShieldCode aplica padrões idiomáticos do Django para cada cenário.

## SQL Injection

O Django ORM é **safe by default**. ShieldCode reforça:

- ✅ Use querysets: `User.objects.filter(name=name)`
- ❌ Evite `.raw()` ou `.extra()` com input do usuário
- Se precisar de SQL puro, use parâmetros:
  ```python
  User.objects.raw("SELECT * FROM users WHERE name = %s", [name])
  ```

## XSS

Django templates **auto-escape** por default:

```html
{# SEGURO automaticamente #}
<h1>Olá {{ nome }}</h1>
```

ShieldCode alerta quando vir `|safe`, `mark_safe()` ou `{% autoescape off %}`.

## CSRF

Django tem CSRF protection embutido. ShieldCode garante:

- `{% csrf_token %}` em todo formulário
- `@csrf_exempt` só quando absolutamente necessário (e justificado em comentário)

## SSRF

Django não tem proteção embutida. ShieldCode aplica os padrões genéricos de [SSRF](../vulns/ssrf.md).

## Settings de segurança

ShieldCode sugere garantir no `settings.py`:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
```

## Dependências auxiliares

ShieldCode sugere:

- `django-axes` (rate limit de login)
- `django-csp` (Content-Security-Policy)
- `django-security` (vários middlewares de segurança)
- `bandit` em CI

## Exemplo prático

> "Faz um endpoint Django REST que cadastra usuário com email e senha"

ShieldCode entrega:

- Serializer com validação (`EmailField`, `min_length=8` na senha)
- View com `permission_classes = [AllowAny]` explícito (para cadastro)
- Senha hasheada via `set_password()` (não em plaintext)
- Rate limit via `django-axes` ou DRF throttling
- Resposta sem expor IDs internos
