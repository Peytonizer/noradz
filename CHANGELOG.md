# Changelog

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
