from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="Vulnerable comment preview")


@app.post("/preview", response_class=HTMLResponse)
def preview_comment(display_name: str = Form(...), comment: str = Form(...)):
    # VULNERABLE: user-controlled strings are inserted directly into an HTML
    # response. If comment contains <script> or an event handler, the browser
    # executes attacker-controlled JavaScript in the victim's session.
    html = f"""
    <html>
      <body>
        <h1>Preview for {display_name}</h1>
        <article class="comment">{comment}</article>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
