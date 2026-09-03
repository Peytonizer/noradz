/*
 * Log renderer.
 *
 * Fetches data/log.json — a JSON Feed (https://www.jsonfeed.org/version/1.1/)
 * that doubles as both the /log page's only data source and a real feed URL
 * — and renders its items as dated entries. feed.xml (RSS) is generated from
 * the same file by tools/build_feed.py for readers that don't speak JSON
 * Feed; this script only ever reads data/log.json.
 *
 * Same pattern as js/ledger.js: vanilla JS, no framework, fails quietly if
 * the fetch doesn't work (e.g. opened via file:// instead of served — see
 * README) since the rest of the page works fine without it.
 */

function formatLogDate(iso) {
  return new Intl.DateTimeFormat('en-AU', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(iso));
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

async function loadLog() {
  const res = await fetch('data/log.json');
  if (!res.ok) throw new Error(`log fetch failed: ${res.status}`);
  return res.json();
}

function renderEntries(feed) {
  const list = document.querySelector('.log-list');
  if (!list) return;
  list.innerHTML = '';

  const items = [...feed.items].sort((a, b) => (a.date_published < b.date_published ? 1 : -1));
  items.forEach((item) => {
    const entry = el('article', 'log-entry');
    entry.id = item.id;
    entry.append(el('p', 'log-date', formatLogDate(item.date_published)));
    entry.append(el('h2', 'log-entry-title', item.title));
    const body = el('div', 'log-entry-body');
    body.innerHTML = item.content_html; // authored by the site owner via data/log.json, not user input
    entry.append(body);
    list.append(entry);
  });
}

loadLog()
  .then(renderEntries)
  .catch((err) => {
    // Non-fatal — the rest of the page works fine without the log.
    console.warn('Log not loaded:', err);
  });
