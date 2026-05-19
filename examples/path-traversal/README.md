# Path Traversal Scenario

This FastAPI example downloads invoice PDFs from a storage directory.

## Attack

The vulnerable endpoint accepts:

```text
GET /invoices/download?filename=../../.env
```

`vulnerable.py` joins the raw filename with the invoice directory. `../`
segments can escape the intended folder and read application secrets or system
files if the process has permission.

## Fix

`hardened.py` applies ShieldCode's file security rules:

- Validate filenames with an allowlist regex.
- Resolve the final path before reading it.
- Verify the resolved path stays inside the allowed base directory.
- Require a regular file and return the expected PDF media type.

## ShieldCode in action

Prompt Claude Code after installing ShieldCode:

```text
Create a FastAPI endpoint to download invoice files by filename.
```

With ShieldCode active, Claude should reject arbitrary path input and keep all
file access inside an explicitly approved directory.
