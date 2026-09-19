"""RSS collector: Google News per ticker + generic market feeds. Free, no auth."""
from __future__ import annotations
import re
import time as _time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime as _p2d
from urllib.parse import urlparse
from .base import RawItem, throttle


def _clean_html(s):
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(s or "", "html.parser").get_text(" ", strip=True)
    except Exception:
        return re.sub(r"<[^>]+>", " ", s or "")


def _pubdate(entry):
    if entry.get("published_parsed"):
        try:
            return datetime.fromtimestamp(_time.mktime(entry["published_parsed"]),
                                          tz=timezone.utc).isoformat()
        except Exception:
            pass
    for k in ("published", "updated"):
        if entry.get(k):
            try:
                return _p2d(entry[k]).isoformat()
            except Exception:
                continue
    return ""


def collect_rss(tickers, cfg):
    import feedparser
    items = []
    urls = []
    for t in tickers:
        for f in cfg.get("rss_feeds", []):
            try:
                urls.append((t, f.format(ticker=t)))
            except Exception:
                urls.append((t, f))
    for t in ["MARKET"]:
        for f in cfg.get("market_feeds", []):
            urls.append((t, f))
    for ticker, url in urls:
        domain = urlparse(url).netloc
        throttle(domain, cfg.get("throttle_sec", 1.0))
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue
        for e in feed.get("entries", [])[:50]:
            link = (e.get("link") or "").strip()
            if not link:
                continue
            title = _clean_html(e.get("title", ""))
            desc = _clean_html(e.get("description", "") or e.get("summary", ""))
            if not title and not desc:
                continue
            items.append(RawItem(source="rss", ticker=ticker, title=title[:500],
                                 text=desc[:cfg.get("max_text_chars", 2000)],
                                 url=link[:1000], published_at=_pubdate(e)))
        _time.sleep(0.1)
    return items
