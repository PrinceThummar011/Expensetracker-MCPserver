<div align="center">

# 💸 ExpenseTracker MCP Server

**A local Model Context Protocol (MCP) server for tracking personal expenses — built with [FastMCP](https://gofastmcp.com) and SQLite.**

[![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python&logoColor=white)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.0+-orange)](https://gofastmcp.com)
[![uv](https://img.shields.io/badge/uv-package%20manager-purple)](https://docs.astral.sh/uv/)
[![SQLite](https://img.shields.io/badge/SQLite-embedded%20DB-lightblue?logo=sqlite)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📖 Overview

**ExpenseTracker MCP Server** lets you manage daily expenses through natural language via any MCP-compatible client (Claude Desktop, Cursor, Gemini CLI, etc.). Add, list, summarize, edit, and delete expenses — all through AI conversation, backed by a fully local SQLite database.

---

## ✨ Features

- 📝 **Add expenses** with date, amount, category, subcategory, and notes
- 📋 **List expenses** within any date range
- 📊 **Summarize spending** by category over any period
- ✏️ **Edit expenses** — update only the fields you want
- 🗑️ **Delete expenses** by ID
- 📂 **Browse categories** as a structured MCP resource
- ⚡ Fully local — no cloud, no API keys, just SQLite

---

## 🗂️ Project Structure

```
Expensetracker-MCPserver/
├── src/
│   └── expensetracker/
│       ├── __init__.py          # Package version
│       ├── server.py            # FastMCP server — all tools & resources
│       └── database.py          # DB path constants & schema init
├── data/
│   ├── categories.json          # Expense categories & subcategories
│   └── expenses.db              # SQLite database (auto-created, git-ignored)
├── main.py                      # Backward-compat entry point shim
├── .env.example                 # Sample environment variable overrides
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## ⚙️ Prerequisites

| Tool | Purpose |
|---|---|
| [Python 3.14+](https://python.org) | Runtime |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | Package & environment manager |

Install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Expensetracker-MCPserver.git
cd Expensetracker-MCPserver
```

### 2. Install dependencies

```bash
uv sync
```

> This installs the package in editable mode and makes the `expensetracker` and `fastmcp` commands available.

### 3. Run the server

```bash
fastmcp run src/expensetracker/server.py
```

> The `data/` directory and `expenses.db` database are created automatically on first run.

---

## 🔌 Install into MCP Clients

### Claude Desktop

```bash
fastmcp install claude-desktop src/expensetracker/server.py
```

### Cursor

```bash
fastmcp install cursor src/expensetracker/server.py
```

### Claude Code

```bash
fastmcp install claude-code src/expensetracker/server.py
```

### Gemini CLI

```bash
fastmcp install gemini-cli src/expensetracker/server.py
```

> Restart the client after installing — tools appear automatically.

---

## 🧪 Testing & Development Commands

### Interactive browser UI — MCP Inspector

```bash
fastmcp dev inspector src/expensetracker/server.py
```

Launches a live browser UI to call all tools interactively. Auto-reloads on file save.

> In the Inspector, select **STDIO** from the transport dropdown and click **Connect**.

---

### Inspect — view tools, resources & metadata

```bash
fastmcp inspect src/expensetracker/server.py
```

Sample output:

```
Server: ExpenseTracker

Components:
  Tools: 5
  Resources: 1

Environment:
  FastMCP: 3.x.x
  MCP: 1.x.x

Use --format [fastmcp|mcp] for complete JSON output
```

Full JSON output:

```bash
fastmcp inspect src/expensetracker/server.py --format fastmcp
fastmcp inspect src/expensetracker/server.py --format mcp -o manifest.json
```

---

### List tools

```bash
fastmcp list src/expensetracker/server.py
```

Include resources and full schemas:

```bash
fastmcp list src/expensetracker/server.py --resources
fastmcp list src/expensetracker/server.py --input-schema
fastmcp list src/expensetracker/server.py --json
```

---

### Call tools directly from terminal

```bash
# Add an expense
fastmcp call src/expensetracker/server.py add_expense \
  date=2026-03-10 amount=150 category=food subcategory=dining_out note="Lunch"

# List expenses
fastmcp call src/expensetracker/server.py list_expenses \
  start_date=2026-03-01 end_date=2026-03-31

# Summarize spending
fastmcp call src/expensetracker/server.py summarize \
  start_date=2026-03-01 end_date=2026-03-31

# Edit an expense
fastmcp call src/expensetracker/server.py edit_expense \
  expense_id=1 amount=200 note="Updated lunch"

# Delete an expense
fastmcp call src/expensetracker/server.py delete_expense expense_id=1
```

JSON output for any call:

```bash
fastmcp call src/expensetracker/server.py list_expenses \
  start_date=2026-03-01 end_date=2026-03-31 --json
```

---

### Run with auto-reload (development)

```bash
fastmcp run src/expensetracker/server.py --reload
```

---

### Discover all configured MCP servers on your machine

```bash
fastmcp discover
```

---

### Check FastMCP version

```bash
fastmcp version
```

---

## 🛠️ Available MCP Tools

| Tool | Description |
|---|---|
| `add_expense` | Add a new expense entry |
| `list_expenses` | List all expenses in a date range |
| `summarize` | Summarize spending by category |
| `edit_expense` | Edit an existing expense by ID |
| `delete_expense` | Delete an expense by ID |

### Tool Details

#### `add_expense`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `str` | ✅ | Date in `YYYY-MM-DD` format |
| `amount` | `float` | ✅ | Expense amount |
| `category` | `str` | ✅ | Main category (e.g. `food`) |
| `subcategory` | `str` | ❌ | Subcategory (e.g. `dining_out`) |
| `note` | `str` | ❌ | Optional note |

#### `list_expenses`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `start_date` | `str` | ✅ | Start date `YYYY-MM-DD` |
| `end_date` | `str` | ✅ | End date `YYYY-MM-DD` |

Returns all records in range, ordered by date and ID.

#### `summarize`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `start_date` | `str` | ✅ | Start date `YYYY-MM-DD` |
| `end_date` | `str` | ✅ | End date `YYYY-MM-DD` |
| `category` | `str` | ❌ | Filter to a single category |

Returns total spending per category, sorted by highest spend.

#### `edit_expense`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `expense_id` | `int` | ✅ | ID of the expense to edit |
| `date` | `str` | ❌ | New date |
| `amount` | `float` | ❌ | New amount |
| `category` | `str` | ❌ | New category |
| `subcategory` | `str` | ❌ | New subcategory |
| `note` | `str` | ❌ | New note |

Only provided fields are updated — all others stay unchanged.

#### `delete_expense`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `expense_id` | `int` | ✅ | ID of the expense to delete |

---

## 📂 Expense Categories

Defined in [`data/categories.json`](data/categories.json) — edit freely without restarting the server.

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

## 💬 Example Prompts (in Claude)

Once connected to Claude Desktop, try:

- *"Add an expense of ₹250 for lunch today under food > dining_out"*
- *"Show me all my expenses this month"*
- *"How much did I spend on transport in February 2026?"*
- *"Edit expense ID 5 — change the amount to ₹500"*
- *"Delete expense number 3"*
- *"Summarize my spending for March 2026 by category"*
- *"What's my biggest spending category this year?"*

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| [`fastmcp`](https://gofastmcp.com) | `>=3.1.0` | MCP server framework |
| `python` | `>=3.14` | Runtime |

```bash
uv sync      # install all dependencies
```

---

## 🔧 Development

### Add a new tool

In [`src/expensetracker/server.py`](src/expensetracker/server.py):

```python
@mcp.tool()
def my_new_tool(param: str) -> dict:
    """Description of what this tool does."""
    # your logic here
    return {"status": "ok"}
```

### Re-install into clients after changes

```bash
fastmcp install claude-desktop src/expensetracker/server.py
```

### Run over HTTP (for remote testing)

```bash
fastmcp run src/expensetracker/server.py --transport http --port 9000
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ using <a href="https://gofastmcp.com">FastMCP</a> + <a href="https://docs.astral.sh/uv/">uv</a>
</div>
