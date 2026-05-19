from fastapi import FastAPI, HTTPException, Query
import logging
import sqlite3

app = FastAPI(title="Hardened SQL search")
logger = logging.getLogger("shieldcode.sql")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("shop.db")
    connection.row_factory = sqlite3.Row
    return connection


def escape_like(value: str) -> str:
    # FIX: escape LIKE wildcards so user input stays data, not pattern control.
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@app.get("/customers")
def search_customers(q: str = Query(..., min_length=1, max_length=80)):
    connection = get_connection()
    pattern = f"%{escape_like(q)}%"

    # FIX: parameterized placeholders keep the SQL structure fixed. The
    # database driver sends attacker input as values, not executable SQL.
    sql = """
        SELECT id, email, full_name
        FROM customers
        WHERE full_name LIKE ? ESCAPE '\\'
           OR email LIKE ? ESCAPE '\\'
        ORDER BY full_name
    """

    try:
        rows = connection.execute(sql, (pattern, pattern)).fetchall()
    except sqlite3.DatabaseError as exc:
        # FIX: log the internal error server-side, return a generic client
        # message, and avoid leaking table or column names.
        logger.exception("customer_search_failed")
        raise HTTPException(status_code=500, detail="Search failed") from exc
    finally:
        connection.close()

    return {"results": [dict(row) for row in rows]}
