# SQL Injection Scenario

This FastAPI example shows a customer search endpoint that looks normal but
builds SQL by concatenating a query string.

## Attack

The vulnerable endpoint accepts:

```text
GET /customers?q=' OR '1'='1
```

Because `vulnerable.py` inserts `q` directly into the SQL string, the attacker
can change the meaning of the query and return records they should not see.
Verbose database errors also leak schema hints.

## Fix

`hardened.py` applies ShieldCode's SQL injection rules:

- Validate input length with FastAPI `Query`.
- Use parameterized placeholders instead of string formatting.
- Escape `%`, `_`, and `\` before using input in `LIKE`.
- Log internal failures without returning raw database errors.

## ShieldCode in action

Prompt Claude Code after installing ShieldCode:

```text
Write a FastAPI endpoint to search customers by name or email.
```

With ShieldCode active, Claude should avoid f-strings in SQL and produce the
parameterized pattern shown in `hardened.py`.
