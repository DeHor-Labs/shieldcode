# Path Traversal

OWASP A01:2021 (Broken Access Control). Atacante usa `../` para escapar do diretório esperado e acessar arquivos arbitrários.

## Vulnerável

```python
# VULNERÁVEL
@app.route("/download/<filename>")
def download(filename):
    return send_file(f"/var/uploads/{filename}")
```

Atacante envia `?filename=../../../etc/passwd` e baixa o arquivo do sistema.

## Padrão seguro: canonicalizar + validar

```python
from pathlib import Path
from flask import abort

UPLOADS = Path("/var/uploads").resolve()

@app.route("/download/<path:filename>")
def download(filename):
    target = (UPLOADS / filename).resolve()

    # Garante que target está DENTRO de UPLOADS
    try:
        target.relative_to(UPLOADS)
    except ValueError:
        abort(403)

    if not target.is_file():
        abort(404)

    return send_file(target)
```

`Path.resolve()` normaliza `../` para o caminho real. Depois `relative_to` confirma que esse caminho real está dentro do diretório esperado.

## Variantes em outras linguagens

=== "Node.js"

    ```javascript
    const path = require("path");
    const UPLOADS = path.resolve("/var/uploads");

    app.get("/download/:filename", (req, res) => {
      const target = path.resolve(UPLOADS, req.params.filename);
      if (!target.startsWith(UPLOADS + path.sep)) {
        return res.status(403).end();
      }
      res.sendFile(target);
    });
    ```

=== "Go"

    ```go
    func download(w http.ResponseWriter, r *http.Request) {
        filename := r.URL.Query().Get("filename")
        target := filepath.Join(uploadsDir, filename)
        target, err := filepath.Abs(target)
        if err != nil {
            http.Error(w, "bad path", 400)
            return
        }
        if !strings.HasPrefix(target, uploadsDir + string(os.PathSeparator)) {
            http.Error(w, "forbidden", 403)
            return
        }
        http.ServeFile(w, r, target)
    }
    ```

## Cuidados adicionais

- **Renomeie uploads**: ao receber upload, salve com nome aleatório (`secrets.token_hex()`), não confie no nome do cliente
- **Whitelist extensions**: `if not filename.endswith((".png", ".jpg", ".pdf")): abort(400)`
- **Permissões de filesystem**: process do app não deve ter permissão de leitura fora de `/var/uploads/`
- **Cuidado com symlinks**: `Path.resolve()` segue symlinks. Em diretórios sensíveis, valide isso explicitamente

## Exemplo no repo

[examples/path-traversal/](https://github.com/nikolasdehor/shieldcode/tree/main/examples/path-traversal)

## Como ShieldCode previne

Skill instrui Claude a:

1. NUNCA usar concatenação direta de string em paths
2. SEMPRE canonicalizar com `Path.resolve()` / `path.resolve()` / `filepath.Abs()`
3. SEMPRE validar que path resolvido começa com diretório esperado
4. Sugerir renomear uploads pra evitar confiar em filename do cliente
5. Sugerir whitelist de extensions quando contextualmente possível
6. Alertar sobre symlinks em diretórios sensíveis
