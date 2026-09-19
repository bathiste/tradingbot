"""One pass: ingest -> score -> aggregate. Used by CLI and scheduler."""
from __future__ import annotations
from . import db
from .scoring.finbert import score_texts


def run_collectors(tickers, cfg, sources=None):
    from .collectors import rss, yfinance_news, sec_edgar
    sources = sources or cfg.get("sources", ["rss", "yfinance", "sec"])
    all_items, stats = [], {}
    if "rss" in sources:
        try:
            got = rss.collect_rss(tickers, cfg)
            all_items += got
            stats["rss"] = len(got)
        except Exception as e:
            stats["rss"] = "error: %s" % e
    if "yfinance" in sources:
        try:
            got = yfinance_news.collect_yfinance(tickers, cfg)
            all_items += got
            stats["yfinance"] = len(got)
        except Exception as e:
            stats["yfinance"] = "error: %s" % e
    if "sec" in sources:
        try:
            got = sec_edgar.collect_sec(tickers, cfg)
            all_items += got
            stats["sec"] = len(got)
        except Exception as e:
            stats["sec"] = "error: %s" % e
    if "reddit" in sources:
        try:
            from .collectors import reddit
            got = reddit.collect_reddit(tickers, cfg)
            all_items += got
            stats["reddit"] = len(got)
        except Exception as e:
            stats["reddit"] = "skipped: %s" % e
    if "gdelt" in sources:
        try:
            from .collectors import gdelt
            got = gdelt.collect_gdelt(tickers, cfg)
            all_items += got
            stats["gdelt"] = len(got)
        except Exception as e:
            stats["gdelt"] = "error: %s" % e
    return all_items, stats


def run_once(cfg, tickers=None, sources=None, use_model=True):
    tickers = [t.upper() for t in (tickers or cfg.get("tickers", []))]
    db_path = cfg["db_path"]
    db.init_db(db_path)
    items, stats = run_collectors(tickers, cfg, sources)
    ins, skip = db.insert_items(db_path, [i.to_row() for i in items])
    pending = db.unscored_items(db_path)
    texts = [(r.get("title", "") + ". " + r.get("text", ""))[:cfg.get("max_text_chars", 2000)]
             for r in pending]
    scored_labels = score_texts(texts, cfg.get("model_name", "ProsusAI/finbert"),
                                cfg.get("score_batch_size", 32), use_model=use_model)
    model_tag = scored_labels[0][5] if scored_labels else ("model" if use_model else "lexical")
    db.save_scores(db_path, [(r["id"], lab, p, ne, ng, sc, mt)
                             for r, (lab, p, ne, ng, sc, mt) in zip(pending, scored_labels)])
    from .aggregate import compute_daily
    daily = compute_daily(db_path)
    db.upsert_daily(db_path, daily)
    return {"tickers": tickers, "collected": stats, "inserted": ins, "dups": skip,
            "scored": len(pending), "model": model_tag, "daily_rows": len(daily)}
