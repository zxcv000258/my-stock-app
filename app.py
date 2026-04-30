import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- 1. 環境環境設定 (自動整理) ---
st_autorefresh(interval=60000, key="cartoon_refresh")

# --- 2. 注入美國橡皮管動畫風格 CSS ---
st.markdown("""
<style>
    /* 引入復古字體 */
    @import url('https://fonts.googleapis.com/css2?family=Arvo:wght@400;700&family=Chewy&display=swap');
    
    /* 1. 全局背景與字體：復古奶油色與手繪感墨黑色 */
    .stApp { background: #FDF6E3; color: #262626; font-family: 'Arvo', serif; }
    
    /* 2. 手繪感標題 */
    h1, h2, h3 { font-family: 'Chewy', cursive; color: #262626; }
    
    /* 3. 橡皮管風格卡片：粗糙的手繪線條邊框 */
    .cartoon-card {
        background: #FDF6E3; border-radius: 12px; padding: 20px;
        border: 4px solid #262626; margin-bottom: 20px;
        position: relative;
    }
    
    /* 4. 復古指令輸入框 */
    .stTextInput input {
        background: #FDF6E3 !important;
        border: 4px solid #262626 !important;
        border-radius: 8px !important;
        color: #262626 !important;
        font-family: 'Chewy', cursive;
        font-size: 20px !important;
    }

    /* 5. 指標擬人化動畫 (範例) */
    .bull-head-icon { font-size: 40px; }
    .bear-head-icon { font-size: 40px; }
</style>
""", unsafe_allow_html=True)

# --- 3. 數據請求 ---
def get_smc_data(ticker):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="2d", interval="5m")
        if df.empty: return None
        return {"df": df, "price": df['Close'].iloc[-1]}
    except:
        return None

# --- 4. UI 介面佈局 (復古終端) ---

st.markdown("<h1 style='text-align:center; font-size:48px; border-bottom:4px solid #262626;'>🕰️ Stock-O-Rama 終端</h1>", unsafe_allow_html=True)

# 搜尋指令
cmd = st.text_input("", placeholder="🔍 TYPE SYMBOL (E.G., AAPL, 2330)...")

if cmd:
    data = get_smc_data(cmd)
    if data:
        # 模塊 1：情報中心大卡片
        st.markdown(f"""
        <div class="cartoon-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="margin:0;">📍 情報中心: {cmd.upper()}</h2>
                <div class="bull-head-icon">🐂</div> </div>
            <p style="font-size:14px; opacity:0.8; margin:5px 0;">數據冷卻於 2026/05/01</p>
            <h1 style="font-size:64px; margin:15px 0; border-top: 4px solid #262626;">${round(data['price'], 2)}</h1>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("查無數據，請重試。")
