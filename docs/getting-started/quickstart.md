# Quickstart

## 1. Instale a skill

Veja [Instalação](install.md).

## 2. Comece um projeto

```bash
cd ~/projects/meu-novo-app
claude
```

## 3. Peça código com proteção

Forma 1 — explicitamente:

> "Use a skill shieldcode. Escreva um endpoint Flask que recebe email do usuário e salva no DB."

Forma 2 — implícita (Claude detecta):

> "Crie um sistema de upload de arquivos em Express"

(O Claude vai automaticamente puxar a skill por causa do contexto de "upload" + "arquivos" envolver path traversal e validação.)

## 4. Resultado

Claude entrega **dois arquivos lado a lado**:

```python
# vulnerable.py — o que NÃO fazer
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(f"/var/uploads/{file.filename}")  # path traversal!


# hardened.py — o jeito seguro
import secrets
from pathlib import Path

UPLOADS = Path("/var/uploads").resolve()

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    safe_name = secrets.token_hex(16) + Path(file.filename).suffix
    target = (UPLOADS / safe_name).resolve()
    if not str(target).startswith(str(UPLOADS) + "/"):
        abort(400)
    file.save(target)
```

+ explicação clara do **porquê** o primeiro é vulnerável.

## 5. Aprender enquanto codifica

A skill ensina padrões seguros conforme você codifica. Depois de algumas semanas, você intuitivamente pensa em segurança ao escrever.

## Próximos passos

- [Como a skill funciona](how.md)
- [Vulnerabilidades cobertas](../vulns/sql-injection.md)
