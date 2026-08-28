# Noradz

Personal landing page for the noradz domain — collates and showcases Matt's AI projects.

Built from [`noradz-site-spec.md`](./noradz-site-spec.md) in the "Signal" direction (red/black,
techy). Plain static HTML/CSS, no build step, no framework — deployed via GitHub Pages.

## Structure

```
index.html      page markup
css/style.css   all styling (colour tokens, type, layout, responsive rules)
```

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
