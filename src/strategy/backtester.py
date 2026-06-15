import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def calculate_zscore(series, window=20):
    """
    Z-Score: how far price is from its rolling mean
    in terms of standard deviations
    Z = (X - mean) / std
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std


def generate_signals(df, z_entry=1.5, z_exit=0.0):
    """
    Mean Reversion Signal Logic:
    - Z < -1.5 → BUY  (price too far below mean)
    - Z >  1.5 → SELL (price too far above mean)
    - Z crosses 0 → EXIT position
    """
    df['ZScore'] = calculate_zscore(df['Close'])
    df['Signal'] = 0

    position = 0
    signals = []

    for i in range(len(df)):
        z = df['ZScore'].iloc[i]

        if pd.isna(z):
            signals.append(0)
            continue

        if position == 0:
            if z < -z_entry:
                position = 1    # BUY
            elif z > z_entry:
                position = -1   # SELL SHORT
        elif position == 1:
            if z >= z_exit:
                position = 0    # EXIT LONG
        elif position == -1:
            if z <= z_exit:
                position = 0    # EXIT SHORT

        signals.append(position)

    df['Signal'] = signals
    return df


def run_backtest(df, ticker, initial_capital=1_000_000):
    """
    Backtest mean reversion strategy
    Tracks PnL, drawdown, Sharpe ratio
    """
    print(f"\n--- Backtesting Mean Reversion — {ticker} ---")

    df = generate_signals(df)

    # Daily returns
    df['Market_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Signal'].shift(1) * df['Market_Return']

    # Cumulative returns
    df['Cumulative_Market'] = (1 + df['Market_Return']).cumprod()
    df['Cumulative_Strategy'] = (1 + df['Strategy_Return']).cumprod()

    # Portfolio value
    df['Portfolio_Value'] = initial_capital * df['Cumulative_Strategy']

    # Performance metrics
    total_return = df['Cumulative_Strategy'].iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(df)) - 1

    # Sharpe Ratio
    sharpe = (df['Strategy_Return'].mean() / df['Strategy_Return'].std()) * np.sqrt(252)

    # Max Drawdown
    rolling_max = df['Portfolio_Value'].cummax()
    drawdown = (df['Portfolio_Value'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # Win rate
    trades = df[df['Signal'] != df['Signal'].shift(1)]
    winning_trades = df[df['Strategy_Return'] > 0]
    win_rate = len(winning_trades) / len(df[df['Strategy_Return'] != 0]) * 100 if len(df[df['Strategy_Return'] != 0]) > 0 else 0

    # Trade count
    trade_count = (df['Signal'].diff() != 0).sum()

    print(f"  Initial Capital:   ₹{initial_capital:,.0f}")
    print(f"  Final Value:       ₹{df['Portfolio_Value'].iloc[-1]:,.0f}")
    print(f"  Total Return:      {total_return*100:.2f}%")
    print(f"  Annual Return:     {annual_return*100:.2f}%")
    print(f"  Sharpe Ratio:      {sharpe:.4f}")
    print(f"  Max Drawdown:      {max_drawdown*100:.2f}%")
    print(f"  Win Rate:          {win_rate:.2f}%")
    print(f"  Total Trades:      {trade_count}")

    return df, {
        "ticker": ticker,
        "total_return": total_return,
        "annual_return": annual_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "trade_count": trade_count,
        "final_value": df['Portfolio_Value'].iloc[-1]
    }


if __name__ == "__main__":
    df = pd.read_csv("python/data/raw/RELIANCE_NS.csv", index_col=0, parse_dates=True)
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(inplace=True)
    run_backtest(df, "RELIANCE.NS")