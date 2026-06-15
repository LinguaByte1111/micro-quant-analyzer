# micro-quant-analyzer

A quantitative research system for analyzing Indian equity markets using market microstructure, statistical modeling, and algorithmic strategy backtesting. Built to simulate core components of a high-frequency trading research pipeline.

Live Demo: [micro-quant-analyzer.vercel.app](#) &nbsp;|&nbsp; Backend API: [micro-quant-analyzer.onrender.com](#)

---

## What This Does

Most trading research tools either show price charts or run simple moving average strategies. This system goes deeper — it models how markets actually work at the microstructure level, tests whether statistical patterns are exploitable, and simulates how an exchange matches orders in real time.

It covers three things AlphaGrep and similar quant firms actually care about:

- **Exchange simulation** — how orders get matched, how the order book clears
- **Market microstructure** — bid-ask spread, VWAP, order flow imbalance, Kyle's Lambda
- **Quantitative strategy research** — mean reversion with statistical validation via Ornstein-Uhlenbeck, ADF, ACF, and Kalman filtering

---

## Architecture

```
micro-quant-analyzer/
│
├── cpp/
│   ├── matching_engine.cpp        # C++ order matching engine (production)
│   └── matching_engine_sim.py     # Python simulation for demonstration
│
├── python/
│   ├── data/
│   │   └── fetch_data.py          # Live NSE data via yfinance
│   ├── microstructure/
│   │   └── analysis.py            # Spread, VWAP, TWAP, OFI, Kyle's Lambda
│   ├── strategy/
│   │   └── backtester.py          # Z-score mean reversion backtester
│   ├── math_models/
│   │   └── models.py              # OU process, ADF, ACF, Kalman filter
│   └── reports/
│       └── charts.py              # Chart generation (PnL, signals, dashboards)
│
├── backend/
│   └── main.py                    # FastAPI REST API
│
├── frontend/
│   └── src/
│       └── App.js                 # React dashboard
│
└── requirements.txt
```

---

## Core Components

### 1. Exchange Simulator (`cpp/matching_engine.cpp`)

Implements a price-time priority order matching engine with:
- Max-heap for bids, min-heap for asks
- Continuous order matching on submission
- Partial fill handling
- Trade log output

The C++ engine uses priority queues for O(log n) order insertion and matching. The Python simulation (`matching_engine_sim.py`) replicates the same logic using `heapq` for demonstration.

### 2. Market Microstructure (`python/microstructure/analysis.py`)

| Metric | Description |
|---|---|
| Bid-Ask Spread | High-Low approximation of market impact cost |
| Spread % | Spread as fraction of mid-price |
| VWAP | Volume-weighted average price (cumulative) |
| TWAP | Time-weighted average price (expanding mean) |
| Order Flow Imbalance | Signed volume — buying vs selling pressure |
| Kyle's Lambda | Price impact per unit of signed order flow |
| Rolling Volatility | 20-day annualized standard deviation of returns |

### 3. Quantitative Math Models (`python/math_models/models.py`)

**Ornstein-Uhlenbeck Process**

Tests whether a price series is statistically mean-reverting by fitting:

```
dX = θ(μ - X)dt + σdW
```

A positive θ confirms mean reversion exists. Half-life is computed as `ln(2) / θ`, giving the expected number of days for price to revert halfway to its long-term mean.

**Augmented Dickey-Fuller Test**

Tests stationarity of the price series. A p-value below 0.05 indicates the series is stationary — a necessary condition for mean reversion strategies.

**Autocorrelation Function (ACF)**

Measures whether past returns predict future returns at specific lags. Significant ACF values indicate exploitable patterns in the return series.

**Kalman Filter**

Estimates the true underlying price by filtering noise via a recursive Bayesian update. Used as a dynamic baseline for detecting price deviations.

### 4. Mean Reversion Backtester (`python/strategy/backtester.py`)

Strategy logic:
- Compute rolling 20-day z-score of close price
- Enter long when z-score < -1.5 (price too far below mean)
- Enter short when z-score > +1.5 (price too far above mean)
- Exit when z-score crosses zero

Performance metrics reported:
- Total return vs buy-and-hold
- Annualized return
- Sharpe ratio
- Maximum drawdown
- Win rate
- Trade count

---

## Stocks Covered

All five are large-cap NSE-listed equities with high liquidity:

| Ticker | Company |
|---|---|
| RELIANCE.NS | Reliance Industries |
| TCS.NS | Tata Consultancy Services |
| INFY.NS | Infosys |
| HDFCBANK.NS | HDFC Bank |
| ICICIBANK.NS | ICICI Bank |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data | yfinance (live NSE data) |
| Analysis | Python, pandas, numpy, scipy, statsmodels |
| Matching Engine | C++ (priority queue), Python simulation |
| Backend | FastAPI |
| Frontend | React |
| Deployment | Vercel (frontend), Render (backend) |

---

## Running Locally

**1. Clone and install:**
```bash
git clone https://github.com/YOURUSERNAME/micro-quant-analyzer.git
cd micro-quant-analyzer
pip install -r requirements.txt
```

**2. Start backend:**
```bash
uvicorn backend.main:app --reload
```

**3. Start frontend:**
```bash
cd frontend
npm install
npm start
```

**4. Open:** `http://localhost:3000`

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/stocks` | List of available tickers |
| `GET /api/analyze/{ticker}` | Full analysis — metrics, microstructure, math models, charts |
| `GET /api/orderbook` | Run order matching simulation |

---

## Sample Output

**RELIANCE.NS — 6 month analysis**

```
Avg Spread:           ₹26.89
Spread %:             1.93%
VWAP:                 ₹1,449.31
Volatility:           0.2441 (annualized)
OFI Direction:        Bearish

OU Theta:             0.0384
Half-Life:            18.05 days  ✓ Mean reversion exists
ADF p-value:          0.5157      ✗ Non-stationary (use returns)

Sharpe Ratio:         0.1691
Max Drawdown:         -6.92%
Win Rate:             45.65%
```

---

## Design Decisions

**Why mean reversion and not momentum?**
Indian large-cap equities show short-term mean reversion characteristics at the daily frequency, as confirmed by the OU half-life estimates (15-20 days). Momentum strategies require higher frequency data which is not available freely.

**Why z-score entry at 1.5 and not 2.0?**
At 2.0, the strategy generates too few trades on 6 months of daily data to be statistically meaningful. 1.5 provides a balance between signal frequency and statistical significance.

**Why Python simulation instead of compiled C++?**
The C++ matching engine (`cpp/matching_engine.cpp`) is the production-grade implementation. The Python simulation exists for portability and demonstration without requiring a compiler in the deployment environment.

---

## What's Next

- Pairs trading using cointegration (HDFCBANK vs ICICIBANK)
- Tick-level data integration via Zerodha Kite API
- Portfolio-level backtesting across all five stocks simultaneously
- Transaction cost modeling (slippage, brokerage)
- Real-time WebSocket order book updates

---

## Author

Built as a quantitative research project focused on Indian equity market microstructure and algorithmic strategy development.