import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from src.core import process_pdf
from src.graph import create_workflow

# 1. 页面样式美化 (注入一点 CSS)
st.set_page_config(page_title="Deep-Insight Pro", layout="wide", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { font-size: 3rem !important; font-weight: 800; color: #1E1E1E; text-align: center; margin-bottom: 2rem; }
    .stChatMessage { border-radius: 15px; padding: 20px; margin-bottom: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True) # 修正为 html

# 2. 侧边栏美化
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("Deep-Insight Pro")
    st.markdown("---")
    uploaded_file = st.file_uploader("📥 上传参考文档 (PDF)", type="pdf")
    if st.button("🗑️ 清除聊天记录"):
        st.session_state.messages = []
        st.rerun()

# 3. 主界面
st.markdown('<div class="main-title">AI 智能深度分析</div>', unsafe_allow_html=True) # 修正为 html

# 初始化逻辑
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 输入框
if prompt := st.chat_input("您可以向我提问，我会自动结合文档与互联网进行分析..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 使用 st.status 展示 Agent 的思考过程 (非常自然且专业)
        with st.status("🔍 正在思考...", expanded=True) as status:
            # 如果没上传文件，我们需要一个默认的检索器（可以做个空的或全局的）
            # 这里简单处理：如果没上传，跳过 retrieve 逻辑直接联网
            if uploaded_file:
                temp_path = "temp.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.write("📖 正在扫描本地文档...")
                retriever = process_pdf(temp_path)
            else:
                st.write("🌐 未检测到本地文档，准备联网搜索...")
                # 这里可以创建一个空的 retriever 模拟逻辑
                retriever = None 

            st.write("🧠 正在规划搜索路径...")
            
            # 运行 Graph
            # 注意：这里需要处理没有 retriever 的情况
            if retriever:
                app = create_workflow(retriever)
                result = app.invoke({"question": prompt})
            else:
                # 如果没文件，直接调用搜索
                from src.graph import web_search
                result = web_search({"question": prompt})
                # 再次用 LLM 总结结果
                from src.graph import generate
                result = generate({"documents": result["documents"], "question": prompt})

            status.update(label="✨ 分析完成！", state="complete", expanded=False)
            
        response = result["generation"]
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})