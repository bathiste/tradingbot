"""YAML config loader with sane defaults (no hard requirement on yaml)."""
from __future__ import annotations
import os


def _project_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)  # parent of sentiment_bot/


def _resolve(path):
    """Absolute paths pass through; relative ones resolve to CWD first,
    then to the project root (so running from C:\\Users\\x still finds
    config.yaml / data/sentiment.db next to the code)."""
    if os.path.isabs(path):
        return path
    if os.path.exists(path):
        return os.path.abspath(path)
    return os.path.join(_project_root(), path)

DEFAULTS = {
    "tickers": ["AAPL", "MSFT", "TSLA"],
    "sources": ["rss", "yfinance", "sec"],
    "poll_interval_min": 30,
    "db_path": "data/sentiment.db",
    "cache_dir": "data/cache",
    "model_name": "ProsusAI/finbert",
    "score_batch_size": 32,
    "max_text_chars": 2000,
    "fetch_bodies": False,
    "throttle_sec": 1.0,
    "user_agent": "tradingbot-mvp/0.1 (+local research)",
    "rss_feeds": [
        "https://news.google.com/rss/search?q={ticker}%20stock&hl=en-US&gl=US&ceid=US:en",
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US",
    ],
    "market_feeds": [
        "https://feeds.marketwatch.com/marketwatch/topstories/",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    ],
}


def load_config(path=None):
    cfg = dict(DEFAULTS)
    if path is None:
        path = os.environ.get("SENTIMENT_BOT_CONFIG", "config.yaml")
    path = _resolve(path)
    if os.path.exists(path):
        try:
            import yaml
            with open(path) as f:
                user = yaml.safe_load(f) or {}
            cfg.update(user)
        except ImportError:
            pass  # yaml missing -> defaults
    # Relative db/cache paths resolve against the project root unless the
    # caller already gave an absolute path or a CWD-relative file exists.
    cfg["db_path"] = _resolve(cfg.get("db_path", "data/sentiment.db"))
    cfg["cache_dir"] = _resolve(cfg.get("cache_dir", "data/cache"))
    cfg["_config_path"] = path
    return cfg
