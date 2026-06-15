# micro-quant-analyzer

> **Data Disclaimer:** All market data is fetched from publicly available sources (yfinance) strictly for educational and research purposes. No real trades are executed. No data is stored or shared.

A quantitative trading research system built on Indian equity markets (NSE). Covers three core areas of high-frequency trading research: exchange simulation, market microstructure analysis, and algorithmic strategy backtesting.

**Live Demo:** https://micro-quant-analyzer-git-main-linguabyte-s-projects.vercel.app  
**Backend API:** https://micro-quant-analyzer-api.onrender.com

---

## What It Does

**1. Exchange Simulator**  
Simulates how a real stock exchange matches buy and sell orders using a priority queue based order book. Written in C++ with a Python simulation for demonstration.

**2. Market Microstructure Analysis**  
Analyzes how prices behave at a granular level on live NSE data:
- Bid-ask spread and spread %
- VWAP and TWAP
- Order flow imbalance (OFI)
- Kyle's Lambda (price impact per unit of order flow)
- Rolling annualized volatility

**3. Mean Reversion Strategy + Backtester**  
Tests whether stock prices statistically return to their mean using:
- Ornstein-Uhlenbeck process (mean reversion speed and half-life)
- Augmented Dickey-Fuller stationarity test
- Autocorrelation function (ACF)
- Kalman filter (dynamic price estimation)

Reports Sharpe ratio, max drawdown, win rate, and annualized return.

---

## Stocks Covered

RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK — live from NSE via yfinance.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Analysis | Python, pandas, numpy, scipy, statsmodels |
| Matching Engine | C++, Python simulation |
| Backend | FastAPI |
| Frontend | React |
| Deployment | Vercel + Render |

---

## Run Locally

```bash
git clone https://github.com/LinguaByte1111/micro-quant-analyzer.git
cd micro-quant-analyzer
pip install -r requirements.txt

# Terminal 1 — backend
uvicorn backend.main:app --reload

# Terminal 2 — frontend
cd frontend && npm install && npm start
```

Open `http://localhost:3000`

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/analyze/{ticker}` | Full analysis — metrics, charts, math models |
| `GET /api/orderbook` | Run order matching simulation |
| `GET /api/stocks` | List available stocks |

---

## Project Structure

```
micro-quant-analyzer/
├── cpp/                  # C++ matching engine + Python simulation
├── quant/
│   ├── data/             # Live NSE data fetcher
│   ├── microstructure/   # Spread, VWAP, OFI, Kyle's Lambda
│   ├── strategy/         # Mean reversion backtester
│   ├── math_models/      # OU process, ADF, ACF, Kalman filter
│   └── reports/          # Chart generation
├── backend/              # FastAPI server
└── frontend/             # React dashboard
```

---

## Sample Output — RELIANCE.NS

```
Avg Spread:        ₹26.89
Spread %:          1.93%
VWAP:              ₹1,449
Volatility:        0.2441 annualized

OU Theta:          0.0384
Half-Life:         18.05 days  ✓ Mean reversion exists
ADF p-value:       0.51        ✗ Non-stationary (expected for price levels)

Sharpe Ratio:      0.1691
Max Drawdown:      -6.92%
Win Rate:          45.65%
Total Trades:      10
```
