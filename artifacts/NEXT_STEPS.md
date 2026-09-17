# Next Steps for tradingbot (from 6-paper synthesis)

> Goal: multimodal (OHLC + structured news + optional satellite) + RL + LLM-explain, rigorously evaluated.
> Start simple, add complexity only if it beats buy-hold net of costs.

## Phase 0 — Repo + data (week 1)
1. Scaffold: `data/ features/ envs/ agents/ backtest/ live/ artifacts/ configs/`.
2. Universe: 5-10 liquid tickers (e.g. BTC, TSLA + 3-8 equities/commodities) — multi-asset from day 1 (P2 lesson).
3. OHLC daily (+intraday later) + news (FNSPID-style or GDELT/Benzinga) keyed by date/ticker.
4. Metrics lib: CR, Sharpe, MDD, vol, turnover, costed + cost-free (track both — P4 gap).
5. Baseline: buy-hold + SMA/RSI/MACD rule. If RL/sentiment can't beat this net costs, stop.

## Phase 1 — Structured news (weeks 2-3, highest ROI per P3)
1. Port P3 Table 9 prompt verbatim into `features/news_structured.py`: FinBERT probs + LLaMA JSON with 6 fields (sentiment, score, event_type×7, impact_subject×3, time_horizon×2, confidence).
2. Store raw JSON + trunc-len + model ver. Never polarity-only.
3. Replicate: 9-dim -> XGBoost next-day up/down; 1000 shared-perm bootstraps, paired test vs FinBERT-only. Target: combined > solo, non-sentiment ablation ~+0.02 (P3 numbers).
4. Cheap LLM first (LLaMA-3.2-1B per P4), upgrade to 70B only if F1 gap justifies cost/latency. Log disagreement rate (expect ~50%).

## Phase 2 — Env + reward (week 3-4)
1. Discrete long/flat/short env (P4) + bounded sizing via TDQN Thm 1-2 (P2). Fee+slippage param.
2. State: filtered/normalised returns + 8-10 tech (not 20 at once — P6) + 9-dim news + date cycle. Compare minmax/z-score.
3. Reward: alpha-reward (excess over BH) + random starts (P4). Ablate vs plain diff and final-only (P6).
4. Vectorise (DummyVecEnv / Gymnasium).

## Phase 3 — Agents (weeks 4-6)
1. DQN full trick-list (double/dueling, target, Huber, clip, Xavier, BN, dropout/L2/early-stop, augment) + DDPG continuous (P4 drawdown winner). Add PPO/PG compare; 100+ trials, val-Sharpe select, frozen test.
2. Walk-forward bull+bear+sideways; ignore +10000% train returns; only costed test CR/SR/MDD count.

## Phase 4 — Regime + Master (weeks 6-8)
1. Regime tag vol x trend -> 4 cells (SAIFIN Tab.3). Report per-cell. Flat/hedge rule for down/high-vol (Sharpe -1 there).
2. Master LLM aggregates Market+News(+Sat) -> stance + rationale + conf. Target: cut BH loss 40-60% in downs.
3. Satellite only if commodities + ablation proves lift.

## Phase 5 — Live + guardrails
1. /signal endpoint in/out like CLEF (P4). Blind select, never reselect on live.
2. Risk: max pos, MDD kill-switch, turnover cap, latency budget, low-conf skip.
3. Paper-trade 4-8 wks. Dashboard: CR/SR/MDD + regime + disagree + rationales.
4. Compliance: manipulation/privacy note (P1), model cards.

## Priority order
Metrics+BH > news extractor+XGB > env+alpha > TDQN+DDPG > walk-forward+regime > Master > live > satellite.

## MVP done = beats BH avg Sharpe>0 net costs, 8/10 tickers, news F1>0.59, smaller down-loss, every call logged.
