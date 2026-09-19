"""yfinance news collector: ticker-linked headlines. Free, no auth."""
from __future__ import annotations
from .base import RawItem


def collect_yfinance(tickers, cfg):
    import yfinance as yf
    items = []
    for t in tickers:
        try:
            news = yf.Ticker(t).news or []
        except Exception:
            continue
        for n in news:
            c = n.get("content", n) if isinstance(n, dict) else {}
            title = (c.get("title") or n.get("title") or "").strip()
            desc = (c.get("description") or c.get("summary") or "").strip()
            url = ((c.get("clickThroughUrl") or {}).get("url")
                   if isinstance(c.get("clickThroughUrl"), dict)
                   else c.get("clickThroughUrl")) or c.get("url") or n.get("link") or ""
            pub = c.get("pubDate") or c.get("pubdate") or n.get("providerPublishTime") or ""
            if isinstance(pub, (int, float)):
                from datetime import datetime, timezone
                pub = datetime.fromtimestamp(pub, tz=timezone.utc).isoformat()
            if not title and not desc:
                continue
            items.append(RawItem(source="yfinance", ticker=t,
                                 title=title[:500],
                                 text=desc[:cfg.get("max_text_chars", 2000)],
                                 url=str(url)[:1000], published_at=str(pub)))
    return items
