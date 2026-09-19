"""Daily per-ticker rollup + price alignment check."""
from __future__ import annotations
import sqlite3
from collections import defaultdict


def compute_daily(db_path):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """SELECT i.ticker, substr(COALESCE(NULLIF(i.published_at,''), i.fetched_at),1,10) d,
                  s.label, s.score
           FROM scores s JOIN items i ON i.id=s.item_id""").fetchall()
    con.close()
    groups = defaultdict(list)
    for r in rows:
        groups[(r["ticker"], r["d"])].append((r["label"], r["score"]))
    out = []
    for (ticker, day), vals in groups.items():
        if not day or len(day) < 10:
            continue
        scores = [v[1] for v in vals]
        n = len(scores)
        pos = sum(1 for l, _ in vals if l == "positive") / n
        neg = sum(1 for l, _ in vals if l == "negative") / n
        out.append({"ticker": ticker, "day": day[:10], "n_items": n,
                    "mean_score": sum(scores) / n, "pos_rate": pos, "neg_rate": neg})
    return sorted(out, key=lambda r: (r["ticker"], r["day"]))


def price_corr(db_path, ticker, days=14):
    """Pearson corr between daily mean_score and next-day return (yfinance closes)."""
    import sqlite3 as sq
    con = sq.connect(db_path)
    con.row_factory = sq.Row
    rows = con.execute("SELECT day, mean_score FROM daily_sentiment WHERE ticker=? ORDER BY day",
                       (ticker.upper(),)).fetchall()
    con.close()
    if len(rows) < 3:
        return {"error": "not enough daily rows (need >=3)"}
    smap = {r["day"]: r["mean_score"] for r in rows}
    try:
        import yfinance as yf
        px = yf.Ticker(ticker).history(period="%dd" % max(days + 5, 10), auto_adjust=True)
    except Exception as e:
        return {"error": "price fetch failed: %s" % e}
    if px is None or len(px) < 3:
        return {"error": "no price data"}
    closes = [(str(i.date()), float(px["Close"].iloc[j])) for j, i in enumerate(px.index)]
    pairs = []
    cmap = dict(closes)
    sdays = sorted(smap)
    for k in range(len(sdays) - 1):
        d0, d1 = sdays[k], sdays[k + 1]
        # find closest closes
        c0 = cmap.get(d0)
        c1 = cmap.get(d1)
        if c0 is None or c1 is None or c0 == 0:
            continue
        pairs.append((smap[d0], (c1 - c0) / c0))
    if len(pairs) < 2:
        return {"error": "could not align sentiment with prices", "pairs": len(pairs)}
    import math
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in pairs)
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    corr = num / den if den else 0.0
    return {"ticker": ticker.upper(), "n_pairs": len(pairs), "pearson": round(corr, 3)}
