# AI Personal Portfolio Manager

This is an AI agent (GPT o3) that gives insights, beyond just stock prices and charts. For the first iteration, I wanted to focus on the storytelling side of markets: what’s happening, why it matters, and how the market feels about it.

This app lets you upload a small portfolio (right now it’s just tickers. no quantities or timestamps yet) and then it pulls in live data from a few places: stock prices, news, and Reddit chatter. Once it’s got that, it generates three short summaries:

1. What’s going on in the market,
2. What’s relevant for your portfolio, and
3. What the market sentiment looks like.

There’s also a chat interface where you can ask questions directly, and it answers using all the live data it just pulled.

## Features

- Upload CSV portfolio or add tickers manually
- Real-time stock prices with price changes
- Breaking financial news headlines
- Reddit sentiment analysis and social mentions
- Summarized market analysis specific to the portfolio
- Chat feature to ask questions about your portfolio/market etc
- Auto-refresh every 60 seconds or manual refresh

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- a .env file containing all the API keys (Sent via mail)

## Installation Steps
Please head to [QUICKSTART_LOCAL.md](https://github.com/phoolcode/PersonalPortfolioManagerAI/blob/main/QUICKSTART_LOCAL.md) for instructions

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── data_fetcher.py     # Handles API calls for stocks, news, Reddit
├── ai_assistant.py     # GPT integration for with prompts for summaries etc
├── pyproject.toml      # Python dependencies
├── poetry.lock         # poetry lock file
├── .env                # API keys secrets (create this)
└── .streamlit/
    └── config.toml    # Streamlit server configuration
```

### What I built in time

It’s a simple Streamlit app that talks to a few APIs — Finnhub for prices, NewsAPI for headlines, Reddit’s public feed for chatter — and uses GPT-5 for all the reasoning and summarization. It refreshes automatically and keeps things conversational instead of dumping numbers.

There’s no backend, no authentication, no user accounts. Right now it’s light and local. I wanted to see how far I could get in three hours without over-engineering anything.


### What I wanted to build but ran out of time

A few features I really wanted to add but didn’t make the cut because I was busy debugging Streamlit:

* **Portfolio planning** — actually generate a portfolio strategy based on holdings, momentum, and sentiment instead of just commentary.
* **Deeper Reddit + insider tracking** — I wanted to scrape subreddits like r/wallstreetbets, r/valueinvesting, and r/investing for ticker mentions in the past 24 hours, cross-check those with insider buying on OpenInsider and superinvestor data from Dataroma, and then rank ideas based on how interesting they are
* **Scoring** — a layer that combines institutional moves and discussion volume to surface tickers worth digging into (Maybe insider moves too, but I dont know how to get there yet).
* **Better summary** — once a ticker scores high, the model would generate a business summary, moat analysis, management record, catalysts, and a bull/bear scenario. 
So I wanted to build a research assistant that could help with due diligence.


### What I’d add next

If I had more time, I’d 
1. make it faster (the API calls stack up right now)
2. Validate prompts properly and do some prompt evaluation/experimentation (I wanted to try COT-few shot, gpt 5 and some other models. Chose o3 because it's a reasoning model for now) 
3. Add multiple pages, one for insights, one for discovery. 
4. I’d also move some of the logic into a backend so it’s scalable. 
5. Eventually, I want it to feel like your personal market analyst and not just reading data, but building intuition alongside you.

### Final thoughts

This is a very cursory sketch at the moment. But I had fun connecting data and building using streamlit, because I hadn't done much of that before. I wanted it to teach me something new about a ticker. It actually did, a few times.

It’s rough around the edges, but it worked!