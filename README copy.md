# AI Market Companion

A Streamlit-based web application that helps you track your portfolio stocks with real-time data, breaking news, Reddit sentiment, and AI-powered insights using GPT-5.

## Features

- 📊 Upload CSV portfolio or add tickers manually
- 💹 Real-time stock prices with price changes
- 📰 Breaking financial news headlines
- 🔴 Reddit sentiment analysis and social mentions
- 🤖 AI-powered market analysis and insights
- 💬 Interactive chat to ask questions about your portfolio
- 🔄 Auto-refresh every 60 seconds or manual refresh

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- API Keys (free to obtain):
  - OpenAI API Key - https://platform.openai.com/api-keys
  - Finnhub API Key - https://finnhub.io/register
  - NewsAPI Key - https://newsapi.org/register

## Installation Steps

### 1. Clone or Download the Project

Download all project files to your local machine.

### 2. Install Python Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install streamlit openai pandas requests
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit the `.env` file and add your API keys:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
FINNHUB_API_KEY=your_actual_finnhub_api_key_here
NEWS_API_KEY=your_actual_newsapi_key_here
```

**Note:** Make sure to replace the placeholder values with your actual API keys.

### 4. Install python-dotenv (for loading .env file)

```bash
pip install python-dotenv
```

### 5. Update the Code to Load .env File

Add this to the top of `data_fetcher.py` and `ai_assistant.py`:

```python
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file
```

## Running the Application

### Option 1: Using Terminal/Command Prompt

Navigate to the project directory and run:

```bash
streamlit run app.py --server.port 5000
```

Or use the default port:

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501` (or port 5000 if specified).

### Option 2: Using VS Code

1. Open the project folder in VS Code
2. Open the integrated terminal (View → Terminal or `` Ctrl+` ``)
3. Run the command:
   ```bash
   streamlit run app.py
   ```
4. Click on the local URL that appears in the terminal

### Option 3: VS Code Run Configuration

Create a `.vscode/launch.json` file:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Streamlit: Run app.py",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": [
                "run",
                "app.py",
                "--server.port",
                "5000"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

Then press F5 or click Run → Start Debugging.

## How to Use the App

1. **Upload Portfolio CSV**:
   - Create a CSV file with a "Ticker" column
   - Example:
     ```
     Ticker
     AAPL
     MSFT
     TSLA
     GOOGL
     ```
   - Upload via the sidebar

2. **Or Add Tickers Manually**:
   - Enter comma-separated ticker symbols in the sidebar
   - Click "Add Tickers"

3. **View AI Analysis**:
   - See what's happening in the market
   - Get actionable insights
   - View market sentiment (bullish/bearish/mixed)

4. **Refresh Data**:
   - Click "🔄 Refresh Now" button
   - Or wait for auto-refresh (every 60 seconds)

5. **Ask Questions**:
   - Use the chat interface at the bottom
   - Ask follow-up questions about your portfolio

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── data_fetcher.py     # Handles API calls for stocks, news, Reddit
├── ai_assistant.py     # OpenAI GPT integration for AI analysis
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .env               # Your actual API keys (create this)
└── .streamlit/
    └── config.toml    # Streamlit server configuration
```

## Troubleshooting

### Import Error with dotenv

If you get an error about dotenv, install it:
```bash
pip install python-dotenv
```

And add these lines to the top of `data_fetcher.py` and `ai_assistant.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### API Key Errors

- Make sure your `.env` file is in the project root directory
- Ensure there are no quotes around your API keys in the `.env` file
- Check that your API keys are valid and active

### Port Already in Use

If port 5000 is already in use, try:
```bash
streamlit run app.py --server.port 8501
```

### Missing Dependencies

If you encounter missing packages:
```bash
pip install streamlit openai pandas requests python-dotenv
```

## API Rate Limits

- **Finnhub Free Tier**: 60 API calls/minute
- **NewsAPI Free Tier**: 100 requests/day
- **Reddit**: No API key needed (using public JSON feeds)

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them
- The `.gitignore` file should include `.env`

## License

This project is provided as-is for educational and personal use.
