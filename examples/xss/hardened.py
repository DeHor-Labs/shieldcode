from html import escape

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="Hardened comment preview")


@app.post("/preview", response_class=HTMLResponse)
def preview_comment(display_name: str = Form(...), comment: str = Form(...)):
    # FIX: escape all user-controlled output before embedding it in HTML.
    # The browser receives text such as &lt;script&gt; instead of executable
    # markup, so attacker payloads render harmlessly.
    safe_name = escape(display_name, quote=True)
    safe_comment = escape(comment, quote=True)

    html = f"""
    <html>
      <head>
        <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
      </head>
      <body>
        <h1>Preview for {safe_name}</h1>
        <article class="comment">{safe_comment}</article>
      </body>
    </html>
    """
    response = HTMLResponse(content=html)

    # FIX: security headers reduce impact if a future rendering bug appears.
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
