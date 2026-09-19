"""SQLite store (stdlib sqlite3). Tables: items, scores, daily_sentiment."""
from __future__ import annotations
import os
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  ticker TEXT NOT NULL,
  title TEXT DEFAULT '',
  text TEXT DEFAULT '',
  url TEXT DEFAULT '',
  published_at TEXT DEFAULT '',
  fetched_at TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  UNIQUE(url),
  UNIQUE(content_hash)
);
CREATE TABLE IF NOT EXISTS scores (
  item_id INTEGER PRIMARY KEY,
  label TEXT NOT NULL,
  pos REAL NOT NULL,
  neu REAL NOT NULL,
  neg REAL NOT NULL,
  score REAL NOT NULL,
  model TEXT NOT NULL,
  scored_at TEXT NOT NULL,
  FOREIGN KEY(item_id) REFERENCES items(id)
);
CREATE TABLE IF NOT EXISTS daily_sentiment (
  ticker TEXT NOT NULL,
  day TEXT NOT NULL,
  n_items INTEGER NOT NULL,
  mean_score REAL NOT NULL,
  pos_rate REAL NOT NULL,
  neg_rate REAL NOT NULL,
  PRIMARY KEY (ticker, day)
);
CREATE INDEX IF NOT EXISTS idx_items_ticker_time ON items(ticker, published_at);
CREATE INDEX IF NOT EXISTS idx_daily_ticker_day ON daily_sentiment(ticker, day);
"""


def connect(db_path):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)) or ".", exist_ok=True)
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def init_db(db_path):
    con = connect(db_path)
    con.executescript(SCHEMA)
    con.commit()
    con.close()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def insert_items(db_path, rows):
    """rows: list of dicts with source,ticker,title,text,url,published_at,fetched_at,content_hash.
    Returns (inserted, skipped)."""
    con = connect(db_path)
    ins = skip = 0
    for r in rows:
        try:
            con.execute(
                "INSERT INTO items (source,ticker,title,text,url,published_at,fetched_at,content_hash)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (r["source"], r["ticker"], r.get("title", ""), r.get("text", ""),
                 r.get("url", ""), r.get("published_at", ""), r.get("fetched_at", now_iso()),
                 r["content_hash"]),
            )
            ins += 1
        except sqlite3.IntegrityError:
            skip += 1
    con.commit()
    con.close()
    return ins, skip


def unscored_items(db_path, limit=10000):
    con = connect(db_path)
    rows = con.execute(
        "SELECT i.* FROM items i LEFT JOIN scores s ON s.item_id=i.id"
        " WHERE s.item_id IS NULL ORDER BY i.id LIMIT ?", (limit,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def save_scores(db_path, scored):
    """scored: list of (item_id, label, pos, neu, neg, score, model)."""
    con = connect(db_path)
    for item_id, label, pos, neu, neg, score, model in scored:
        con.execute(
            "INSERT OR REPLACE INTO scores (item_id,label,pos,neu,neg,score,model,scored_at)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (item_id, label, pos, neu, neg, score, model, now_iso()),
        )
    con.commit()
    con.close()


def upsert_daily(db_path, rows):
    con = connect(db_path)
    for r in rows:
        con.execute(
            "INSERT OR REPLACE INTO daily_sentiment (ticker,day,n_items,mean_score,pos_rate,neg_rate)"
            " VALUES (?,?,?,?,?,?)",
            (r["ticker"], r["day"], r["n_items"], r["mean_score"], r["pos_rate"], r["neg_rate"]),
        )
    con.commit()
    con.close()


def daily_trend(db_path, ticker, days=7):
    con = connect(db_path)
    rows = con.execute(
        "SELECT * FROM daily_sentiment WHERE ticker=? ORDER BY day DESC LIMIT ?",
        (ticker.upper(), days),
    ).fetchall()
    con.close()
    return [dict(r) for r in reversed(rows)]


def latest_all(db_path, days=7):
    con = connect(db_path)
    rows = con.execute(
        """SELECT d.* FROM daily_sentiment d
           JOIN (SELECT ticker, MAX(day) AS m FROM daily_sentiment GROUP BY ticker) m
             ON m.ticker=d.ticker AND m.m=d.day"""
    ).fetchall()
    con.close()
    out = [dict(r) for r in rows]
    return sorted(out, key=lambda r: r["ticker"])


def recent_items(db_path, ticker, limit=10):
    con = connect(db_path)
    rows = con.execute(
        """SELECT i.title,i.url,i.published_at,i.source,s.label,s.score
           FROM items i LEFT JOIN scores s ON s.item_id=i.id
           WHERE i.ticker=? ORDER BY i.id DESC LIMIT ?""",
        (ticker.upper(), limit),
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def counts(db_path):
    con = connect(db_path)
    n_items = con.execute("SELECT COUNT(*) c FROM items").fetchone()["c"]
    n_scored = con.execute("SELECT COUNT(*) c FROM scores").fetchone()["c"]
    n_days = con.execute("SELECT COUNT(*) c FROM daily_sentiment").fetchone()["c"]
    by_src = con.execute("SELECT source, COUNT(*) c FROM items GROUP BY source").fetchall()
    con.close()
    return {"items": n_items, "scored": n_scored, "daily_rows": n_days,
            "by_source": {r["source"]: r["c"] for r in by_src}}
