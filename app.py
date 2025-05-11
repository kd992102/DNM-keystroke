import streamlit as st
from streamlit.components.v1 import declare_component
import os

# 設定 custom component 位置（本地開發或 Streamlit Cloud）
_component_func = declare_component(
    "js_input_component",
    path=os.path.join(os.path.dirname(__file__), "my_component/frontend")
)

# 取得前端傳來的值
value = _component_func()
st.write("接收到的 JS 傳值：", value)
