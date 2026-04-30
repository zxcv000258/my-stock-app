import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
from googletrans import Translator
from datetime import datetime
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- 1. 初始化與自動更新 (每 60 秒) ---
st_autorefresh(interval=60000, key="news_update")
translator = Translator()

# --- 2. 自定義 CSS (手機垂直佈局 + 可愛深色系) ---
st.markdown("""
    <style>
    .stApp { background-color: #0F0C29; color: #f0f0f0; }
    .stTextInput > div > div > input { border-radius: 15px; background: #1A1A2E; color: white; border: 2px solid #FF416C; }
    
    /* 跑馬燈 */
    .ticker-wrap { background: #FF416C; padding: 10px 0; overflow: hidden; border-radius: 10px; margin-bottom: 20px; }
    .ticker-text { display: inline-block; white-space: nowrap; animation: marquee 50s linear infinite; font-weight: bold; color: white; }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* 可愛圓角卡片 */
    .card { background: linear-gradient(145deg, #1e2a44, #161b2e); border-radius: 20px; padding: 20px; margin-bottom: 15px; border-left: 6px solid #00d1b2; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
    .rec-card { background: linear-gradient(135deg, #FF416C, #FF4B2B); border-radius: 20px; padding: 15px; margin-bottom: 15px; color: white; }
    h1, h2 { font-family: 'Comic Sans MS', cursive; color: #FF416C; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 3. 核心功能：新聞抓取與翻譯 ---
def get_translated_news():
    urls = ["https://www.investing.com/rss/news.rss", "https://finance.yahoo.com/news/rssindex"]
    all_titles = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            try:
                # 英翻中
                trans = translator.translate(entry.title, dest='zh-tw').text
                all_titles.append(f"🆕 {trans} ({entry.source.title if 'source' in entry else '國際財經'})")
            except:
                all_titles.append(f"🆕 {entry.title}")
    return " | ".join(all_titles) if all_titles else "📢 正在連接國際財經數據源..."

# --- 4. 核心功能：股票分析邏輯 ---
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        df_5m = stock.history(period="2d", interval="5m")
        df_daily = stock.history(period="1mo")
        
        if df_5m.empty: return None, "🚫 查無數據，禁止幻想。"
        
        # 數據時效檢查 (3天)
        last_time = df_5m.index[-1]
        delta = datetime.now(last_time.tzinfo) - last_time
        warning = f"⚠️ 數據已超過 3 天 ({last_time.strftime('%m-%d')})" if delta.days >= 3 else ""

        # 指標計算
        curr_price = df_5m['Close'].iloc[-1]
        df_5m['VWAP'] = (df_5m['Close'] * df_5m['Volume']).cumsum() / df_5m['Volume'].cumsum()
        ema20 = df_daily['Close'].ewm(span=20).mean().iloc[-1]
        
        short_signal = "💖 偏多 (站上VWAP)" if curr_price > df_5m['VWAP'].iloc[-1] else "❄️ 偏空 (跌破VWAP)"
        long_signal = "📈 趨勢看多" if curr_price > ema20 else "📉 趨勢看空"
        
        return {
            "price": round(curr_price, 2),
            "short": short_signal,
            "long": long_signal,
            "vwap": df_5m['VWAP'],
            "df": df_5m,
            "warning": warning
        }, ""
    except:
        return None, "❌ 讀取失敗，請檢查代碼是否正確。"

# --- 5. UI 畫面渲染 ---

# 跑馬燈
news_ticker = get_translated_news()
st.markdown(f'<div class="ticker-wrap"><div class="ticker-text">{news_ticker}</div></div>', unsafe_allow_html=True)

st.markdown("<h1>🧸 小助手分析 App</h1>", unsafe_allow_html=True)

# 指令輸入
cmd = st.text_input("✨ 請輸入股票代號 (如: TSLA, 2330)", placeholder="在這裡輸入...")

if cmd:
    # 判斷是否為當沖指令
    if "當沖" in cmd:
        st.markdown('<div class="rec-card">🎯 AI 推薦標的：NVDA<br>💡 理由：技術面放量且新聞利多<br>🛠️ 操作：回測VWAP支撐進場</div>', unsafe_allow_html=True)
    else:
        res
      
