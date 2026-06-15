import pandas as pd
import numpy as np

def calculate_spread(df):
    """Bid-Ask Spread approximation using High-Low"""
    df['Spread'] = df['High'] - df['Low']
    df['Spread_Pct'] = (df['Spread'] / df['Close']) * 100
    return df

def calculate_vwap(df):
    """Volume Weighted Average Price"""
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    return df

def calculate_twap(df):
    """Time Weighted Average Price"""
    df['TWAP'] = df['Close'].expanding().mean()
    return df

def calculate_order_flow_imbalance(df):
    """
    Order Flow Imbalance (OFI)
    Positive = buying pressure
    Negative = selling pressure
    """
    df['Return'] = df['Close'].pct_change()
    df['OFI'] = np.where(df['Return'] > 0, df['Volume'], -df['Volume'])
    df['OFI_Cumulative'] = df['OFI'].cumsum()
    return df

def calculate_volatility(df, window=20):
    """Rolling volatility — annualized"""
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Daily_Return'].rolling(window=window).std() * np.sqrt(252)
    return df

def calculate_price_impact(df):
    """
    Kyle's Lambda — price impact of trades
    Measures how much price moves per unit of order flow
    """
    df['Return'] = df['Close'].pct_change()
    df['Signed_Volume'] = np.where(df['Return'] > 0, df['Volume'], -df['Volume'])
    df['Kyle_Lambda'] = df['Return'].rolling(20).cov(df['Signed_Volume']) / \
                        df['Signed_Volume'].rolling(20).var()
    return df

def run_microstructure(df, ticker):
    print(f"\nRunning Microstructure Analysis — {ticker}")
    df = calculate_spread(df)
    df = calculate_vwap(df)
    df = calculate_twap(df)
    df = calculate_order_flow_imbalance(df)
    df = calculate_volatility(df)
    df = calculate_price_impact(df)

    print(f"  Avg Spread:       {df['Spread'].mean():.2f}")
    print(f"  Avg Spread %:     {df['Spread_Pct'].mean():.4f}%")
    print(f"  Avg VWAP:         {df['VWAP'].mean():.2f}")
    print(f"  Avg Volatility:   {df['Volatility'].mean():.4f}")
    print(f"  OFI Direction:    {'Bullish' if df['OFI_Cumulative'].iloc[-1] > 0 else 'Bearish'}")

    return df

if __name__ == "__main__":
    df = pd.read_csv("python/data/raw/RELIANCE_NS.csv", index_col=0, parse_dates=True)
    run_microstructure(df, "RELIANCE.NS")