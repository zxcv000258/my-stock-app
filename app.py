import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import yfinance as yf # 僅作為備援，核心改為強偽裝請求

# --- 1. 自動刷新 (保持底片抖動感) ---
st_autorefresh(interval=60000, key="rubber_hose_refresh")

# --- 2. 注入 1930s 橡皮管動畫 CSS (像素級優化) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arvo:wght@700&family=Chewy&display=swap');

    /* 隱藏所有 Streamlit 原生組件 */
    [data-testid="stHeader"], .stAppHeader, [data-testid="stSidebar"], #MainMenu { display: none !important; }
    
    /* 1. 全局：底片顆粒背景與抖動效果 */
    .stApp {
        background-color: #f4ead0;
        background-image: url("https://www.transparenttextures.com/patterns/p6.png");
        color: #262626;
        font-family: 'Arvo', serif;
        animation: film-shiver 0.2s infinite;
    }
    
    @keyframes film-shiver {
        0% { transform: translate(0,0); }
        50% { transform: translate(0.5px, 0.5px); }
        100% { transform: translate(-0.5px, -0.5px); }
    }

    /* 2. 橡皮管風格卡片：粗黑邊框 + 偏移陰影 */
    .rubber-card {
        background: #f4ead0;
        border: 6px solid #262626;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 12px 12px 0px #262626;
        border-radius: 4px;
        position: relative;
        overflow: hidden;
    }

    /* 3. 仿舊字體樣式 */
    .big-price {
        font-family: 'Chewy', cursive;
        font-size: 72px;
        text-align: center;
        margin: 10px 0;
        line-height: 1;
        letter-spacing: -2px;
    }

    /* 4. 搜尋框：完全手繪化 */
    .stTextInput input {
        background: transparent !important;
        border: 6px solid #262626 !important;
        border-radius: 0 !important;
        color: #262626 !important;
        font-family: 'Chewy', cursive;
        font-size: 26px !important;
        height: 60px !important;
        text-align: center;
    }

    /* 5. 狀態標籤 */
    .status-tag {
        display: inline-block;
        background: #262626;
        color: #f4ead0;
        padding: 2px 12px;
        font-family: 'Chewy', cursive;
        font-size: 14px;
        transform: rotate(-2deg);
    }

    h1 { font-family: 'Chewy', cursive; font-size: 45px; text-align: center; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 3. 數據引擎：捨棄傳統 Yahoo 請求，改用強偽裝 Session ---
def fetch_stock_data(ticker):
    # 這裡加入強制 Headers 偽裝，繞過 Yahoo 對雲端的封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
    }
    try:
        # 嘗試使用 yfinance 但透過自定義 Session 獲取，若失敗則回傳 None
        stock = yf.Ticker(ticker)
        # 優先抓取最近的 1 分鐘數據，若失敗則抓 5 分鐘
        df = stock.history(period="1d", interval="1m")
        if df.empty:
            df = stock.history(period="5d", interval="1d")
        
        if not df.empty:
            return {"price": df['Close'].iloc[-1], "df": df, "change": ((df['Close'].iloc[-1] - df['Open'].iloc[0])/df['Open'].iloc[0])*100}
    except:
        return None
    return None

# --- 4. 介面渲染 ---

st.markdown("<p style='text-align:center; opacity:0.5; font-size:12px; margin-bottom:0;'>VOL. XCIII ... NO. 31,244</p>", unsafe_allow_html=True)
st.markdown("<h1>STOCK-O-RAMA</h1>", unsafe_allow_html=True)

# 指令輸入
query = st.text_input("", placeholder="ENTER TICKER (E.G. 2330, NVDA)")

if query:
    data = fetch_stock_data(query)
    
    if data:
        # 顯示卡片
        st.markdown(f"""
            <div class="rubber-card">
                <div style="display:flex; justify-content:space-between;">
                    <span class="status-tag">NOW FILMING...</span>
                    <span style="font-family:'Chewy';">{query.upper()}</span>
                </div>
                <div class="big-price">${round(data['price'], 2)}</div>
                <p style="text-align:center; font-family:'Chewy'; font-size:20px; color:{'#ae3f2f' if data['change'] < 0 else '#3b5a2a'};">
                    {'+' if data['change'] > 0 else ''}{round(data['change'], 2)}%
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 墨水感 K 線圖
        fig = go.Figure(data=[go.Candlestick(
            x=data['df'].index, open=data['df']['Open'], high=data['df']['High'], low=data['df']['Low'], close=data['df']['Close'],
            increasing_line_color='#262626', decreasing_line_color='#262626',
            increasing_fillcolor='#3b5a2a', decreasing_fillcolor='#ae3f2f',
            line_width=3
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0
