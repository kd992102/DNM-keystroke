import streamlit as st
from streamlit.components.v1 import html

# 使用 components.html() 直接插入原生 JS 傳值
value = html(
    """
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
    """,
    height=100,
    key="simple_js"
)

st.write("JS 傳回的值是：", value)