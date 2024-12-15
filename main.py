import streamlit as st
import os
from utils import generate_script

st.title("视频脚本生成器")

subject = st.text_input("请输入视频的主题: ")
video_length = st.number_input("请输入视频时长: ", min_value=0.1, value=0.5, step=0.1)
creativity = st.slider("请选择创造力（数字越小越严谨，数字越大越多样）: ", min_value=0.0, max_value=1.0, step=0.1, value=0.2)

submit = st.button("生成脚本")
openai_api_key=os.getenv("OPENAI_API_KEY")

# 提交按钮事件处理：
# 1. 没有APIKEY
# 2. 没有输入主题
# 3. 正常运行
if submit and not openai_api_key:
    st.info("请先设置 OPENAI_API_KEY 环境变量")
    st.stop()  # 后面的代码不再执行
if submit and not subject:
    st.info("请输入视频主题")
    st.stop()
if submit:
    with st.spinner(("AI正在思考中，请稍候...")):  # 显示加载动画
        title, script = generate_script(subject, video_length, creativity, openai_api_key)
    st.success("AI已经生成脚本啦，快去复制吧！")
    st.subheader("标题")
    st.write(title)
    st.subheader("视频脚本")
    st.write(script)


