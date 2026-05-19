from fastapi import FastAPI, HTTPException, Query
import httpx

app = FastAPI(title="Vulnerable webhook tester")


@app.get("/webhook/test")
async def test_webhook(url: str = Query(...)):
    # VULNERABLE: the server fetches an arbitrary user-supplied URL. Attackers
    # can target internal services such as http://169.254.169.254/latest/meta-data
    # or http://localhost:8000/admin from the server's network position.
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    # VULNERABLE: reflecting status and body from internal services can expose
    # secrets, metadata, or private admin responses.
    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text[:2000],
    }
