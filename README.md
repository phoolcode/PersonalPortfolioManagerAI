# AI Personal Portfolio Manager

An AI-powered investment analyst that connects market data, news, and social sentiment to give you insights you won't find on Yahoo Finance.

![Image](https://github.com/phoolcode/PersonalPortfolioManagerAI/blob/main/images/Screenshot%202025-10-16%20at%209.11.34%E2%80%AFPM.png)

## What It Actually Does
Instead of just showing you stock prices, this tool tells you why things are moving and what it means for your holdings.

## Example Output
### Portfolio:
NVDA, DHR, ISRG, BTDR

### What's been happening?

```"The portfolio is edging higher as the broader market rallies on stronger-than-expected bank earnings and renewed hopes for a 2024 Fed rate cut. Money is flowing back into mega-cap tech and high-quality industrials. Nvidia (+1.1%) continues to benefit from eye-popping AI infrastructure deals and the belief that hyperscalers will keep spending regardless of the economic backdrop. Danaher (+2.3%) is rebounding after analyst pieces highlighted its 'monopoly-like' margins and a valuation discount—investors are rotating into steady life-science cash flows as a defensive growth play. Intuitive Surgical (-0.2%) is treading water; options activity and upcoming earnings are keeping traders on the sidelines until guidance firm up. Bitdeer (-0.1%) is flat—new analyst coverage adds visibility, but crypto mining stays hostage to muted bitcoin price action. Retail chatter on Reddit is euphoric for AI names ("mania stage" posts) while interest in the other holdings is lukewarm, reinforcing a narrow leadership narrative."```

### What it means for you?

```"1. NVDA: Keep a core position but consider trimming around strength or adding a protective collar—sentiment is stretched and implied volatility is rich. 2) DHR: Add on weakness; multiple expansion could continue as investors seek defensive growth ahead of an uncertain macro tape. 3) ISRG: Hold and wait for earnings clarity; if you want to be proactive, sell out-of-the-money puts to get paid for patience. 4) BTDR: Treat as a small satellite; maintain or hedge until a clear bitcoin up-trend emerges. Portfolio is AI-heavy—rebalance 3-5% into cash or short-duration Treasuries to dampen any sudden momentum unwind."```

### How are people feeling?

```"BULLISH - Strong earnings beats, falling bond yields, and retail enthusiasm for AI have reignited risk appetite; institutional flows are migrating back into quality growth, overpowering pockets of caution in crypto and pre-earnings healthcare names."```

### Then I Asked: "What risk am I not seeing in this portfolio? What would hurt all four of these at once?"

AI's response:

> "Key blind spot: despite spanning different industries they are all 'long-duration, growth-premium' assets. Anything that forces the market to re-price the future cash flows of expensive growth franchises will knock all four down in tandem. The common shock vectors are:
>
> 1. **Rates & Liquidity Shock** - A jump in real yields or an extended 'higher-for-longer' Fed path raises the discount rate on long-dated cash flows. NVDA (38x forward earnings), ISRG (~50x), DHR (~26x) and BTDR (still cash-burning) all rely on heavy multiple support. A 50 bp rise in the 10-yr real yield has historically clipped 10-15% off high-growth multiples.
>
> 2. **Stronger-for-longer USD** - All four generate a meaningful share of revenue abroad. A dollar spike compresses overseas earnings when translated back, while also tightening global financial conditions.
>
> 3. **Regulatory / Geo-political hit to tech supply chains** - Escalated U.S.–China tech export controls, Taiwan risk, or sanctions could curb NVDA GPU sales, snarl robot-component supply for ISRG, and raise cap-ex costs for DHR labs. BTDR's mining rigs and hosting centers are Asia-linked as well.
>
> 4. **Energy-price shock → margin pinch + sentiment risk** - BTDR's cost of goods is electricity. NVDA's data-center clients and ISRG hospitals are power-hungry; higher energy prices pressure both demand and costs. Inflation flare-up would feed back into #1 via rates.
>
> 5. **Risk-off volatility spike** - Positioning is crowded. Reddit sentiment shows 'mania' around NVDA and general bullishness. If the VIX shoots from 14 to, say, 25, systematic deleveraging will hammer anything with high beta to the Nasdaq 100—these four all sit in the 1.2-1.6 range.
>
> In short, the portfolio is structurally exposed to a single macro factor: the market's willingness to pay for future innovation."

**This is was not super generic** The portfolio *looks* diversified across sectors (semiconductors, life sciences, medtech, crypto mining), but we identified they're all duration plays with rich multiples—a hidden correlation that would only show up during a rates shock.


## Why This Is Different
Most portfolio trackers just show you numbers. This one:

* Connects the dots between your holdings and broader market moves
* Surfaces social sentiment from Reddit to catch early momentum or concern
* Explains causality - not just "NVDA is up 2%" but why and what drove it
* Lets you interrogate the analysis through chat

## Installation
See [QUICKSTART_LOCAL.md](https://github.com/phoolcode/PersonalPortfolioManagerAI/blob/main/QUICKSTART_LOCAL.md) for detailed setup instructions.

## How It Works

1. Upload a CSV with tickers (or add them manually)
2. The app pulls:
   - Real-time prices from Finnhub
   - Breaking news from NewsAPI
   - Reddit mentions and sentiment from public feeds
3. GPT-o3 (OpenAI's reasoning model) synthesizes all of this into three summaries:
   - What's happening in the market broadly
   - What's relevant to your specific portfolio
   - What the sentiment looks like on social
4. Chat with the AI to dig deeper

Auto-refreshes every 60 seconds so you stay current.

## Tech Stack

- **Frontend:** Streamlit (fast to build, conversational UX)
- **Data Sources:** Finnhub (prices), NewsAPI (headlines), Reddit API (sentiment)
- **AI:** OpenAI o3 (reasoning model for connecting multi-source insights)
- **Language:** Python 3.11+

## Project Structure

```
├── app.py              # Main Streamlit application
├── data_fetcher.py     # API calls for stocks, news, Reddit
├── ai_assistant.py     # GPT integration and prompt templates
├── pyproject.toml      # Dependencies
├── poetry.lock         # Lock file
├── .env                # API keys (you create this)
└── .streamlit/
    └── config.toml     # Streamlit configuration
```
## What I Learned Building This

* **The insight that surprised me:** When I ran this on NVDA/DHR/ISRG/BTDR, the AI identified that despite looking sector-diverse, they're all "long-duration growth-premium" assets that would get hit simultaneously by a rates shock. That's a correlation you wouldn't see from sector labels alone—it required synthesizing valuation multiples, revenue exposure, and macro sensitivity.
* **The technical challenge:** Streamlit's session state is quirky. I burned 45 minutes debugging why the chat history wasn't persisting across refreshes. Solution: explicitly store everything in `st.session_state` and reinitialize on every run.
* **What took longer than expected:** Getting the Reddit API to return useful data. The public feed is noisy—needed to filter by subreddit, upvotes, and recency to get signal. But it was worth it; catching "mania stage" sentiment around NVDA before it showed up in institutional commentary was valuable.

## What I'd Build Next

If I had another few hours:

* **Portfolio planning** — actually generate a portfolio strategy based on holdings, momentum, and sentiment instead of just commentary.
* **Deeper Reddit + insider tracking** — I wanted to scrape subreddits like r/wallstreetbets, r/valueinvesting, and r/investing for ticker mentions in the past 24 hours, cross-check those with insider buying on OpenInsider and superinvestor data from Dataroma, and then rank ideas based on how interesting they are
* **Scoring** — a layer that combines institutional moves and discussion volume to surface tickers worth digging into (Maybe insider moves too, but I dont know how to get there yet).
* **Better summary** — once a ticker scores high, the model would generate a business summary, moat analysis, management record, catalysts, and a bull/bear scenario. So I wanted to build a research assistant that could help with due diligence.
What I’d add next
* **Prommpting** - Validate prompts properly and do some prompt evaluation/experimentation (I wanted to try COT-few shot, gpt 5 and some other models. Chose o3 because it's a reasoning model for now)

## Known Limitations
- **No position sizing yet** - Right now it's just tickers, not quantities or entry prices, so recommendations aren't truly personalized to your P&L
- **API rate limits** - If you have 20+ tickers, you'll hit rate limits on free tiers
- **Refresh latency** - Pulling from 3 APIs sequentially takes ~8-10 seconds
- **No historical context** - It only looks at today's data, doesn't track trends over time or calculate rolling correlations

## Why I Built It This Way

#### I wanted to see if I could make market data feel like a conversation with an analyst instead of a dashboard full of charts. The goal was to build something that teaches you something *non-obvious* about your portfolio.
#### Three hours isn't enough to build everything, so I focused on the insight quality and functionality. The data pipeline is simple, but the summaries actually surface hidden correlations and connect social sentiment to institutional flows.
---

**Feedback welcome.** This is v0.1 and intentionally rough around the edges. If you find it useful or have ideas for what to add next, let me know.
