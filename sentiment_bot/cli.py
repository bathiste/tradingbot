"""CLI: init-db, run-once, ingest stats, trend, latest, items, evaluate."""
from __future__ import annotations
import argparse
from .config import load_config
from . import db


def main():
    ap = argparse.ArgumentParser(prog="sentiment-bot")
    ap.add_argument("--config", default="config.yaml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init-db")
    p = sub.add_parser("run-once")
    p.add_argument("--tickers", nargs="*", default=None)
    p.add_argument("--sources", nargs="*", default=None)
    p.add_argument("--no-model", action="store_true")
    p = sub.add_parser("trend")
    p.add_argument("--ticker", required=True)
    p.add_argument("--days", type=int, default=7)
    p = sub.add_parser("latest")
    p.add_argument("--days", type=int, default=7)
    p = sub.add_parser("items")
    p.add_argument("--ticker", required=True)
    p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("evaluate")
    p.add_argument("--ticker", required=True)
    p.add_argument("--days", type=int, default=14)
    sub.add_parser("stats")

    args = ap.parse_args()
    cfg = load_config(args.config)

    if args.cmd == "init-db":
        db.init_db(cfg["db_path"])
        print("db ready:", cfg["db_path"])
    elif args.cmd == "run-once":
        from .pipeline import run_once
        res = run_once(cfg, tickers=args.tickers, sources=args.sources,
                       use_model=not args.no_model)
        print("collected:", res["collected"])
        print("inserted=%d dups=%d scored=%d model=%s daily_rows=%d" % (
            res["inserted"], res["dups"], res["scored"], res["model"], res["daily_rows"]))
    elif args.cmd == "trend":
        rows = db.daily_trend(cfg["db_path"], args.ticker, args.days)
        if not rows:
            print("no data for", args.ticker.upper())
            return
        print("day        n   mean   pos   neg")
        for r in rows:
            print("%s  %3d  %+0.3f  %.2f  %.2f" % (
                r["day"], r["n_items"], r["mean_score"], r["pos_rate"], r["neg_rate"]))
    elif args.cmd == "latest":
        rows = db.latest_all(cfg["db_path"], args.days)
        if not rows:
            print("db empty — run run-once first")
            return
        print("ticker  day         n   mean")
        for r in rows:
            print("%-6s  %s  %3d  %+0.3f" % (r["ticker"], r["day"], r["n_items"], r["mean_score"]))
    elif args.cmd == "items":
        for r in db.recent_items(cfg["db_path"], args.ticker, args.limit):
            print("[%s %+.2f] %s (%s)" % (r.get("label"), r.get("score") or 0, r["title"][:110], r["source"]))
            print("   ", (r["url"] or "")[:120])
    elif args.cmd == "stats":
        print(db.counts(cfg["db_path"]))
    elif args.cmd == "evaluate":
        from .aggregate import price_corr
        print(price_corr(cfg["db_path"], args.ticker, args.days))


if __name__ == "__main__":
    main()
