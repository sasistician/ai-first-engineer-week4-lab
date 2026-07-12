"""
Week 4 lab starter template — a minimal MCP server exposing one real tool:
live web search, using DuckDuckGo (no API key required).

Run it directly to sanity-check it starts:
    uv run python server.py

Register it with Claude Code — see week4-lab-guide.md for the full
walkthrough, including exactly how to phrase the `claude mcp add` command.
"""

from fastmcp import FastMCP
from ddgs import DDGS

mcp = FastMCP("week4-web-search")


@mcp.tool()
def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search the live web and return the top results.

    Use this when the user's question needs current information that isn't
    likely to be in Claude's training data or in a local knowledge base —
    pricing, news, recent product specs, anything that changes after a
    model's training cutoff. Do not use this for questions answerable from
    general knowledge alone.

    Args:
        query: the search query, in plain language (e.g. "2026 Rivian R1S insurance cost").
        max_results: how many results to return (default 5, max 10).

    Returns:
        A list of results, each a dict with "title", "url", and "snippet".
    """
    max_results = max(1, min(max_results, 10))
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
    return [
        {"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")}
        for r in results
    ]


if __name__ == "__main__":
    mcp.run()
