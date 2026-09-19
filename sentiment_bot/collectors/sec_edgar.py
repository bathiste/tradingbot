"""SEC EDGAR 8-K collector: free, legal, stable. No auth, honest UA required."""
from __future__ import annotations
import json
import os
import time
from datetime import datetime, timezone
from urllib.parse import urlparse
from .base import RawItem, throttle, USER_AGENT

SEC_FORMS = "https://data.sec.gov/submissions/CIK{cik10}.json"
SEC_BROWSE = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=8-K&count=20&output=atom"
TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"
ARCHIVE = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}"


def _sec_get(url, cfg):
    import requests
    throttle(urlparse(url).netloc, max(1.0, cfg.get("throttle_sec", 1.0)))
    try:
        r = requests.get(url, headers={"User-Agent": cfg.get("user_agent", USER_AGENT),
                                       "Accept": "application/json",
                                       "Host": "data.sec.gov" if "data.sec.gov" in url else urlparse(url).netloc},
                         timeout=20)
        return r if r.status_code == 200 else None
    except Exception:
        return None


def _cik_map(cfg):
    cache = os.path.join(cfg.get("cache_dir", "data/cache"), "sec_tickers.json")
    if os.path.exists(cache) and time.time() - os.path.getmtime(cache) < 86400:
        try:
            with open(cache) as f:
                return json.load(f)
        except Exception:
            pass
    r = _sec_get(TICKER_MAP, cfg)
    if not r:
        return {}
    try:
        data = r.json()
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        with open(cache, "w") as f:
            json.dump(data, f)
        return data
    except Exception:
        return {}


def collect_sec(tickers, cfg):
    mapping = _cik_map(cfg)
    t2cik = {}
    if isinstance(mapping, dict):
        for v in mapping.values():
            if isinstance(v, dict) and v.get("ticker"):
                t2cik[str(v["ticker"]).upper()] = str(v["cik_str"]).zfill(10)
    items = []
    for t in tickers:
        cik10 = t2cik.get(t.upper())
        if not cik10:
            continue
        r = _sec_get(SEC_FORMS.format(cik10=cik10), cfg)
        if not r:
            continue
        try:
            data = r.json()
        except Exception:
            continue
        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accs = recent.get("accessionNumber", [])
        docs = recent.get("primaryDocument", [])
        for form, fdate, acc, doc in zip(forms, dates, accs, docs):
            if form != "8-K":
                continue
            acc_nodash = acc.replace("-", "")
            url = ARCHIVE.format(cik=int(cik10), acc=acc_nodash, doc=doc)
            try:
                pub = datetime.strptime(fdate, "%Y-%m-%d").replace(tzinfo=timezone.utc).isoformat()
            except Exception:
                pub = fdate
            items.append(RawItem(source="sec", ticker=t,
                                 title="8-K filing %s %s" % (t.upper(), fdate),
                                 text="8-K filed %s accession %s doc %s" % (fdate, acc, doc),
                                 url=url, published_at=pub))
            if len([i for i in items if i.ticker == t.upper()]) >= 10:
                break
    return items
