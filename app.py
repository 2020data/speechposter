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

st.set_page_config(page_title="演講海報產生器", layout="wide")

# 處理圖片轉 Base64，支援上傳檔案與本地預設檔案
def get_image_base64(uploaded_file, default_local_path):
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
    else:
        # 如果沒有上傳，則嘗試讀取本地的預設圖檔
        try:
            img = Image.open(default_local_path)
        except FileNotFoundError:
            # 如果本地檔案不存在，回傳空字串防呆
            return "" 
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

st.title("🎨 演講海報產生器 (支援雙 Logo & 一鍵下載)")
st.write("在左側輸入資訊，右側將即時生成海報，並可直接下載為圖檔！")

col_input, col_preview = st.columns([1, 1.5])

with col_input:
    st.header("📝 填寫海報資訊")
    
    # Logo 區塊
    st.subheader("🖼️ 圖示設定")
    logo1_file = st.file_uploader("更換主辦單位 Logo (左上)", type=["png", "jpg", "jpeg"])
    logo2_file = st.file_uploader("更換校徽 Logo (左下)", type=["png", "jpg", "jpeg"])
    
    # 因為深耕計畫 Logo 已經自帶文字，預設將純文字名稱清空，以免重複
    org_name = st.text_input("主辦單位補充名稱 (選填)", "")
    
    st.divider()
    
    # 演講內容
    st.subheader("🗣️ 演講內容")
    topic = st.text_area("演講題目", "你的題目")
    speaker = st.text_input("演講者姓名", "演講帥哥或美女")
    position = st.text_input("職稱", "執行長")
    company = st.text_input("公司名稱", "富裕有限公司")
    
    # 時間與地點
    date_time = st.text_input("日期與時間", "115年 月 日 15:10-17:10")
    location = st.text_input("地點", "創藝學院 C214")
    
    # 摘要與聯絡資訊
    summary = st.text_area("演講摘要", "東海大學創校於1955年，位於台中，是一所深具基督教背景、重視「博雅教育」的綜合性私立大學。以路思義教堂、文理大道及乳品小棧聞名，致力於培養具獨立思考、人文素養與社會關懷的「理想畢業生」。2026年《QS亞洲大學排名》顯示，東海大學在學術與創新方面榮登全台私立非醫學類大學第一名。")
    
    st.divider()
    st.subheader("📞 聯絡資訊")
    contact_name = st.text_input("聯絡人姓名", "王小明")
    contact_email = st.text_input("聯絡人信箱", "contact@thu.edu.tw")

with col_preview:
    st.header("👀 海報預覽與下載")
    
    # 讀取圖片（請確認這兩個檔名與您存放於同資料夾的圖檔名稱一致）
    b64_logo1 = get_image_base64(logo1_file, "thuLOGOHigh.png")
    b64_logo2 = get_image_base64(logo2_file, "Tunghai_Logo.png")
    
    # 產生 Logo 的 HTML 標籤
    logo1_html = f'<img src="data:image/png;base64,{b64_logo1}" style="height: 55px; margin-right: 15px;">' if b64_logo1 else ""
    logo2_html = f'<img src="data:image/png;base64,{b64_logo2}" style="height: 80px;">' if b64_logo2 else ""

    topic_html = topic.replace("\n", "<br>")
    org_html = org_name.replace("\n", "<br>")
    summary_html = summary.replace("\n", "<br><br>")

    # 包含匯出功能的完整 HTML 結構
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
        background-color: #f0f0f0; 
        background-image: radial-gradient(circle at 70% 60%, rgba(255,200,200,0.4) 0%, rgba(240,240,240,0) 50%), radial-gradient(circle at 30% 80%, rgba(200,200,255,0.4) 0%, rgba(240,240,240,0) 50%);
        padding: 40px; 
        box-sizing: border-box; 
        font-family: 'Microsoft JhengHei', sans-serif;
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin: auto;
        border: 1px solid #ddd;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 30px;">
            {logo1_html}
            <div style="font-weight: bold; font-size: 16px; line-height: 1.2; color: #333;">
                {org_html}
            </div>
        </div>

        <div style="font-size: 55px; font-weight: 900; color: #6b2118; line-height: 1.2; margin-bottom: 30px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            {topic_html}
        </div>

        <div style="margin-bottom: 25px;">
            <span style="font-size: 32px; font-weight: bold; color: #111;">{speaker}</span>
            <span style="font-size: 24px; font-weight: bold; color: #111; margin-left: 10px;">{position}</span><br>
            <span style="font-size: 22px; font-weight: bold; color: #111;">{company}</span>
        </div>
        
        <hr style="border: 0; border-top: 2px solid #555; margin-bottom: 15px;">

        <div style="font-size: 24px; font-weight: bold; color: #6b2118; margin-bottom: 30px; line-height: 1.4;">
            {date_time}<br>
            {location}
        </div>

        <div style="font-size: 18px; font-weight: bold; color: #000; line-height: 1.6; margin-left: 10px;">
            {summary_html}
        </div>

        <div style="position: absolute; bottom: 30px; left: 40px; right: 40px;">
            <hr style="border: 0; border-top: 2px solid #555; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    {logo2_html}
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; color: #555; margin-bottom: 5px;">
                        聯絡人：{contact_name} | {contact_email}
                    </div>
                    <div style="font-size: 18px; font-weight: bold; color: #333;">
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

    st.components.v1.html(poster_html, height=900, scrolling=True)