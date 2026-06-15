import yfinance as yf
import pandas as pd
import os

STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

def fetch_stock_data(ticker, period="6mo", interval="1d"):
    print(f"Fetching {ticker}...")
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    
    # Fix multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df.dropna(inplace=True)
    
    # Force numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(inplace=True)
    df['Ticker'] = ticker
    return df

def fetch_all():
    os.makedirs("python/data/raw", exist_ok=True)
    all_data = {}
    for stock in STOCKS:
        df = fetch_stock_data(stock)
        df.to_csv(f"python/data/raw/{stock.replace('.', '_')}.csv")
        all_data[stock] = df
        print(f"✓ {stock} — {len(df)} rows saved")
    return all_data

if __name__ == "__main__":
    fetch_all()