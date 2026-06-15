import { useState, useEffect } from "react";
import axios from "axios";

const API = "https://micro-quant-analyzer-api.onrender.com";

const STOCKS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"];

const MetricCard = ({ label, value, sub }) => (
  <div style={{
    background: "#0f1117",
    border: "1px solid #1e2433",
    borderRadius: 8,
    padding: "16px 20px",
  }}>
    <div style={{ color: "#6b7280", fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 6 }}>{label}</div>
    <div style={{ color: "#f0f4ff", fontSize: 22, fontWeight: 700, fontFamily: "monospace" }}>{value}</div>
    {sub && <div style={{ color: "#4b5563", fontSize: 11, marginTop: 4 }}>{sub}</div>}
  </div>
);

const Tag = ({ value, positive }) => (
  <span style={{
    background: positive ? "#052e16" : "#2d0a0a",
    color: positive ? "#4ade80" : "#f87171",
    borderRadius: 4,
    padding: "2px 8px",
    fontSize: 12,
    fontFamily: "monospace",
    fontWeight: 600
  }}>{value}</span>
);

export default function App() {
  const [ticker, setTicker] = useState("RELIANCE");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [orderbook, setOrderbook] = useState(null);
  const [activeTab, setActiveTab] = useState("dashboard");

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`${API}/api/analyze/${ticker}`);
      if (res.data.error) throw new Error(res.data.error);
      setData(res.data);
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  const fetchOrderbook = async () => {
    try {
      const res = await axios.get(`${API}/api/orderbook`);
      setOrderbook(res.data);
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => { fetchOrderbook(); }, []);

  const m = data?.metrics;
  const ms = data?.microstructure;
  const math = data?.math_models;

  return (
    <div style={{ background: "#080b12", minHeight: "100vh", color: "#f0f4ff", fontFamily: "'Inter', sans-serif" }}>

      {/* Header */}
      <div style={{ borderBottom: "1px solid #1e2433", padding: "16px 32px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <span style={{ fontFamily: "monospace", fontWeight: 800, fontSize: 18, color: "#60a5fa", letterSpacing: 2 }}>MICRO</span>
          <span style={{ fontFamily: "monospace", fontWeight: 800, fontSize: 18, color: "#f0f4ff", letterSpacing: 2 }}>QUANT</span>
          <span style={{ fontFamily: "monospace", fontWeight: 400, fontSize: 18, color: "#6b7280", letterSpacing: 2 }}>.ANALYZER</span>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <span style={{ color: "#4b5563", fontSize: 12, marginRight: 8 }}>NSE India</span>
          {STOCKS.map(s => (
            <button key={s} onClick={() => setTicker(s)} style={{
              background: ticker === s ? "#1d4ed8" : "#0f1117",
              border: `1px solid ${ticker === s ? "#3b82f6" : "#1e2433"}`,
              color: ticker === s ? "#fff" : "#6b7280",
              borderRadius: 6, padding: "6px 14px", fontSize: 12,
              fontFamily: "monospace", cursor: "pointer", fontWeight: 600
            }}>{s}</button>
          ))}
          <button onClick={fetchData} disabled={loading} style={{
            background: loading ? "#1e3a5f" : "#1d4ed8",
            border: "none", color: "#fff", borderRadius: 6,
            padding: "8px 20px", fontSize: 13, cursor: loading ? "not-allowed" : "pointer",
            fontWeight: 700, marginLeft: 8, letterSpacing: 0.5
          }}>
            {loading ? "Fetching..." : "↻ Refresh"}
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ borderBottom: "1px solid #1e2433", padding: "0 32px", display: "flex", gap: 0 }}>
        {["dashboard", "charts", "orderbook"].map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)} style={{
            background: "none", border: "none",
            borderBottom: activeTab === tab ? "2px solid #3b82f6" : "2px solid transparent",
            color: activeTab === tab ? "#60a5fa" : "#4b5563",
            padding: "14px 20px", fontSize: 13, cursor: "pointer",
            fontWeight: activeTab === tab ? 700 : 400,
            textTransform: "capitalize", letterSpacing: 0.5
          }}>{tab}</button>
        ))}
      </div>

      <div style={{ padding: "28px 32px" }}>

        {error && (
          <div style={{ background: "#2d0a0a", border: "1px solid #7f1d1d", borderRadius: 8, padding: 16, marginBottom: 20, color: "#f87171", fontSize: 13 }}>
            {error}
          </div>
        )}

        {!data && !loading && activeTab === "dashboard" && (
          <div style={{ textAlign: "center", padding: "80px 0", color: "#4b5563" }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>📈</div>
            <div style={{ fontSize: 16, marginBottom: 8 }}>Select a stock and click Refresh</div>
            <div style={{ fontSize: 13 }}>Fetches live NSE data and runs full microstructure + quant analysis</div>
          </div>
        )}

        {loading && (
          <div style={{ textAlign: "center", padding: "80px 0", color: "#4b5563" }}>
            <div style={{ fontSize: 16 }}>Running analysis on {ticker}.NS...</div>
            <div style={{ fontSize: 13, marginTop: 8 }}>Fetching live data → Microstructure → Backtest → Math Models</div>
          </div>
        )}

        {/* Dashboard Tab */}
        {activeTab === "dashboard" && data && !loading && (
          <div>
            <div style={{ marginBottom: 24, display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ fontFamily: "monospace", fontSize: 22, fontWeight: 800 }}>{data.ticker}</span>
              <Tag value={ms?.ofi_direction} positive={ms?.ofi_direction === "Bullish"} />
              <Tag value={math?.ou_mean_reversion ? "Price Returns to Mean ✓" : "No Return Pattern"} positive={math?.ou_mean_reversion} />
              <Tag value={math?.adf_stationary ? "Stable Pattern ✓" : "Unstable Pattern"} positive={math?.adf_stationary} />
            </div>

            {/* Backtest Metrics */}
            <div style={{ marginBottom: 8, color: "#6b7280", fontSize: 11, letterSpacing: 1, textTransform: "uppercase" }}>Strategy Performance (Backtest Results)</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 24 }}>
              <MetricCard label="Strategy Profit/Loss (Total Return)" value={`${m?.total_return}%`} sub="compared to just holding the stock" />
              <MetricCard label="Risk-Adjusted Score (Sharpe Ratio)" value={m?.sharpe} sub="higher = better strategy" />
              <MetricCard label="Worst Loss Period (Max Drawdown)" value={`${m?.max_drawdown}%`} sub="biggest loss from peak" />
              <MetricCard label="Profitable Trades (Win Rate)" value={`${m?.win_rate}%`} sub={`out of ${m?.trade_count} total trades`} />
            </div>

            {/* Microstructure Metrics */}
            <div style={{ marginBottom: 8, color: "#6b7280", fontSize: 11, letterSpacing: 1, textTransform: "uppercase" }}>Market Activity (Microstructure)</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 24 }}>
              <MetricCard label="Buy-Sell Price Gap (Spread)" value={`₹${ms?.avg_spread}`} sub="difference between buy and sell price" />
              <MetricCard label="Gap as % of Price (Spread %)" value={`${ms?.avg_spread_pct}%`} sub="smaller = more efficient market" />
              <MetricCard label="Volume-Weighted Price (VWAP)" value={`₹${ms?.avg_vwap}`} sub="avg price weighted by trade volume" />
              <MetricCard label="Price Swing (Volatility)" value={ms?.avg_volatility} sub="how much price swings yearly" />
            </div>

            {/* Math Models */}
            <div style={{ marginBottom: 8, color: "#6b7280", fontSize: 11, letterSpacing: 1, textTransform: "uppercase" }}>Statistical Models (Quant Analysis)</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
              <MetricCard label="Reversion Speed (OU Theta)" value={math?.ou_theta} sub="how fast price snaps back to average" />
              <MetricCard label="Days to Normalize (Half-Life)" value={`${math?.ou_halflife} days`} sub="time for price to return halfway to mean" />
              <MetricCard label="Trend Stability Score (ADF p-value)" value={math?.adf_pvalue} sub="below 0.05 = stable tradeable pattern" />
            </div>
          </div>
        )}

        {/* Charts Tab */}
        {activeTab === "charts" && data && !loading && (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(500px, 1fr))", gap: 20 }}>
              {[
                { key: "pnl", label: "Strategy Profit vs Just Holding Stock (PnL Chart)" },
                { key: "signals", label: "When Strategy Buys and Sells (Entry/Exit Signals)" },
                { key: "microstructure", label: "Market Activity Dashboard (Microstructure)" },
                { key: "math_models", label: "Statistical Model Results (ACF, Kalman, Sharpe)" }
              ].map(({ key, label }) => (
                <div key={key} style={{ background: "#0f1117", border: "1px solid #1e2433", borderRadius: 8, overflow: "hidden" }}>
                  <div style={{ padding: "12px 16px", borderBottom: "1px solid #1e2433", fontSize: 12, color: "#6b7280", letterSpacing: 0.5 }}>{label}</div>
                  <img
                    src={`data:image/png;base64,${data.charts[key]}`}
                    alt={label}
                    style={{ width: "100%", height: "auto", display: "block", cursor: "zoom-in" }}
                    onClick={(e) => {
                      if (e.target.style.position === "fixed") {
                        e.target.style = "width:100%;height:auto;display:block;cursor:zoom-in";
                      } else {
                        Object.assign(e.target.style, {
                          position: "fixed", top: "0", left: "0",
                          width: "100vw", height: "100vh",
                          objectFit: "contain", background: "#080b12",
                          zIndex: "1000", cursor: "zoom-out"
                        });
                      }
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {!data && activeTab === "charts" && (
          <div style={{ textAlign: "center", padding: "80px 0", color: "#4b5563" }}>
            <div style={{ fontSize: 16 }}>Select a stock and click Refresh to generate charts</div>
          </div>
        )}

        {/* Orderbook Tab */}
        {activeTab === "orderbook" && (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
              <div>
                <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>Live Order Matching Simulator</div>
                <div style={{ fontSize: 12, color: "#4b5563" }}>Simulates how a real stock exchange matches buy and sell orders in real time</div>
              </div>
              <button onClick={fetchOrderbook} style={{
                background: "#0f1117", border: "1px solid #1e2433",
                color: "#60a5fa", borderRadius: 6, padding: "8px 16px",
                fontSize: 12, cursor: "pointer", fontFamily: "monospace"
              }}>↻ Re-run Simulator</button>
            </div>

            {orderbook && (
              <div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 24 }}>
                  <MetricCard label="Orders Matched" value={orderbook.trade_count} sub="total buy-sell pairs executed" />
                  <MetricCard label="Waiting Buyers (Pending Bids)" value={orderbook.pending_bids} sub="buy orders not yet matched" />
                  <MetricCard label="Waiting Sellers (Pending Asks)" value={orderbook.pending_asks} sub="sell orders not yet matched" />
                </div>

                <div style={{ background: "#0f1117", border: "1px solid #1e2433", borderRadius: 8, overflow: "hidden", marginBottom: 20 }}>
                  <div style={{ padding: "12px 16px", borderBottom: "1px solid #1e2433", fontSize: 12, color: "#6b7280" }}>MATCHED TRADES (EXECUTED ORDERS)</div>
                  <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                      <tr style={{ borderBottom: "1px solid #1e2433" }}>
                        {["Trade #", "Executed Price", "Quantity", "Buyer ID", "Seller ID"].map(h => (
                          <th key={h} style={{ padding: "10px 16px", textAlign: "left", fontSize: 11, color: "#4b5563", letterSpacing: 1, textTransform: "uppercase" }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {orderbook.trades.map((t, i) => (
                        <tr key={i} style={{ borderBottom: "1px solid #0f1117" }}>
                          <td style={{ padding: "10px 16px", fontFamily: "monospace", color: "#6b7280", fontSize: 13 }}>#{i + 1}</td>
                          <td style={{ padding: "10px 16px", fontFamily: "monospace", color: "#4ade80", fontSize: 13 }}>₹{t.price.toFixed(2)}</td>
                          <td style={{ padding: "10px 16px", fontFamily: "monospace", color: "#f0f4ff", fontSize: 13 }}>{t.quantity}</td>
                          <td style={{ padding: "10px 16px", fontFamily: "monospace", color: "#60a5fa", fontSize: 13 }}>#{t.buy_id}</td>
                          <td style={{ padding: "10px 16px", fontFamily: "monospace", color: "#f87171", fontSize: 13 }}>#{t.sell_id}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div style={{ background: "#0f1117", border: "1px solid #1e2433", borderRadius: 8, overflow: "hidden" }}>
                  <div style={{ padding: "12px 16px", borderBottom: "1px solid #1e2433", fontSize: 12, color: "#6b7280" }}>ENGINE LOG (MATCHING ENGINE OUTPUT)</div>
                  <pre style={{ padding: 16, margin: 0, fontSize: 12, color: "#4b5563", fontFamily: "monospace", overflowX: "auto", lineHeight: 1.8 }}>
                    {orderbook.log}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
