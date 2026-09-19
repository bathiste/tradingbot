"""Reddit collector (optional, disabled by default). Needs free-tier API creds.

Env: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT.
Raises RuntimeError with a clear message when creds are missing so the
pipeline can skip it with a warning instead of crashing.
"""
from __future__ import annotations
import os
from .base import RawItem


def collect_reddit(tickers, cfg, subreddits=("stocks", "wallstreetbets"), limit=25):
    cid = os.getenv("REDDIT_CLIENT_ID", "")
    sec = os.getenv("REDDIT_CLIENT_SECRET", "")
    if not cid or not sec:
        raise RuntimeError("Reddit disabled: set REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET")
    try:
        import requests
        from requests.auth import HTTPBasicAuth
    except Exception as e:
        raise RuntimeError("requests needed for reddit: %s" % e)
    ua = os.getenv("REDDIT_USER_AGENT", "tradingbot-mvp/0.1")
    tok = requests.post("https://www.reddit.com/api/v1/access_token",
                        auth=HTTPBasicAuth(cid, sec),
                        data={"grant_type": "client_credentials"},
                        headers={"User-Agent": ua}, timeout=20).json().get("access_token")
    if not tok:
        raise RuntimeError("Reddit token failed")
    items = []
    for sub in subreddits:
        for q in tickers:
            try:
                r = requests.get("https://oauth.reddit.com/r/%s/search" % sub,
                                 headers={"User-Agent": ua, "Authorization": "bearer " + tok},
                                 params={"q": q, "restrict_sr": "1", "sort": "new", "limit": limit},
                                 timeout=20)
                for p in r.json().get("data", {}).get("children", []):
                    d = p.get("data", {})
                    title = d.get("title", "")
                    body = (d.get("selftext") or "")[:cfg.get("max_text_chars", 2000)]
                    url = "https://www.reddit.com" + d.get("permalink", "")
                    from datetime import datetime, timezone
                    pub = datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc).isoformat()
                    items.append(RawItem(source="reddit", ticker=q, title=title[:500],
                                         text=body, url=url, published_at=pub))
            except Exception:
                continue
    return items
