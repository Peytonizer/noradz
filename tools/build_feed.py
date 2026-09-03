#!/usr/bin/env python3
"""Build feed.xml (RSS 2.0) from data/log.json, the canonical JSON Feed.

data/log.json is itself a valid JSON Feed (https://www.jsonfeed.org/version/1.1/)
and doubles as both the /log page's data source and a feed URL for readers
that speak JSON Feed directly. This script covers the readers that only speak
RSS, generating a static feed.xml from that same file — no server, no second
place to author entries. Run it after editing data/log.json and commit the
result, the same local-script-then-commit pattern as tools/build_ledger.py:

    python3 tools/build_feed.py

Options:
    --feed PATH   source JSON Feed (default data/log.json)
    --out PATH    output file (default feed.xml)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


def rfc822(iso_date):
    """Convert a JSON Feed date_published (RFC 3339) to RSS's RFC 822 format."""
    return datetime.fromisoformat(iso_date).strftime("%a, %d %b %Y %H:%M:%S %z")


def rss_item(item):
    return (
        "    <item>\n"
        f"      <title>{escape(item['title'])}</title>\n"
        f"      <link>{escape(item['url'])}</link>\n"
        f"      <guid isPermaLink=\"true\">{escape(item['url'])}</guid>\n"
        f"      <pubDate>{rfc822(item['date_published'])}</pubDate>\n"
        f"      <description>{escape(item['content_html'])}</description>\n"
        "    </item>"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--feed", default="data/log.json")
    parser.add_argument("--out", default="feed.xml")
    args = parser.parse_args()

    feed = json.loads(Path(args.feed).read_text(encoding="utf-8"))
    items = sorted(feed["items"], key=lambda i: i["date_published"], reverse=True)
    items_xml = "\n".join(rss_item(item) for item in items)

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        "  <channel>\n"
        f"    <title>{escape(feed['title'])}</title>\n"
        f"    <link>{escape(feed['home_page_url'])}</link>\n"
        f"    <description>{escape(feed.get('description', ''))}</description>\n"
        f"{items_xml}\n"
        "  </channel>\n"
        "</rss>\n"
    )

    out_path = Path(args.out)
    out_path.write_text(xml, encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
