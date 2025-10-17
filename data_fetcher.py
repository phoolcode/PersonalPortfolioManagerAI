import requests
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import requests

load_dotenv()

class DataFetcher:
    def __init__(self):
        # API Keys from environment variables
        self.finnhub_key = os.getenv("FINNHUB_API_KEY", "")
        self.news_api_key = os.getenv("NEWS_API_KEY", "")
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
        
        # Base URLs
        # Used these because they are free to use.
        self.finnhub_base = "https://finnhub.io/api/v1"
        self.news_api_base = "https://newsapi.org/v2"
        self.reddit_base = "https://www.reddit.com"
    
    def get_stock_prices(self, tickers: List[str]) -> Dict[str, Any]:
        """Fetch current stock prices for given tickers"""
        stock_data = {}
        
        for ticker in tickers:
            try:
                # Finnhub API for stock prices
                url = f"{self.finnhub_base}/quote"
                params = {
                    'symbol': ticker,
                    'token': self.finnhub_key
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    current_price = data.get('c', 0)
                    previous_close = data.get('pc', 0)
                    change = current_price - previous_close if current_price and previous_close else 0
                    change_percent = (change / previous_close * 100) if previous_close else 0
                    
                    stock_data[ticker] = {
                        'price': round(current_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'high': data.get('h', 0),
                        'low': data.get('l', 0),
                        'open': data.get('o', 0),
                        'previous_close': previous_close
                    }
                else:
                    stock_data[ticker] = {
                        'error': f'Failed to fetch data: {response.status_code}'
                    }
                    
            except Exception as e:
                stock_data[ticker] = {
                    'error': f'Error fetching {ticker}: {str(e)}'
                }
        
        return stock_data
    
    def get_news(self, tickers: List[str]) -> Dict[str, List[Dict]]:
        """Fetch breaking news for given tickers and extract full article text"""
        news_data = {}

        for ticker in tickers:
            try:
                url = f"{self.news_api_base}/everything"
                params = {
                    'q': f'{ticker} stock OR {ticker} earnings OR {ticker} financial',
                    'apiKey': self.news_api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 5
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])

                    news_items = []
                    for article in articles:
                        news_items.append({
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'url': article.get('url', ''),
                            'published_at': article.get('publishedAt', ''),
                            'source': article.get('source', {}).get('name', '')
                        })

                    news_data[ticker] = news_items
                else:
                    news_data[ticker] = [{'error': f'Failed to fetch news: {response.status_code}'}]

            except Exception as e:
                news_data[ticker] = [{'error': f'Error fetching news for {ticker}: {str(e)}'}]

        return news_data
    
    def get_reddit_sentiment(self, tickers: List[str]) -> Dict[str, List[Dict]]:
        """Fetches Reddit mentions for given tickers"""
        reddit_data = {}
        
        for ticker in tickers:
            try:
                # Using Reddit JSON API
                subreddits = ['investing', 'stocks', 'SecurityAnalysis', 'ValueInvesting', 'wallstreetbets']
                all_posts = []
                # What I would additionally do is not just check mentions but maybe topic modeling on posts in these subreddits to find more relevant posts and not just mentions
                # While testing I realised not all subreddits have posts about all tickers. So if i dont find any posts in one subreddit i will move to the next one.
                for subreddit in subreddits[:5]:  # Limiting rn to 5 subreddits to avoid rate limits
                    try:
                        url = f"{self.reddit_base}/r/{subreddit}/search.json"
                        params = {
                            'q': ticker,
                            'restrict_sr': '1',
                            'sort': 'new',
                            'limit': 3
                        }
                        
                        headers = {'User-Agent': 'AIMarketCompanion/1.0'}
                        response = requests.get(url, params=params, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            posts = data.get('data', {}).get('children', [])
                            
                            for post in posts:
                                post_data = post.get('data', {})
                                all_posts.append({
                                    'title': post_data.get('title', ''),
                                    'score': post_data.get('score', 0),
                                    'num_comments': post_data.get('num_comments', 0),
                                    'created_utc': post_data.get('created_utc', 0),
                                    'subreddit': post_data.get('subreddit', ''),
                                    'url': f"https://reddit.com{post_data.get('permalink', '')}" if post_data.get('permalink') else '',
                                    'selftext': post_data.get('selftext', '')[:200] + '...' if len(post_data.get('selftext', '')) > 200 else post_data.get('selftext', '')
                                })
                    except:
                        continue
                
                # Sort by score and take top posts
                all_posts.sort(key=lambda x: x['score'], reverse=True)
                reddit_data[ticker] = all_posts[:5]
                
            except Exception as e:
                reddit_data[ticker] = [{'error': f'Error fetching Reddit data for {ticker}: {str(e)}'}]
        
        return reddit_data
    
    # Could add tests only here but was super important for me to test if all APIs are reachable
    def test_api_connections(self) -> Dict[str, bool]:
        """Test all API connections"""
        results = {}
        
        # Finnhub
        try:
            url = f"{self.finnhub_base}/quote"
            params = {'symbol': 'AAPL', 'token': self.finnhub_key}
            response = requests.get(url, params=params, timeout=5)
            results['finnhub'] = response.status_code == 200
        except:
            results['finnhub'] = False
        
        # NewsAPI
        try:
            url = f"{self.news_api_base}/everything"
            params = {'q': 'stocks', 'apiKey': self.news_api_key, 'pageSize': 1}
            response = requests.get(url, params=params, timeout=5)
            results['newsapi'] = response.status_code == 200
        except:
            results['newsapi'] = False
        
        # Reddit
        try:
            url = f"{self.reddit_base}/r/investing/hot.json"
            headers = {'User-Agent': 'AIMarketCompanion/1.0'}
            response = requests.get(url, headers=headers, params={'limit': 1}, timeout=5)
            results['reddit'] = response.status_code == 200
        except:
            results['reddit'] = False
        
        return results
