# micro-quant-analyzer

> **Data Disclaimer:** All market data used in this project is fetched from publicly available sources (yfinance) strictly for educational and research purposes. No real trades are executed. No data is stored or shared.

A quantitative trading research system built on Indian equity markets (NSE). Covers three core areas of high-frequency trading research: exchange simulation, market microstructure analysis, and algorithmic strategy backtesting.

Live Demo: [micro-quant-analyzer.vercel.app](#)

---

## What It Does

**1. Exchange Simulator**
Simulates how a real stock exchange matches buy and sell orders. Built in C++ using priority queues. Python version included for demonstration.

**2. Market Microstructure Analysis**
Analyzes how prices behave at a granular level — bid-ask spread, VWAP, order flow imbalance, and price impact (Kyle's Lambda) on live NSE data.

**3. Mean Reversion Strategy + Backtester**
Tests whether stock prices statistically return to their mean using Ornstein-Uhlenbeck process, ADF stationarity test, ACF, and Kalman filter. Runs a z-score based trading strategy and reports Sharpe ratio, drawdown, and win rate.

---

## Stocks Covered

RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK — all live from NSE via yfinance.

---

## Tech Stack

- **Analysis:** Python, pandas, numpy, scipy, statsmodels
- **Matching Engine:** C++, Python simulation
- **Backend:** FastAPI
- **Frontend:** React
- **Deployment:** Vercel + Render

---

## Run Locally

```bash
git clone https://github.com/YOURUSERNAME/micro-quant-analyzer.git
cd micro-quant-analyzer
pip install -r requirements.txt

# Terminal 1 — backend
uvicorn backend.main:app --reload

# Terminal 2 — frontend
cd frontend && npm install && npm start
```

---

## API

| Endpoint | What It Does |
|---|---|
| `GET /api/analyze/{ticker}` | Full analysis — metrics, charts, math models |
| `GET /api/orderbook` | Run order matching simulation |
| `GET /api/stocks` | List available stocks |

---

## Project Structure

```
micro-quant-analyzer/
├── cpp/                  # C++ matching engine
├── python/
│   ├── data/             # Live NSE data fetcher
│   ├── microstructure/   # Spread, VWAP, OFI, Kyle's Lambda
│   ├── strategy/         # Mean reversion backtester
│   ├── math_models/      # OU, ADF, ACF, Kalman filter
│   └── reports/          # Chart generation
├── backend/              # FastAPI server
└── frontend/             # React dashboard
```
