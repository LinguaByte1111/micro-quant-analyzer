import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf, adfuller
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
import warnings
warnings.filterwarnings('ignore')


def test_mean_reversion_ou(df, ticker):
    """
    Ornstein-Uhlenbeck Process
    Tests if price series is statistically mean-reverting
    dX = theta(mu - X)dt + sigma*dW
    theta > 0 means mean reversion exists
    """
    print(f"\n--- Ornstein-Uhlenbeck Test — {ticker} ---")
    
    prices = df['Close'].values
    X = prices[:-1]
    Y = prices[1:]
    
    # OLS regression: Y = a + b*X
    X_const = add_constant(X)
    model = OLS(Y, X_const).fit()
    
    a = model.params[0]  # intercept
    b = model.params[1]  # slope
    
    # OU parameters
    theta = -np.log(b)                    # mean reversion speed
    mu = a / (1 - b)                      # long-term mean
    sigma = np.std(model.resid)           # volatility
    half_life = np.log(2) / theta         # half-life of mean reversion
    
    print(f"  Theta (reversion speed): {theta:.4f}")
    print(f"  Mu (long-term mean):     {mu:.2f}")
    print(f"  Sigma (volatility):      {sigma:.4f}")
    print(f"  Half-life:               {half_life:.2f} days")
    
    if theta > 0:
        print(f"  ✓ Mean reversion EXISTS — half-life {half_life:.1f} days")
    else:
        print(f"  ✗ No mean reversion detected")
    
    return {"theta": theta, "mu": mu, "sigma": sigma, "half_life": half_life}


def test_stationarity_adf(df, ticker):
    """
    Augmented Dickey-Fuller Test
    Tests if price series is stationary (required for mean reversion)
    p-value < 0.05 = stationary = mean reverting
    """
    print(f"\n--- ADF Stationarity Test — {ticker} ---")
    
    prices = df['Close'].dropna()
    result = adfuller(prices)
    
    adf_stat = result[0]
    p_value = result[1]
    critical_values = result[4]
    
    print(f"  ADF Statistic:  {adf_stat:.4f}")
    print(f"  p-value:        {p_value:.4f}")
    print(f"  Critical (1%):  {critical_values['1%']:.4f}")
    print(f"  Critical (5%):  {critical_values['5%']:.4f}")
    
    if p_value < 0.05:
        print(f"  ✓ Series is STATIONARY — mean reversion tradeable")
    else:
        print(f"  ✗ Series is NON-STATIONARY — use returns instead")
    
    return {"adf_stat": adf_stat, "p_value": p_value}


def calculate_autocorrelation(df, ticker, nlags=20):
    """
    Autocorrelation Function (ACF)
    Measures if past returns predict future returns
    Significant ACF = exploitable pattern exists
    """
    print(f"\n--- Autocorrelation Analysis — {ticker} ---")
    
    returns = df['Close'].pct_change().dropna()
    acf_values = acf(returns, nlags=nlags)
    
    # Significance threshold
    confidence = 1.96 / np.sqrt(len(returns))
    significant_lags = [i for i, v in enumerate(acf_values) if abs(v) > confidence and i > 0]
    
    print(f"  Confidence interval: ±{confidence:.4f}")
    print(f"  Significant lags:    {significant_lags[:5]}")
    
    if significant_lags:
        print(f"  ✓ Price patterns EXIST at lags {significant_lags[:3]}")
    else:
        print(f"  ✗ No significant autocorrelation found")
    
    return {"acf_values": acf_values, "significant_lags": significant_lags}


def kalman_filter(df, ticker):
    """
    Kalman Filter — dynamic price estimation
    Smooths noisy price signal to find true underlying value
    Used in pairs trading for dynamic hedge ratio
    """
    print(f"\n--- Kalman Filter — {ticker} ---")
    
    prices = df['Close'].values
    n = len(prices)
    
    # Initialize
    x_est = np.zeros(n)       # estimated price
    p_est = np.zeros(n)       # estimation error
    
    # Kalman parameters
    Q = 1e-5    # process noise
    R = 0.01    # measurement noise
    
    x_est[0] = prices[0]
    p_est[0] = 1.0
    
    for t in range(1, n):
        # Predict
        x_pred = x_est[t-1]
        p_pred = p_est[t-1] + Q
        
        # Update (Kalman Gain)
        K = p_pred / (p_pred + R)
        x_est[t] = x_pred + K * (prices[t] - x_pred)
        p_est[t] = (1 - K) * p_pred
    
    df['Kalman_Estimate'] = x_est
    df['Kalman_Deviation'] = df['Close'] - df['Kalman_Estimate']
    
    avg_deviation = df['Kalman_Deviation'].abs().mean()
    print(f"  Avg price deviation from Kalman estimate: {avg_deviation:.2f}")
    print(f"  ✓ Kalman filter applied successfully")
    
    return df


def rolling_sharpe(returns, window=30):
    """Rolling Sharpe Ratio — risk adjusted returns over time"""
    roll_mean = returns.rolling(window).mean()
    roll_std = returns.rolling(window).std()
    sharpe = (roll_mean / roll_std) * np.sqrt(252)
    return sharpe


def run_all_models(df, ticker):
    ou_results = test_mean_reversion_ou(df, ticker)
    adf_results = test_stationarity_adf(df, ticker)
    acf_results = calculate_autocorrelation(df, ticker)
    df = kalman_filter(df, ticker)
    return df, ou_results, adf_results, acf_results


if __name__ == "__main__":
    df = pd.read_csv("python/data/raw/RELIANCE_NS.csv", index_col=0, parse_dates=True)
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(inplace=True)
    run_all_models(df, "RELIANCE.NS")