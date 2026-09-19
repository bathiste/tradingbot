"""GDELT collector (optional, disabled by default). Global news metadata, no auth."""
from __future__ import annotations
from .base import RawItem, throttle


def collect_gdelt(tickers, cfg, max_records=50):
    import requests
    items = []
    for t in tickers:
        throttle("api.gdeltproject.org", cfg.get("throttle_sec", 1.0))
        try:
            r = requests.get("https://api.gdeltproject.org/api/v2/doc/doc",
                             params={"query": t, "mode": "artlist",
                                     "maxrecords": max_records, "format": "json"},
                             timeout=20)
            arts = r.json().get("articles", [])
        except Exception:
            continue
        for a in arts:
            items.append(RawItem(source="gdelt", ticker=t,
                                 title=(a.get("title") or "")[:500],
                                 text=(a.get("seendate") or "")[:500],
                                 url=(a.get("url") or "")[:1000],
                                 published_at=a.get("seendate", "")))
    return items
