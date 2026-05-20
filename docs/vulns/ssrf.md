# SSRF (Server-Side Request Forgery)

OWASP A10:2021. Atacante faz seu servidor requisitar URLs que ele controla, expondo recursos internos.

## Como acontece

App permite que usuário forneça URL para "preview" / "thumbnail" / "webhook":

```python
# VULNERÁVEL
@app.route("/preview")
def preview():
    url = request.args.get("url")
    response = requests.get(url)  # qualquer URL!
    return response.text
```

Atacante envia:

- `http://169.254.169.254/latest/meta-data/` → metadata de cloud (AWS/GCP/Azure)
- `http://localhost:6379/INFO` → consulta Redis interno
- `http://internal-admin.local/users` → endpoint admin
- `file:///etc/passwd` → arquivos locais

## Padrão seguro: allowlist + validação

```python
import ipaddress
from urllib.parse import urlparse
import socket

ALLOWED_HOSTS = {"example.com", "trusted-cdn.com"}

def fetch_safe(url: str) -> str:
    parsed = urlparse(url)

    # 1. Só HTTP(S)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Schema inválido")

    # 2. Host na allowlist
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Host não permitido")

    # 3. Resolver DNS e validar IP (evita DNS rebinding)
    ip = socket.gethostbyname(parsed.hostname)
    ip_obj = ipaddress.ip_address(ip)

    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
        raise ValueError("IP interno bloqueado")

    # 4. Faz request com timeout e sem follow_redirects (atacante pode redirecionar)
    response = requests.get(url, timeout=5, allow_redirects=False)
    return response.text
```

## Se NÃO precisar de allowlist

Quando o app é tipo "webhook delivery" (usuário cadastra URL pra receber notificações), allowlist não rola. Mitigações:

- Bloquear IPs privados (RFC 1918)
- Bloquear loopback e link-local
- Bloquear AWS metadata IP (`169.254.169.254`)
- Timeout curto
- Sem follow_redirects (ou validar destino)
- Rede isolada (egress firewall que só permite saída pra internet pública)

## Exemplo no repo

[examples/ssrf/](https://github.com/nikolasdehor/shieldcode/tree/main/examples/ssrf)

## Como ShieldCode previne

Skill instrui Claude a:

1. Identificar quando código faz request HTTP a URL fornecida por usuário
2. SEMPRE validar schema (`http`/`https` apenas)
3. SEMPRE resolver DNS e validar que IP não é interno
4. Bloquear `169.254.169.254` e RFC 1918 explicitamente
5. Timeout curto (5-10s)
6. `allow_redirects=False` (ou validar destino)
7. Em ambientes cloud, alertar sobre risco de IMDSv1 (use IMDSv2)
