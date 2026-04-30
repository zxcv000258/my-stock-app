import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. 極致高級感 CSS 注入 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Arvo:wght@700&family=Chewy&display=swap');

    /* 徹底隱藏原生組件 */
    [data-testid="stHeader"], .stAppHeader { display: none !important; }
    
    .stApp {
        background-color: #f4ead0;
        background-image: url("https://www.transparenttextures.com/patterns/p6.png");
        font-family: 'Arvo', serif;
    }

    /* 高級橡皮管卡片 */
    .premium-card {
        background: transparent;
        border: 8px solid #262626;
        padding: 30px;
        margin: 20px;
        box-shadow: 15px 15px 0px #262626;
        text-align: center;
        border-radius: 4px;
    }

    .ticker-title { font-family: 'Chewy', cursive; font-size: 32px; color: #262626; }
    .price-display { font-family: 'Chewy', cursive; font-size: 85px; margin: 20px 0; color: #262626; line-height: 1; }
    
    /* 輸入框美化 */
    .stTextInput input {
        background: transparent !important;
        border: 6px solid #262626 !important;
        border-radius: 0 !important;
        font-family: 'Chewy', cursive;
        font-size: 28px !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據請求 ---
def get_stock_data(tk):
    try:
        s = yf.Ticker(tk)
        d = s.history(period="1d", interval="1m")
        if d.empty: d = s.history(period="5d", interval="1d")
        return {"p": d['Close'].iloc[-1], "d": d} if not d.empty else None
    except: return None

# --- 3. 頁面渲染 ---
st.markdown("<h1 style='text-align:center; font-family:Chewy; font-size:45px; margin-top:30px;'>📽️ STOCK-O-RAMA</h1>", unsafe_allow_html=True)

q = st.text_input("", placeholder="TYPE TICKER...")

if q:
    res = get_stock_data(q)
    if res:
        # 顯示專業卡片
        st.markdown(f"""
            <div class="premium-card">
                <div class="ticker-title">{q.upper()}</div>
                <div class="price-display">${round(res['p'], 2)}</div>
                <div style="font-family:Chewy; border-top:4px solid #262626; padding-top:10px;">MOTION PICTURE TRADING</div>
            </div>
        """, unsafe_allow_html=True)

        # 墨水感技術圖表
        fig = go.Figure(data=[go.Candlestick(
            x=res['d'].index, open=res['d']['Open'], high=res['d']['High'], low=res['d']['Low'], close=res['d']['Close'],
            increasing_line_color='#262626', decreasing_line_color='#262626',
            increasing_fillcolor='#3b5a2a', decreasing_fillcolor='#ae3f2f',
            line_width=3
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis_visible=False, yaxis_gridcolor='rgba(38,38,38,0.2)',
            height=400, margin=dict(l=10, r=10, t=0, b=0),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("🚫 訊號中斷，請重試。")
