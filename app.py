import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
from datetime import datetime
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- 1. 自動更新 (每 60 秒) ---
st_autorefresh(interval=60000, key="news_update")

# --- 2. 自定義 CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0F0C29; color: #f0f0f0; }
    .ticker-wrap { background: #FF416C; padding: 10px 0; overflow: hidden; border-radius: 10px; margin-bottom: 20px; }
    .ticker-text { display: inline-block; white-space: nowrap; animation: marquee 50s linear infinite; font-weight: bold; color: white; }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .card { background: linear-gradient(145deg, #1e2a44, #161b2e); border-radius: 20px; padding: 20px; margin-bottom: 15px; border-left: 6px solid #00d1b2; }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
""", unsafe_allow_html=True)

# --- 3. 穩定版新聞抓取 (暫時不翻譯) ---
def get_news():
    feed = feedparser.parse("https://www.investing.com/rss/news.rss")
    titles = [f"🆕 {entry.title}" for entry in feed.entries[:5]]
    return " | ".join(titles) if titles else "📢 正在獲取最新國際動態..."

# --- 4. 股票分析邏輯 ---
def analyze_stock(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="2d", interval="5m")
    if df.empty: return None
    curr_price = df['Close'].iloc[-1]
    return {"price": round(curr_price, 2), "df": df}

# --- 5. UI 渲染 ---
news_ticker = get_news()
st.markdown(f'<div class="ticker-wrap"><div class="ticker-text">{news_ticker}</div></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#FF416C;'>🧸 Stock Assistant</h1>", unsafe_allow_html=True)

cmd = st.text_input("✨ 輸入代號 (如: TSLA, 2330)")
if cmd:
    res = analyze_stock(cmd)
    if res:
        st.markdown(f'<div class="card"><h3>📍 {cmd.upper()}</h3><p style="font-size:1.5rem;">Price: ${res["price"]}</p></div>', unsafe_allow_html=True)
        fig = go.Figure(data=[go.Candlestick(x=res['df'].index, open=res['df']['Open'], high=res['df']['High'], low=res['df']['Low'], close=res['df']['Close'])])
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("查無數據")
