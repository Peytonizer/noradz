# Noradz

Personal landing page for the noradz domain — collates and showcases Matt's AI projects.

Built to a "Signal" design direction (red/black, techy). Plain static HTML/CSS, no build
step, no framework — deployed via GitHub Pages.

The build spec and the forward-looking idea backlog are kept in a private repo rather than
here, so this repo stays the published site and nothing else.

## Structure

```
index.html               homepage markup
log.html                 /log — dated short entries (see below)
now.html                 /now — what's being built this month, hand-edited
css/style.css            all styling (colour tokens, type, layout, responsive rules)
js/ledger.js             fetches data/ledger.json and renders the build ledger (see below)
js/log.js                fetches data/log.json and renders the log entries (see below)
data/ledger.json         generated build-ledger data (committed — see below)
data/log.json            log entries, authored by hand — also a valid JSON Feed
feed.xml                 RSS version of data/log.json, generated (see below)
tools/build_ledger.py    generates data/ledger.json from Claude Code transcripts
tools/ledger-projects.json  which working directories belong to which project
tools/build_feed.py      generates feed.xml from data/log.json
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

`js/ledger.js` fetches `data/ledger.json` at page load and renders it: a one-line stat
footer on each project card (matched to the ledger by a `data-ledger-slug` attribute on
the card), and a `#ledger` section with sitewide totals and a per-project table. There's
no build step tying the two together — regenerate `data/ledger.json` and commit it, and
the site picks up the new numbers on next load.

## Log

`/log` is dated short entries — what shipped, broke, or changed. `data/log.json` is the
only place entries are authored, and it's written as a valid
[JSON Feed](https://www.jsonfeed.org/version/1.1/) (`version`, `title`, `items[]` with
`id`/`url`/`title`/`content_html`/`date_published`), so the same file is both the page's
data source and a feed URL for readers that speak JSON Feed directly.
`js/log.js` fetches it at page load and renders each item as a dated entry — same
fetch-and-render pattern as `js/ledger.js`, no framework, no build step.

`feed.xml` covers readers that only speak RSS. It's generated from `data/log.json` by
`tools/build_feed.py`, so entries are never authored twice:

```sh
python3 tools/build_feed.py
```

Adding an entry means adding an item to `data/log.json` and re-running that script —
the same local-script-then-commit pattern as the build ledger.

`/now` (`now.html`) is a single hand-edited page — what's being built this month,
updated when it changes and left stale-with-a-date otherwise. No data file, no script.

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
