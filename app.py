import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. 防止被封鎖的 Session 設定 ---
import requests
from requests import Session
session = Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
})

# --- 2. 自動整理 (每分鐘) ---
st_autorefresh(interval=60000, key="cartoon_refresh")

# --- 3. 徹底封裝！注入像素級舊底片動畫 CSS ---
st.markdown("""
<style>
    /* 引入復古字體 (類似舊海報) */
    @import url('https://fonts.googleapis.com/css2?family=Arvo:wght@400;700&family=Chewy&display=swap');
    
    /* 1. 徹底隱藏 Streamlit 原生外殼 (藍色頂部、白色背景、Padding) */
    [data-testid="stHeader"], [data-testid="stSidebar"], .stAppHeader { display: none !important; }
    [data-testid="stMain"] { padding: 0 !important; }

    /* 2. 全局背景：仿舊紙張顆粒與雜訊背景 (#f4ead0) */
    .stApp {
        background-color: #f4ead0;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'%3E%3Cpath fill='%23262626' fill-opacity='0.1' d='M1 3h1v1H1V3zm2-2h1v1H3V1z'%3E%3C/path%3E%3C/svg%3E");
        color: #262626;
        font-family: 'Arvo', serif;
    }
    
    /* 3. 橡皮管卡片：粗糙的手繪線條邊框 */
    .cartoon-card {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        border: 4px solid #262626;
        margin-bottom: 15px;
        position: relative;
        box-shadow: 5px 5px 0px #262626;
    }
    
    /* BULL/BEAR 標籤：手繪風 */
    .bull-head-label {
        font-family: 'Chewy', cursive;
        color: #f4ead0;
        background-color: #3b5a2a; /* 墨綠色 */
        padding: 2px 10px;
        border-radius: 8px;
        border: 3px solid #262626;
        font-size: 14px;
    }

    /* 指令輸入框美化：圓潤且粗邊框 */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 4px solid #262626 !important;
        border-radius: 10px !important;
        color: #262626 !important;
        font-family: 'Chewy', cursive;
        font-size: 18px !important;
        padding: 12px 20px !important;
    }

    h1 { font-family: 'Chewy', cursive; color: #262626; font-size: 32px; text-align: center; margin-top: 10px;}
    h3 { font-family: 'Chewy', cursive; color: #262626; margin: 0; }
</style>
""", unsafe_allow_html=True)

# --- 4. 數據請求 (修復連線阻斷) ---
def get_clean_data(ticker):
    try:
        stock = yf.Ticker(ticker, session=session) # 使用 Session 繞過限制
        df = stock.history(period="2d", interval="5m")
        if df.empty: return None
        return {"df": df, "price": df['Close'].iloc[-1]}
    except Exception as e:
        return str(e)

# --- 5. UI 介面佈局 (手機端垂直垂直佈局) ---

# 仿舊報紙頂部
st.markdown("<p style='text-align:center; font-size:12px; color:#262626; opacity:0.5; margin:0;'>2026/05/01 MARKET INTEL - 橡皮管動畫版</p>", unsafe_allow_html=True)
st.markdown("<h1>🕰️ Stock-O-Rama 終端</h1>", unsafe_allow_html=True)

# 指令輸入
cmd = st.text_input("", placeholder="TYPE SYMBOL (E.G., AAPL, 2330)...")

if cmd:
    res = get_clean_data(cmd)
    
    if isinstance(res, dict):
        # 情報卡片
        st.markdown(f"""
            <div class="cartoon-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3>📍 情報中心: {cmd.upper()}</h3>
                    <div class="bull-head-label">BULLISH 🐂</div>
                </div>
                <p style="font-size:12px; color:#262626; margin:5px 0;">情報來源：Real-time Signal 📡</p>
                <h1 style="font-size:48px; font-weight:700; margin:10px 0;">${round(res['price'], 2)}</h1>
            </div>
        """, unsafe_allow_html=True)

        # Plotly K線圖美化 (復古墨黑色蠟燭)
        fig = go.Figure(data=[go.Candlestick(
            x=res['df'].index, open=res['df']['Open'], 
            high=res['df']['High'], low=res['df']['Low'], close=res['df']['Close'],
            increasing_line_color='#262626', decreasing_line_color='#262626', 
            increasing_fillcolor='#3b5a2a', decreasing_fillcolor='#ae3f2f'
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_visible=False,
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"連線失敗或無代號。")
else:
    st.markdown("""
        <div style="text-align:center; margin-top:50px; opacity:0.3;">
            <p>🐾 舊底片載入中，等待指令...</p>
        </div>
    """, unsafe_allow_html=True)
