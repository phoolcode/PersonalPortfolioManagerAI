import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIAssistant:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.openai_api_key)
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        self.model = "o3"
    
    def generate_summary(self, tickers: List[str], market_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate AI-powered market summary with 3 sections"""
        
        # Format the market data for the prompt
        formatted_data = self._format_market_data(tickers, market_data)
        
        prompt = f"""
You are the world’s top portfolio strategist — fluent in equities, macro, sentiment, and risk analytics.
You can also communicute in a way any smart investor can understand — concise, confident, and free of jargon.
Summarize the latest events for this portfolio: {', '.join(tickers)}
You have the latest portfolio data (tickers, performance, sector weights), market news, and Reddit sentiment.  
Your job: synthesize all signals to explain what’s happening, what it means for the portfolio owner, and how the market feels.

Recent portfolio + market data:
{formatted_data}

Output only valid JSON with these 4 fields:

1. "current_events": "Describe current market and portfolio movements — key drivers, news catalysts, sector rotations, or sentiment shifts affecting this portfolio. Make it easy to understand, and more user-friendly than purely technical. Talk about domain, market and what that has changed and not just summarizing the head-lines",
2. "actionable_insights": "Explain what this means for the portfolio owner — specific strategic or tactical takeaways (add, trim, hedge, rebalance, hold).",
3.  "sentiment": "Overall market sentiment — 'bullish', 'bearish', or 'mixed'.",
4.  "sentiment_reasoning": "One or two sentences on why sentiment leans that way, referencing macro tone, flow dynamics, and retail vs institutional behavior."

Be analytical, confident, and concise — like a high-stakes investment briefing, not a summary.

Respond with valid JSON only."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_completion_tokens=1024
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "current_events": f"Error generating summary: {str(e)}",
                "actionable_insights": "Unable to provide insights at this time.",
                "sentiment": "mixed",
                "sentiment_reasoning": "Error in analysis"
            }
    
    def chat_response(
    self,
    question: str,
    tickers: List[str],
    market_data: Dict[str, Any],
    chat_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a portfolio-aware response using system, user, and assistant roles.
        Maintains chat history and grounds each response in market + portfolio data.
        """

        formatted_data = self._format_market_data(tickers, market_data)

        # ---- SYSTEM PROMPT ----
        system_message = {
            "role": "system",
            "content": (
                "You are a world-class portfolio strategist and financial advisor. "
                "You analyze portfolios using real-time data from stock performance, market news, and Reddit sentiment. "
                "You think like a chief investment officer — combining macro, micro, and behavioral signals "
                "to interpret what’s happening in the markets and what it means for the user’s portfolio.\n\n"
                "Your role:\n"
                "- Engage in intelligent, data-driven conversation with the user about their portfolio and the market.\n"
                "- Ground every response in the provided portfolio data, current market trends, and sentiment context.\n"
                "- Provide clear reasoning, causal insights, and professional-grade analysis — not financial advice.\n"
                "- Maintain a concise, confident tone — as if briefing a sophisticated investor.\n"
                "- Use analytical depth: reference sector rotations, volatility shifts, valuation pressures, liquidity flows, "
                "or macro catalysts when relevant.\n"
                "- Be rational, factual, and portfolio-focused.\n\n"
                f"User context:\n{formatted_data}\n\n"
                "Respond conversationally but precisely — analytical, confident, and insight-rich."
            )
        }

        # ---- BUILD MESSAGE SEQUENCE ----
        messages = [system_message]

        # Add chat history if any (each item must include "role" and "content")
        if chat_history:
            for msg in chat_history:
                if msg.get("role") in ["user", "assistant"]:
                    messages.append(msg)
        # curr question
        messages.append({
            "role": "user",
            "content": f"Portfolio tickers: {', '.join(tickers)}\n\nUser question: {question}"
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_completion_tokens=1024
            )
            answer = response.choices[0].message.content.strip()

            return answer

        except Exception as e:
            return f"I’m having trouble processing your question right now. Error: {str(e)}"

    
    def _format_market_data(self, tickers: List[str], market_data: Dict[str, Any]) -> str:
        """Format market data for AI prompts"""
        formatted = []
        
        # Format stock data
        stock_data = market_data.get('stocks', {})
        if stock_data:
            formatted.append("STOCK PRICES:")
            for ticker in tickers:
                if ticker in stock_data:
                    data = stock_data[ticker]
                    if 'error' not in data:
                        price = data.get('price', 'N/A')
                        change_pct = data.get('change_percent', 0)
                        direction = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"
                        formatted.append(f"  {ticker}: ${price} ({change_pct:+.2f}%) {direction}")
                    else:
                        formatted.append(f"  {ticker}: {data['error']}")
        
        # Format news data
        news_data = market_data.get('news', {})
        if news_data:
            formatted.append("\nNEWS HEADLINES:")
            for ticker in tickers:
                if ticker in news_data and news_data[ticker]:
                    articles = news_data[ticker][:2]  # Top 2 articles
                    formatted.append(f"  {ticker}:")
                    for article in articles:
                        if 'error' not in article:
                            title = article.get('title', 'No title')
                            formatted.append(f"    - {title}")
        
        # Format Reddit data
        reddit_data = market_data.get('reddit', {})
        if reddit_data:
            formatted.append("\nREDDIT SENTIMENT:")
            for ticker in tickers:
                if ticker in reddit_data and reddit_data[ticker]:
                    posts = reddit_data[ticker][:2]  # Top 2 posts
                    formatted.append(f"  {ticker}:")
                    for post in posts:
                        if 'error' not in post:
                            title = post.get('title', 'No title')
                            score = post.get('score', 0)
                            sentiment_indicator = "👍" if score > 0 else "👎" if score < 0 else "😐"
                            formatted.append(f"    - {title} (Score: {score} {sentiment_indicator})")
        
        return '\n'.join(formatted) if formatted else "No market data available"
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of given text"""
        prompt = f"""Analyze the sentiment of this financial text and provide a rating.
        
Text: {text}

Respond with JSON containing:
- "sentiment": "bullish", "bearish", or "mixed"
- "confidence": number between 0 and 1
- "reasoning": brief explanation

Respond with valid JSON only."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_completion_tokens=256
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "sentiment": "mixed",
                "confidence": 0.0,
                "reasoning": f"Error analyzing sentiment: {str(e)}"
            }
