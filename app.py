# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:32:19 2026

@author: e010
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:32:19 2026

@author: e010
"""
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import random
import sqlite3
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="演講海報產生器", layout="wide")

# ==========================================
# 資料庫功能 (SQLite)
# ==========================================
DB_NAME = "posters.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            speaker TEXT,
            position TEXT,
            company TEXT,
            date_time TEXT,
            location TEXT,
            summary TEXT,
            contact_name TEXT,
            contact_email TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(topic, speaker, position, company, date_time, location, summary, contact_name, contact_email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO posters 
        (topic, speaker, position, company, date_time, location, summary, contact_name, contact_email, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, speaker, position, company, date_time, location, summary, contact_name, contact_email, now))
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM posters ORDER BY id DESC", conn)
    conn.close()
    return df

def get_record_by_id(record_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM posters WHERE id=?", (record_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# 啟動時初始化資料庫
init_db()

# ==========================================
# 狀態管理與 Callback 函數
# ==========================================
# 背景色
if 'bg_color1' not in st.session_state:
    st.session_state['bg_color1'] = "rgba(255,200,200,0.4)"
if 'bg_color2' not in st.session_state:
    st.session_state['bg_color2'] = "rgba(200,200,255,0.4)"

# 表單預設值初始化
default_form_values = {
    'form_org_name': "",
    'form_topic': "你的成功我的成功",
    'form_speaker': "好運到",
    'form_position': "財富自由執行長",
    'form_company': "錢一直來有限公司",
    'form_date_time': "115年2月23日 13:00-14:00",
    'form_location': "ST635",
    'form_summary': "東海大學創校於1955年，位於台中，是一所深具基督教背景、重視「博雅教育」的綜合性私立大學。以路思義教堂、文理大道及乳品小棧聞名，致力於培養具獨立思考、人文素養與社會關懷的「理想畢業生」。2026年《QS亞洲大學排名》顯示，東海大學在學術與創新方面榮登全台私立非醫學類大學第一名。",
    'form_contact_name': "王小明",
    'form_contact_email': "contact@thu.edu.tw"
}
for k, v in default_form_values.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- 修正核心：將載入動作寫成 Callback 函數 ---
def load_record_callback():
    selected_option = st.session_state['history_selector']
    if selected_option:
        selected_id = int(selected_option.split(" - ")[0])
        record = get_record_by_id(selected_id)
        if record:
            st.session_state['form_topic'] = record['topic']
            st.session_state['form_speaker'] = record['speaker']
            st.session_state['form_position'] = record['position']
            st.session_state['form_company'] = record['company']
            st.session_state['form_date_time'] = record['date_time']
            st.session_state['form_location'] = record['location']
            st.session_state['form_summary'] = record['summary']
            st.session_state['form_contact_name'] = record['contact_name']
            st.session_state['form_contact_email'] = record['contact_email']

# 其他輔助函數
def generate_light_color():
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)
    return f"rgba({r},{g},{b},0.5)"

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

# ==========================================
# 網頁介面 UI
# ==========================================
st.title("🎨 演講海報產生器 (支援歷史紀錄回填)")
st.write("支援雙 Logo、字體微調、隨機淺色背景、歷史紀錄儲存與一鍵回填！")

col_input, col_preview = st.columns([1, 1.5])

with col_input:
    st.header("📝 填寫海報資訊")
    
    with st.expander("🎨 背景風格設定", expanded=False):
        st.write("點擊按鈕隨機更換背景氣氛")
        if st.button("🎲 隨機更換淺色背景"):
            st.session_state['bg_color1'] = generate_light_color()
            st.session_state['bg_color2'] = generate_light_color()
            st.rerun()

    with st.expander("🖼️ 圖示設定", expanded=False):
        logo1_file = st.file_uploader("更換主辦單位 Logo (左上)", type=["png", "jpg", "jpeg"])
        logo2_file = st.file_uploader("更換校徽 Logo (左下)", type=["png", "jpg", "jpeg"])
        org_name = st.text_input("主辦單位補充名稱 (選填)", key='form_org_name')
    
    st.subheader("🗣️ 演講內容")
    topic = st.text_area("演講題目", key='form_topic')
    speaker = st.text_input("演講者姓名", key='form_speaker')
    position = st.text_input("職稱", key='form_position')
    company = st.text_input("公司名稱", key='form_company')
    
    date_time = st.text_input("日期與時間", key='form_date_time')
    location = st.text_input("地點", key='form_location')
    
    summary = st.text_area("演講摘要", key='form_summary')
    
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
    contact_name = st.text_input("聯絡人姓名", key='form_contact_name')
    contact_email = st.text_input("聯絡人信箱", key='form_contact_email')

    # --- 資料庫儲存與讀取區塊 ---
    st.divider()
    st.subheader("💾 資料庫操作")
    
    # 儲存按鈕
    if st.button("📥 將以上資訊存入資料庫", type="primary"):
        save_to_db(topic, speaker, position, company, date_time, location, summary, contact_name, contact_email)
        st.success(f"✅ 已成功儲存講者「{speaker}」的海報資訊！")
        
    # 查看與回填歷史紀錄
    with st.expander("🗂️ 查看與回填歷史紀錄", expanded=True):
        df_history = load_from_db()
        if not df_history.empty:
            options = df_history['id'].astype(str) + " - " + df_history['speaker'] + " : " + df_history['topic']
            # 給下拉選單綁定 key
            st.selectbox("選擇要載入的紀錄", options, key='history_selector')
            
            # 使用 on_click 觸發 callback，完美避開元件渲染順序問題
            st.button("🔄 載入此紀錄並回填表單", on_click=load_record_callback)
            
            st.write("▼ 資料庫詳細紀錄預覽：")
            st.dataframe(df_history, use_container_width=True, hide_index=True)
        else:
            st.info("目前資料庫中還沒有紀錄喔！請先儲存一筆試試看。")

with col_preview:
    st.header("👀 海報預覽與下載")
    
    b64_logo1 = get_image_base64(logo1_file, "thuLOGOHigh.png")
    b64_logo2 = get_image_base64(logo2_file, "Tunghai_Logo.png")
    
    logo1_html = f'<img src="data:image/png;base64,{b64_logo1}" style="height: 55px; margin-right: 15px;">' if b64_logo1 else ""
    logo2_html = f'<img src="data:image/png;base64,{b64_logo2}" style="height: 60px;">' if b64_logo2 else ""

    topic_html = topic.replace("\n", "<br>")
    org_html = org_name.replace("\n", "<br>")
    summary_html = summary.replace("\n", "<br><br>")

    bg_c1 = st.session_state['bg_color1']
    bg_c2 = st.session_state['bg_color2']

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
        background-color: #f8f8f8; 
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

    st.components.v1.html(poster_html, height=1000, scrolling=True)