import streamlit as st
import pandas as pd
import time
import uuid
import json
import base64
import urllib.parse
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Keystroke Dynamics Study", layout="centered")

# --- 背景資料填寫 ---
st.markdown("## 👤 基本資料填寫")
col1, col2 = st.columns(2)
with col1:
    gender = st.radio("性別", ["男", "女", "不透露"])
    age = st.selectbox("年齡區間", ["18-24", "25-34", "35-44", "45+"])
    education = st.selectbox("最高學歷", ["高中", "大學", "碩士", "博士"])
with col2:
    dominant_hand = st.radio("慣用手", ["左手", "右手", "雙手皆可"])
    typing_exp = st.selectbox("每日打字時間", ["<1 小時", "1-3 小時", ">3 小時"])
    device_type = st.selectbox("目前使用的裝置", ["手機", "平板", "筆電", "桌機"])

user_id = str(uuid.uuid4())[:8]
sentence = "我每天都會使用電腦打字處理工作"
st.markdown("---")
st.markdown(f"## ✍️ 請輸入下列句子：\n\n**{sentence}**")

# --- 用 session_state 儲存 keylog base64 傳回資料 ---
# 加在 st.markdown(...) 輸入區那裡


# --- 解碼 query_params 並儲存 keylog ---
# 接收前端傳來的 keylog
def js_code():  
    return """  
    <script>   
        function returnNumber() {  
            return 2;  
        }  
        const result = returnNumber();  
        window.parent.postMessage(result, "*");  
    </script>   
    """  

# Displaying HTML + JS in Streamlit and capturing response  
response = st.empty()  
components.html(js_code(), height=0)  

# Using JavaScript listener to capture the returned value  
st.write("Waiting for JavaScript response...")  

# Listening for the message event from JavaScript  
@st.cache_data  
def listen_for_js_message(data):  
    response.write(f"JavaScript returned: {data}")
st.caption("專題名稱：DNM-keystroke | Powered by Streamlit")
