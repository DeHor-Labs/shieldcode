from pathlib import Path
import re

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

app = FastAPI(title="Hardened invoice download")

BASE_DIR = Path("storage/invoices").resolve()
SAFE_INVOICE_NAME = re.compile(r"^[a-zA-Z0-9_-]+\.pdf$")


@app.get("/invoices/download")
def download_invoice(filename: str = Query(..., min_length=5, max_length=80)):
    # FIX: allowlist the exact filename format the endpoint supports. Path
    # separators, hidden files, and alternate extensions are rejected up front.
    if not SAFE_INVOICE_NAME.fullmatch(filename):
        raise HTTPException(status_code=400, detail="Invalid invoice filename")

    target = (BASE_DIR / filename).resolve()

    # FIX: resolve the final path and verify it remains inside BASE_DIR before
    # reading. This defends even if symlinks or unusual path segments appear.
    if BASE_DIR not in target.parents:
        raise HTTPException(status_code=400, detail="Invalid invoice path")

    if not target.is_file():
        raise HTTPException(status_code=404, detail="Invoice not found")

    return FileResponse(
        target,
        media_type="application/pdf",
        filename=filename,
    )
