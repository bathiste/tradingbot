Academic Editor: Shaolong Sun Received: 22 December 2025 Revised: 4 February 2026 Accepted: 11 February 2026 Published: 13 February 2026 **Copyright:** © 2026 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license. 

Article 

# Satellite Data and Artificial Intelligence for FINtech 

**Alberto Garinei 1,2,*, Massimiliano Proietti 2 , Alessandro Vispa 2 , Stefano Speziali 2 , Giovanni Bartolini 2 , Marcello Marconi 1,2, Emanuele Piccioni 2 , Matteo Martini 1 , Francesca Fallucchi 1 , Romeo Giuliano 1 , Ernesto William De Luca 1 , Umberto Di Matteo 1 and Valerio Lemma 1** 

(^1) Department of Engineering Sciences, Guglielmo Marconi University, 00193 Rome, Italy; m.marconi@unimarconi.it (M.M.); m.martini@unimarconi.it (M.M.); u.dimatteo@unimarconi.it (U.D.M.); v.lemma@unimarconi.it (V.L.) (^2) Idea-Re S.r.l., 06128 Perugia, Italy; mproietti@idea-re.eu (M.P.); avispa@idea-re.eu (A.V.); sspeziali@idea-re.eu (S.S.); gbartolini@idea-re.eu (G.B.); epiccioni@idea-re.eu (E.P.) ***** Correspondence: a.garinei@unimarconi.it **Highlights What are the main findings?** 

- The study presents SAIFIN (Satellite data and Artificial Intelligence for FINtech), a     modular multi-agent trading framework that fuses OHLC market data, news senti-     ment, and satellite-derived indicators. 

- By introducing specialized Market, News, Satellite and Master Agents coordinated     through LLM-based orchestration, the system aims to produce coherent, explain-     able recommendations, with high agreement between quantitative signals and     generated narratives. **What is the implication of the main finding?** 

- The results indicate that multimodal, agent-based architectures that combine gener-     ative AI and alternative data (including satellite-derived environmental indicators)     offer a practical route to more robust and transparent algorithmic trading systems,     particularly under volatile or data-sparse market conditions. 

- The SAIFIN framework provides a reusable blueprint for regulation-aware decision-     support platforms in finance, showing how explainability, heterogeneous data inte-     gration, and high-performance computing can be jointly engineered to meet modern     requirements on accuracy, latency, and interpretability. 

 Abstract The SAIFIN project (Satellite data and Artificial Intelligence for FINtech) develops a novel algorithmic trading system that integrates satellite imagery, financial data, and advanced artificial intelligence to enhance decision-making, particularly in commodity and agricultural markets. This paper presents the motivation, design, implementation, and validation of the SAIFIN framework. Leveraging alternative data and modular multi-agent architectures, SAIFIN aims to deliver robust, context-aware trading signals in diverse market conditions. 

 Keywords: algorithmic trading; time-series forecasting; multi-agent systems; generative AI 

Forecasting **2026** , 8 , 17 https://doi.org/10.3390/forecast8010017 


<!-- PAGE_BREAK -->
### 1. Introduction 

1.1. Overview 

Over the past decades, algorithmic trading has profoundly transformed global financial markets by enabling high-speed, high-volume execution of trades with minimal human intervention. These systems have come to dominate trading activity worldwide, enhancing liquidity, reducing transaction costs, and improving price discovery mechanisms [1,2]. Their ability to remove emotional biases and execute complex strategies with split-second precision has made them indispensable tools for both institutional and retail investors. However, this technological evolution also introduced systemic risks, particularly in the context of high-frequency trading (HFT), where ultra-low latency strategies may amplify volatility during turbulent periods [3]. In parallel, financial markets are increasingly shaped by the integration of artificial intelligence (AI) and big data analytics. Machine learning and deep learning models can process vast volumes of structured and unstructured data, identifying hidden patterns and nonlinear relationships that would remain invisible to human analysts [4]. More recently, generative models and large language models (LLMs) have further expanded this frontier, enabling not only quantitative prediction but also the synthesis of coherent, explainable narratives to support decision-making [5,6]. Recent surveys on financial large language models (FinLLMs) summarize core tasks, datasets, evaluation practices, and key challenges for LLM deployment in finance [7]. Such models are now being deployed for tasks ranging from time-series forecasting to natural language sentiment analysis, bridging the gap between statistical modeling and interpretability [8]. A major shift is also occurring in the type of data used for financial decision-making. Beyond traditional financial indicators, traders and hedge funds are increasingly exploiting alternative data—non-conventional sources that provide unique market insights [9]. This trend is also documented by recent surveys that review the rapid expansion of alternative data (including sensorand satellite-derived signals) and their growing role in financial prediction and investment decision-making [10]. Among these, social media sentiment, corporate tracking, geospatial intelligence, and particularly satellite imagery are emerging as key differentiators. Recent multimodal forecasting evidence shows that augmenting price-based models with news—including LLM-based sentiment signals—can measurably improve predictive performance over price-only baselines [11]. Satellite data, in particular, deliver real-time information on physical and economic activities: crop health and yield forecasts, oil storage levels, mining stockpiles, logistics and shipping flows, and infrastructure development [12]. Such indicators have demonstrated predictive power in commodity markets, energy, and agriculture [13], offering a strategic advantage to firms capable of processing them effectively. The introduction of satellite alternative data has been shown to enable more informed trading by sophisticated investors, while potentially widening information asymmetry when access is unequal [13]. Notably, hedge funds have already exploited satellite-based signals to estimate retail sales from parking lot occupancy [14]. Yet, integrating these heterogeneous data sources into robust trading frameworks remains a formidable challenge. Traditional algorithmic systems often suffer from rigidity, opacity, and limited adaptability to exogenous shocks such as geopolitical conflicts, pandemics, or climate-related disruptions [15]. The convergence of AI, alternative data, and high-performance computing (HPC) provides a new paradigm to address these limitations. GPU-accelerated infrastructures, in particular, enable the large-scale training of deep models and real-time inference required for both high-frequency and medium-term trading strategies. The SAIFIN project (Satellite data and Artificial Intelligence for FINtech) is situated at this intersection of financial innovation and technological advancement. Its central 


<!-- PAGE_BREAK -->
goal is to develop a next-generation algorithmic trading framework that fuses multimodal data—including satellite imagery, OHLC financial data, and news sentiment—within a modular, explainable, and adaptive architecture. The system relies on a multi-agent design where specialized agents handle market dynamics, textual sentiment, and satellite analytics, while higher-level agents integrate these insights into coherent trading strategies. Large language models serve as interpreters across all layers, ensuring that outputs are both quantitatively rigorous and narratively explainable. By combining generative AI, agent-based orchestration, satellite-derived indicators, and HPC acceleration, SAIFIN addresses two fundamental challenges of modern trading: (i) the need for rapid, data-driven decision-making in increasingly complex and uncertain environments, and (ii) the demand for transparency and interpretability in AI-driven systems, in compliance with financial regulation [1,6]. This emphasis is aligned with recent evidence syntheses highlighting that, alongside performance gains, generative AI in finance raises replicability and governance challenges that motivate auditability and transparent design choices [5]. This integrated approach holds the potential not only to enhance predictive accuracy and robustness of trading strategies but also to democratize access to cutting-edge algorithmic tools, supporting ongoing efforts toward sustainable and explainable AI in finance. Below, we summarize our main objectives. 

1.2. Key Objectives 

 We aim to achieve the following: 

- **Fuse multimodal data sources** : Integrate satellite data, OHLC financial data, news     sentiment, and alternative data into coherent trading signals. 

- **Develop AI-centric forecasting** : Employ technical indicators, deep learning, and     LLMs for pattern recognition, sentiment analysis, and report generation. 

- **Create a scalable multi-agent architecture** : Modular AI agents specializing in distinct     domains such as market dynamics, news, satellite analytics, strategy modeling, and     decision making. 

- **Validate in realistic simulation environments** : Test and refine system performance     and stress scenarios before potential live deployment. 

1.3. Algorithmic Trading Evolution 

Algorithmic trading has undergone a profound transformation over the past five decades. Its origins can be traced back to the 1970s with the early automation of order routing, which paved the way for more sophisticated program trading strategies in the 1980s, such as index arbitrage and portfolio insurance. The 1990s saw the consolidation of these practices, coinciding with the advent of fully electronic markets and decimalization, which enabled tighter bid-ask spreads and higher trading volumes [1]. The rise in high-frequency trading (HFT) in the 2000s marked a new era, characterized by ultra-low latency strategies that now account for a substantial portion of market volume. HFT employs statistical arbitrage, market making, and cross-market latency exploitation to capitalize on millisecond-level opportunities [2]. While such strategies contribute to market efficiency by synchronizing prices and reducing transaction costs, they also introduce systemic risks, especially during turbulent conditions, as highlighted by episodes such as the 2010 “Flash Crash” [3]. Despite these risks, algorithmic trading remains the dominant paradigm in modern markets, with institutions continuously seeking competitive advantage through the integration of advanced data sources, machine learning models, and infrastructure optimizations [4]. 


<!-- PAGE_BREAK -->
1.4. Alternative Data in Trading 

In recent years, alternative data has emerged as a critical differentiator in financial markets. Unlike traditional data (e.g., balance sheets, market prices), alternative data encompasses non-traditional sources such as satellite imagery, social media, web traffic, and corporate supply chain tracking [9]. These datasets provide unique insights into realworld economic activity, allowing market participants to anticipate movements before they are reflected in official statistics. Satellite imagery, in particular, has proven highly valuable. Applications include monitoring crop health and yields, tracking oil storage volumes, estimating retail sales via parking lot occupancy, and evaluating infrastructure development [12,14]. Empirical studies have shown that satellite-based signals can improve the forecasting accuracy of earnings by significant improvements [13]. The adoption of alternative data is expected to expand significantly, with a global market strong growth [13]. Several hedge funds and quantitative firms have already integrated these techniques. For instance, SynMax employs satellite-based monitoring of hydraulic fracturing activity to predict natural gas supply, while other firms use shipping tracking and geospatial intelligence to forecast commodity flows [14]. The ability to systematically harness such heterogeneous data is becoming a key determinant of trading performance. 

1.5. AI and Generative Techniques 

The integration of artificial intelligence into algorithmic trading represents one of the most significant paradigm shifts in the financial industry. Early applications focused on machine learning and deep learning models, capable of identifying complex nonlinear relationships in financial time series [4]. Recent advances have expanded to reinforcement learning, attention mechanisms, and transformer-based models, which provide superior forecasting and adaptability across diverse market conditions [8]. Large language models (LLMs) and generative AI have introduced an additional layer of capability by bridging quantitative prediction with natural language interpretation. These models enable the synthesis of heterogeneous signals—including market indicators, textual sentiment, and satellite imagery—into coherent, explainable narratives [6,7]. Such integration reduces the “black box” problem that has historically limited the trust and adoption of AI-driven systems. Nevertheless, the increasing reliance on AI also raises new risks. Issues such as model opacity, susceptibility to herd behavior, algorithmic collusion, and liquidity shocks pose systemic challenges [15]. Regulatory frameworks and explainability-focused approaches (XAI) are therefore becoming crucial to ensure compliance, transparency, and accountability in AI-powered trading. The balance between innovation and risk mitigation remains a central theme in the ongoing evolution of algorithmic trading systems. The remainder of this paper is organized as follows: Section 2 describes the proposed methodology and system architecture, including the modular multi-agent design and the specialized Market, News, Satellite, and Master Agents. Section 3 presents the experimental results and performance analysis across ten commodity futures, including the contribution of satellite-derived indicators. Section 4 discusses the main findings, limitations, and future research directions. 

### 2. Methodology 

The SAIFIN system is designed as a next-generation decision support platform for financial trading. Traditional algorithmic trading frameworks often suffer from rigidity, opacity, and the inability to integrate heterogeneous information sources. SAIFIN addresses these limitations by adopting a modular and asynchronous multi-agent architecture, where 


<!-- PAGE_BREAK -->
each module specializes in a different domain but contributes to a unified decision-making process. At its core, the system embodies four design principles: explainability, adaptability, predictive accuracy, and scalability. These principles are achieved by combining large language models (LLMs), satellite-based remote sensing, and high-performance computing infrastructures. The foundation of SAIFIN is a central orchestration engine that coordinates the execution of all tasks in an asynchronous and concurrent manner. Unlike monolithic predictive engines, this design allows the system to process multiple data streams and user interactions simultaneously while maintaining modular separation. The operational pipeline progresses through the following well-defined stages: 

- User requests are first parsed by an LLM equipped with logical fallback rules. 

- Market data are continuously ingested and stored in a local SQLite database. 

- Key indicators such as Average True Range (ATR) are computed to facilitate dynamic     risk adjustment. 

- And specialized analytical agents are activated asynchronously. 

2.1. A Modular and Asynchronous Orchestration Layer 

SAIFIN adopts a contemporary LLM-driven architecture, integrating language models deeply within every decision node. Rather than being confined to a final summarization role, LLMs act as interpreters of specialized analyses, converting raw indicators, sentiment scores, and remote sensing metrics into structured insights. This approach ensures that every recommendation is not only quantitatively supported but also narratively explainable in natural language. To this end, three Agents have been defined, each with a specific task to carry out. These are the Market Agent, the News Agent and the Satellite Agent, which are briefly introduced below. The detailed description of the agents is provided in the next sections. 

- **The Market Agent** computes classical indicators such as RSI, MACD, and ATR (see     the Abbreviations at the end of the document and Appendix A), as well as candlestick     patterns—like Bullish Engulfing or Morning Star—for a given Future and over a given     period of time that the user is free to decide in advance. It is through an embedded     LLM that these signals are synthesized into a coherent judgment (BUY, SELL, HOLD)     for the user. They are given along with a confidence score and links the output of     documented strategies stored in the SAIFIN knowledge base. The documented trading     strategies are reviewed in the Appendix A and can be chosen (or changed) each time     by the user according to their will. 

- **The News Agent** integrates fundamental information by analyzing geopolitical de-     velopments, regulatory changes, or macroeconomic shifts for the given Future and     period of time. It then generates contextual explanations of their likely market impact.     It gives a confidence score just as the Market Agent. 

- **The Satellite Agent** extends this paradigm to environmental data: vegetation indices,     climatic stress, or water scarcity indicators are translated into financial signals relevant     for commodities. It also generates a contextual explanations and a confidence score.     The three Agents pass their decision over to a **Master Agent** which gathers all pieces of information and makes a final decision on whether to BUY/SELL/HOLD and, in case of BUY/SELL the amount the user should invest/capitalize.     All in all, the complete workflow unfolds as follows: 

1. The user provides a natural language request (e.g., “Analyze Cocoa”). 

2. The system parses and reformulates it into structured queries—i.e., it pulls out ticker     (e.g., CC = F for Cocoa). 

3. The database is updated, and indicators are computed. 


<!-- PAGE_BREAK -->
4. Agents conduct asynchronous analyses. 

5. The Master Agent synthesizes a strategic decision. 

6. The user optionally confirms or overrides the decision. 

7. Results are persisted and logged. This sequence ensures a seamless integration of     automation, transparency, and human oversight. By embedding generative models within each agent, SAIFIN ensures transparency and narrative justification at every layer of analysis, reducing the “black-box” effect that plagues many AI-driven trading systems. The LLM components used in the agent analysis are based on several versions of GPT models, including GPT-4o, GPT-4.1-mini, and GPT- 5-nano, selected to balance reasoning capability, latency, and computational cost across agents [16].     All inputs used in our experiments are collected from publicly accessible resources via web interfaces and APIs. In particular, market OHLC data and news are retrieved from Yahoo Finance (https://finance.yahoo.com/), while historical weather variables are sourced from the Open-Meteo API (https://open-meteo.com/).     We can now proceed to discuss in detail how each agent works and how a final decision is made thanks to the Master Agent, which determines which option (BUY/HOLD/SELL) is appropriate for each ticker/future and the capital to invest. 

2.2. The Market Agent 

The Market Agent is a decision service leveraging LLMs and is designed to combine structured outputs with conversational explanations, thereby supporting interpretability and usability in financial decision-making. The agent requires, as input, a financial ticker together with a start and end date and operates on two complementary streams of information. The first consists of enriched market data, which includes technical indicators such as moving averages, Bollinger bands, volatility measures, and oscillators, as well as a wide range of candlestick pattern detections. The second source is a knowledge base of trading strategies, from which relevant excerpts are dynamically retrieved. The integration of these two sources enables the agent to ground its decisions both in quantitative evidence and in domain-specific strategic knowledge. The agent is implemented as a LangGraph pipeline with sequential nodes for data retrieval, strategy retrieval, and LLM decision. The agent builds a concise indicator/pattern summary for the latest trading day (emphasizing the last 7 days) and augments it with strategy passages retrieved from the knowledge base using OpenAI embeddings and a Chroma vector store. It then calls GPT-4o via the OpenAI Chat Completions API (with temperature = 0.0) in a zero-shot setup (no fine-tuning present). Based on these parameters, it produces the following structured outputs: 

- A structured dataset of enriched market information, including technical indicators     and pattern detections. 

- A concise **summary** of the most recent market conditions, expressed in natural language. 

- A set of relevant **strategies** retrieved from a curated knowledge base. 

- A trading **signal** (BUY, SELL, or HOLD). 

- A textual **explanation** linking the observed conditions to the suggested action. 

- A numerical **confidence score** quantifying the reliability of the recommendation. 

This Agent combines technical evidence with contextual reasoning. For instance, it considers whether moving average crossovers, oscillators, or candlestick formations suggest bullish or bearish momentum, and aligns these signals with retrieved strategies. Rather than returning isolated metrics, the system produces an interpretable rationale that explains why a given signal is recommended. 


<!-- PAGE_BREAK -->
2.3. The News Agent 

The News Agent is a decision component focused on transforming unstructured news into an actionable next-day trading stance. It ingests ticker-scoped news within a userspecified window, emphasizes recency (with particular weight on the last seven days), synthesizes sentiment, and produces a trading signal accompanied by an explanation and a confidence score. Its conversational output style aims to make the underlying reasoning transparent and easy to audit. The agent is implemented as a LangGraph pipeline with nodes for fetching news and then running an LLM-based sentiment assessment. The agent concatenates available news snippets and calls GPT-4o via the OpenAI Chat Completions API (with temperature = 0.0) using a zero-shot prompt that requests an overall sentiment and a final actionable recommendation. Given a financial ticker and a start–end date interval, the agent processes the available news and operates on a stream of ticker-aligned news. Each item may include publication date, headline, and summary/body text. The analysis distinguishes between recent items (within the last seven days relative to the end date) and older items, assigning greater evidentiary weight to recent developments. This recency-aware view aligns the final stance with the most current market-moving information. It returns the following: 

- A curated collection of **news items** for the specified interval. 

- A natural-language **explanation** that summarizes the prevailing sentiment and     its drivers. 

- A trading **signal** in BUY, SELL, or HOLD. 

- A numerical **confidence score** in [0, 1] quantifying the recommendation’s strength. 

The News Agent prioritizes interpretability. Rather than merely aggregating polarity scores, it contextualizes how salient themes (e.g., guidance revisions, regulatory actions, litigation, product/partnership announcements, macro shocks) drive the overall stance. The final recommendation is presented as a concise, auditable narrative that links the observed news flow to the proposed action and confidence. 

2.4. The Satellite Agent 

The Satellite Agent is a remote-sensing–aware decision component focused on turning satellite-informed physical indicators into an actionable next-day trading stance on the underlying future. The agent operates on pre-processed satellite data streams that are aligned with the underlying ticker. Each observation typically consists of an observation date, one or more satellite-derived features (mostly environmental stress indices), and their corresponding anomaly scores relative to historical baselines. Weather and environmental data are sourced from the Open-Meteo API [17]. The time series are provided at daily or aggregated (e.g., weekly) frequency and are already quality-controlled upstream (e.g., cloud filtering, basic denoising). The data is produced through large-scale meteorological analyses that integrate broad observation networks, including satellite observations, thereby providing remote-sensing–informed environmental indicators without requiring direct image-level processing in our pipeline. The analysis explicitly differentiates between normal seasonal patterns and abnormal conditions, with anomalous readings carrying more evidentiary weight in the final decision. Given a financial ticker and a start–end date interval, the agent processes the available features and returns the following: 

- A curated collection of **environmental indicators** for the specified interval. 

- A natural-language **explanation** that summarizes the obtained indicators and their     likely market implications. 

- A trading **signal** in BUY, SELL, or HOLD for the corresponding future. 


<!-- PAGE_BREAK -->
- A numerical **confidence score** in [0, 1] quantifying the recommendation’s strength. 

The agent is orchestrated in Langflow via a small set of deterministic LLM calls (zero-shot instruction-based prompting, no fine-tuning). The pipeline is composed of three stages: 

1. **Query parsing (structured extraction).** A first LLM call (GPT-5-nano, temperature = 1.0     (GPT-5 models require temperature to be fixed at 1.0. See https://platform.openai.     com/docs/guides/gpt-5, accessed on 9 February 2026), seed = 1, max retries = 5)     converts the user request into a machine-readable schema containing the commodity     futures ticker and the weather observation window. 

2. **Weather data retrieval and aggregation.** The agent retrieves daily historical weather     from the Open-Meteo Archive API for the top-producing countries associated with the     selected commodity through a fixed lookup table including country name, production     share, and representative latitude/longitude. Collected variables include temperature     (max/min), relative humidity, wind speed, precipitation, and cloud cover. Daily     observations are grouped by month to compute monthly summaries (averages for all     variables except precipitation, for which monthly totals are used) and formatted into     a textual report. The end-to-end retrieval and formatting step is latency-dominant     and typically requires almost 2 minutes per request (network calls + aggregation). 

3. **Contextual interpretation and trading signal.** In parallel, another agent uses GPT-5-     nano (same parameters as above) to generate a short commodity climate/agronomic     context. The weather summary and commodity context are then included in a prompt     to be analyzed by GPT-4.1-mini (temperature = 0.01, seed = 1, max retries = 5). A     final GPT-4.1-mini call (same parameters as previous call) formats the output as a     JSON object for later analysis. The use of GPT-5-nano for the early structured parsing     steps and GPT-4.1-mini for the final reasoning and formatting stages provides a good     compromise between latency, cost, and output quality. The Satellite Agent is designed for interpretability rather than black-box scoring. Its logic links physical observations to expected price pressure via intuitive rules. For supply-driven contracts, persistent above-baseline production or throughput signals tend to tilt the stance toward SELL, while below-baseline signals (suggesting scarcity, stress, or disruption) tilt it toward BUY. For demand- or activity-oriented features, the direction of the effect is reversed. Conflicting or weak anomalies, short-lived spikes, or noisy signals naturally lead to a HOLD recommendation with a lower confidence score. The final output is a concise, auditable narrative that ties remote-sensing–informed environmental conditions to a concrete next-day action and an explicit assessment of uncertainty. 

2.5. The Master Agent 

The Master Agent is a coordination and arbitration component that consolidates heterogeneous signals into a single, interpretable next-day trading stance. It ingests the outputs of specialized sub-agents which encapsulate complementary views: price/indicator structure (market), information flow and sentiment (news), and exogenous or satellitederived cues (satellite). The Master Agent is implemented as a LangGraph workflow with explicit nodes for LLM invocation, JSON parsing, and output validation. The fusion step calls GPT-4o through LangChain ChatOpenAI (with temperature = 0.1) in a zero-shot, structured-output setting. The Master agent’s signals fusion is therefore LLM-mediated rather than a hard-coded weighting formula. The prompt instruct to respond strictly in JSON format with the following: 

- A trading **action** in BUY, SELL, or HOLD. 

- A natural-language **explanation** that traces how inputs inform the final stance. 

- A numerical **confidence score** in [0, 1] reflecting recommendation strength. 


<!-- PAGE_BREAK -->
The Master Agent is instructed to give higher weight to market and satellite evidence when consolidating views, with news acting as an adjustment factor. Explanations explicitly cite which evidentiary elements (agent signals, agent reasons, or constraints) were most decisive. The overall structure is displayed in Figure 1. 

 User Input (Natural Language) 

 LLM Parsing & Query Construction 

 USER INTERFACE 

 Master Agent (Strategic Decision via LangGraph) 

 Trading Recommendation + User Confirmation 

 DECISION & EXECUTION 

 Market Agent (Tech. Indicators + LLM) 

 News Agent (Sentiment + LLM) 

 Satellite Agent (Remote Sensing + LLM) 

 ANALYTIC AGENTS 

**Figure 1.** Overview of the SAIFIN architecture. Natural-language user input is routed through an LLM parsing layer to three domain-specific agents (Market, News, Satellite), whose signals are fused by the Master Agent to produce an actionable trading recommendation. 

### 3. Results and Discussion 

By combining generative AI and satellite data, SAIFIN offers a modular framework consistent with current approaches to AI-driven decision support in finance. To assess the quality of the proposed solution, we measure the performance of the setup by means of standard signal metrics. Following [18–20], we adopt the indicators described in the following subsection. 

3.1. Performance Analysis Metrics 

We use a unified and reproducible protocol to evaluate how each trading agent behaves over time and across assets. For each traded instrument and each trading day, the agent makes a decision by selecting a signal between BUY, SELL, or HOLD. These signals are represented as wt ∈ {1, 0, − 1 }, 

where wt = 1 means BUY, wt = −1 means SELL, and wt = 0 means HOLD. To avoid lookahead bias, we interpret wt as the position decided using information available up to the close of day t − 1 and held over the period (t − 1, t]. Let Pt be the closing price at day t. The one-period (daily) return delivered by a strategy is 

 rt = wt · Pt − Pt− 1 Pt− 1 

#### . (1) 

Cumulative return up to day T is computed by compounding: 

#### RT = 

 T 

## ∏ 

 t= 1 

 ( 1 + rt) − 1. (2) 


<!-- PAGE_BREAK -->
From the daily return series {rt}Tt= 1 , we compute standard performance indicators used in the literature [18–20]. In particular, we report the following: 

- **Total return (Tot. Ret.)** as the cumulative return RT over the backtest horizon, typically     reported in percent. 

- **Annualized return (AR)** and **annualized volatility (AV)** : 

 AR = 252 · E[rt], AV = 

#### √ 

 252 · Std(rt), 

 where 252 is the assumed number of trading days per year. 

- **Sharpe ratio (SR)** (assuming a zero risk-free rate): 

#### SR = 

#### AR 

#### AV 

#### = 

 E[rt] Std(rt) 

#### √ 

#### 252. 

• **Maximum drawdown (MDD)** computed from the equity curve Et = (^) ∏ti= 1 ( 1 + ri): MDD = min t 

####  

 Et maxs≤t Es 

#### − 1 

####  

#### . 

- **Win rate** as the fraction of trading days with strictly positive strategy return: 

 Win Rate = 

#### 1 

#### T 

 T 

## ∑ 

 t= 1 

 I(rt > 0 ). 

For simplicity, we set the risk-free rate to zero when computing the Sharpe ratio, since our futures backtest uses price-based profit/loss and does not model collateral yield. This choice primarily affects the absolute level of the ratio while preserving its role for relative comparisons across strategies. All indicators are computed for each strategy–asset pair and summarized in tables for side-by-side comparison of profitability, risk exposure, and stability across agent designs. 

3.2. Aggregate Performance Across the 10 Futures 

We evaluate the three agents (Market, News and Satellite) separately on ten commodity futures (CC, CT, KC, KE, OJ, SB, ZC, ZO, ZR, ZS) over the same daily backtesting window along with the Master Agent, which combines their decisions. We use the passive Buy&Hold as a benchmark. The backtesting window spans across almost a year, from August 2024 to July 2025. The results reported in this section are equal-weight averages across the ten contracts, so they summarize typical behavior for the assets considered in this paper. Figure 2 reports the average risk–return profile (annualized return versus annualized volatility). We plot (AV, AR) for each strategy, where both AR and AV are computed per asset and then averaged across the ten futures to obtain a single point per strategy. On average, the Master Agent achieves the highest annualized return (16.6%) at a volatility comparable to Buy&Hold (29.9% vs. 32.6%), yielding a positive Sharpe ratio (0.374) compared to a slightly negative Sharpe for Buy&Hold (Table 1). The Satellite Agent is consistently the second-best strategy in aggregate (annualized return 10.5%, Sharpe 0.306), suggesting that satellite-derived signals can be informative in this experimental setting. The Market Agent delivers low-to-moderate volatility with a small positive return and Sharpe, while the News Agent exhibits very low volatility but negative average performance, indicating that the current news-driven pipeline is not yet competitive as a stand-alone signal source (Table 1). This suggests that the current news-driven pipeline is not yet extracting a sufficiently predictive signal in this setting. A plausible explanation is that (i) headline-level sentiment is often noisy and weakly aligned with next-day commodity 


<!-- PAGE_BREAK -->
futures returns, especially when relevant information is embedded in supply-chain or macro reports rather than in generic news polarity; (ii) timing and availability effects may introduce a lag (e.g., articles published after the market close may be acted upon with delay under our next-day protocol), reducing actionable content; and (iii) the Yahoo Finance news stream may vary in coverage and quality across tickers, yielding sparse or heterogeneous inputs. In addition, the current implementation emphasizes recency and produces conservative stances, which can translate into limited opportunity capture when sentiment is ambiguous. These observations motivate future improvements such as entity/event resolution, novelty and time-decay calibration, source filtering, and hybrid signals that condition news interpretations on market context. Another natural extension is to expand the ingestion to a broader set of news websites and aggregators and to incorporate social signals (e.g., from social networks and forums), while accounting for their higher noise level and potential manipulation, through source credibility weighting and stronger filtering. 

**Figure 2.** Average risk–return profile across the ten futures. Each point is computed by averaging annualized return and annualized volatility across contracts for the corresponding strategy. 

**Table 1.** Average performance across ten futures (three significant digits). Returns, volatility, drawdown, and win rate are reported in %. 

 Strategy Tot. Ret. Ann. Ret. Ann. Vol. Sharpe Max DD Win Rate Buy&Hold 0.442 0.460 32.6 −0.0371 −28.8 48.5 Market Agent 0.630 0.671 21.0 0.240 −16.6 20.3 News Agent −2.37 −2.40 2.96 −0.403 −4.10 0.724 Satellite Agent 10.3 10.5 30.3 0.306 −28.5 43.9 Master Agent 16.3 16.6 29.9 0.374 −28.8 42.1 

Overall, these averages are indeed encouraging, even though they do not imply uniform dominance. Table 2 summarizes how often each agent improves upon Buy&Hold on a per-contract basis. The Master Agent outperforms Buy&Hold in annualized return on 8/10 contracts (and in Sharpe on 7/10), but it underperforms on a minority of markets (notably CT and ZO in annualized return), highlighting that the decision policies are not equally effective across all commodity microstructures. In contrast, the Market Agent improves drawdown on most contracts (9/10), but the improvement is not necessarily accompanied by large gains in return, suggesting a more conservative exposure pattern. 


<!-- PAGE_BREAK -->
**Table 2.** Number of contracts (out of 10) for which each agent improves upon Buy&Hold. “Shallower DD” means a less negative maximum drawdown. 

 Strategy Better Ann. Return Better Sharpe Shallower DD Master Agent 8/10 7/10 7/10 Satellite Agent 7/10 7/10 6/10 Market Agent 6/10 6/10 9/10 News Agent 5/10 3/10 10/10 

3.3. Rolling Excess Returns and the Contribution of Satellite Signals 

To inspect when and on which contracts the Master Agent adds value, we analyze the 20-day rolling excess return relative to Buy&Hold (Figure 3a,b). Let rMaster t denote the return of the Master Agent and rB&H t the return of the Buy&Hold benchmark. The daily excess return for a given ticker is 

 eMaster t = rMaster t − rB&H t. 

We then report the **20-day rolling mean excess return** 

 e ¯Master, t (^20 )= 

#### 1 

#### 20 

 t 

## ∑ 

 i=t− 19 

 eMaster i , 

plotted separately for each future contract. Positive values indicate outperformance of the benchmark over the corresponding rolling window. With satellite features enabled, several contracts exhibit extended regimes of positive excess performance and large positive excursions (peaking near the top of the plotted range). Without satellite features, the rolling excess return trajectories are visibly more adverse for multiple contracts, with deeper and more persistent negative regimes (approaching the bottom of the plotted range) and smaller positive peaks. This ablation provides evidence that satellite-derived indicators contribute useful information in parts of the sample, improving the overall behavior of the decision stack and increasing the Master Agent’s average Sharpe ratio across tickers by almost 0.45. 

 ( a ) With satellite inputs. 

**Figure 3.** Cont. 


<!-- PAGE_BREAK -->
 ( b ) Without satellite inputs (ablation). 

**Figure 3.** 20-day rolling excess return of the Master Agent over Buy&Hold, shown for each future contract. 

3.4. Statistical Significance Tests 

To assess whether the observed performance differences are statistically meaningful, we analyze daily excess returns between the Master Agent and the Buy&Hold benchmark, defined as above ei,t = rMaster i,t − rB&H i,t , but where the i index is referred to the different tickers. For each futures contract, we test the one-sided null hypothesis H 0 : E[ei,t] ≤ 0 against H 1 : E[ei,t] > 0 using heteroskedasticityand autocorrelation-consistent (HAC) Newey–West standard errors, reporting results for two lag choices (L = 5 and L = 10). In addition, we compute block-bootstrap confidence intervals for E[ei,t] as a nonparametric robustness check under time-series dependence. Finally, we estimate a pooled panel model ei,t = _α_ + _ε_ i,t and report two-way clustered standard errors by ticker and date to account for both cross-sectional and time dependence. The per-ticker HAC tests provide only limited evidence of outperformance: Cocoa (CC) and Coffee (KC) exhibit positive mean excess returns with marginal significance (10% level), while the remaining contracts are not statistically significant and some display negative average excess returns. This inference is stable across the two Newey–West lag choices (L = 5 and L = 10), which yield qualitatively consistent t-statistics and p-values. The blockbootstrap confidence intervals for E[ei,t] include zero for all tickers, indicating again that a strictly positive mean excess return cannot be asserted at the 95% confidence level within the current sample. Consistently, the pooled estimate is positive (i.e., _α_ ≈ 3.21 × 10 −^4 ), but not statistically distinguishable from zero under two-way clustering (one-sided p-value ≈ 0.30), indicating that, over the evaluation window, the average outperformance of the Master Agent relative to Buy&Hold is not supported at conventional significance levels, and motivating longer horizons and broader regime coverage in future validation. Overall, these results support two main findings: (i) in this internal evaluation, the Master Agent improves average risk-adjusted performance relative to a Buy&Hold baseline, and (ii) incorporating satellite-derived indicators is associated with more favorable rolling excess return profiles and stronger aggregate metrics compared to the ablated (no-satellite) configuration. However, the gains are not universal across all contracts, and the dispersion across commodities suggests that extra effort is needed to improve robustness and generalization (e.g., broader market coverage, longer and more diverse evaluation periods, and more stringent baselines and stress tests). 


<!-- PAGE_BREAK -->
3.5. Diagnostic Analysis of Underperformance 

To move beyond aggregate metrics, we diagnose where performance weakens (by commodity and period) and when/why signals degrade (by market regime). A commodity–time decomposition of monthly strategy returns, shown in Figure 4, highlights two persistently underperforming contracts, ZO = F and CT = F, with mean monthly returns of −4.23% and −2.76% and negative months in 67% and 75% of the sample, respectively; ZO = F also exhibits a pronounced downside tail (worst month 2024–12: −24.6%), consistent with episodic breakdowns. In contrast, OJ = F has near-zero average performance (−0.08%) but extreme instability (best 2025–02: +34.0%, worst 2025–07: −21.6%), suggestive of regime switches and reversal risk. Across commodities, losses cluster in specific windows (e.g., 2025–04 cross-sectional mean −3.79% with 60% of contracts negative; 2024–12: −2.50%; 2025–03: −1.72% with 80% negative). At the quarterly level, the strategy exhibits a progressive improvement over time: the first two quarters are negative (2024–Q3: −1.14%, 2024–Q4: −2.15%), but a marked recovery starts from 2025–Q1 (mean +6.05%), followed by continued strength in 2025–Q2 (mean +3.54%). 

**Figure 4.** Commodity–time decomposition of monthly Master Agent returns. 

Conditioning performance on a simple trend/volatility regime split, shown in Table 3, reveals a clear regime-dependence for the main components: the Master and Satellite agents are strongly trend-dependent, achieving positive Sharpe ratios in UPTREND regimes (Sharpe 1.86 and 3.00) but materially negative Sharpe in DOWNTREND regimes (−1.07 and −1.96), consistent with directional exposure that breaks in bearish phases. However, in bearish regimes the Master agent still provides meaningful capital preservation relative to the baseline exposure, reducing losses by 44% in HIGH-VOLATILITY/DOWNTREND and by 64% in LOW-VOLATILITY/DOWNTREND. The News agent is additionally fragile in HIGH-VOLATILITY regimes (Sharpe −0.70 vs. 0.18 in LOW-VOLATILITY), aligning with a shock/noise-dominance mechanism where textual signals become less reliable. Overall, these diagnostics show that performance is heterogeneous across commodities and time windows. Failure modes are largely explained by trend-regime mismatch for the dominant agents, volatility-driven fragility for news-based signals, and time-varying signal efficacy, alongside evidence of improving aggregate performance after 2025–Q1 and partial downside protection from the Master agent in downtrends. 


<!-- PAGE_BREAK -->
**Table 3.** Regime-split performance across volatility and trend regimes. Each cell reports annualized return/Sharpe computed from daily returns within the corresponding regime. Regime sample sizes are N = {545, 650, 771, 519} trading days for {High-Vol/Downtrend, High-Vol/Uptrend, LowVol/Downtrend, Low-Vol/Uptrend}, respectively. 

 High Volatility Low Volatility Strategy Downtrend Uptrend Downtrend Uptrend Buy&Hold −62.3%/−1.68 83.1%/2.47 −87.7%/−3.33 116.0%/4.17 Market Agent −10.5%/0.07 −5.5%/0.48 8.9%/0.83 2.8%/−0.07 Satellite Agent −40.3%/−1.23 74.2%/2.38 −72.5%/−2.70 102.2%/3.63 News Agent −6.7%/−0.59 −2.9%/−0.82 2.9%/0.36 −4.0%/−0.01 Master Agent −32.7%/−0.94 56.7%/1.73 −34.1%/−1.19 73.2%/1.99 

### 4. Conclusions and Outlooks 

This paper introduced SAIFIN, a modular multi-agent trading framework designed to fuse heterogeneous information sources—market technical signals, news-driven context, and satellite-derived indicators—into interpretable trading stances mediated by LLMbased reasoning and orchestration. The architecture is intentionally decomposed into specialized agents and a Master Agent that aggregates their outputs, enabling incremental improvements to individual components without redesigning the full pipeline. Across the ten commodity futures considered in our internal evaluation, the Master Agent exhibits a more favorable average risk–return profile than the Buy&Hold benchmark. When metrics are averaged across tickers, the Master Agent attains a higher annualized return at a volatility comparable to Buy&Hold, resulting in a positive Sharpe ratio, whereas Buy&Hold is approximately flat in return and slightly negative in Sharpe (Table 1). Importantly, this improvement is not uniform: the Master Agent outperforms Buy&Hold in annualized return on a majority of contracts (8/10), but underperforms on a minority, indicating meaningful cross-asset heterogeneity (Table 2). This dispersion suggests that the learned decision policies capture market structure in several contracts, but do not generalize equally well across all commodity microstructures and regimes. The diagnostic analysis further indicates that underperformance is not diffuse, but concentrated in specific contracts and windows, and is largely explained by regime mismatch: the dominant agents exhibit strong trend dependence, with materially weaker performance in downtrend regimes (Table 3) and persistent laggards emerge in the commodity–time return map (Figure 4). This suggests that improving regime awareness and robustness in bearish/high-volatility conditions is a primary lever for generalization. Ablation results provide evidence that satellite inputs can be a useful contributor within the multimodal decision stack. The Satellite Agent is consistently among the strongest individual modalities in aggregate, and the rolling excess-return analysis indicates that enabling satellite features is associated with more frequent and more sustained positive excess-return regimes for several contracts, while the no-satellite configuration shows deeper and more persistent negative regimes and smaller positive excursions (Figure 3). At the same time, the observed benefit is episodic and contract-dependent, and therefore should be interpreted as evidence of potential rather than a universal performance guarantee. Despite encouraging results, several limitations prevent strong external performance claims. First, the evaluation spans a limited set of instruments and a finite historical window; broader market coverage and longer horizons may help to reduce the risk of selection effects and regime dependence. This is supported by the statistical significance analysis, where the pooled mean excess return is positive but not statistically distinguishable from zero under two-way clustered inference (p-value ≈ 0.30), indicating the need for longer multi-regime evaluations along with possible model improvements. Second, robust deployability in 


<!-- PAGE_BREAK -->
futures markets requires explicit treatment of realistic trading frictions and operational constraints (e.g., transaction costs, slippage, contract rollover, margining, and liquidity limits), which may materially affect net performance. Third, the reliance on LLM-mediated reasoning introduces additional considerations regarding determinism, auditability, and failure modes (e.g., prompt sensitivity and inconsistent reasoning traces). Finally, as with any AI-enabled trading technology, regulatory compliance, transparency obligations, and systemic-risk concerns (including feedback loops and herding behaviors) must be addressed through governance and monitoring mechanisms. Future work will focus on improving robustness, attribution, and deployability of multimodal agentic trading systems. In particular, we identify the following next steps: 

- **Stronger validation protocols:** Extend evaluation across more commodities and market     regimes, adopt walk-forward testing, and add regime-conditioned performance tests. 

- **Realistic execution modeling:** Incorporate trading costs, slippage, liquidity con-     straints, and futures-specific mechanics (roll schedules and margin requirements) to     assess net performance under practical conditions. 

- **Sharper multimodal attribution:** Perform controlled ablations and sensitivity stud-     ies to quantify the marginal contribution of each agent, and to identify when each     modality is most informative. 

- **Agent improvements:** Enhance the news pipeline (entity resolution, event novelty,     and time-decay calibration), and refine the Master Agent aggregation logic with     uncertainty-aware weighting and risk budgeting. 

- **Governance and compliance:** In a deployment setting, regulation-aware design     should be grounded in (i) MiFID II algorithmic-trading systems-and-controls (Art. 17)     and related RTS 6 requirements on testing, pre-trade risk limits, and kill-switch proce-     dures; (ii) the Market Abuse Regulation (MAR) obligations to prevent and monitor     market manipulation; (iii) DORA requirements on ICT risk management, incident     reporting, and operational resilience; and (iv) the EU AI Act governance expectations     for transparency, human oversight, logging, and robustness of AI systems. SAIFIN’s     modular architecture and structured, per-agent JSON outputs provide natural hooks     for an auditable decision trail, human-in-the-loop approvals, and enforceable safety     constraints (e.g., conservative defaults, bounded actions, and monitoring alerts) that     can support these regulatory objectives.     Overall, SAIFIN demonstrates the feasibility of integrating satellite imagery, financial time series, and generative AI within a scalable, modular framework, and the reported results suggest that multimodal fusion can improve average performance relative to a Buy&Hold benchmark on the assets studied. At the same time, the observed heterogeneity across contracts motivates a cautious interpretation and highlights the need for broader validation and execution-aware evaluation before any real-world deployment. 

**Author Contributions:** Conceptualization, A.G., M.P., A.V., S.S., M.M. (Marcello Marconi) and E.P.; methodology, A.G., M.P., A.V., S.S., M.M. (Matteo Martini), F.F., R.G., E.W.D.L., U.D.M. and V.L.; software, M.P., A.V., S.S. and G.B.; validation, A.V., S.S., G.B., M.M. (Matteo Martini), F.F., R.G., E.W.D.L., U.D.M. and V.L.; writing—original draft preparation, S.S.; writing—review and editing, A.V., S.S. and G.B.; project administration, A.G., M.M. (Marcello Marconi), E.P., F.F. and R.G.; funding acquisition, A.G., M.M. (Marcello Marconi) and E.P. All authors have read and agreed to the published version of the manuscript. 


<!-- PAGE_BREAK -->
**Funding:** This paper is supported by the Fondazione ICSC, SPOKE 2—“Fundamental Research & Space Economy” nell’ambito del progetto PNRR ICSC, codice CN00000013, CUP I53C21000340006—Missione 4—Componente 2—1.4 “Potenziamento strutture di ricerca e creazione di campioni nazionali di R&S su alcune Key Enabling Technologies”. 

**Data Availability Statement:** The raw data supporting the conclusions of this article were obtained from the following resources available in the public domain: Market OHLC data and News: https://finance.yahoo.com/. Historical Weather data: https://open-meteo.com/. 

**Conflicts of Interest:** Authors Alberto Garinei, Massimiliano Proietti, Alessandro Vispa, Stefano Speziali, Giovanni Bartolini, Marcello Marconi and Emanuele Piccioni were employed by the company Idea-Re S.r.l. The remaining authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest. 

### Abbreviations 

The following abbreviations are used in this manuscript: 

AI Artificial Intelligence ATR Average True Range EMA Exponential Moving Average GPU Graphics Processing Unit HFT High-Frequency Trading HPC High-Performance Computing LLM Large Language Model MACD Moving Average Convergence Divergence OBV On-Balance Volume OHLC Open, High, Low, Close RSI Relative Strength Index SAIFIN Satellite Data and Artificial Intelligence for FINtech SMA Simple Moving Average XAI Explainable Artificial Intelligence 

### Appendix A. Technical Analysis Strategies for the Market Agent 

Appendix A.1. Foundations of Technical Analysis 

Technical analysis relies on the systematic study of past market data—primarily price and volume—to anticipate future price movements. Central to this approach are OHLC data (Open, High, Low, Close), candlestick charts, and trading indicators. OHLC values form the basis of candlestick representation, offering a concise view of market action over a given time frame. The reliability of all subsequent interpretations depends on the quality of these inputs [21]. Candlestick charts, introduced in Western finance by Steve Nison, provide an intuitive depiction of market psychology. Their global adoption creates a feedback loop: widely recognized patterns (e.g., RSI thresholds, classic reversals) may become self-fulfilling due to collective trader behavior [22]. 

Appendix A.2. Key Candlestick Patterns 

Candlestick configurations convey critical information about market indecision, reversals, or continuation: 

- **Single-candle signals:** Doji (indecision) [22], Hammer (bullish reversal in downtrend),     Hanging Man (bearish reversal in uptrend), Inverted Hammer and Shooting Star     (potential reversals). 

- **Multi-candle reversals:** Engulfing (bullish/bearish), Morning Star (bullish), Evening     Star (bearish), Harami, Dark Cloud Cover, Piercing Line [22]. 


<!-- PAGE_BREAK -->
- **Continuation patterns:** Three White Soldiers, Three Black Crows, Rising/Falling     Three Methods.     The effectiveness of these patterns depends on timely confirmation—typically within three to five subsequent candles—and their contextual alignment with trend, sup- port/resistance, or volume. 

Appendix A.3. Core Trading Indicators 

 Technical indicators enrich price-based analysis with quantitative metrics: 

- **Moving Averages (MA):** SMA provides smooth long-term trend filtering, while EMA     responds faster to recent price shifts. Crossovers (Golden Cross, Death Cross) act as     pivotal trend-change signals [23]. 

- **Relative Strength Index (RSI):** Identifies overbought (>70) and oversold (<30) condi-     tions, divergence with price, and momentum shifts [23,24]. 

- **MACD:** Combines short- and long-term EMAs to highlight momentum, with     crossovers (MACD/Signal or zero-line) signaling bullish/bearish shifts [25]. 

- **Stochastic Oscillator:** Measures closing price position relative to range; crossovers in     overbought (>80) or oversold (<20) zones provide early reversal signals [26]. 

- **Bollinger Bands:** Volatility envelopes that expand/contract with market variabil-     ity. “Squeeze” anticipates breakout, while outer-band touches suggest relative     extremes [27]. 

- **Volume:** Serves as a confirmation layer for trend strength, breakouts, and candlestick     patterns. Divergences (e.g., OBV vs. price) often prelude reversals [23]. 

Appendix A.4. Combined Strategies 

 The robustness of trading signals improves when multiple tools converge: 

- **Pattern + Momentum:** Hammer with RSI exiting oversold; Shooting Star confirmed     by RSI divergence [23]. 

- **Pattern + MACD:** Morning Star validated by bullish MACD crossover; Evening Star     reinforced by bearish MACD [25]. 

- **Pattern + Stochastic:** Doji/Shooting Star at overbought levels with stochastic     crossover [26]. 

- **Pattern + Moving Average:** Reversals aligned with key MAs (support/resistance)     increase reliability [23]. 

- **Bollinger Bands + Oscillators:** Reversal patterns near bands confirmed by RSI or     MACD provide strong signals [27]. 

- **Multi-indicator synergy:** Aligning signals across momentum, trend, and volatility     indicators filters noise and increases confidence [23].     Cross-timeframe validation (e.g., hourly reversal aligning with daily trend) further strengthens outcomes. 

Appendix A.5. Risk Management and Best Practices 

 Even sophisticated strategies fail without disciplined risk management: 

- Confirm signals using independent indicators or volume to mitigate false positives [23]. 

- Place stop-loss orders logically (below pattern lows/highs or beyond MA levels). 

- Define take-profit targets based on resistance/support, Bollinger bands, or risk/reward     ratios (e.g., 1:2). 

- Adapt strategies to timeframes and market regimes (trend vs. range). 

- Manage parameter sensitivity (e.g., RSI length, MA periods) based on asset volatility. 


<!-- PAGE_BREAK -->
 Ultimately, technical analysis gains predictive strength from the convergence of tools rather than isolated signals. Success depends on combining price action, indicators, and disciplined execution within adaptive frameworks. 

### References 

1. Falaiye, T.; Addy, W.A.; Ajayi-Nifise, A.O.; Bello, B.G.; Tula, S.T.; Odeyemi, O. Algorithmic Trading and AI: A Review of Strategies     and Market Impact. World J. Adv. Eng. Technol. Sci. **2024** , 11 , 258–267. [CrossRef] 

2. Hendershott, T.; Jones, C.M.; Menkveld, A.J. Does Algorithmic Trading Improve Liquidity? J. Financ. **2011** , 66 , 1–33. [CrossRef] 

3. Menkveld, A.J. High Frequency Trading and the New Market Makers. J. Financ. Mark. **2013** , 16 , 712–740. [CrossRef] 

4. Bhuiyan, M.D.S.M. Deep learning for algorithmic trading: A systematic review of predictive models and optimization strategies.     Array **2025** , 26 , 100390. [CrossRef] 

5. Ali, H.; Zafar, M.B.; Aysan, A.F. Generative AI in finance: Replicability, methodological contingencies, and future research     directions. Financ. Res. Lett. **2025** , 86 , 108797. [CrossRef] 

6. Khan, A.T.; Li, S.; Cao, X. Bridging Finance and AI: A Comprehensive Survey of Large Language Models in Financial System.     Digit. Financ. **2025** , 7 , 679–701. [CrossRef] 

7. Lee, J.; Stevens, N.; Han, S.C. Large Language Models in Finance (FinLLMs). Neural Comput. Appl. **2025** , 37 , 24853–24867.     [CrossRef] 

8. Guntuka, S. AI-Driven Algorithmic Trading: Advanced Techniques Reshaping Financial Markets. Int. J. Comput. Eng. Technol.     **2024** , 15 , 564–571. [CrossRef] 

9. Bondo Hansen, K.; Borch, C. Alternative Data and Sentiment Analysis: Prospecting Non-standard Data in Machine Learning-     driven Finance. Big Data Soc. **2022** , 9 , 1–14. [CrossRef] 

10. Sun, Y.; Liu, L.; Xu, Y.; Zeng, X.; Shi, Y.; Hu, H.; Jiang, J.; Abraham, A. Alternative data in finance and business: Emerging     applications and theory analysis (review). Financ. Innov. **2024** , 10 , 127. [CrossRef] 

11. Chen, P.; Boukouvalas, Z.; Corizzo, R. A Deep Fusion Model for Stock Market Prediction with News Headlines and Time Series     Data. Neural Comput. Appl. **2024** , 36 , 21229–21271. [CrossRef] 

12. Caldecott, B.; McCarten, M.; Christiaen, C.; Hickey, C. Spatial finance: Practical and theoretical contributions to financial analysis.     J. Sustain. Financ. Invest. **2022** , 1–17; Advance online publication. [CrossRef] 

13. Katona, Z.; Painter, M.O.; Patatoukas, P.N.; Zeng, J. On the Capital Market Consequences of Big Data: Evidence from Outer Space.     J. Financ. Quant. Anal. **2025** , 60 , 551–579. [CrossRef] 

14. Feng, C.; Fay, S. An Empirical Investigation of Forward-Looking Retailer Performance Using Parking Lot Traffic Data Derived     from Satellite Imagery. J. Retail. **2022** , 98 , 633–646. [CrossRef] 

15. Beverungen, A. Algorithmic Trading, Artificial Intelligence and the Politics of Cognition. In The Democratization of Artificial     Intelligence: Net Politics in the Era of Learning Algorithms; Sudmann, A., Ed.; Transcript Verlag: Bielefeld, Germany, 2019; pp. 77–94.     [CrossRef] 

16. OpenAI. OpenAI API Documentation. 2025. Available online: https://platform.openai.com/docs/api-reference (accessed on     22 December 2025). 

17. Zippenfenig, P. Open-Meteo.com Weather API. 2023. Available online: https://doi.org/10.5281/ZENODO.7970649 (accessed on     22 December 2025). 

18. Sharpe, W.F. The Sharpe Ratio. J. Portf. Manag. **1994** , 21 , 49–58. [CrossRef] 

19. Lo, A.W. The Statistics of Sharpe Ratios. Financ. Anal. J. **2002** , 58 , 36–52. [CrossRef] 

20. Magdon-Ismail, M.; Atiya, A.F.; Pratap, A.; Abu-Mostafa, Y.S. On the Maximum Drawdown of a Brownian Motion. J. Appl.     Probab. **2004** , 41 , 147–161. [CrossRef] 

21. Marshall, B.R.; Young, M.R.; Rose, L.C. Candlestick Technical Trading Strategies: Can They Create Value for Investors? J. Bank.     Financ. **2006** , 30 , 2303–2323. [CrossRef] 

22. Lu, T.H.; Shiu, Y.M.; Liu, T.C. Profitable Candlestick Trading Strategies—The Evidence from a New Perspective. Rev. Financ.     Econ. **2012** , 21 , 63–68. [CrossRef] 

23. Park, C.H.; Irwin, S.H. What Do We Know About the Profitability of Technical Analysis? J. Econ. Surv. **2007** , 21 , 786–826.     [CrossRef] 

24. Chong, T.T.L.; Ng, W.K. Technical Analysis and the London Stock Exchange: Testing the MACD and RSI Rules Using the FT30.     Appl. Econ. Lett. **2008** , 15 , 1111–1114. [CrossRef] 

25. Chong, T.T.L.; Ng, W.K.; Liew, V.K.S. Revisiting the Performance of MACD and RSI Oscillators. J. Risk Financ. Manag. **2014** ,     7 , 1–12. [CrossRef] 


<!-- PAGE_BREAK -->
26. Paik, C.K.; Choi, J.; Ureta Vaquero, I. Algorithm-Based Low-Frequency Trading Using a Stochastic Oscillator and William%R: A     Case Study on the U.S. and Korean Indices. J. Risk Financ. Manag. **2024** , 17 , 92. [CrossRef] 

27. Fang, J.; Jacobsen, B.; Qin, Y. Popularity versus Profitability: Evidence from Bollinger Bands. J. Portf. Manag. **2017** , 43 , 152–159.     [CrossRef] 

**Disclaimer/Publisher’s Note:** The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.