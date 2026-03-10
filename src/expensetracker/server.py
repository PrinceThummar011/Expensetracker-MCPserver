"""ExpenseTracker MCP Server — tools and resources."""

import sqlite3

from fastmcp import FastMCP

from expensetracker.database import CATEGORIES_PATH, DB_PATH, init_db

# ── Initialise ────────────────────────────────────────────────────────────────
init_db()

mcp = FastMCP(
    "ExpenseTracker",
    instructions=(
        "Track, list, summarize, edit, and delete personal expenses. "
        "Dates must be in YYYY-MM-DD format."
    ),
)


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = "",
) -> dict:
    """Add a new expense entry to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note)"
            " VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note),
        )
        return {"status": "ok", "id": cur.lastrowid}


@mcp.tool()
def list_expenses(start_date: str, end_date: str) -> list[dict]:
    """List expense entries within an inclusive date range."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
              FROM expenses
             WHERE date BETWEEN ? AND ?
             ORDER BY date ASC, id ASC
            """,
            (start_date, end_date),
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


@mcp.tool()
def summarize(
    start_date: str,
    end_date: str,
    category: str | None = None,
) -> list[dict]:
    """Summarize expenses by category within an inclusive date range."""
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT   category, SUM(amount) AS total_amount
              FROM   expenses
             WHERE   date BETWEEN ? AND ?
        """
        params: list = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY total_amount DESC"

        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


@mcp.tool()
def delete_expense(expense_id: int) -> dict:
    """Delete an expense entry by its ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No expense found with id {expense_id}"}
        return {"status": "ok", "deleted_id": expense_id}


@mcp.tool()
def edit_expense(
    expense_id: int,
    date: str | None = None,
    amount: float | None = None,
    category: str | None = None,
    subcategory: str | None = None,
    note: str | None = None,
) -> dict:
    """Edit an existing expense entry by its ID. Only provided fields are updated."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT id, date, amount, category, subcategory, note"
            "  FROM expenses WHERE id = ?",
            (expense_id,),
        )
        row = cur.fetchone()
        if not row:
            return {"status": "error", "message": f"No expense found with id {expense_id}"}

        existing = dict(zip(["id", "date", "amount", "category", "subcategory", "note"], row))
        updated = {
            "date":        date        if date        is not None else existing["date"],
            "amount":      amount      if amount      is not None else existing["amount"],
            "category":    category    if category    is not None else existing["category"],
            "subcategory": subcategory if subcategory is not None else existing["subcategory"],
            "note":        note        if note        is not None else existing["note"],
        }

        conn.execute(
            "UPDATE expenses"
            "   SET date=?, amount=?, category=?, subcategory=?, note=?"
            " WHERE id=?",
            (
                updated["date"],
                updated["amount"],
                updated["category"],
                updated["subcategory"],
                updated["note"],
                expense_id,
            ),
        )
        return {"status": "ok", "updated": {"id": expense_id, **updated}}


# ── Resources ─────────────────────────────────────────────────────────────────

@mcp.resource("expense://categories", mime_type="application/json")
def categories() -> str:
    """Return the full categories tree. Read fresh so file edits take effect immediately."""
    with open(CATEGORIES_PATH, encoding="utf-8") as fh:
        return fh.read()


# ── Entry-point ───────────────────────────────────────────────────────────────

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
