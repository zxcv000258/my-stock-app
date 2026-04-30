import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import re

# --- 1. 極速 Google Finance 數據引擎 (完全取代 Yahoo) ---
def get_google_data(tk):
    try:
        # 處理台股代號格式 (如 2330 -> TPE:2330)
        symbol = f"TPE:{tk}" if tk.isdigit() else tk
        url = f"https://www.google.com/search?q={symbol}+stock+price"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers).text
        
        # 使用正則表達式直接從 Google 搜尋結果抓取價格
        price = re.search(r'data-precision="2">([\d,.]+)<', resp).group(1).replace(',', '')
        return float(price)
    except:
        return None

# --- 2. 徹底封裝 UI：注入 1930s 動畫靈魂 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Chewy&display=swap');
    [data-testid="stHeader"], .stAppHeader { display: none !important; }
    
    .stApp {
        background-color: #f4ead0;
        background-image: url("https://www.transparenttextures.com/patterns/black-paper.png");
        color: #262626;
        animation: film-grain 0.1s infinite;
    }

    @keyframes film-grain { 0% { opacity: 0.98; } 100% { opacity: 1; } }

    .rubber-box {
        border: 10px solid #262626;
        padding: 40px;
        margin: 20px;
        box-shadow: 20px 20px 0px #262626;
        text-align: center;
        background: transparent;
    }

    .stTextInput input {
        background: transparent !important;
        border: 6px solid #262626 !important;
        border-radius: 0 !important;
        font-family: 'Chewy', cursive;
        font-size: 32px !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 介面渲染 ---
st.markdown("<h1 style='text-align:center; font-family:Chewy; font-size:50px;'>🎬 STOCK-O-RAMA</h1>", unsafe_allow_html=True)

q = st.text_input("", placeholder="ENTER TICKER...")

if q:
    price = get_google_data(q)
    if price:
        st.markdown(f"""
            <div class="rubber-box">
                <div style="font-family:Chewy; font-size:30px;">TICKER: {q.upper()}</div>
                <div style="font-family:Chewy; font-size:100px; margin:20px 0;">${price}</div>
                <div style="font-family:Chewy; font-size:20px; border-top:5px solid #262626; padding-top:10px;">
                    REAL-TIME GOOGLE DATA 📡
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center; color:#ae3f2f; font-family:Chewy;'>🚫 SIGNAL LOST!</h2>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:center; font-size:100px; margin-top:50px;'>📽️</div>", unsafe_allow_html=True)
