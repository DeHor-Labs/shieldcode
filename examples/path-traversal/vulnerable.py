from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

app = FastAPI(title="Vulnerable invoice download")

BASE_DIR = Path("storage/invoices")


@app.get("/invoices/download")
def download_invoice(filename: str = Query(...)):
    # VULNERABLE: joining untrusted input allows ../ path traversal. A request
    # like filename=../../.env can escape storage/invoices and read server files.
    target = BASE_DIR / filename

    if not target.exists():
        raise HTTPException(status_code=404, detail="Invoice not found")

    # VULNERABLE: the response returns whatever path the attacker reached.
    return FileResponse(target)
