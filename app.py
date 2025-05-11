import streamlit as st
from streamlit.components.v1 import html

# 使用 components.html() 直接插入原生 JS 傳值
html("""
    <button onclick="sendToStreamlit()">點我送資料</button>
    <script>
      function sendToStreamlit() {
        const msg = "Hello from raw JS!";
        window.parent.postMessage({
          isStreamlitMessage: true,
          type: "streamlit:setComponentValue",
          value: msg
        }, "*");
      }
    </script>
""", height=100)

# Streamlit 不會自動接收回傳值，所以你應該只顯示這段 HTML
st.info("請點上方按鈕測試 JS 傳值（目前不支援回傳值顯示）")