#!/usr/bin/env bash
# Check-and-guide onboarding for the Week 4 MCP lab starter template. Safe
# to re-run after fixing any single reported issue — it never installs
# anything without showing you the exact command first.
#
# Windows: run this from Git Bash (installed alongside Git for Windows,
# https://git-scm.com/download/win) or WSL, same as the Week 3 EVBot setup.
set -euo pipefail

cd "$(dirname "$0")"

fail() {
  echo ""
  echo "❌ $1"
  echo ""
  exit 1
}

echo "== Week 4 MCP lab setup =="

# 1. uv
if ! command -v uv >/dev/null 2>&1; then
  fail "uv is not installed. Install it, then re-run bash setup.sh:
    curl -LsSf https://astral.sh/uv/install.sh | sh"
fi
echo "✓ uv found ($(uv --version))"

# 2. Install deps
echo ""
echo "== Installing dependencies with uv =="
uv sync

# 3. Sanity-check network access — the one thing this lab needs that EVBot didn't
echo ""
echo "== Checking network access for live web search =="
if ! uv run python -c "from ddgs import DDGS; DDGS().text('test', max_results=1)" >/dev/null 2>&1; then
  fail "Couldn't reach the web search backend. Check your internet connection
    and that nothing (VPN, firewall, corporate proxy) is blocking outbound
    HTTPS, then re-run: bash setup.sh"
fi
echo "✓ web search backend reachable"

echo ""
echo "✅ Setup complete. Run the test suite with:"
echo "    uv run pytest"
echo ""
echo "Then see week4-lab-guide.md to register this server with Claude Code."
