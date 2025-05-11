import streamlit as st
from streamlit.components.v1 import declare_component
import os

# 設定 custom component 位置（本地開發或 Streamlit Cloud）
my_component2 = declare_component(
    name="js_input_component",
    path="my_component/build"
)

# 取得前端傳來的值
value = my_component2()
st.write("接收到的 JS 傳值：", value)
