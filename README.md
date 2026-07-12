# Week 4 lab repo — MCP web-search starter template

A minimal, working [FastMCP](https://gofastmcp.com) server exposing one real
tool — `search_web` — backed by live DuckDuckGo search, no API key required.

It's deliberately small and already working: this week's new skill isn't
writing search-API glue code under time pressure, it's registering an MCP
server with Claude Code and using it live. See `LAB_GUIDE.md`.

## Run it

    bash setup.sh
    uv run pytest

## Files

- `server.py` — the MCP server and its one tool. Start here.
- `tests/test_server.py` — tests for `search_web`'s behavior (mocked
  network calls — see the file's docstring for why this is the one place
  this repo departs from Week 3 EVBot's real-but-isolated testing
  convention).
