# Express / Node.js

ShieldCode aplica padrões idiomáticos do Express e ecossistema Node.

## SQL Injection

Use ORM ou drivers com parametrização:

```javascript
// Prisma (recomendado)
const user = await prisma.user.findUnique({ where: { email } });

// pg (driver Postgres) parametrizado
await db.query("SELECT * FROM users WHERE name = $1", [name]);

// mysql2 prepared statements
await db.execute("SELECT * FROM users WHERE name = ?", [name]);
```

## Input validation

Use Zod:

```typescript
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(128),
});

app.post("/users", (req, res) => {
  const parsed = UserSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ errors: parsed.error.errors });
  }
  // parsed.data tem tipos corretos
});
```

## XSS prevention

Use template engines com auto-escape (Pug, EJS com `<%- %>` cuidadoso, Handlebars):

```javascript
// Sem escape: VULNERÁVEL em EJS
<%- userInput %>

// Com escape: SEGURO em EJS
<%= userInput %>
```

Em SPAs (React, Vue, Svelte), frameworks escapam por padrão.

## Helmet (security headers)

```javascript
import helmet from "helmet";

app.use(helmet());  // CSP, HSTS, X-Frame-Options, etc

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'nonce-RANDOM'"],
  },
}));
```

## Auth (passport / jose)

Para JWT, prefira `jose` (moderno) ou `jsonwebtoken`:

```javascript
import { SignJWT, jwtVerify } from "jose";

const secret = new TextEncoder().encode(process.env.JWT_SECRET);

const token = await new SignJWT({ sub: userId })
  .setProtectedHeader({ alg: "HS256" })
  .setExpirationTime("15m")
  .sign(secret);
```

Senha: use `bcrypt` ou `argon2`:

```javascript
import bcrypt from "bcrypt";

const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.compare(password, hash);
```

## Rate limit

```javascript
import rateLimit from "express-rate-limit";

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 min
  max: 5,
});

app.post("/login", loginLimiter, loginHandler);
```

## CORS

```javascript
import cors from "cors";

app.use(cors({
  origin: ["https://meu-frontend.com"],
  credentials: true,
}));
```

NUNCA `origin: "*"` com `credentials: true`.

## Exemplo prático

> "Faz API Express com login JWT e CRUD de posts"

ShieldCode entrega:

- Helmet ON
- Zod validando body em todo POST/PUT
- Senha hasheada com bcrypt cost 12
- JWT com expiração 15min + refresh tokens
- Rate limit no login (5/15min)
- Posts: SQL via Prisma (zero injection)
- Auth middleware (`Bearer token` obrigatório)
- CORS restrito ao frontend conhecido
