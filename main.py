"""
Backward-compatible entry point.
Prefer:  fastmcp run src/expensetracker/server.py
"""
from expensetracker.server import mcp  # noqa: F401 — re-exported so `fastmcp run main.py` resolves `mcp`

if __name__ == "__main__":
    mcp.run()
