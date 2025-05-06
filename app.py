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

# --- 說明與知情同意 ---
st.markdown("""
## 📄 實驗說明與參與者同意
我們正在進行一項關於「打字行為與使用者辨識」的機器學習實驗。過程中會紀錄：
- 每個鍵的按下與放開時間
- 您的基本背景資料（匿名）
- 所輸入的特定句子

✅ 不會蒐集任何可識別身分的資訊。資料僅用於課程報告，並遵守個資法與學術研究倫理。

請勾選下方同意後再開始填寫。
""")

consent = st.checkbox("我已閱讀說明並同意參與研究")
if not consent:
    st.stop()
else:
    listen = st_javascript("startListening();")
    if listen:
        st.success("已開始監聽")

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
if "keylog_data" not in st.session_state:
    st.session_state.keylog_data = []

# 加在 st.markdown(...) 輸入區那裡
st.markdown("""
<textarea id="inputArea" rows="4" style="width:100%; font-size:20px;" placeholder="請輸入上方句子..."></textarea>
<script>
  const log = [];
  let input = null;
  let keydownHandler = null;
  let keyupHandler = null;

  function startListening() {
    input = document.getElementById("inputArea");
    if (!input) return;

    keydownHandler = e => log.push({ key: e.key, type: 'down', time: Date.now() });
    keyupHandler = e => log.push({ key: e.key, type: 'up', time: Date.now() });

    input.addEventListener('keydown', keydownHandler);
    input.addEventListener('keyup', keyupHandler);
    console.log("📝 keylog:", log);
  }

  function stopListeningAndSend() {
    console.log("📝 keylog:", log);
    if (input && keydownHandler && keyupHandler) {
      input.removeEventListener('keydown', keydownHandler);
      input.removeEventListener('keyup', keyupHandler);
    }
    console.log("📝 keylog:", log);
    const event = new CustomEvent("streamlit:keystrokeData", {
      detail: JSON.stringify(log)
    });
    window.dispatchEvent(event);
    console.log("🚀 stopListeningAndSend() triggered");
  }
</script>
""", unsafe_allow_html=True)


# --- 解碼 query_params 並儲存 keylog ---
# 接收前端傳來的 keylog
if st.button("📩 接收按鍵紀錄"):
    result = st_javascript("""
    new Promise((resolve) => {
        window.addEventListener("streamlit:keystrokeData", (event) => {
        resolve(event.detail);
        }, { once: true });
        stopListeningAndSend();  // 這個觸發事件
    });
    """)
    st.write("結果：", result)
    if result:
        try:
            parsed = json.loads(result)
            st.success("✅ 已接收按鍵資料")
            # save_keylog_to_sheet2(user_id, parsed)
        except Exception as e:
            st.error(f"❌ 無法解析按鍵資料：{e}")
    else:
        st.warning("⚠️ 沒有收到任何按鍵紀錄")

# --- 寫入 Google Sheet ---
def save_to_gsheet(record: dict):
    try:
        info = json.loads(st.secrets["GOOGLE_SHEET_CREDENTIALS"])
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
        client = gspread.authorize(creds)
        sheet = client.open("DNM-keystroke-log").sheet1

        ordered = [
            record["user_id"],
            record["gender"],
            record["age"],
            record["education"],
            record["dominant_hand"],
            record["typing_exp"],
            record["device_type"],
            record["sentence"],
            record["timestamp"]
        ]
        sheet.append_row(ordered)
        st.success("✅ 背景資料已成功寫入 Google Sheet！")
    except Exception as e:
        st.error(f"❌ Google Sheet 寫入失敗：{e}")

# --- 送出資料 ---
if st.button("📤 送出資料"):
    st.markdown("⏳ 資料傳送中...")
    st.query_params.clear()

    user_profile = {
        "user_id": user_id,
        "gender": gender,
        "age": age,
        "education": education,
        "dominant_hand": dominant_hand,
        "typing_exp": typing_exp,
        "device_type": device_type,
        "sentence": sentence,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    st.json(user_profile)
    save_to_gsheet(user_profile)

    st.download_button(
        label="⬇ 下載背景資料 JSON",
        file_name="user_profile.json",
        mime="application/json",
        data=json.dumps(user_profile, ensure_ascii=False)
    )

    '''if st.session_state.keylog_data:
        st.download_button(
            label="⬇ 下載 keystroke log JSON",
            file_name="keystroke_log.json",
            mime="application/json",
            data=json.dumps(st.session_state.keylog_data, ensure_ascii=False)
        )'''

st.markdown("---")
st.caption("專題名稱：DNM-keystroke | Powered by Streamlit")
