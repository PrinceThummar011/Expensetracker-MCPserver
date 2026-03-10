<div align="center">

# 💸 ExpenseTracker MCP Server

**Track your expenses through natural language — no dashboards, no friction, just vibes and SQLite.**

[![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python&logoColor=white)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.0+-orange)](https://gofastmcp.com)
[![uv](https://img.shields.io/badge/uv-package%20manager-purple)](https://docs.astral.sh/uv/)
[![SQLite](https://img.shields.io/badge/SQLite-embedded%20DB-lightblue?logo=sqlite)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## what is this

**ExpenseTracker MCP Server** is a lightweight, fully local expense tracker that plugs directly into any MCP-compatible AI client — Claude Desktop, Cursor, Gemini CLI, you name it. Instead of opening some bloated finance app, you just *talk* to your AI and your expenses get logged, edited, summarized, or deleted. Backed by SQLite, zero cloud dependencies, zero API keys.

Built with [FastMCP](https://gofastmcp.com) + Python. Runs locally. Actually fast.

---

## features

- 📝 **Add expenses** — date, amount, category, subcategory, notes, the whole nine
- 📋 **List expenses** — pull everything within any date range
- 📊 **Summarize spending** — group by category, spot where your money actually goes
- ✏️ **Edit expenses** — patch only the fields you want, nothing else changes
- 🗑️ **Delete expenses** — gone, no confirm dialog, no drama
- 📂 **Browse categories** — exposed as a live MCP resource, edit the JSON anytime
- ⚡ **Fully local** — no cloud, no subscriptions, no data leaving your machine

---

## project structure

```
ExpenseTracker-MCPserver/
├── main.py              # all the MCP tools & resources live here
├── categories.json      # expense categories — edit freely, no restart needed
├── expenses.db          # SQLite database (auto-created on first run)
├── pyproject.toml       # project metadata & dependencies
└── README.md
```

---

## prerequisites

| Tool | Purpose |
|---|---|
| [Python 3.14+](https://python.org) | Runtime |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | Package & env manager |

Install `uv` if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## getting started

### 1. Clone the repo

```bash
git clone https://github.com/PrinceThummar011/Expensetracker-MCPserver.git
cd Expensetracker-MCPserver
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the server

```bash
uv run fastmcp run main.py
```

> `expenses.db` gets created automatically on first run. No setup needed.

---

## install into your AI client

One command per client. Done.

```bash
# Claude Desktop
uv run fastmcp install claude-desktop main.py

# Cursor
uv run fastmcp install cursor main.py

# Claude Code
uv run fastmcp install claude-code main.py

# Gemini CLI
uv run fastmcp install gemini-cli main.py
```

Restart the client after installing — tools appear automatically.

---

## available tools

| Tool | What it does |
|---|---|
| `add_expense` | Log a new expense |
| `list_expenses` | Fetch all expenses in a date range |
| `summarize` | Spending breakdown by category |
| `edit_expense` | Update specific fields on an existing expense |
| `delete_expense` | Remove an expense by ID |

### tool reference

#### `add_expense`

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `date` | `str` | ✅ | `YYYY-MM-DD` |
| `amount` | `float` | ✅ | Expense amount |
| `category` | `str` | ✅ | e.g. `food`, `transport` |
| `subcategory` | `str` | ❌ | e.g. `dining_out`, `fuel` |
| `note` | `str` | ❌ | Free text |

#### `list_expenses`

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `start_date` | `str` | ✅ | `YYYY-MM-DD` |
| `end_date` | `str` | ✅ | `YYYY-MM-DD` |

Returns all records in range, ordered by ID ascending.

#### `summarize`

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `start_date` | `str` | ✅ | `YYYY-MM-DD` |
| `end_date` | `str` | ✅ | `YYYY-MM-DD` |
| `category` | `str` | ❌ | Filter to a single category |

Returns total per category, sorted alphabetically.

#### `edit_expense`

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `expense_id` | `int` | ✅ | ID of the expense |
| `date` | `str` | ❌ | New date |
| `amount` | `float` | ❌ | New amount |
| `category` | `str` | ❌ | New category |
| `subcategory` | `str` | ❌ | New subcategory |
| `note` | `str` | ❌ | New note |

Only the fields you pass get updated. Everything else stays untouched.

#### `delete_expense`

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `expense_id` | `int` | ✅ | ID of the expense to delete |

---

## expense categories

Defined in `categories.json`. Edit the file freely — no server restart needed, it's read fresh every time.

| Category | Sample Subcategories |
|---|---|
| `food` | groceries, dining_out, coffee_tea, delivery_fees |
| `transport` | fuel, public_transport, cab_ride_hailing, parking |
| `housing` | rent, maintenance_hoa, repairs_service |
| `utilities` | electricity, internet_broadband, mobile_phone |
| `health` | medicines, doctor_consultation, fitness_gym |
| `education` | books, courses, online_subscriptions |
| `entertainment` | movies_events, streaming_subscriptions, games_apps |
| `shopping` | clothing, electronics_gadgets, home_decor |
| `travel` | flights, hotels, visa_passport |
| `investments` | mutual_funds, stocks, crypto |
| `subscriptions` | saas_tools, cloud_ai, music_video |
| `misc` | uncategorized, other |

---

## example prompts (once connected to Claude)

Literally just talk to it:

```
"Add an expense of ₹250 for lunch today under food > dining_out"
"Show me all my expenses this month"
"How much did I spend on transport in February 2026?"
"Edit expense ID 5 — change the amount to ₹500"
"Delete expense number 3"
"Summarize my spending for March 2026 by category"
"What's my biggest spending category this year?"
```

---

## dev & testing

### Interactive MCP Inspector (browser UI)

```bash
uv run fastmcp dev inspector main.py
```

Spins up a live browser UI to call all tools interactively. Auto-reloads on save. In the Inspector, select **STDIO** from the transport dropdown and hit **Connect**.

### Inspect the server

```bash
# Quick summary
uv run fastmcp inspect main.py

# Full JSON output
uv run fastmcp inspect main.py --format fastmcp
uv run fastmcp inspect main.py --format mcp -o manifest.json
```

### List tools

```bash
uv run fastmcp list main.py
uv run fastmcp list main.py --resources
uv run fastmcp list main.py --input-schema
uv run fastmcp list main.py --json
```

### Call tools from terminal

```bash
# add
uv run fastmcp call main.py add_expense \
  date=2026-03-10 amount=150 category=food subcategory=dining_out note="Lunch"

# list
uv run fastmcp call main.py list_expenses \
  start_date=2026-03-01 end_date=2026-03-31

# summarize
uv run fastmcp call main.py summarize \
  start_date=2026-03-01 end_date=2026-03-31

# edit
uv run fastmcp call main.py edit_expense \
  expense_id=1 amount=200 note="Updated"

# delete
uv run fastmcp call main.py delete_expense expense_id=1

# json output
uv run fastmcp call main.py list_expenses \
  start_date=2026-03-01 end_date=2026-03-31 --json
```

### Run with auto-reload

```bash
uv run fastmcp run main.py --reload
```

### Discover all configured MCP servers

```bash
uv run fastmcp discover
```

---

## adding a new tool

Open `main.py` and add a decorated function:

```python
@mcp.tool()
def my_new_tool(param: str):
    '''Description of what this tool does.'''
    # your logic here
    return {"status": "ok"}
```

Then reinstall into your client:

```bash
uv run fastmcp install claude-desktop main.py
```

---

## dependencies

| Package | Version | Purpose |
|---|---|---|
| [`fastmcp`](https://gofastmcp.com) | `>=3.1.0` | MCP server framework |
| `python` | `>=3.14` | Runtime |

```bash
uv sync
```

---

## license

MIT — use it, fork it, ship it.

---
