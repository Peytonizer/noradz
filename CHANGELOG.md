# Changelog

## 2026-08-28 (12)

- Dropped the wall-clock hours column from the ledger. It measured elapsed time
  between a session's first and last message, so a session left open overnight
  counted as 20 hours of "work" — misleading enough not to be worth showing.
- `ledger-projects.json` now takes ordinary `~/git/<repo>` paths instead of
  pre-slugified transcript directory names, and the script does the conversion.
  Keeps an absolute home path (and the username in it) out of a public repo.

## 2026-08-28 (11)

- Added `tools/build_ledger.py` + `tools/ledger-projects.json`, generating
  `data/ledger.json` — per-project sessions, prompts, tokens, cost and lines
  changed, read from the local Claude Code transcripts in `~/.claude/projects`.
  Data only for now; nothing renders it yet.
- Must run locally and have its output committed: GitHub Actions can't read
  `~/.claude`, and the transcripts exist only on the machine that produced them,
  so the committed JSON is the durable record.
- Only aggregates are written out. Transcripts hold full prompt text and file
  contents, so no per-session detail, paths or session IDs reach the output.
- Costs: sessions from newer Claude Code versions carry a recorded cost; older
  ones predate that and are priced from token counts using a rate table in the
  script (cache reads at 0.1x the input rate, 1-hour cache writes at 2x — checked
  against sessions that do carry a cost, and they reproduce it exactly). Those
  sessions are flagged rather than silently mixed in.

## 2026-08-28 (10)

- Added `IDEAS.md` — a blue-sky backlog for the site's future (detail pages,
  a build log, `projects.json`-driven rendering, AI-native ideas, polish).
  Kept out of `noradz-site-spec.md` deliberately: the spec stays the frozen
  v1 build record, so speculative work needed its own home.

## v1.0.0 — 2026-08-28

First public release, tagged and shipped to https://noradz.io and
https://www.noradz.io. Everything below this line is what shipped in it.

## 2026-08-28 (9)

- Added `favicon.svg` (the nav's razor mark) and linked it in `<head>` —
  browser tab now shows the brand mark instead of a generic icon.
- Removed "— does what it says on the tin" from the About lead sentence
  (kept on the hero subhead and meta description).
- Removed the "© noradz" copyright line from the footer; the `nothing here
  is spilled` line now stands alone. Dropped the now-unused `.copyright`
  CSS rule.

## 2026-08-28 (8)

- Private-repo badge: "unspilled" -> "classified" (dropped the unexplained
  lore pun for a word that reads correctly with no context). Renamed the CSS
  class `badge-sealed` -> `badge-private` so future wording changes don't
  require another rename.

## 2026-08-28 (7)

- About lead: "A running list of the AI stuff that's actually shipped" -> "A
  record of AI builds that made it out the door".

## 2026-08-28 (6)

- Tagline: "it is what it is" -> "does what it says on the tin" (hero subhead,
  meta description, About lead).

## 2026-08-28 (5)

- Added an About section (id `about`, in-page — no separate route) between
  the project grid and footer: what the log is, plus a one-line "who's
  behind it". `about the site` CTA and the nav `about` link now scroll to it
  instead of pointing nowhere.
- Replaced "kept simple, kept honest" with "it is what it is" everywhere it
  appeared (hero subhead, meta description, About section).

## 2026-08-28 (4)

- Removed the `contact` nav link by design — the site isn't meant to be a
  contact channel.

## 2026-08-28 (3)

- Set up the custom domain: `noradz.io` as primary (CNAME committed, Pages API
  configured), `www.noradz.io` redirecting to it once DNS is pointed at
  GitHub's Pages IPs.
- Swapped the nav's single status dot for a 3x3 dot grid (an alternate mark
  from the design canvas session).
- Hero headline changed from "Quiet systems. / Loud results." to "Noradzeer!".
- Added an `unspilled` badge for cards whose repo is still private (currently
  Aristaeus) — dashed border, padlock glyph, muted colour so it doesn't
  compete with the red accent. Plays on the footer's existing "nothing here
  is spilled" line: an unspilled project is one that hasn't been released.

## 2026-08-28 (2)

- Enabled GitHub Pages (deploy from `main`, root) — live at
  https://peytonizer.github.io/noradz/
- Replaced the three placeholder project cards with real projects, pulled from
  each repo's README: Torn Battlecards, Strata Bot, Aristaeus. Categories and
  tags were picked to describe each project's actual nature rather than reused
  from the placeholder mockup.

## 2026-08-28

- Scaffolded the site from `noradz-site-spec.md`: nav, hero, 3-up project grid (placeholder
  cards), footer. Plain static HTML/CSS, no framework — matches the Strata / Torn Battlecards
  pattern and deploys cleanly to GitHub Pages with zero tooling.
- Project cards use placeholder copy (`[Project Alpha/Beta/Gamma]`) per the spec's copy status —
  real projects still needed.
- `work`/`about`/`contact` nav links and the "about the site" CTA point nowhere yet (`#`) —
  destinations are an open decision from the spec.
- Mobile/tablet breakpoints aren't in the spec (desktop-only mockup); added a build-time
  responsive pass at 900px and 560px to keep the layout usable on smaller screens.
