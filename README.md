Deep-Insight Pro: 智能体辅助的增强型文档分析与搜索引擎
![alt text](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
<!-- 如果你部署了，放链接 -->
Deep-Insight Pro 是一款基于 DeepSeek-V3 和 LangGraph 开发的下一代智能分析工具。它突破了传统 RAG 的局限，通过智能体（Agent）的自主决策，能够根据问题的复杂程度，自动在“本地私有知识库”与“实时互联网搜索”之间进行动态切换和深度融合。
🚀 核心进化功能
🤖 动态路由智能体 (Dynamic Routing Agent)：采用 LangGraph 构建决策状态机。Agent 会自动分析用户意图：
若本地文档存在答案，执行本地向量检索。
若本地知识缺失或涉及实时信息（如：今天的天气、最新的融资），自动触发 Tavily AI 联网搜索。
🌐 实时情报获取：集成 Tavily Search API，使 AI 具备获取 2025 年最新信息的能力，彻底告别大模型的信息滞后性。
⚡ 混合架构模型：
LLM: DeepSeek-V3 (通过高效 API 调用)。
Embeddings: 本地运行 HuggingFace all-MiniLM-L6-v2，实现 0 成本、低延迟的向量化处理。
💎 工业级 UI/UX：
仿 Perplexity 的沉浸式对话界面。
实时展示 Agent 思考链（Thinking Process），通过 st.status 增强 AI 的可解释性。
🛠️ 技术栈
模块	技术实现
核心框架	LangChain / LangGraph (State Machine)
大语言模型	DeepSeek-V3
搜索增强	Tavily AI API
向量数据库	FAISS
嵌入模型	HuggingFace (Local CPU)
前端界面	Streamlit (Custom CSS)
📦 快速部署
环境克隆
code
Bash
git clone https://github.com/你的用户名/deep-insight-pro.git
cd deep-insight-pro
依赖安装
code
Bash
pip install -r requirements.txt
环境变量配置
在根目录创建 .env 文件：
code
Env
DEEPSEEK_API_KEY=你的_DEEPSEEK_KEY
DEEPSEEK_BASE_URL=https://api.deepseek.com
TAVILY_API_KEY=你的_TAVILY_KEY
启动应用
code
Bash
streamlit run app.py
🧠 系统架构图
code
Mermaid
graph TD
    A[用户提问] --> B{Agent 决策逻辑}
    B -- 本地文档匹配 --> C[FAISS 向量检索]
    B -- 知识缺失/实时需求 --> D[Tavily 联网搜索]
    C --> E[信息汇总与清洗]
    D --> E
    E --> F[DeepSeek-V3 推理生成]
    F --> G[最终回答呈现]