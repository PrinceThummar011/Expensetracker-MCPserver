"""Database configuration and initialisation."""

import sqlite3
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
# src/expensetracker/database.py  →  project root is three levels up
ROOT_DIR: Path = Path(__file__).parent.parent.parent
DATA_DIR: Path = ROOT_DIR / "data"

DB_PATH: Path = DATA_DIR / "expenses.db"
CATEGORIES_PATH: Path = DATA_DIR / "categories.json"


# ── Schema ────────────────────────────────────────────────────────────────────
_CREATE_EXPENSES = """
    CREATE TABLE IF NOT EXISTS expenses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT    NOT NULL,
        amount      REAL    NOT NULL,
        category    TEXT    NOT NULL,
        subcategory TEXT    DEFAULT '',
        note        TEXT    DEFAULT ''
    )
"""


def init_db() -> None:
    """Create the data directory and expenses table if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(_CREATE_EXPENSES)
