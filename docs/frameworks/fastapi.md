# FastAPI

ShieldCode aplica padrões idiomáticos do FastAPI.

## SQL Injection

Use SQLAlchemy / SQLModel:

```python
# SEGURO
@app.get("/users/{name}")
async def get_user(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    return user
```

Para queries cruas:

```python
from sqlalchemy import text

result = db.execute(
    text("SELECT * FROM users WHERE name = :name"),
    {"name": name},
)
```

## Input validation com Pydantic

FastAPI usa Pydantic. ShieldCode reforça schemas estritos:

```python
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)
    age: int

    @validator("age")
    def age_must_be_adult(cls, v):
        if v < 18:
            raise ValueError("Idade mínima 18")
        return v
```

Pydantic rejeita input inválido antes da view ver, sem você escrever validação manual.

## CORS

FastAPI tem middleware. ShieldCode sugere:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meu-frontend.com"],  # NUNCA "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Auth (OAuth2 + JWT)

Pattern padrão FastAPI. ShieldCode garante:

- Algoritmo `HS256` ou `RS256` (NUNCA `none`)
- Secret forte (`secrets.token_urlsafe(32)`)
- Expiração curta (15-30 min)
- Refresh tokens separados
- Senha hasheada com `bcrypt` ou `argon2`

## Rate limit

FastAPI não tem nativo. ShieldCode sugere `slowapi`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/login")
@limiter.limit("5/minute")
async def login(...):
    ...
```

## Exemplo prático

> "Faz endpoint FastAPI de upload de arquivo"

ShieldCode entrega:

- Validação de Content-Type (`UploadFile` do FastAPI já valida)
- Tamanho máximo (`MAX_FILE_SIZE = 10 * 1024 * 1024`)
- Whitelist de extensions
- Salvamento com nome aleatório
- Path canonicalizado com check
- Rate limit
- Auth obrigatório (`Depends(get_current_user)`)
