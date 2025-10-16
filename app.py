import streamlit as st
import pandas as pd
import time
import asyncio
from datetime import datetime
import os
from data_fetcher import DataFetcher
from ai_assistant import AIAssistant

# Page configuration
st.set_page_config(
    page_title="Gaus Take Home Assignment",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'tickers' not in st.session_state:
    st.session_state.tickers = []
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = {}
if 'news_data' not in st.session_state:
    st.session_state.news_data = {}
if 'reddit_data' not in st.session_state:
    st.session_state.reddit_data = {}
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = None

# Initialize data fetcher and AI assistant
@st.cache_resource
def get_data_fetcher():
    return DataFetcher()

@st.cache_resource
def get_ai_assistant():
    return AIAssistant()

data_fetcher = get_data_fetcher()
ai_assistant = get_ai_assistant()

def fetch_all_data():
    """Fetch all data for the current tickers"""
    if not st.session_state.tickers:
        return
    
    with st.spinner("Fetching market data..."):
        # Fetch stock prices
        st.session_state.stock_data = data_fetcher.get_stock_prices(st.session_state.tickers)
        
        # Fetch news
        st.session_state.news_data = data_fetcher.get_news(st.session_state.tickers)
        
        # Fetch Reddit sentiment
        st.session_state.reddit_data = data_fetcher.get_reddit_sentiment(st.session_state.tickers)
        
        # Generate AI summary
        combined_data = {
            'stocks': st.session_state.stock_data,
            'news': st.session_state.news_data,
            'reddit': st.session_state.reddit_data
        }
        st.session_state.ai_summary = ai_assistant.generate_summary(st.session_state.tickers, combined_data)
        st.session_state.last_update = datetime.now()

def get_sentiment_color(sentiment):
    """Return color based on sentiment"""
    if sentiment.lower() in ['bullish', 'positive']:
        return '#28a745'  # Green
    elif sentiment.lower() in ['bearish', 'negative']:
        return '#dc3545'  # Red
    else:
        return '#ffc107'  # Yellow for mixed/neutral

# Main UI
st.title("Gaus Take Home Assignment")
st.markdown("Track your portfolio with real-time data, news, and AI-powered insights")

# Sidebar for portfolio management
with st.sidebar:
    st.header("Portfolio Management")
    
    # CSV Upload
    uploaded_file = st.file_uploader("Upload Portfolio CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'Ticker' in df.columns:
                new_tickers = df['Ticker'].str.upper().tolist()
                if new_tickers != st.session_state.tickers:
                    st.session_state.tickers = new_tickers
                    st.success(f"Loaded {len(new_tickers)} tickers")
                    fetch_all_data()
            else:
                st.error("CSV must contain a 'Ticker' column")
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
    
    # Manual ticker entry
    st.subheader("Or Add Tickers Manually")
    ticker_input = st.text_input("Enter ticker symbols (comma-separated)")
    
    if st.button("Add Tickers"):
        if ticker_input:
            new_tickers = [t.strip().upper() for t in ticker_input.split(',')]
            st.session_state.tickers = list(set(st.session_state.tickers + new_tickers))
            st.success(f"Added tickers: {', '.join(new_tickers)}")
            fetch_all_data()
    
    # Current portfolio
    if st.session_state.tickers:
        st.subheader("Current Portfolio")
        for ticker in st.session_state.tickers:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📊 {ticker}")
            with col2:
                if st.button("❌", key=f"remove_{ticker}"):
                    st.session_state.tickers.remove(ticker)
                    st.rerun()
    
    # Refresh controls
    st.subheader("Data Controls")
    if st.button("🔄 Refresh Now"):
        fetch_all_data()
        st.success("Data refreshed!")
    
    if st.session_state.last_update:
        st.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

# Main content area
if not st.session_state.tickers:
    st.info("👆 Upload a CSV file with tickers or add them manually to get started!")
else:
    # Auto-refresh every 60 seconds
    placeholder = st.empty()
    
    # Display AI Summary
    if st.session_state.ai_summary:
        st.header("Here's a Summary since you last checked in:")
        try:
            summary_data = eval(st.session_state.ai_summary) if isinstance(st.session_state.ai_summary, str) else st.session_state.ai_summary
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("What's been happening?")
                st.write(summary_data.get('current_events', 'No data available'))
            
            with col2:
                st.subheader("What it means for you?")
                st.write(summary_data.get('actionable_insights', 'No insights available'))
            
            with col3:
                st.subheader("How are people feeling?")
                sentiment = summary_data.get('sentiment', 'neutral')
                color = get_sentiment_color(sentiment)
                st.markdown(f"<div style='color: {color}; font-weight: bold;'>{sentiment.upper()}</div>", unsafe_allow_html=True)
                st.write(summary_data.get('sentiment_reasoning', 'No reasoning available'))
        
        except:
            st.write(st.session_state.ai_summary)
    
    # Stock prices display
    if st.session_state.stock_data:
        st.header("Stock Prices")
        
        cols = st.columns(min(len(st.session_state.tickers), 4))
        for i, ticker in enumerate(st.session_state.tickers):
            with cols[i % 4]:
                if ticker in st.session_state.stock_data:
                    data = st.session_state.stock_data[ticker]
                    price = data.get('price', 'N/A')
                    change = data.get('change', 0)
                    change_pct = data.get('change_percent', 0)
                    
                    color = '#28a745' if change >= 0 else '#dc3545'
                    
                    st.metric(
                        label=ticker,
                        value=f"${price}",
                        delta=f"{change_pct:.2f}%" if isinstance(change_pct, (int, float)) else "N/A"
                    )
    
    # News and Reddit data in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📰 Breaking News")
        if st.session_state.news_data:
            for ticker in st.session_state.tickers[:3]:  # Show top 3 tickers
                if ticker in st.session_state.news_data:
                    st.subheader(f"News for {ticker}")
                    news_items = st.session_state.news_data[ticker][:3]  # Show top 3 news items
                    for article in news_items:
                        st.write(f"• **{article.get('title', 'No title')}**")
                        st.caption(article.get('description', 'No description'))
                        if article.get('url'):
                            st.markdown(f"[Read more]({article['url']})")
                        st.divider()
        else:
            st.info("No news data available")
    
    with col2:
        st.header("🔴 Reddit Sentiment")
        if st.session_state.reddit_data:
            for ticker in st.session_state.tickers[:3]:  # Show top 3 tickers
                if ticker in st.session_state.reddit_data:
                    st.subheader(f"Reddit mentions for {ticker}")
                    reddit_items = st.session_state.reddit_data[ticker][:3]  # Show top 3 posts
                    for post in reddit_items:
                        st.write(f"• **{post.get('title', 'No title')}**")
                        score = post.get('score', 0)
                        color = '#28a745' if score > 0 else '#dc3545' if score < 0 else '#6c757d'
                        st.markdown(f"<span style='color: {color}'>Score: {score}</span>", unsafe_allow_html=True)
                        st.divider()
        else:
            st.info("No Reddit data available")
    
    # Chat interface
    st.header("Ask me anything")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)
    
    # Chat input
    chat_input = st.chat_input("Ask about your portfolio...")
    
    if chat_input:
        # Add to chat history
        with st.chat_message("user"):
            st.write(chat_input)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                combined_data = {
                    'stocks': st.session_state.stock_data,
                    'news': st.session_state.news_data,
                    'reddit': st.session_state.reddit_data
                }
                response = ai_assistant.chat_response(chat_input, st.session_state.tickers, combined_data, chat_history=st.session_state.chat_history)
                st.write(response)
                
                st.session_state.chat_history.append((chat_input, response))

# Auto-refresh mechanism
if st.session_state.tickers and st.session_state.last_update:
    time_since_update = (datetime.now() - st.session_state.last_update).seconds
    if time_since_update > 60:  # Auto refresh every 60 seconds
        fetch_all_data()
        st.rerun()
