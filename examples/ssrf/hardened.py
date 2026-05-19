from ipaddress import ip_address
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
import httpx

app = FastAPI(title="Hardened webhook tester")

ALLOWED_WEBHOOK_HOSTS = {"hooks.stripe.com", "api.github.com", "discord.com"}


def validate_webhook_url(url: str) -> str:
    parsed = urlparse(url)

    # FIX: allow only HTTPS and an explicit host allowlist. This prevents users
    # from turning the API into a proxy for arbitrary internal services.
    if parsed.scheme != "https":
        raise HTTPException(status_code=400, detail="Webhook URL must use HTTPS")
    if parsed.hostname not in ALLOWED_WEBHOOK_HOSTS:
        raise HTTPException(status_code=400, detail="Webhook host is not allowed")

    # FIX: reject literal private, loopback, and link-local IP addresses. Host
    # allowlists are still the main control; this blocks obvious bypass attempts.
    try:
        host_ip = ip_address(parsed.hostname)
    except ValueError:
        return url

    if host_ip.is_private or host_ip.is_loopback or host_ip.is_link_local:
        raise HTTPException(status_code=400, detail="Webhook host is not allowed")
    return url


@app.get("/webhook/test")
async def test_webhook(url: str = Query(..., max_length=300)):
    safe_url = validate_webhook_url(url)

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(3.0),
            follow_redirects=False,
        ) as client:
            response = await client.get(safe_url)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Webhook test failed") from exc

    # FIX: return only minimal metadata. Do not proxy response bodies or headers
    # from third-party systems back to the caller.
    return {"status_code": response.status_code, "reachable": response.is_success}
