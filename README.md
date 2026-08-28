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

The three project cards on the page are placeholders (`[Project Alpha/Beta/Gamma]`) — real
project content still needs to go in before this ships. See "Open decisions for the build" in
the spec for what's still undecided (mobile breakpoints, real project count, link
destinations for `work` / `about` / `contact`).
