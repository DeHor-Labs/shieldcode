from fastapi import FastAPI, HTTPException, Query
import sqlite3

app = FastAPI(title="Vulnerable SQL search")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("shop.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.get("/customers")
def search_customers(q: str = Query(..., min_length=1)):
    connection = get_connection()

    # VULNERABLE: user-controlled input is interpolated directly into SQL.
    # An attacker can send q=' OR '1'='1 to turn the WHERE clause into a
    # tautology, or append UNION queries to read unrelated tables.
    sql = (
        "SELECT id, email, full_name FROM customers "
        f"WHERE full_name LIKE '%{q}%' OR email LIKE '%{q}%' "
        "ORDER BY full_name"
    )

    try:
        rows = connection.execute(sql).fetchall()
    except sqlite3.DatabaseError as exc:
        # VULNERABLE: returning raw database errors can reveal schema details
        # that make injection attacks easier to refine.
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        connection.close()

    return {"results": [dict(row) for row in rows]}
