# tradingbot - sentiment MVP

Local free-only pipeline: public text - FinBERT pos/neg/neu -
per-ticker daily sentiment - CLI and dashboard.
One Python service (scheduler + SQLite). Verified 2026-09-19.

## Run

See sentiment_bot package: config.yaml, requirements-mvp.txt.

- pip install -r requirements-mvp.txt
- python -m sentiment_bot.cli init-db
- python -m sentiment_bot.cli run-once --tickers AAPL MSFT TSLA --sources rss yfinance sec --no-model
- python -m sentiment_bot.cli trend --ticker AAPL --days 7
- python -m sentiment_bot.cli latest --days 7
- python -m sentiment_bot.scheduler --interval-min 30
- streamlit run sentiment_bot/dashboard.py
- python -m sentiment_bot.cli evaluate --ticker AAPL --days 14

## Sources (free, legal, stable)

RSS (Google News per ticker + market feeds), yfinance news, SEC EDGAR 8-K.
Reddit and GDELT collectors exist but are optional/off by default.

## Polite scraping

robots.txt checked, 1 req/s per domain, cache in data/cache, honest UA,
requests + trafilatura/BS4 only, no Playwright, no X/Twitter/paywalls/logins.
Raw text stored with fetch date for re-scoring.

Live check 2026-09-19: 275 items scored, AAPL 7-day trend OK,
AAPL sentiment-vs-return pearson 0.158 over 11 pairs.
