# Quick Start Guide - Running Locally in VS Code

## Step-by-Step Installation

### 1. **Download the Project**
   - Download all files from this Replit project to your local machine
   - Keep the same folder structure

### 2. **Open in VS Code**
   ```bash
   cd path/to/ai-market-companion
   code .
   ```

### 3. **Install Python Dependencies**
   
   Open terminal in VS Code (Ctrl+` or View → Terminal) and run:
   
   ```bash
   pip install -r local_requirements.txt
   ```

### 4. **Set Up Your API Keys**
   
   Create a `.env` file in the project root:
   
   ```bash
   # On Windows
   copy .env.example .env
   
   # On Mac/Linux
   cp .env.example .env
   ```
   
   Edit `.env` and add your actual API keys:
   
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   FINNHUB_API_KEY=xxxxxxxxxxxxx
   NEWS_API_KEY=xxxxxxxxxxxxx
   ```

### 5. **Run the App**
   
   In VS Code terminal, run:
   
   ```bash
   streamlit run app.py
   ```
   
   The app will automatically open in your browser at `http://localhost:8501`

## Get Your Free API Keys

1. **OpenAI** → https://platform.openai.com/api-keys
   - Sign up/login
   - Create new secret key
   - Copy the key (starts with `sk-proj-...`)

2. **Finnhub** → https://finnhub.io/register
   - Sign up for free account
   - Get your API key from dashboard
   - Free tier: 60 calls/minute

3. **NewsAPI** → https://newsapi.org/register
   - Sign up for developer account
   - Get your API key
   - Free tier: 100 requests/day

## Quick Test

After running the app:

1. Create a test CSV file called `portfolio.csv`:
   ```
   Ticker
   AAPL
   MSFT
   TSLA
   ```

2. Upload it in the app sidebar
3. Click "Refresh Now" to fetch data
4. See your AI-powered market analysis!

## Common Issues

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`
- **Solution:** Run `pip install -r local_requirements.txt`

**Problem:** API keys not loading
- **Solution:** Make sure `.env` file is in the root folder, same level as `app.py`

**Problem:** Port 8501 already in use
- **Solution:** Run `streamlit run app.py --server.port 5000`

**Problem:** OpenAI API error
- **Solution:** Make sure your API key is valid and has credits

## Files You Need

Essential files:
- `app.py` - Main application
- `data_fetcher.py` - Data collection
- `ai_assistant.py` - AI analysis
- `local_requirements.txt` - Dependencies
- `.env` - Your API keys (you create this)
- `.env.example` - Template for .env
- `.streamlit/config.toml` - Server config

## Folder Structure

```
ai-market-companion/
│
├── app.py
├── data_fetcher.py
├── ai_assistant.py
├── local_requirements.txt
├── .env.example
├── .env                    ← Create this!
├── README.md
├── QUICKSTART_LOCAL.md
│
└── .streamlit/
    └── config.toml
```

## VS Code Tips

### Run with F5 (Debug Mode)

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Streamlit App",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": ["run", "app.py"],
            "console": "integratedTerminal"
        }
    ]
}
```

Then press F5 to run!

### Recommended VS Code Extensions

- Python (Microsoft)
- Pylance
- Python Indent

## Next Steps

Once running:
1. Upload your portfolio CSV or add tickers manually
2. Explore the AI-powered insights
3. Use the chat feature to ask questions
4. Click refresh to update data
5. Customize the code to your needs!

---

**Need help?** Check the full README.md for detailed documentation.
