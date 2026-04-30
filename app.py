import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# 1. 自動整理與隱藏原生 UI
st_autorefresh(interval=60000, key="rrefresh")
st.markdown("<style>[data-testid='stHeader'],.stAppHeader{display:none!important;} .stApp{background-color:#f4ead0;background-image:url('https://www.transparenttextures.com/patterns/p6.png');color:#262626;font-family:'Courier New',Courier,monospace;animation:flicker 0.1s infinite;} @keyframes flicker{0%{opacity:0.99;} 100%{opacity:1;}} .rubber-card{border:6px solid #262626;padding:20px;margin:10px;box-shadow:10px 10px 0px #262626;text-align:center;} .stTextInput input{background:transparent!important;border:5px solid #262626!important;border-radius:0!important;font-weight:bold;text-align:center;}</style>", unsafe_allow_html=True)

# 2. 穩定版數據抓取
def get_data(tk):
    try:
        s = yf.Ticker(tk)
        d = s.history(period="2d", interval="5m")
        if d.empty: d = s.history(period="5d", interval="1d")
        return {"p": d['Close'].iloc[-1], "d": d} if not d.empty else None
    except: return None

# 3. 介面渲染
st.markdown("<h1 style='text-align:center;'>🎞️ STOCK-O-RAMA</h1>", unsafe_allow_html=True)
q = st.text_input("", placeholder="ENTER TICKER (e.g. 2330, NVDA)")

if q:
    res = get_data(q)
    if res:
        st.markdown(f"<div class='rubber-card'><h2 style='margin:0;'>{q.upper()}</h2><h1 style='font-size:60px;margin:10px 0;'>${round(res['p'],2)}</h1><p>STATUS: SWINGIN'</p></div>", unsafe_allow_html=True)
        fig = go.Figure(data=[go.Candlestick(x=res['d'].index, open=res['d']['Open'], high=res['d']['High'], low=res['d']['Low'], close=res['d']['Close'], increasing_line_color='#262626', decreasing_line_color='#262626', increasing_fillcolor='#3b5a2a', decreasing_fillcolor='#ae3f2f')])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_visible=False, height=300, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("🚫 訊號中斷，請重試。")
else:
    st.markdown("<div style='text-align:center;font-size:60px;margin-top:50px;'>📽️</div>", unsafe_allow_html=True)
