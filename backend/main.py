import os
import sys
import base64
import io
import matplotlib
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUANT_DIR = os.path.join(BASE_DIR, 'quant')
CPP_DIR = os.path.join(BASE_DIR, 'cpp')

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, QUANT_DIR)
sys.path.insert(0, CPP_DIR)

from data.fetch_data import fetch_stock_data
from microstructure.analysis import run_microstructure
from strategy.backtester import run_backtest
from math_models.models import run_all_models
from reports.charts import generate_all_charts
from matching_engine_sim import run_simulator

app = FastAPI(title="Micro Quant Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]


def fig_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_and_process(ticker):
    df = fetch_stock_data(ticker)
    df = run_microstructure(df, ticker)
    df, metrics = run_backtest(df, ticker)
    df, ou, adf, acf = run_all_models(df, ticker)
    charts = generate_all_charts(df, ticker, metrics)
    return df, metrics, ou, adf, acf, charts


@app.get("/")
def root():
    return {"status": "Micro Quant Analyzer API running"}


@app.get("/api/analyze/{ticker}")
def analyze(ticker: str):
    ticker = ticker.upper() + ".NS"
    try:
        df, metrics, ou, adf, acf_r, charts = load_and_process(ticker)
        return {
            "ticker": ticker,
            "metrics": {
                "total_return": float(round(metrics["total_return"] * 100, 2)),
                "annual_return": float(round(metrics["annual_return"] * 100, 2)),
                "sharpe": float(round(metrics["sharpe"], 4)),
                "max_drawdown": float(round(metrics["max_drawdown"] * 100, 2)),
                "win_rate": float(round(metrics["win_rate"], 2)),
                "trade_count": int(metrics["trade_count"]),
                "final_value": float(round(metrics["final_value"], 2))
            },
            "microstructure": {
                "avg_spread": float(round(float(df['Spread'].mean()), 2)),
                "avg_spread_pct": float(round(float(df['Spread_Pct'].mean()), 4)),
                "avg_vwap": float(round(float(df['VWAP'].mean()), 2)),
                "avg_volatility": float(round(float(df['Volatility'].mean()), 4)),
                "ofi_direction": "Bullish" if float(df['OFI_Cumulative'].iloc[-1]) > 0 else "Bearish"
            },
            "math_models": {
                "ou_theta": float(round(ou["theta"], 4)),
                "ou_halflife": float(round(ou["half_life"], 2)),
                "ou_mean_reversion": bool(ou["theta"] > 0),
                "adf_pvalue": float(round(adf["p_value"], 4)),
                "adf_stationary": bool(adf["p_value"] < 0.05)
            },
            "charts": {
                "pnl": fig_to_base64(charts["pnl"]),
                "signals": fig_to_base64(charts["signals"]),
                "microstructure": fig_to_base64(charts["microstructure"]),
                "math_models": fig_to_base64(charts["math_models"])
            }
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/orderbook")
def get_orderbook():
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        book = run_simulator()
    output = f.getvalue()

    trades = [
        {
            "id": t.buy_order_id,
            "price": t.price,
            "quantity": t.quantity,
            "buy_id": t.buy_order_id,
            "sell_id": t.sell_order_id
        }
        for t in book.trades
    ]

    return {
        "trades": trades,
        "trade_count": book.trade_count,
        "pending_bids": len(book.bids),
        "pending_asks": len(book.asks),
        "log": output
    }


@app.get("/api/stocks")
def get_stocks():
    return {"stocks": [s.replace(".NS", "") for s in STOCKS]}