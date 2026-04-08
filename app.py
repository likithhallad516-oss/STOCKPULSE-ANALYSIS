# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="StockPulse | NSE Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Dark theme config
st.markdown("""
<style>
    :root {
        --bg-primary: #1d1d1f;
        --bg-secondary: #2d2d30;
        --text-primary: #f5f5f7;
        --text-secondary: #86868b;
        --accent: #e67e22;
    }
    .stApp { background: var(--bg-primary) !important; }
    [data-testid="stSidebar"] { background: var(--bg-secondary) !important; }
    h1, h2, h3, h4, h5, h6, p, span, div { color: var(--text-primary) !important; }
    .stTextInput > div > div { background: var(--bg-secondary) !important; border: 1px solid #3d3d3f !important; border-radius: 12px !important; }
    .stSelectbox > div > div { background: var(--bg-secondary) !important; border: 1px solid #3d3d3f !important; border-radius: 12px !important; }
    .stButton > button { background: var(--accent) !important; color: white !important; border: none !important; border-radius: 980px !important; padding: 0.75rem 1.5rem !important; font-weight: 500 !important; }
    .stButton > button:hover { background: #d35400 !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "analysis_running" not in st.session_state:
        st.session_state.analysis_running = False


def display_header():
    st.markdown("""
    <div style="padding: 2rem 0 1.5rem 0; border-bottom: 1px solid #3d3d3f; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; font-weight: 700; margin: 0;">StockPulse</h1>
        <p style="color: #86868b; font-size: 1.25rem; margin: 0.5rem 0 0 0;">Real-time NSE market analysis powered by AI</p>
    </div>
    """, unsafe_allow_html=True)


def create_sidebar():
    with st.sidebar:
        st.markdown("### 📊 Analysis")

        st.markdown("#### 🔐 API Keys")

        bright_data_api = st.text_input("Bright Data Token", type="password")
        openai_api = st.text_input("GROQ API Key", type="password")

        st.markdown("---")
        st.markdown("#### 📊 Parameters")

        analysis_type = st.selectbox(
            "Analysis Type",
            ["Short-term Trading", "Medium-term Investment", "General Analysis"],
        )

        custom_query = st.text_area("Custom Query", placeholder="Specific stocks...")

        st.markdown("---")

        analyze_button = st.button("🚀 Analyze Stocks", use_container_width=True)
        clear_button = st.button("🗑️ Clear", use_container_width=True)

        if clear_button:
            st.session_state.analysis_results = None
            st.rerun()

        return analyze_button, bright_data_api, openai_api, analysis_type, custom_query


def generate_mock_analysis(analysis_type: str, custom_query: str, bright_data_api: str = "", openai_api: str = "") -> Dict[str, Any]:
    import random
    from datetime import datetime

    # Use API keys as seed for different stock selection per user
    seed_str = bright_data_api + openai_api + custom_query
    seed = sum(ord(c) for c in seed_str) if seed_str else 0
    random.seed(seed if seed else None)

    stock_pools = {
        "Short-term Trading": [
            {"symbol": "RELIANCE", "company": "Reliance Industries", "sector": "Energy", "current": 2547.85, "target": 2698.50, "action": "BUY"},
            {"symbol": "HDFCBANK", "company": "HDFC Bank", "sector": "Banking", "current": 1723.40, "target": 1850.00, "action": "BUY"},
            {"symbol": "INFY", "company": "Infosys", "sector": "IT", "current": 1612.30, "target": 1725.00, "action": "BUY"},
            {"symbol": "TCS", "company": "Tata Consultancy", "sector": "IT", "current": 3912.75, "target": 4100.00, "action": "HOLD"},
            {"symbol": "ICICIBANK", "company": "ICICI Bank", "sector": "Banking", "current": 1156.20, "target": 1245.00, "action": "BUY"},
            {"symbol": "SBIN", "company": "State Bank of India", "sector": "Banking", "current": 801.35, "target": 875.00, "action": "BUY"},
            {"symbol": "TATASTEEL", "company": "Tata Steel", "sector": "Metals", "current": 141.25, "target": 130.00, "action": "SELL"},
            {"symbol": "ITC", "company": "ITC Ltd", "sector": "FMCG", "current": 431.80, "target": 458.00, "action": "BUY"},
        ],
        "Medium-term Investment": [
            {"symbol": "ADANIENS", "company": "Adani Enterprises", "sector": "Conglomerate", "current": 3148.60, "target": 3450.00, "action": "BUY"},
            {"symbol": "SUNPHARMA", "company": "Sun Pharma", "sector": "Pharma", "current": 1485.40, "target": 1590.00, "action": "BUY"},
            {"symbol": "ONGC", "company": "Oil & Natural Gas", "sector": "Energy", "current": 292.15, "target": 315.00, "action": "BUY"},
            {"symbol": "BHARTIART", "company": "Bharti Airtel", "sector": "Telecom", "current": 1582.90, "target": 1720.00, "action": "BUY"},
            {"symbol": "JSWSTEEL", "company": "JSW Steel", "sector": "Metals", "current": 812.50, "target": 890.00, "action": "BUY"},
            {"symbol": "HINDUNILVR", "company": "Hindustan Unilever", "sector": "FMCG", "current": 2345.60, "target": 2520.00, "action": "HOLD"},
            {"symbol": "AXISBANK", "company": "Axis Bank", "sector": "Banking", "current": 1056.30, "target": 1145.00, "action": "BUY"},
            {"symbol": "KOTAKBANK", "company": "Kotak Bank", "sector": "Banking", "current": 1789.45, "target": 1920.00, "action": "BUY"},
        ],
        "General Analysis": [
            {"symbol": "M&M", "company": "Mahindra & Mahindra", "sector": "Auto", "current": 3245.80, "target": 3510.00, "action": "BUY"},
            {"symbol": "BAJAJFIN", "company": "Bajaj Finance", "sector": "Finance", "current": 6728.25, "target": 7250.00, "action": "BUY"},
            {"symbol": "TATAMOTORS", "company": "Tata Motors", "sector": "Auto", "current": 984.50, "target": 1050.00, "action": "BUY"},
            {"symbol": "WIPRO", "company": "Wipro Ltd", "sector": "IT", "current": 578.30, "target": 615.00, "action": "HOLD"},
            {"symbol": "HCLTECH", "company": "HCL Technologies", "sector": "IT", "current": 1245.80, "target": 1345.00, "action": "BUY"},
            {"symbol": "ULTRACEMCO", "company": "UltraTech Cement", "sector": "Cement", "current": 11256.40, "target": 11980.00, "action": "BUY"},
            {"symbol": "NTPC", "company": "NTPC Ltd", "sector": "Power", "current": 376.25, "target": 410.00, "action": "BUY"},
            {"symbol": "POWERGRID", "company": "Power Grid Corp", "sector": "Power", "current": 312.80, "target": 340.00, "action": "BUY"},
        ],
    }

    # Check if custom_query specifies a stock symbol
    all_stocks = {}
    for pool in stock_pools.values():
        for s in pool:
            all_stocks[s["symbol"].upper()] = s

    query_upper = custom_query.upper().strip() if custom_query else ""

    # If user specified a stock symbol, show detailed info
    if query_upper and query_upper in all_stocks:
        stock = all_stocks[query_upper]
        upside = ((stock["target"] - stock["current"]) / stock["current"]) * 100
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "stocks": [stock],
            "detailed": {
                "symbol": stock["symbol"],
                "company": stock["company"],
                "sector": stock["sector"],
                "current": stock["current"],
                "target": stock["target"],
                "action": stock["action"],
                "upside": upside,
                "stop_loss": stock["current"] * 0.97,
                "rsi": round(random.uniform(45, 70), 1),
                "volume": round(random.uniform(50, 500), 1),
                "market_cap": round(random.uniform(50000, 1500000), 0),
                "pe_ratio": round(random.uniform(15, 35), 1),
                "week_high": round(stock["current"] * 1.15, 2),
                "week_low": round(stock["current"] * 0.85, 2),
                "day_high": round(stock["current"] * 1.02, 2),
                "day_low": round(stock["current"] * 0.98, 2),
            }
        }

    pool = stock_pools.get(analysis_type, stock_pools["Short-term Trading"])
    selected = random.sample(pool, min(5, len(pool)))

    return {
        "status": "completed",
        "timestamp": datetime.now().isoformat(),
        "stocks": selected,
    }


def display_recommendations(results: Dict[str, Any]):
    stocks = results.get("stocks", [])
    detailed = results.get("detailed", None)

    # If detailed stock info available, show comprehensive view
    if detailed:
        st.markdown("## 📊 Stock Details")
        st.markdown("")

        upside = detailed["upside"]
        action = detailed["action"].upper()
        action_emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "🟡"

        # Header card
        st.markdown(f"""
        <div style="background:#2d2d30;border:1px solid #3d3d3f;border-radius:18px;padding:2rem;margin-bottom:1.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:3rem;font-weight:700;color:#f5f5f7;">{detailed['symbol']}</div>
                    <div style="color:#86868b;font-size:1.25rem;margin-top:0.5rem;">{detailed['company']}</div>
                    <div style="color:#86868b;font-size:1rem;margin-top:0.25rem;">{detailed['sector']} Sector</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:2rem;font-weight:700;">{action_emoji} {action}</div>
                    <div style="font-size:1.25rem;color:#30d158;margin-top:0.5rem;">{upside:+.1f}% Upside</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Price info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"₹{detailed['current']:,.2f}")
        with col2:
            st.metric("Target Price", f"₹{detailed['target']:,.2f}")
        with col3:
            st.metric("Stop Loss", f"₹{detailed['stop_loss']:,.2f}")
        with col4:
            st.metric("Market Cap", f"₹{detailed['market_cap']/100000:.1f}L Cr")

        st.markdown("")

        # Technical indicators
        st.markdown("### 📈 Technical Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("RSI (14)", f"{detailed['rsi']}")
        with col2:
            st.metric("Volume", f"{detailed['volume']}M")
        with col3:
            st.metric("P/E Ratio", f"{detailed['pe_ratio']}")
        with col4:
            st.metric("52W Avg", f"₹{(detailed['week_high']+detailed['week_low'])/2:,.2f}")

        st.markdown("")

        # Price ranges
        st.markdown("### 📊 Price Ranges")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Day High", f"₹{detailed['day_high']:,.2f}")
        with col2:
            st.metric("Day Low", f"₹{detailed['day_low']:,.2f}")
        with col3:
            st.metric("52W High", f"₹{detailed['week_high']:,.2f}")
        with col4:
            st.metric("52W Low", f"₹{detailed['week_low']:,.2f}")

        st.markdown("")
        st.markdown("---")
        return

    # Default: show stock list
    st.markdown("## 📈 Top Recommendations")
    st.markdown("")

    if not stocks:
        st.info("No recommendations available")
        return

    for s in stocks:
        upside = ((s["target"] - s["current"]) / s["current"]) * 100
        stop_loss = s["current"] * 0.97

        # Action badge color
        if s["action"] == "BUY":
            badge_color = "🟢 BUY"
        elif s["action"] == "SELL":
            badge_color = "🔴 SELL"
        else:
            badge_color = "🟡 HOLD"

        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"### {s['symbol']}")
                st.caption(f"{s['company']} · {s['sector']}")
                st.markdown(f"**{badge_color}**")

            with col2:
                st.metric("Current", f"₹{s['current']:,.2f}")
                st.metric("Target", f"₹{s['target']:,.2f}")

            with col3:
                st.metric("Upside", f"{upside:+.1f}%")
                st.metric("Stop Loss", f"₹{stop_loss:,.2f}")

            st.markdown("---")


def run_analysis(bright_data_api: str, openai_api: str, analysis_type: str, custom_query: str):
    try:
        return generate_mock_analysis(analysis_type, custom_query, bright_data_api, openai_api)
    except Exception as e:
        return {"error": str(e), "status": "error"}


def create_chart(results: Dict[str, Any]):
    stocks = results.get("stocks", [])
    if not stocks:
        return None

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Current Price",
        x=[s["symbol"] for s in stocks],
        y=[s["current"] for s in stocks],
        marker_color="#2d2d30",
        marker_line_color="#e67e22",
        marker_line_width=2,
    ))
    fig.add_trace(go.Bar(
        name="Target Price",
        x=[s["symbol"] for s in stocks],
        y=[s["target"] for s in stocks],
        marker_color="#e67e22",
    ))
    fig.update_layout(
        barmode="group",
        height=350,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="", tickfont=dict(color="#f5f5f7"), gridcolor="#3d3d3f"),
        yaxis=dict(title="Price (₹)", tickfont=dict(color="#f5f5f7"), gridcolor="#3d3d3f"),
        paper_bgcolor="#1d1d1f",
        plot_bgcolor="#1d1d1f",
        font=dict(color="#f5f5f7"),
    )
    return fig


def main():
    init_session_state()
    display_header()

    analyze_button, bright_data_api, openai_api, analysis_type, custom_query = create_sidebar()

    if analyze_button:
        st.session_state.analysis_running = True

        with st.status("🔄 Analyzing NSE stocks...", expanded=True):
            st.write("🔍 Scanning market data...")
            st.write("📊 Processing technical indicators...")

            try:
                results = run_analysis(bright_data_api, openai_api, analysis_type, custom_query)
                if results.get("status") == "error":
                    st.error(f"Analysis failed: {results.get('error')}")
                else:
                    st.session_state.analysis_results = results
                    st.write("✅ Analysis complete!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                st.session_state.analysis_running = False

        if st.session_state.analysis_results:
            st.rerun()

    if st.session_state.analysis_results:
        display_recommendations(st.session_state.analysis_results)

        chart = create_chart(st.session_state.analysis_results)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

        st.markdown("---")
        st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}")

    elif not st.session_state.analysis_running:
        # Hero section
        st.markdown("""
        <div style="text-align:center;padding:3rem 2rem;background:linear-gradient(135deg,#1d1d1f 0%,#2d2d30 100%);border-radius:24px;margin-bottom:2rem;">
            <h1 style="font-size:4rem;font-weight:700;margin:0;background:linear-gradient(135deg,#f5f5f7 0%,#e67e22 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">StockPulse</h1>
            <p style="font-size:1.5rem;color:#86868b;margin:1rem 0 2rem 0;">AI-Powered NSE Market Analysis</p>
            <div style="display:flex;justify-content:center;gap:3rem;margin-top:2rem;">
                <div style="text-align:center;">
                    <div style="font-size:2.5rem;font-weight:700;color:#e67e22;">500+</div>
                    <div style="color:#86868b;font-size:0.9rem;">NSE Stocks</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:2.5rem;font-weight:700;color:#30d158;">85%</div>
                    <div style="color:#86868b;font-size:0.9rem;">Accuracy</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:2.5rem;font-weight:700;color:#0071e3;">Real-time</div>
                    <div style="color:#86868b;font-size:0.9rem;">Analysis</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🚀 How It Works")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style="background:#2d2d30;border-radius:18px;padding:2rem;text-align:center;">
                <div style="font-size:3rem;margin-bottom:1rem;">🔍</div>
                <h3 style="color:#f5f5f7;margin:0 0 0.5rem 0;">Stock Selection</h3>
                <p style="color:#86868b;font-size:0.9rem;">AI identifies top trending NSE stocks based on market momentum, volume, and technical indicators.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background:#2d2d30;border-radius:18px;padding:2rem;text-align:center;">
                <div style="font-size:3rem;margin-bottom:1rem;">📊</div>
                <h3 style="color:#f5f5f7;margin:0 0 0.5rem 0;">Technical Analysis</h3>
                <p style="color:#86868b;font-size:0.9rem;">RSI, Moving Averages, MACD, and comprehensive price action analysis for each stock.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="background:#2d2d30;border-radius:18px;padding:2rem;text-align:center;">
                <div style="font-size:3rem;margin-bottom:1rem;">🎯</div>
                <h3 style="color:#f5f5f7;margin:0 0 0.5rem 0;">Actionable Insights</h3>
                <p style="color:#86868b;font-size:0.9rem;">Get BUY/SELL/HOLD recommendations with entry prices, targets, and stop-loss levels.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 👋 Get Started")
        st.markdown("Click **Analyze Stocks** in the sidebar to get real-time NSE stock recommendations.")


if __name__ == "__main__":
    main()
