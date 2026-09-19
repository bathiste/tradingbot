"""Offline tests: dedupe hash, lexical fallback, db roundtrip, aggregate."""
from sentiment_bot.collectors.base import content_hash
from sentiment_bot.scoring.finbert import lexical_scores, score_texts
from sentiment_bot import db as dbm
from sentiment_bot.aggregate import compute_daily


def test_content_hash_dedupe():
    assert content_hash("A  lot   of space", "x") == content_hash("a lot of space", "x")
    assert content_hash("a", "b") != content_hash("a", "c")


def test_lexical_fallback_labels():
    out = lexical_scores(["record profits and upgrade, strong growth",
                          "miss lawsuit layoffs downgrade probe",
                          "the meeting is on tuesday"])
    assert [o[0] for o in out] == ["positive", "negative", "neutral"]
    assert out[0][4] > 0 and out[1][4] < 0 and out[2][4] == 0


def test_score_texts_no_model():
    out = score_texts(["good beat raise", "bad miss loss"], use_model=False)
    assert out[0][0] == "positive" and out[1][0] == "negative"


def test_db_roundtrip_and_aggregate(tmp_path):
    p = str(tmp_path / "t.db")
    dbm.init_db(p)
    rows = [
        {"source": "rss", "ticker": "AAPL", "title": "t1", "text": "record profit",
         "url": "http://x/1", "published_at": "2026-09-18T10:00:00+00:00",
         "fetched_at": "2026-09-18T11:00:00+00:00",
         "content_hash": content_hash("t1", "record profit")},
        {"source": "rss", "ticker": "AAPL", "title": "t1", "text": "record profit",
         "url": "http://x/1", "published_at": "2026-09-18T10:00:00+00:00",
         "fetched_at": "2026-09-18T11:00:00+00:00",
         "content_hash": content_hash("t1", "record profit")},
    ]
    ins, skip = dbm.insert_items(p, rows)
    assert (ins, skip) == (1, 1)
    dbm.save_scores(p, [(1, "positive", 0.6, 0.2, 0.2, 0.4, "lexical")])
    daily = compute_daily(p)
    assert len(daily) == 1 and daily[0]["mean_score"] > 0
    dbm.upsert_daily(p, daily)
    assert dbm.daily_trend(p, "AAPL")[0]["n_items"] == 1
