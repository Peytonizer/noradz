#!/usr/bin/env python3
"""Build the AI build ledger — how much AI work went into each project on the site.

Claude Code writes one JSONL transcript per session to
~/.claude/projects/<slugified-cwd>/<session-uuid>.jsonl. Every session is kept,
including ones ended with /clear (that starts a new session file rather than
deleting the old one), so the transcripts are a complete local record of how each
project was built. This script reduces them to per-project aggregates and writes
data/ledger.json for the site to render.

Only aggregate numbers come out. Transcripts contain full prompt text, file
contents and command output, so nothing but counts and totals is ever written to
the output file — see README for the reasoning.

Run locally (GitHub Actions can't see ~/.claude) and commit the result:

    python3 tools/build_ledger.py --print

Options:
    --projects PATH   project→transcript mapping (default tools/ledger-projects.json)
    --out PATH        output file (default data/ledger.json)
    --print           also print a summary table to stdout
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

TRANSCRIPT_ROOT = Path.home() / ".claude" / "projects"

# Base API list prices in USD per million tokens, as published by Anthropic
# (checked 2026-08-28). Only needed for older transcripts that predate the
# 'cost-state' record — newer sessions carry a cost Claude Code worked out itself.
MODEL_PRICES = {
    "claude-fable-5": (10.00, 50.00),
    "claude-opus-5": (5.00, 25.00),
    "claude-opus-4-8": (5.00, 25.00),
    "claude-opus-4-7": (5.00, 25.00),
    "claude-opus-4-6": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
}

# Cache tokens are priced as multiples of the model's base input rate: reads are
# heavily discounted, writes carry a premium that depends on the cache lifetime.
# Verified against sessions where Claude Code recorded its own cost — these
# multipliers reproduce its totals exactly.
CACHE_READ_MULTIPLIER = 0.1
CACHE_WRITE_5M_MULTIPLIER = 1.25
CACHE_WRITE_1H_MULTIPLIER = 2.0


def price_for(model):
    """Look up (input, output) $/MTok, tolerating dated model IDs like -20251001."""
    if model in MODEL_PRICES:
        return MODEL_PRICES[model]
    for known, prices in MODEL_PRICES.items():
        if model.startswith(known):
            return prices
    return None


def read_records(path):
    """Yield parsed JSON objects from a transcript, skipping unparseable lines.

    Transcripts are appended to live, so the final line of an in-progress session
    can be truncated mid-write. That's expected, not an error worth stopping for.
    """
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def patch_line_counts(result):
    """Count added/removed lines from an Edit/Write tool result's structured patch."""
    added = removed = 0
    for hunk in result.get("structuredPatch") or []:
        for line in hunk.get("lines", []):
            if line.startswith("+"):
                added += 1
            elif line.startswith("-"):
                removed += 1
    return added, removed


def summarise_session(path):
    """Reduce one session transcript to a stats dict, or None if it's empty.

    Two sources of truth, in order of preference:

    1. The 'cost-state' record Claude Code appends as the session runs. It is
       cumulative and rewritten repeatedly, so the last one wins. Authoritative,
       but only present in transcripts from newer Claude Code versions.
    2. Otherwise, sum the assistant messages' own usage blocks and price them
       from MODEL_PRICES, and count changed lines from the edit tool results.
       Assistant records are deduplicated by requestId because retries and
       streaming can write the same message to the transcript more than once.
    """
    cost_state = None
    usage_by_request = {}
    counted_tool_results = set()
    human_turns = 0
    patch_added = patch_removed = 0
    timestamps = []
    models = set()

    for record in read_records(path):
        kind = record.get("type")

        if kind == "cost-state":
            cost_state = record

        elif kind == "user":
            # origin.kind == "human" marks a real typed or pasted turn. Tool
            # results and injected context also arrive as type "user" and must
            # not be counted as the user saying something.
            if record.get("origin", {}).get("kind") == "human" and not record.get("isSidechain"):
                human_turns += 1
            result = record.get("toolUseResult")
            # Keyed by uuid so a replayed tool result isn't counted twice.
            if isinstance(result, dict) and record.get("uuid") not in counted_tool_results:
                counted_tool_results.add(record.get("uuid"))
                added, removed = patch_line_counts(result)
                patch_added += added
                patch_removed += removed

        elif kind == "assistant":
            message = record.get("message", {})
            model = message.get("model")
            if model:
                models.add(model)
            request_id = record.get("requestId") or record.get("uuid")
            if request_id and request_id not in usage_by_request:
                usage_by_request[request_id] = (model, message.get("usage", {}))

        stamp = record.get("timestamp")
        if stamp:
            timestamps.append(stamp)

    if not timestamps and not cost_state:
        return None

    stats = {
        "session_id": path.stem,
        "human_turns": human_turns,
        "started": min(timestamps) if timestamps else None,
        "ended": max(timestamps) if timestamps else None,
        "cost_usd": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "lines_added": 0,
        "lines_removed": 0,
        "wall_seconds": 0,
        "cost_is_estimate": cost_state is None,
        "unpriced_models": [],
    }

    if cost_state:
        stats["cost_usd"] = cost_state.get("totalCostUSD", 0.0)
        stats["lines_added"] = cost_state.get("totalLinesAdded", 0)
        stats["lines_removed"] = cost_state.get("totalLinesRemoved", 0)
        stats["wall_seconds"] = round(cost_state.get("totalDuration", 0) / 1000)
        for model, usage in (cost_state.get("modelUsage") or {}).items():
            models.add(model)
            stats["input_tokens"] += usage.get("inputTokens", 0)
            stats["output_tokens"] += usage.get("outputTokens", 0)
            stats["cache_read_tokens"] += usage.get("cacheReadInputTokens", 0)
            stats["cache_creation_tokens"] += usage.get("cacheCreationInputTokens", 0)
    else:
        unpriced = set()
        for model, usage in usage_by_request.values():
            cache_creation = usage.get("cache_creation") or {}
            write_5m = cache_creation.get("ephemeral_5m_input_tokens", 0)
            write_1h = cache_creation.get("ephemeral_1h_input_tokens", 0)
            # Older transcripts may only carry the undifferentiated total; assume
            # the cheaper 5-minute rate rather than overstate the cost.
            total_write = usage.get("cache_creation_input_tokens", 0)
            if not (write_5m or write_1h):
                write_5m = total_write

            stats["input_tokens"] += usage.get("input_tokens", 0)
            stats["output_tokens"] += usage.get("output_tokens", 0)
            stats["cache_read_tokens"] += usage.get("cache_read_input_tokens", 0)
            stats["cache_creation_tokens"] += total_write

            prices = price_for(model) if model else None
            if not prices:
                if model:
                    unpriced.add(model)
                continue
            rate_in, rate_out = prices
            stats["cost_usd"] += (
                usage.get("input_tokens", 0) * rate_in
                + usage.get("output_tokens", 0) * rate_out
                + usage.get("cache_read_input_tokens", 0) * rate_in * CACHE_READ_MULTIPLIER
                + write_5m * rate_in * CACHE_WRITE_5M_MULTIPLIER
                + write_1h * rate_in * CACHE_WRITE_1H_MULTIPLIER
            ) / 1_000_000

        stats["lines_added"] = patch_added
        stats["lines_removed"] = patch_removed
        stats["unpriced_models"] = sorted(unpriced)
        if stats["started"] and stats["ended"]:
            start = datetime.fromisoformat(stats["started"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(stats["ended"].replace("Z", "+00:00"))
            stats["wall_seconds"] = round((end - start).total_seconds())

    stats["models"] = sorted(models)
    return stats


def collect_project(project):
    """Aggregate every session belonging to one project."""
    sessions = []
    missing = []

    for dirname in project["transcript_dirs"]:
        directory = TRANSCRIPT_ROOT / dirname
        if not directory.is_dir():
            missing.append(dirname)
            continue
        for path in sorted(directory.glob("*.jsonl")):
            summary = summarise_session(path)
            if summary:
                sessions.append(summary)

    since = project.get("since")
    if since:
        sessions = [s for s in sessions if (s["started"] or "") >= since]

    totals = defaultdict(int)
    models = set()
    unpriced = set()
    estimated_sessions = 0
    for session in sessions:
        totals["cost_usd"] += session["cost_usd"]
        for key in ("human_turns", "input_tokens", "output_tokens", "cache_read_tokens",
                    "cache_creation_tokens", "lines_added", "lines_removed", "wall_seconds"):
            totals[key] += session[key]
        models.update(session["models"])
        unpriced.update(session["unpriced_models"])
        estimated_sessions += 1 if session["cost_is_estimate"] else 0

    starts = [s["started"] for s in sessions if s["started"]]
    ends = [s["ended"] for s in sessions if s["ended"]]

    return {
        "slug": project["slug"],
        "name": project["name"],
        "sessions": len(sessions),
        "human_turns": totals["human_turns"],
        "cost_usd": round(totals["cost_usd"], 2),
        "estimated_cost_sessions": estimated_sessions,
        "tokens": {
            "input": totals["input_tokens"],
            "output": totals["output_tokens"],
            "cache_read": totals["cache_read_tokens"],
            "cache_creation": totals["cache_creation_tokens"],
        },
        "lines_added": totals["lines_added"],
        "lines_removed": totals["lines_removed"],
        # Wall-clock time from first to last message in each session, so it counts
        # thinking-about-it time and coffee breaks, not just time spent generating.
        "wall_hours": round(totals["wall_seconds"] / 3600, 1),
        "models": sorted(models),
        "first_session": min(starts) if starts else None,
        "last_session": max(ends) if ends else None,
        "unpriced_models": sorted(unpriced),
        # Warned about on stderr but stripped before writing: the directory names
        # encode a local home path, and nothing on a published page needs it.
        "_missing_transcript_dirs": missing,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--projects", default="tools/ledger-projects.json")
    parser.add_argument("--out", default="data/ledger.json")
    parser.add_argument("--print", action="store_true", dest="show")
    args = parser.parse_args()

    if not TRANSCRIPT_ROOT.is_dir():
        sys.exit(f"No transcripts at {TRANSCRIPT_ROOT} — run this on the machine you build from.")

    config = json.loads(Path(args.projects).read_text(encoding="utf-8"))
    entries = [collect_project(p) for p in config["projects"]]

    # Report problems, and strip the internal-only fields, before anything is written.
    for entry in entries:
        missing = entry.pop("_missing_transcript_dirs")
        if missing:
            print(f"warning: {entry['slug']} — no transcript directory for "
                  f"{', '.join(missing)}", file=sys.stderr)
        if entry["unpriced_models"]:
            print(f"warning: {entry['slug']} — no price known for "
                  f"{', '.join(entry['unpriced_models'])}; cost understated", file=sys.stderr)

    ledger = {
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "notes": [
            "Costs are the API-equivalent list price of the tokens used. On a "
            "subscription plan that is not the amount actually paid.",
            "Sessions counted in estimated_cost_sessions predate Claude Code recording "
            "its own cost; those figures are priced from token counts by this script.",
            "wall_hours is elapsed session time, not time spent generating.",
        ],
        "totals": {
            "projects": len(entries),
            "sessions": sum(e["sessions"] for e in entries),
            "human_turns": sum(e["human_turns"] for e in entries),
            "cost_usd": round(sum(e["cost_usd"] for e in entries), 2),
            "lines_added": sum(e["lines_added"] for e in entries),
            "lines_removed": sum(e["lines_removed"] for e in entries),
            "wall_hours": round(sum(e["wall_hours"] for e in entries), 1),
        },
        "projects": entries,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    if args.show:
        print(f"{'project':<20} {'sess':>5} {'turns':>6} {'cost':>9} {'+lines':>7} "
              f"{'-lines':>7} {'hours':>6}")
        for entry in entries:
            flag = "~" if entry["estimated_cost_sessions"] else " "
            print(f"{entry['slug']:<20} {entry['sessions']:>5} {entry['human_turns']:>6} "
                  f"{flag}${entry['cost_usd']:>7.2f} {entry['lines_added']:>7} "
                  f"{entry['lines_removed']:>7} {entry['wall_hours']:>6}")
        totals = ledger["totals"]
        print(f"{'TOTAL':<20} {totals['sessions']:>5} {totals['human_turns']:>6} "
              f" ${totals['cost_usd']:>7.2f} {totals['lines_added']:>7} "
              f"{totals['lines_removed']:>7} {totals['wall_hours']:>6}")
        print("~ = includes sessions whose cost this script estimated from token counts")

    print(f"wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
