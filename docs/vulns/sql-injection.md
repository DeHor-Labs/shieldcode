# SQL Injection

OWASP A03:2021 (Injection). A vulnerabilidade mais antiga e ainda mais explorada da web.

## Como acontece

Concatenação de input do usuário em query SQL:

```python
# VULNERÁVEL
@app.route("/search")
def search():
    name = request.args.get("name")
    cursor.execute(f"SELECT * FROM users WHERE name='{name}'")
```

Input `' OR '1'='1` retorna todos os usuários. Input `'; DROP TABLE users; --` apaga a tabela.

## Padrão seguro (parametrização)

```python
# SEGURO
@app.route("/search")
def search():
    name = request.args.get("name")
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

O driver do banco escapa o valor antes de enviar. Input malicioso vira string literal, sem efeito.

## Variantes em outras linguagens

=== "Node.js (pg)"

    ```javascript
    // VULNERÁVEL
    db.query(`SELECT * FROM users WHERE name='${name}'`);

    // SEGURO
    db.query("SELECT * FROM users WHERE name = $1", [name]);
    ```

=== "Go (database/sql)"

    ```go
    // VULNERÁVEL
    db.Query(fmt.Sprintf("SELECT * FROM users WHERE name='%s'", name))

    // SEGURO
    db.Query("SELECT * FROM users WHERE name = ?", name)
    ```

=== "Java (PreparedStatement)"

    ```java
    // VULNERÁVEL
    Statement stmt = conn.createStatement();
    stmt.executeQuery("SELECT * FROM users WHERE name='" + name + "'");

    // SEGURO
    PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE name = ?");
    ps.setString(1, name);
    ps.executeQuery();
    ```

## Por que `eval` SQL acontece tanto

ORMs amenizam o problema, mas em "queries cruas" (raw queries) o desenvolvedor volta a concatenar. Pesquisas tipo "WHERE LIKE %x%" tentam parametrizar wildcards e quebram. Solução: parametrize a string base, deixe wildcards fora:

```python
# SEGURO
cursor.execute(
    "SELECT * FROM users WHERE name LIKE %s",
    (f"%{name}%",)  # wildcards fora da query, dentro do parâmetro
)
```

## Exemplo no repo

[examples/sql-injection/](https://github.com/nikolasdehor/shieldcode/tree/main/examples/sql-injection) tem `vulnerable.py` e `hardened.py` lado a lado.

## Defenses extras

- **ORM** quando possível (Django ORM, SQLAlchemy, Prisma)
- **Least privilege**: usuário do DB com SELECT só onde precisa
- **WAF**: bloqueia padrões óbvios em produção
- **Logging**: log queries para forense
- **Pentest periódico**

## Como ShieldCode previne

A skill instrui o Claude a:

1. NUNCA concatenar input em SQL
2. SEMPRE usar `?`/`$1`/`%s` placeholders
3. Aplicar `LIKE` com wildcards dentro do parâmetro
4. Validar tipos antes de mandar pra query
5. Quando o usuário pedir "query raw", explicar o risco e ainda parametrizar
