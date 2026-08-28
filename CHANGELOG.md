# Changelog

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
