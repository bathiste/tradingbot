"""Shared collector helpers: schema, throttle, cache, robots, polite fetch."""
from __future__ import annotations
import hashlib
import os
import re
import time
import urllib.robotparser as robotparser
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from urllib.parse import urlparse

USER_AGENT = "tradingbot-mvp/0.1 (+local research)"
_last_hit = {}

@dataclass
class RawItem:
    source: str
    ticker: str
    title: str
    text: str
    url: str
    published_at: str
    fetched_at: str = ""
    def __post_init__(self):
        if not self.fetched_at:
            self.fetched_at = datetime.now(timezone.utc).isoformat()
        self.ticker = (self.ticker or "MARKET").upper()
        self.title = (self.title or "").strip()
        self.text = (self.text or "").strip()

    def to_row(self):
        d = asdict(self)
        d["content_hash"] = content_hash(self.title, self.text)
        return d


def content_hash(title, text):
    norm = re.sub(r"\s+", " ", (str(title) + "\n" + str(text)).strip().lower())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def throttle(domain, min_sec=1.0):
    now = time.time()
    elapsed = now - _last_hit.get(domain, 0.0)
    wait = min_sec - elapsed
    if wait > 0:
        time.sleep(wait)
    _last_hit[domain] = time.time()


def robots_allowed(url, ua=USER_AGENT):
    try:
        parts = urlparse(url)
        robots_url = parts.scheme + "://" + parts.netloc + "/robots.txt"
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(ua, url)
    except Exception:
        return True


def cache_path(cache_dir, url):
    h = hashlib.sha256(url.encode()).hexdigest()[:32]
    return os.path.join(cache_dir, h + ".html")


def polite_get(url, cache_dir=None, throttle_sec=1.0, timeout=15):
    import requests
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        p = cache_path(cache_dir, url)
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="ignore") as f:
                return f.read()
    throttle(urlparse(url).netloc, throttle_sec)
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        if r.status_code != 200:
            return ""
        if cache_dir:
            with open(cache_path(cache_dir, url), "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)
        return r.text
    except Exception:
        return ""


def extract_text(html):
    if not html:
        return ""
    try:
        import trafilatura
        t = trafilatura.extract(html) or ""
        if len(t.strip()) > 200:
            return t.strip()
    except Exception:
        pass
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(" ", strip=True)[:8000]
    except Exception:
        return ""


