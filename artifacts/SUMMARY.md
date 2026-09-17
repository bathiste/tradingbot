
# Detailed Summary — resources (MARKDOWN)/ (6 Papers)
> Workspace tradingbot | Sources: 6 md + 6 pdf | Date 2026-09-17
## 0. TL;DR — price-only plateaus; multimodal + RL wins if evaluated across assets/regimes with costs.
| # | Paper | Idea | Number |
|---|-------|------|--------|
| 1 | Robert 2024 Sentiment-Enhanced | real-time NLP into algos | P85/R80/F1 82.5 corr .65 (.75 events) |
| 2 | Theate Ernst TDQN | DQN for max Sharpe, 30-stock bench | train12-17/test18-19 + full tricks |
| 3 | Zhu Beyond Sentiment 2026 | 6-dim LLM > polarity | N41618 F1 .576->.600 p<.0001 disagree 53.5% |
| 4 | Neagu CLEF T3 2026 | PG/PPO/DQL/DDPG BTC+TSLA alpha-reward | TSLA 55 vs 16% BH; BTC +1.6 vs -34% BH |
| 5 | SAIFIN 2026 | Market+News+Sat+Master LLM, 10 commods | 8/10 win, cut down-loss 44-64% |
| 6 | Yasin Gill JHU | 20 inds, 4 norms, 3 rewards, A2C/PPO/DQN | immediate=myopic, final=no credit |
> Repo today: only README + resources/. No code.

## 1. Paper-by-Paper Deep Dive

### Paper 1 — Sentiment-Enhanced Algos (Robert, 2024)

**Question:** does real-time sentiment give an edge over price-only algos?
**Pipeline proposed:** ingest (news APIs, Twitter/Reddit, filings) → clean/tokenize → NLP (lexicon → ML → BERT-era) → sentiment score → fuse with price/tech signal → execution (HFT/arb/trend/MM).
**Claims:** precision 85% / recall 80% / F1 82.5% for sentiment classifier; Pearson 0.65 sentiment→next move, >0.75 around earnings/geopolitics; better profitability, risk-adjusted return, execution speed vs baseline.
**Challenges named (still valid):** data quality/consistency across sources, latency budget, non-stationary sentiment, ethics/manipulation + privacy, feedback loops if everyone runs same signal.
**Limits:** EasyChair preprint, thin on backtest protocol, no costs/slippage detail, reference list noisy. Treat as motivation, not evidence.
**Takeaway for bot:** build a `sentiment` micro-service from day 1, but score it like Paper 3 does — not as magic alpha.

### Paper 2 — TDQN (Théate & Ernst, Liège)

**Question:** how to make DQN actually work for `max Sharpe` position sizing?
**Formulation:** MDP where state = filtered/normalized price window, action = discrete share quantity Q bounded to keep cash >=0 and allow return-to-neutral (Theorems 1-2 in Appendix A derive Qt bounds with cost C and margin epsilon), reward = Sharpe-linked.
**Key adaptations over vanilla DQN:** Double/Dueling heads, target net (N^- steps), Huber loss, gradient clipping, Xavier init, BatchNorm, Dropout+L2+EarlyStopping, low-pass prefilter + returns transform + normalization, augmentation (shift/filter/noise), epsilon-greedy annealing, **double trajectory trick** — step both chosen action and opposite action in a copied env and store both experiences to double sample efficiency.
**Evaluation contribution:** 30-stock diverse testbench (sector/region/vol/liquidity), 8y window (2012-17 train, 2018-19 test, val split inside train), fixed hyperparams across stocks, frozen weights at test — explicitly to kill cherry-picking one ticker/one window.
**Takeaway for bot:** copy the testbench discipline + trick-list verbatim for your DQN baseline. Reuse the Qt bound math for position sizing with costs.

### Paper 3 — Beyond Sentiment (Zhu et al., 2026) — MOST ACTIONABLE

**Hypothesis:** news → single polarity discards alpha. Six orthogonal dims: `sentiment, sentiment_score [-1,1], event_type (earnings/merger/policy/product/management/macro/other), impact_subject (company/industry/macro), time_horizon (short/long), confidence [0,1]`.
**Method:** FinBERT probs + LLaMA-3.1-70B-Instruct JSON extraction (2k-char truncate, temp 0, exact prompt in Table 9/App A.5) → 9-dim vector → XGBoost next-day move on 41,618 FNSPID news-stock pairs; 1000-iteration shared-permutation bootstrap, paired tests.
**Findings:**
- FinBERT alone: F1 0.576 with XGB (nonlinear) but only 0.230 linear → sentiment-return is highly nonlinear.
- LLM structured alone weaker solo, but disagrees with FinBERT 53.5% (39.4% mergers → 67.4% other) → orthogonal info. Example: "FAA urges airlines..." scores FinBERT +0.94 (words "boost/plan") but is a negative policy event.
- Combined F1 0.600 (p<0.0001), +0.010 to +0.023 in every event type; non-sentiment dims alone add +0.019; all six dims 14-21% importance (balanced, no single killer).
- Earnings paradox: FinBERT most confident (0.849 vs 0.820 product) yet wrong most (50.1% disagree) — boilerplate fools lexicons.
- Robustness: integer vs one-hot encoding delta 0.0002 — not an artifact.
**Takeaway for bot:** implement this exact 6-field extractor as `features/news_structured.py`. Never store just polarity. Keep raw JSON + confidence for audit.
### P4 — CLEF FinMMEval T3 (Neagu et al. 2026)
Task: daily long/flat/short BTC+TSLA from news+OHLC. Feats: EMA/RSI/MACD/Boll/volume + dates + LLaMA-3.2-1B sentiment. Alpha-reward = excess over buy-hold + random starts (train only); 180 Ray Tune trials, Sharpe select.
TSLA: DDPG 54.96% SR1.44 MDD19.2% / DQL 52.62% SR1.38 MDD35.8% vs BH 16.45% SR0.61. BTC: DDPG +1.58% SR0.23 vs BH -34.27% SR-0.87 MDD49.7%; PG -14.5%, DQL -23.2%, PPO -33.8%. DQL picked blind (val SR 3.29/2.11) but DDPG won test. Lesson: bull-val -> bear-test gap; need walk-forward; PPO train +114k% meaningless. DDPG continuous actor best at long->flat/short shifts.

### P5 — SAIFIN (Garinei et al. 2026)
Agents: Market (tech) + News + Satellite (weather/env) + Master LLM aggregator. 10 commodity futures. Master beats BH avg (pos Sharpe vs flat/neg), wins 8/10. Regime (N=545/650/771/519): up Sharpe 1.73/2.38-3.63, down -0.94/-1.19 and -1.23/-2.70; but Master cuts BH losses 44% high-vol-down / 64% low-vol-down. News fragile high-vol (-0.70 vs +0.18 low-vol). Improving post-2025Q1. Blueprint for explainable stack.

### P6 — JHU Cookbook (Yasin & Gill)
20 TA-Lib (SMA OBV Mom Stoch MACD CCI ADX TRIX ROC SAR TEMA TRIMA WMA DEMA MFI CMO STOCHRSI UO BOP ATR), minmax/z/sigmoid/L2; DummyVecEnv; Backtesting.py; A2C/PPO/DQN. R1 immediate diff -> scalps noise. R2 log-on-flip -> sparse. R3 final-only -> no credit assign. Too many inds drown agent. Test wide + detect decay.


## 2. Cross-cutting synthesis
Signals: OHLC+tech table stakes; polarity alone lossy — need event/impact/horizon/conf (P3); sentiment nonlinear -> trees/NN not linear; alt/satellite helps commodities but regime-sensitive (P5); earnings fools FinBERT (P3).
Decision: RL fits MDP; DQN needs full trick-list (P2); DDPG better drawdown/timing (P4); alpha-reward + random starts align objective (P4); reward shaping make-or-break (P6); Master-LLM gives explain + cushion (P5).
Eval: multi-asset bench + frozen hypers (P2), shared-perm bootstrap + paired tests (P3), walk-forward bull+bear (P4), regime-split tables (P5), costs always. Watch val SR -> test gap (DQL 2.11 -> -0.55 BTC).
Failures: downtrend breaks trend agents; high-vol kills news; +100k% train returns = overfit; feature bloat; latency drift; crowding.
To beat: news F1 0.600; TSLA 55% vs 16% BH; BTC +1.6% vs -34% BH; Master 8/10 + cut 44-64%; Sharpe>1 up, <0 down w/o regime switch.

## 3. Gaps for tradingbot
No code/data/live endpoint/cost model/regime detector/explain log; single-window risk; 1B vs 70B LLM tradeoff open; satellite only if commodities; ethics empty.
