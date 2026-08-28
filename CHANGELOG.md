# Changelog

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
