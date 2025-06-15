import streamlit as st
from utils2 import generate_script

# sidebar
with st.sidebar:
    api_key = st.text_input("请输入阿里云百炼的API密钥：", type="password")
    st.markdown("[如何获取阿里云百炼的API密钥?](https://bailian.console.aliyun.com/?tab=model#/api-key)")

# main_body
st.title("🎬视频脚本生成器")
subject = st.text_input("主题：")
video_length = st.slider("视频时长(单位:分钟)：", min_value=0.1, max_value=10.0, value=5.0, step=0.1)
creativity = st.slider("创造力(数字小说明更严谨，数字大说明更多样)：", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
submit = st.button("生成脚本")

# loading
if submit:
    if not api_key:
        st.info("请输入你的阿里云百炼 API密钥")
        st.stop()
    if not subject:
        st.info("请输入视频的主题")
        st.stop()
    if not video_length >= 0.1:
        st.info("视频长度需要大于或等于0.1")
        st.stop()
    else:
        with st.spinner("AI正在思考中，请稍等..."):
            search_result, title, script = generate_script(subject, video_length, creativity, api_key)
            st.success("视频脚本已生成！")

        st.divider()

        column1,column2 = st.columns([1,2])
        with column1:
            st.write("🔥 标题：")
            st.write(title)
        with column2:
            st.write("📝 视频脚本：")
            st.write(script)

        st.divider()

        with st.expander("维基百科搜索结果 👀"):
            st.info(search_result)