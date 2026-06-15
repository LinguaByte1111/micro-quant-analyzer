import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from statsmodels.tsa.stattools import acf
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs("python/reports", exist_ok=True)


def plot_pnl(df, ticker, metrics):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df['Cumulative_Strategy'], label='Strategy', color='blue', linewidth=2)
    ax.plot(df.index, df['Cumulative_Market'], label='Buy & Hold', color='gray', linewidth=1.5, linestyle='--')
    ax.set_title(f'{ticker} — Strategy PnL vs Buy & Hold', fontsize=14)
    ax.set_ylabel('Cumulative Return')
    ax.legend()
    ax.grid(True, alpha=0.3)

    textstr = f"Sharpe: {metrics['sharpe']:.2f} | Return: {metrics['total_return']*100:.2f}% | Drawdown: {metrics['max_drawdown']*100:.2f}%"
    ax.text(0.01, 0.01, textstr, transform=ax.transAxes, fontsize=9, color='black',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    path = f"python/reports/{ticker.replace('.', '_')}_pnl.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ PnL chart saved: {path}")
    return path


def plot_signals(df, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.plot(df.index, df['Close'], color='black', linewidth=1, label='Price')
    ax1.plot(df.index, df['VWAP'], color='orange', linewidth=1, linestyle='--', label='VWAP')

    buys = df[df['Signal'] == 1]
    sells = df[df['Signal'] == -1]
    ax1.scatter(buys.index, buys['Close'], marker='^', color='green', s=80, label='BUY', zorder=5)
    ax1.scatter(sells.index, sells['Close'], marker='v', color='red', s=80, label='SELL', zorder=5)
    ax1.set_title(f'{ticker} — Price with Entry/Exit Signals', fontsize=14)
    ax1.set_ylabel('Price (₹)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(df.index, df['ZScore'], color='purple', linewidth=1.5)
    ax2.axhline(1.5, color='red', linestyle='--', alpha=0.7, label='Sell threshold')
    ax2.axhline(-1.5, color='green', linestyle='--', alpha=0.7, label='Buy threshold')
    ax2.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax2.fill_between(df.index, df['ZScore'], 0, where=df['ZScore'] > 1.5, color='red', alpha=0.2)
    ax2.fill_between(df.index, df['ZScore'], 0, where=df['ZScore'] < -1.5, color='green', alpha=0.2)
    ax2.set_title('Z-Score Signal')
    ax2.set_ylabel('Z-Score')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"python/reports/{ticker.replace('.', '_')}_signals.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ Signals chart saved: {path}")
    return path


def plot_microstructure(df, ticker):
    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 2, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(df.index, df['Spread'], color='blue', linewidth=1)
    ax1.set_title('Bid-Ask Spread')
    ax1.set_ylabel('Spread (₹)')
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(df.index, df['Close'], color='black', linewidth=1, label='Close')
    ax2.plot(df.index, df['VWAP'], color='orange', linewidth=1.5, label='VWAP')
    ax2.plot(df.index, df['TWAP'], color='blue', linewidth=1.5, linestyle='--', label='TWAP')
    ax2.set_title('Price vs VWAP vs TWAP')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(df.index, df['OFI_Cumulative'], color='green', linewidth=1.5)
    ax3.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax3.fill_between(df.index, df['OFI_Cumulative'], 0,
                     where=df['OFI_Cumulative'] > 0, color='green', alpha=0.2)
    ax3.fill_between(df.index, df['OFI_Cumulative'], 0,
                     where=df['OFI_Cumulative'] < 0, color='red', alpha=0.2)
    ax3.set_title('Cumulative Order Flow Imbalance')
    ax3.set_ylabel('OFI')
    ax3.grid(True, alpha=0.3)

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(df.index, df['Volatility'], color='red', linewidth=1.5)
    ax4.set_title('Rolling Volatility (20-day annualized)')
    ax4.set_ylabel('Volatility')
    ax4.grid(True, alpha=0.3)

    fig.suptitle(f'{ticker} — Microstructure Dashboard', fontsize=16, fontweight='bold')
    plt.tight_layout()
    path = f"python/reports/{ticker.replace('.', '_')}_microstructure.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ Microstructure chart saved: {path}")
    return path


def plot_math_models(df, ticker):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    returns = df['Close'].pct_change().dropna()
    acf_vals = acf(returns, nlags=20)
    confidence = 1.96 / np.sqrt(len(returns))
    axes[0].bar(range(len(acf_vals)), acf_vals, color='steelblue', alpha=0.7)
    axes[0].axhline(confidence, color='red', linestyle='--', label=f'95% CI: ±{confidence:.3f}')
    axes[0].axhline(-confidence, color='red', linestyle='--')
    axes[0].set_title('Autocorrelation (ACF)')
    axes[0].set_xlabel('Lag')
    axes[0].set_ylabel('ACF')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    if 'Kalman_Estimate' in df.columns:
        axes[1].plot(df.index, df['Close'], color='black', linewidth=1, label='Actual Price')
        axes[1].plot(df.index, df['Kalman_Estimate'], color='blue',
                     linewidth=2, label='Kalman Estimate')
        axes[1].set_title('Kalman Filter vs Actual Price')
        axes[1].set_ylabel('Price (₹)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

    strategy_returns = df['Strategy_Return'] if 'Strategy_Return' in df.columns else returns
    roll_sharpe = (strategy_returns.rolling(30).mean() /
                   strategy_returns.rolling(30).std()) * np.sqrt(252)
    axes[2].plot(df.index, roll_sharpe, color='purple', linewidth=1.5)
    axes[2].axhline(0, color='black', linestyle='-', alpha=0.3)
    axes[2].axhline(1, color='green', linestyle='--', alpha=0.7, label='Sharpe=1')
    axes[2].fill_between(df.index, roll_sharpe, 0,
                         where=roll_sharpe > 0, color='green', alpha=0.15)
    axes[2].fill_between(df.index, roll_sharpe, 0,
                         where=roll_sharpe < 0, color='red', alpha=0.15)
    axes[2].set_title('Rolling Sharpe Ratio (30-day)')
    axes[2].set_ylabel('Sharpe')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    fig.suptitle(f'{ticker} — Math Models', fontsize=16, fontweight='bold')
    plt.tight_layout()
    path = f"python/reports/{ticker.replace('.', '_')}_math_models.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ Math models chart saved: {path}")
    return path


def generate_all_charts(df, ticker, metrics):
    print(f"\nGenerating charts for {ticker}...")
    paths = {
        "pnl": plot_pnl(df, ticker, metrics),
        "signals": plot_signals(df, ticker),
        "microstructure": plot_microstructure(df, ticker),
        "math_models": plot_math_models(df, ticker)
    }
    return paths


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from microstructure.analysis import run_microstructure
    from strategy.backtester import run_backtest
    from math_models.models import kalman_filter

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, "data", "raw", "RELIANCE_NS.csv")

    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(inplace=True)

    df = run_microstructure(df, "RELIANCE.NS")
    df, metrics = run_backtest(df, "RELIANCE.NS")
    df = kalman_filter(df, "RELIANCE.NS")
    generate_all_charts(df, "RELIANCE.NS", metrics)