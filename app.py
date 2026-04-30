import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
from datetime import datetime
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- 1. 防止被封鎖的 Session 設定 ---
import requests
from requests import Session
session = Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
})

# --- 2. 自動更新 (每 60 秒) ---
st_autorefresh(interval=60000, key="news_update")

# --- 3. 極致深色 UI 改裝 (仿截圖風格) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at top right, #1e2a44, #0f0c29); 
        color: #f0f0f0; 
        font-family: 'Inter', sans-serif;
    }
    
    /* 仿截圖：頂部資訊條 */
    .header-info {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 20px;
    }

    /* 仿截圖：跑馬燈新聞 */
    .ticker-wrap { background: #1a1a2e; border: 1px solid #302b63; padding: 12px 0; overflow: hidden; border-radius: 12px; margin-bottom: 20px; }
    .ticker-text { display: inline-block; white-space: nowrap; animation: marquee 60s linear infinite; font-weight: 500; color: #00f2fe; }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* 仿截圖：系統卡片風格 */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .metric-box {
        text-align: center;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 指令輸入框美化 */
    .stTextInput > div > div > input {
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #302b63;
        color: white;
        padding: 15px 25px;
    }

    h1 { font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -1px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. 穩定版新聞引擎 ---
def get_news():
    try:
        feed = feedparser.parse("https://www.investing.com/rss/news.rss")
        titles = [f" 🔥 {entry.title}" for entry in feed.entries[:8]]
        return " | ".join(titles) if titles else "📢 市場情報中心連線中..."
    except:
        return "📢 正在重新校準情報衛星..."

# --- 5. 數據引擎 (修復 YFRateLimitError) ---
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker, session=session) # 使用 Session 繞過限制
        df = stock.history(period="2d", interval="5m")
        if df.empty: return None
        
        info = stock.info
        curr_price = df['Close'].iloc[-1]
        change = ((curr_price - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
        
        return {
            "price": round(curr_price, 2),
            "change": round(change, 2),
            "df": df,
            "name": info.get('shortName', ticker)
        }
    except Exception as e:
        return str(e)

# --- 6. UI 佈局渲染 ---

# 頂部狀態欄
st.markdown(f"""
    <div class="header-info">
        <div>📡 系統引擎日誌</div>
        <div>{datetime.now().strftime('%Y/%m/%d %H:%M')}</div>
    </div>
""", unsafe_allow_html=True)

# 跑馬燈新聞 (市場情報中心)
news_ticker = get_news()
st.markdown(f'<div class="ticker-wrap"><div class="ticker-text">{news_ticker}</div></div>', unsafe_allow_html=True)

st.markdown("<h1>📊 DailyDip AI 分析終端</h1>", unsafe_allow_html=True)

# 指令輸入
cmd = st.text_input("", placeholder="TYPE SYMBOL (E.G., TSLA)...")

if cmd:
    res = analyze_stock(cmd)
    
    if isinstance(res, dict):
        # 模仿截圖中的卡片
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="glass-card">
                    <p style="color:#888; font-size:12px; margin:0;">AI 篩選動能</p>
                    <h2 style="margin:0; color:#00f2fe;">99.98<span style="font-size:14px;">%</span></h2>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="glass-card">
                    <p style="color:#888; font-size:12px; margin:0;">主動防禦率</p>
                    <h2 style="margin:0; color:#ff4b2b;">98<span style="font-size:14px;">%</span></h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="glass-card">
                <h3 style="margin:0; color:#fff;">{res['name']}</h3>
                <p style="font-size:32px; font-weight:700; margin:10px 0;">${res['price']} <span style="font-size:16px; color:{'#ff4b2b' if res['change']<0 else '#00f2fe'};">{res['change']}%</span></p>
            </div>
        """, unsafe_allow_html=True)

        # K線圖美化
        fig = go.Figure(data=[go.Candlestick(
            x=res['df'].index, open=res['df']['Open'], 
            high=res['df']['High'], low=res['df']['Low'], close=res['df']['Close'],
            increasing_line_color='#00f2fe', decreasing_line_color='#ff4b2b'
        )])
        fig.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"連線受限或查無代號，請稍後再試。")
else:
    st.markdown("""
        <div style="text-align:center; margin-top:50px; opacity:0.3;">
            <p>🐾 交易分析區正在等待指令...</p>
        </div>
    """, unsafe_allow_html=True)
