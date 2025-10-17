## Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/phoolcode/PersonalPortfolioManagerAI.git
   ```
   > All code is currently in the main branch

2. **Open in VS Code**

3. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install all dependencies**
   ```bash
   poetry install --no-root
   ```

5. **Set up environment variables**
   - Create an empty `.env` file in the root directory
   - Copy the `.env` file keys sent via email

6. **Run the application**
   ```bash
   streamlit run app.py
   ```
   Or with a custom port:
   ```bash
   streamlit run app.py --server.port 5001
   ```
   
   The app will automatically open in your browser at `http://localhost:5001`

### Optional: Create Test Data

You can create a test CSV file called `portfolio.csv`:
```csv
Ticker
AAPL
MSFT
TSLA
```

## Issues I encountered

### Not getting a chat response.
I got this multiple times and I just relaunched it using another port. Worked 90% of the time

### Alternative Installation Method

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:** Run one of the following:
```bash
pip install -r local_requirements.txt
```

OR

```bash
pip install streamlit openai pandas requests python-dotenv
```

> Make sure your `.env` file is in the same directory as `app.py`

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

Then press **F5** to run!

## API Rate Limits

- **Finnhub Free Tier**: 60 API calls/minute
- **NewsAPI Free Tier**: 100 requests/day