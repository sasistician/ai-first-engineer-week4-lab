# Week 4 Lab Guide — MCP: Build and Connect a Live Web-Search Server

**Time budget:** ~35–40 min within the 90-min live session, plus ~5 min
pre-class setup (no model downloads this week — just `uv sync` and a network
check).

**Prerequisite:** Today's deck covered MCP — the host/client/server model,
its three primitives, and the security risks specific to giving an agent a
live connection to a real system. This lab is a working starter template: a
FastMCP server exposing one real tool, `search_web`, backed by live
DuckDuckGo search with no API key required. By the end you'll have it
registered and running inside Claude Code, and you'll extend it yourself.

This lab is deliberately **not** a modification of Week 3's EVBot — it's a
small, standalone repo, so nothing here depends on your EVBot install still
working. The connection is narrative, not code: `search_web` closes exactly
the gap EVBot's own knowledge base couldn't (Step 4 in question, EV
insurance costs) — you'll prove that live in Step 3.

---

## 1. Setup

1. Clone this repo and run the onboarding script.

   macOS/Linux:
   ```
   git clone https://github.com/sasistician/ai-first-engineer-week4-lab.git
   cd ai-first-engineer-week4-lab
   ./setup.sh
   ```
   Windows: run this from [Git Bash](https://git-scm.com/download/win) or
   WSL, same as Week 3:
   ```
   git clone https://github.com/sasistician/ai-first-engineer-week4-lab.git
   cd ai-first-engineer-week4-lab
   bash setup.sh
   ```
2. Follow whatever `setup.sh` prints. It checks for `uv`, installs
   dependencies, and confirms the web-search backend is actually reachable
   from your machine (the one new failure mode this week — a VPN, firewall,
   or corporate proxy blocking outbound HTTPS will show up here, not later).
3. Confirm the baseline passes:
   ```
   uv run pytest
   ```
   All 3 tests should pass.

---

## 2. Quick-reference card

| Piece | File | Role |
|---|---|---|
| The server | `server.py` | Declares the `FastMCP` instance and registers `search_web` |
| The tool | `server.py` — `search_web` | The one capability exposed: live web search, no API key |
| Tests | `tests/test_server.py` | Mocked-network tests for `search_web`'s behavior — see the file's docstring for why this repo mocks where EVBot's tests don't |
| Registration | Claude Code CLI | `claude mcp add` / `list` / `get` / `remove` — covered in Step 2 |

---

## 3. The exercise

### Step 1 — Read the server before you run it

Open `server.py`. It's under 40 lines. Find:

- The `FastMCP("week4-web-search")` line — this is the server's name, what
  a host displays.
- The `@mcp.tool()` decorator and `search_web`'s docstring.

**Checkpoint:** Without running anything, answer this yourself: if a
malicious version of this file wanted to smuggle an instruction to Claude,
where exactly would it hide it, and would you notice? (This is today's
deck, Part 2, made concrete against real code you can actually read.)

### Step 2 — Register the server with Claude Code

From inside this repo's directory, run:
```
claude mcp add week4-web-search -- uv run --directory "$(pwd)" python server.py
```
Then confirm it connected:
```
claude mcp list
```

**Checkpoint:** Confirm `week4-web-search` shows as connected. If it
doesn't, run `claude mcp get week4-web-search` — it prints the exact
command Claude Code is trying to run, which is almost always enough to spot
a wrong path.

### Step 3 — Use it live, on the exact question EVBot couldn't answer

In a Claude Code session (with `week4-web-search` connected), ask:

*"Using the search_web tool, what does insurance typically cost for a 2026
Rivian R1S?"*

**Checkpoint:** Confirm Claude actually invokes `search_web` (Claude Code
will show the tool call) and comes back with a real, current answer —
something EVBot's RAG-only setup could never do, because the docs simply
don't contain it.

### Step 4 — Direct Claude Code to add a second tool

Still in that Claude Code session, ask it to add a second tool to
`server.py` — for example `search_news(topic: str)`, restricted to recent
results. Don't write the code yourself; direct Claude Code to do it,
following the same pattern as `search_web`.

**Checkpoint:** Confirm the new tool has its own clear docstring (the
discovery/attack surface from today's deck, Parts 1 and 2), and that
`uv run pytest` still passes after the change.

### Step 5 — Reconnect and verify the new tool

MCP servers are inspected once, at connection time — Claude Code won't
see a newly-added tool until you reconnect:
```
claude mcp remove week4-web-search -s local
claude mcp add week4-web-search -- uv run --directory "$(pwd)" python server.py
```

**Checkpoint:** Ask a question that should trigger your new tool, and
confirm Claude Code calls it by name.

### Step 6 — Self-audit against today's checklist

Open today's deck to the mitigations checklist (Part 2). Go through it
against your own two tools — not EVBot, not someone else's server, the one
you just wrote.

**Checkpoint:** Name one place your own server would fail the checklist if
this were a real production tool (for example: no rate limiting, no input
length cap on `query`). You don't have to fix it — noticing it is the
point.

---

## 4. Reflection prompts

1. You wrote this server yourself, so you trust it. What would you actually
   check before running a *real* third-party MCP server you didn't write?
2. Compare this exercise to Week 3's Skill-packaging exercise — both give
   Claude a new capability, through different mechanisms. What made this
   week's gap (EV insurance costs) an MCP problem and not a Skill problem?
3. Step 5 required a full reconnect for a new tool to show up. What does
   that imply about how often a production MCP server's tool list should
   change, if reconnecting isn't seamless for every client?
4. If `search_web` were rewritten to also let the model reach a private,
   authenticated API instead of public search results — which specific
   line in today's mitigations checklist would you re-check hardest?

---

## 5. APPLY — your reps this week

- From today's deck, Part "Apply": pick one real internal system from your
  own job that Claude currently can't reach. Sketch — doesn't need to run —
  what its `search_web`-equivalent tool signature and docstring would look
  like.
- Optional stretch: using Claude Code with `week4-web-search` connected,
  direct it to port `search_web`'s approach into a genuine fallback inside
  EVBot's `evbot/agent.py` — called only when RAG returns no relevant
  chunks. This is a real code change to a separate repo; treat it as
  optional extra reps, not required for this week.

Bring your biggest find to next session.

---

## Look ahead

Week 5 is **orchestration and guardrails** — the capstone build. The Skill
you packaged in Week 3 and the MCP server you built this week combine into
one supervised system, with orchestration/guardrails logic deciding when
each piece runs.
