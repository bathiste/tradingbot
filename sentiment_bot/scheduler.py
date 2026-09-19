"""APScheduler loop: one local service, ingest -> score -> aggregate on interval."""
from __future__ import annotations
import argparse
import logging
from .config import load_config
from .pipeline import run_once

log = logging.getLogger("sentiment_bot")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--interval-min", type=float, default=None)
    ap.add_argument("--tickers", nargs="*", default=None)
    ap.add_argument("--sources", nargs="*", default=None)
    ap.add_argument("--no-model", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(args.config)
    interval = args.interval_min or cfg.get("poll_interval_min", 30)

    def job():
        try:
            res = run_once(cfg, tickers=args.tickers, sources=args.sources,
                           use_model=not args.no_model)
            log.info("pass done: %s", res)
        except Exception:
            log.exception("scheduled pass failed")

    log.info("running first pass now (tickers=%s)", args.tickers or cfg.get("tickers"))
    job()
    from apscheduler.schedulers.blocking import BlockingScheduler
    sch = BlockingScheduler()
    sch.add_job(job, "interval", minutes=interval, max_instances=1, coalesce=True)
    log.info("scheduler every %.1f min — Ctrl+C to stop", interval)
    sch.start()


if __name__ == "__main__":
    main()
