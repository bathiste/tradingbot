import streamlit as st
from sentiment_bot.config import load_config
from sentiment_bot import db

st.set_page_config(page_title="Sentiment MVP", layout="wide")
cfg = load_config()

st.title("Ticker sentiment (MVP)")
days = st.sidebar.slider("Trend days", 3, 30, 7)
try:
    latest = db.latest_all(cfg["db_path"], days)
except Exception as e:
    st.error("DB not ready (%s). Run: python -m sentiment_bot.cli init-db" % e)
    st.stop()

if not latest:
    st.warning("DB empty. Run: python -m sentiment_bot.cli run-once --no-model")
    st.stop()

tickers = [r["ticker"] for r in latest]
sel = st.sidebar.selectbox("Ticker", tickers)
st.subheader("Latest per ticker")
st.dataframe(latest, width="stretch")

trend = db.daily_trend(cfg["db_path"], sel, days)
st.subheader("%s — last %d days" % (sel, days))
if trend:
    chart = {r["day"]: r["mean_score"] for r in trend}
    st.line_chart(chart)
    st.dataframe(trend, width="stretch")
else:
    st.info("No trend rows yet.")

st.subheader("Recent headlines — %s" % sel)
for r in db.recent_items(cfg["db_path"], sel, 15):
    st.markdown("- [%s %+.2f] %s ([link](%s))" % (
        r.get("label"), r.get("score") or 0, r["title"] or "(no title)", r["url"] or "#"))

