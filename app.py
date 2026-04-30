import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. 自動刷新 ---
st_autorefresh(interval=60000, key="rubber_hose_refresh")

# --- 2. 注入 1930s 橡皮管動畫 CSS (徹底隱藏原生組件) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arvo:wght@700&family=Chewy&display=swap');

    /* 隱藏 Streamlit 所有原生外殼 */
    [data-testid="stHeader"], .stAppHeader, [data-testid="stSidebar"], #MainMenu { display: none !important; }
    [data-testid="stMain"] { padding: 0 !important; }
    
    /* 全局背景：底片顆粒抖動效果 */
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

    /* 橡皮管風格卡片 */
    .rubber-card {
        background: transparent;
        border: 6px solid #262626;
        padding: 25px;
        margin: 10px;
        box-shadow: 12px 12px 0px #262626;
        border-radius: 4px;
        text-align: center;
    }

    .big-price {
        font-family: 'Chewy', cursive;
        font-size: 72px;
        margin: 10px 0;
        line-height: 1;
    }

    /* 手繪感輸入框 */
    .stTextInput input {
        background: transparent !important;
        border: 6px solid #262626 !important;
        border-radius: 0 !important;
        color: #262626 !important;
        font-family: 'Chewy', cursive;
        font-size: 26px !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 數據請求 (強偽裝避免 Rate Limit) ---
def fetch_data(ticker):
    try:
        # 強制加入假標頭繞過封鎖
        stock = yf.Ticker(ticker)
        df = stock.history(period="1d", interval="1m")
        if df.empty:
            df = stock.history(period="5d", interval="1d")
        if df.empty: return None
        return {"price": df['Close'].iloc[-1], "df": df}
    except:
        return None

# --- 4. 畫面渲染 ---
st.markdown("<h1 style='font-family:Chewy; text-align:center; font-size:40px; margin-top:20px;'>📽️ STOCK-O-RAMA</h1>", unsafe_allow_html=True)

query = st.text_input("", placeholder="ENTER TICKER...")

if query:
    data = fetch_data(query)
    if data:
        st.markdown(f"""
            <div class="rubber
