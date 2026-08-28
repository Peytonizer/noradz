# Noradz

Personal landing page for the noradz domain — collates and showcases Matt's AI projects.

Built to a "Signal" design direction (red/black, techy). Plain static HTML/CSS, no build
step, no framework — deployed via GitHub Pages.

The build spec and the forward-looking idea backlog are kept in a private repo rather than
here, so this repo stays the published site and nothing else.

## Structure

```
index.html               page markup
css/style.css            all styling (colour tokens, type, layout, responsive rules)
data/ledger.json         generated build-ledger data (committed — see below)
tools/build_ledger.py    generates data/ledger.json from Claude Code transcripts
tools/ledger-projects.json  which working directories belong to which project
```

## Build ledger

An honest record of how much AI work went into each project: sessions, prompts typed,
tokens, API-equivalent cost, lines changed.

Claude Code keeps a JSONL transcript of every session under
`~/.claude/projects/<slugified-cwd>/`. Nothing is lost when a session ends — `/clear`
starts a new transcript rather than deleting the old one — so those files are a complete
local history of how each project was built. `tools/build_ledger.py` reduces them to
per-project aggregates:

```sh
python3 tools/build_ledger.py --print
```

Three things about it worth knowing:

- **It has to run locally and its output is committed.** GitHub Actions can't see
  `~/.claude`, so this can't be a CI step. `data/ledger.json` is committed deliberately —
  it's the durable snapshot. Transcripts live only on the machine that produced them and
  could be pruned or lost, at which point the committed JSON is the only remaining record.
- **Only aggregates leave the transcripts.** They contain full prompt text, file contents
  and command output, so the script emits nothing but counts, totals and dates. Never
  publish the transcripts themselves.
- **Costs are API-equivalent list prices, not what was paid.** Newer sessions carry a cost
  Claude Code worked out itself; sessions predating that are priced from token counts using
  the table in the script, and are flagged with `estimated_cost_sessions`. On a
  subscription plan neither figure is money that changed hands — the site should say so
  wherever these numbers are shown.

Adding a project means adding an entry to `tools/ledger-projects.json` and re-running.

## Run locally

No build step — open `index.html` directly in a browser, or serve it so relative paths and
fonts behave the same as production:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Status

**v1.0.0 — released.** Live at https://noradz.io and https://www.noradz.io (GitHub Pages,
deployed from `main`, custom domain with a GitHub-managed HTTPS cert).

Project cards show real projects (Torn Battlecards, Strata Bot, Aristaeus). No `contact` link
by design — this isn't meant to be a contact channel. `work` and `about` are in-page anchors
(no separate routes). Mobile/tablet breakpoints are a build-time addition — the spec only
covers the 1440px desktop mockup.
