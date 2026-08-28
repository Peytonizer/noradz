# Noradz — Homepage Build Spec

Direction: **Signal** (red/black, techy). Source mockup: `Main.dc.html` on the design canvas — https://claude.ai/code/artifact/3543b41a-3356-4d70-b140-3d55917b5c1a

This is a single-page layout: nav, hero, a 3-up project grid, footer.

## Fonts

Google Fonts, loaded in `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
```

- Body / headings: `'Space Grotesk', system-ui, sans-serif`
- Labels, nav, tags, footer, all-caps micro-copy: `'IBM Plex Mono', 'Courier New', monospace`

## Color tokens

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0b0b0d` | page background |
| `--surface` | `#131315` | project cards |
| `--border` | `#212124` | hairline dividers, card borders |
| `--border-soft` | `#2c2c30` | button/tag borders |
| `--text` | `#ededed` | primary text |
| `--text-muted` | `#9a9aa0` | nav links, subhead |
| `--text-dim` | `#8a8a90` | card body copy |
| `--text-faint` | `#6a6a70` | section eyebrow |
| `--text-faintest` | `#4a4a50` | footer, counters |
| `--accent` | `#d1293d` | red accent — links, eyebrow text, tags, primary CTA, live-dot |
| `--accent-hover` | `#ee5a6b` | link hover |

Red = the Ra-Kacharz (ruling accent), black/near-black = the citizens (base surface) — that split is the whole color logic, so don't dilute it with a second accent color.

## Nav mark

The chosen icon ("Straight Razor" / The Shave — a nod to Noradz citizens' shaved heads under the cleanliness rule). 18px in the nav, stroke `#d1293d`, `stroke-width: 1.6`, round caps. The chord touches the circle exactly at both ends — don't let it overhang.

```svg
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d1293d" stroke-width="1.6" stroke-linecap="round">
  <circle cx="12" cy="13" r="6"/>
  <path d="M7.13 9.5L16.87 9.5"/>
</svg>
```

## Layout

Desktop canvas ~1440px wide; scale down responsively (this spec doesn't cover the mobile breakpoint — that's a build decision, not something the mockup settled).

**Nav** — flex row, space-between, `padding: 28px 72px`, bottom border `1px solid var(--border)`.
- Left: mark (18px) + `NORADZ` wordmark, mono, 15px, `letter-spacing: 0.14em`.
- Right: `work` / `about` / `contact` links (mono, 13px, `--text-muted`) + an 8px red dot with a soft glow (`box-shadow: 0 0 8px #d1293d`) as a live/status indicator.

**Hero** — `padding: 140px 72px 120px`, bottom border.
- Eyebrow: `// AI PROJECTS & EXPERIMENTS`, mono, 12px, `letter-spacing: 0.2em`, accent color.
- H1: "Quiet systems.<br>Loud results." — 64px, weight 700, line-height 1.08, max-width 780px.
- Subhead: "A working log of models, tools and small AI builds — kept simple, kept honest." 17px, `--text-muted`, max-width 520px.
- Two CTAs: primary solid-red button "See the work →" (14px, weight 600, dark text on red, `border-radius: 3px`), secondary outline button "about the site" (mono, 13px, 1px border).

**Projects** — `padding: 100px 72px`.
- Section header row: eyebrow "SELECTED WORK" (mono, 13px, uppercase, `letter-spacing: 0.18em`, `--text-faint`) left, entry count right (mono, 12px, `--text-faintest`).
- 3-column grid, `gap: 24px`. Each card: `--surface` bg, `1px solid var(--border)`, `border-radius: 4px`, `padding: 32px`.
  - Kicker: `01 · agent` style (index + category), mono, 11px, accent color.
  - Title: 20px, weight 600.
  - One-line description: 14px, `--text-dim`.
  - Tag pills: mono, 11px, `1px solid var(--border-soft)`, `border-radius: 20px`, `padding: 4px 10px`.

**Footer** — `padding: 32px 72px`, top border, space-between.
- Left: `nothing here is spilled` (mono, 11px, `--text-faintest`, `letter-spacing: 0.08em`) — the site's one lore easter egg, playing on Noradz's "spilled food is evil" rule.
- Right: `© noradz`.

## Copy status — what's real vs. placeholder

Structural copy (headline, subhead, nav labels, button labels, footer lines) is final. The three project cards are **placeholders** — `[Project Alpha/Beta/Gamma]`, their one-liners, and their tags all need your real projects before this ships. Everything else in the mockup is ready to build from as-is.

## Open decisions for the build

- Mobile / tablet breakpoints aren't designed yet — only the 1440px desktop layout exists.
- Real project count: layout assumes 3 cards in a row; more than 3 needs a grid/pagination decision.
- Link destinations (`work`, `about`, `contact`, per-project links) aren't defined.
