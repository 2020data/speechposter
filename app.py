# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:32:19 2026

@author: e010
"""
import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import os
import random

st.set_page_config(page_title="演講海報產生器", layout="wide")

# 初始化 Session State，用於儲存背景顏色
# 預設使用原本範例的淺紅與淺藍
if 'bg_color1' not in st.session_state:
    st.session_state['bg_color1'] = "rgba(255,200,200,0.4)"
if 'bg_color2' not in st.session_state:
    st.session_state['bg_color2'] = "rgba(200,200,255,0.4)"

# 產生隨機淺色 (確保不與深色文字衝突)
# 策略：產生 RGB 三個通道都偏高的顏色 (180-255)，並帶有透明度
def generate_light_color():
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)
    # 透明度設為 0.5 讓漸層疊加更自然
    return f"rgba({r},{g},{b},0.5)"

# 處理圖片轉 Base64
def get_image_base64(uploaded_file, default_local_path):
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
    else:
        try:
            img = Image.open(default_local_path)
        except FileNotFoundError:
            return "" 
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

st.title("🎨 演講海報產生器 (最終完整版)")
st.write("支援雙 Logo、字體微調、隨機淺色背景與一鍵下載！")

col_input, col_preview = st.columns([1, 1.5])

with col_input:
    st.header("📝 填寫海報資訊")
    
    # --- 新增：背景色控制區塊 ---
    with st.expander("🎨 背景風格設定", expanded=True):
        st.write("點擊按鈕隨機更換背景氣氛 (已確保文字清晰度)")
        if st.button("🎲 隨機更換淺色背景"):
            st.session_state['bg_color1'] = generate_light_color()
            st.session_state['bg_color2'] = generate_light_color()
            st.rerun() # 強制重新執行以套用新顏色

    # Logo 區塊
    with st.expander("🖼️ 圖示設定", expanded=False):
        logo1_file = st.file_uploader("更換主辦單位 Logo (左上)", type=["png", "jpg", "jpeg"])
        logo2_file = st.file_uploader("更換校徽 Logo (左下)", type=["png", "jpg", "jpeg"])
        org_name = st.text_input("主辦單位補充名稱 (選填)", "")
    
    # 演講內容
    st.subheader("🗣️ 演講內容")
    topic = st.text_area("演講題目", "你的成功我的成功")
    speaker = st.text_input("演講者姓名", "好運到")
    position = st.text_input("職稱", "財富自由執行長")
    company = st.text_input("公司名稱", "錢一直來有限公司")
    
    # 時間與地點
    date_time = st.text_input("日期與時間", "115年2月23日 13:00-14:00")
    location = st.text_input("地點", "ST635")
    
    # 摘要與聯絡資訊
    summary = st.text_area("演講摘要", "東海大學創校於1955年，位於台中，是一所深具基督教背景、重視「博雅教育」的綜合性私立大學。以路思義教堂、文理大道及乳品小棧聞名，致力於培養具獨立思考、人文素養與社會關懷的「理想畢業生」。2026年《QS亞洲大學排名》顯示，東海大學在學術與創新方面榮登全台私立非醫學類大學第一名。")
    
    # 字體大小微調區塊
    st.divider()
    st.subheader("⚙️ 版面與字體微調")
    with st.expander("點此調整字體大小 (解決文字重疊)", expanded=False):
        title_size = st.slider("標題文字大小", 20, 80, 50)
        speaker_size = st.slider("講者文字大小", 15, 60, 32)
        info_size = st.slider("日期地點文字大小", 12, 40, 24)
        summary_size = st.slider("摘要文字大小", 10, 30, 18)
        line_height = st.slider("摘要行距", 1.0, 2.5, 1.6, 0.1)

    st.divider()
    st.subheader("📞 聯絡資訊")
    contact_name = st.text_input("聯絡人姓名", "王小明")
    contact_email = st.text_input("聯絡人信箱", "contact@thu.edu.tw")

with col_preview:
    st.header("👀 海報預覽與下載")
    
    # 讀取圖片
    b64_logo1 = get_image_base64(logo1_file, "thuLOGOHigh.png")
    b64_logo2 = get_image_base64(logo2_file, "Tunghai_Logo.png")
    
    logo1_html = f'<img src="data:image/png;base64,{b64_logo1}" style="height: 55px; margin-right: 15px;">' if b64_logo1 else ""
    logo2_html = f'<img src="data:image/png;base64,{b64_logo2}" style="height: 60px;">' if b64_logo2 else ""

    topic_html = topic.replace("\n", "<br>")
    org_html = org_name.replace("\n", "<br>")
    summary_html = summary.replace("\n", "<br><br>")

    # 取得目前的背景顏色狀態
    bg_c1 = st.session_state['bg_color1']
    bg_c2 = st.session_state['bg_color2']

    # 將動態變數注入 HTML 中
    poster_html = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    
    <div style="text-align: center; margin-bottom: 20px;">
        <button onclick="downloadPoster()" style="
            background-color: #FF4B4B; border: none; color: white; 
            padding: 12px 24px; text-align: center; text-decoration: none; 
            display: inline-block; font-size: 16px; margin: 4px 2px; 
            cursor: pointer; border-radius: 8px; font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;
        ">📥 點我下載海報 (PNG 高畫質)</button>
    </div>

    <div id="poster-area" style="
        width: 100%; 
        max-width: 600px; 
        aspect-ratio: 1 / 1.414;
        /* 使用較亮的基礎背景色 */
        background-color: #f8f8f8; 
        /* 將隨機產生的兩個淺色變數應用到漸層中 */
        background-image: 
            radial-gradient(circle at 70% 60%, {bg_c1} 0%, rgba(240,240,240,0) 60%), 
            radial-gradient(circle at 30% 80%, {bg_c2} 0%, rgba(240,240,240,0) 60%);
        padding: 40px; 
        box-sizing: border-box; 
        font-family: 'Microsoft JhengHei', sans-serif;
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin: auto;
        border: 1px solid #ddd;
        overflow: hidden;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            {logo1_html}
            <div style="font-weight: bold; font-size: 14px; line-height: 1.2; color: #333;">
                {org_html}
            </div>
        </div>

        <div style="font-size: {title_size}px; font-weight: 900; color: #6b2118; line-height: 1.2; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            {topic_html}
        </div>

        <div style="margin-bottom: 20px;">
            <span style="font-size: {speaker_size}px; font-weight: bold; color: #111;">{speaker}</span>
            <span style="font-size: {int(speaker_size*0.75)}px; font-weight: bold; color: #111; margin-left: 10px;">{position}</span><br>
            <span style="font-size: {int(speaker_size*0.7)}px; font-weight: bold; color: #111;">{company}</span>
        </div>
        
        <hr style="border: 0; border-top: 2px solid #555; margin-bottom: 15px;">

        <div style="font-size: {info_size}px; font-weight: bold; color: #6b2118; margin-bottom: 20px; line-height: 1.3;">
            {date_time}<br>
            {location}
        </div>

        <div style="font-size: {summary_size}px; font-weight: bold; color: #000; line-height: {line_height}; margin-left: 5px; margin-right: 5px;">
            {summary_html}
        </div>

        <div style="position: absolute; bottom: 30px; left: 40px; right: 40px; background-color: rgba(255,255,255,0.7); padding: 10px; border-radius: 10px;">
            <hr style="border: 0; border-top: 2px solid #555; margin-bottom: 10px; margin-top: 0;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    {logo2_html}
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 12px; color: #555; margin-bottom: 5px;">
                        聯絡人：{contact_name} | {contact_email}
                    </div>
                    <div style="font-size: 16px; font-weight: bold; color: #333;">
                        ！歡迎全校師生共同參與！
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
    function downloadPoster() {{
        const posterArea = document.getElementById("poster-area");
        html2canvas(posterArea, {{ scale: 2, useCORS: true }}).then(canvas => {{
            let link = document.createElement('a');
            link.download = '{speaker}_演講海報.png';
            link.href = canvas.toDataURL("image/png");
            link.click();
        }});
    }}
    </script>
    """

    # 增加預覽區高度
    st.components.v1.html(poster_html, height=1000, scrolling=True)