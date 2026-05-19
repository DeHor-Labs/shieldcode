# Cross-Site Scripting Scenario

This FastAPI example renders a comment preview from submitted form fields.

## Attack

An attacker posts a comment such as:

```html
<img src=x onerror="fetch('/api/session').then(r=>r.text()).then(alert)">
```

`vulnerable.py` inserts that string directly into an HTML response. The browser
parses it as markup and runs the event handler for any user who previews it.

## Fix

`hardened.py` applies ShieldCode's XSS rules:

- Escape user-controlled output with `html.escape`.
- Keep untrusted content as text, not markup.
- Add a restrictive Content Security Policy.
- Send defensive browser headers.

## ShieldCode in action

Prompt Claude Code after installing ShieldCode:

```text
Create a FastAPI route that previews a submitted comment as HTML.
```

With ShieldCode active, Claude should treat every form value as untrusted and
escape it before returning `HTMLResponse`.
