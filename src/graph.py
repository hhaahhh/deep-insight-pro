import os
from typing import List, TypedDict, Annotated
from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient

# 初始化工具
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model='deepseek-chat', openai_api_key=os.getenv("DEEPSEEK_API_KEY"), openai_api_base=os.getenv("DEEPSEEK_BASE_URL"))

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    use_web_search: bool # 新增：标记是否需要联网

def retrieve(state: GraphState, retriever):
    print("--- 检索本地知识库 ---")
    question = state["question"]
    documents = retriever.invoke(question)
    
    # 逻辑判断：如果检索到的内容太少或不相关，标记需要联网搜索
    use_web_search = False
    if len(documents) == 0 or len(documents[0].page_content) < 50:
        use_web_search = True
        
    return {"documents": documents, "question": question, "use_web_search": use_web_search}

def web_search(state: GraphState):
    print("--- 联网搜索中 ---")
    question = state["question"]
    # 调用 Tavily 搜索最新信息
    search_result = tavily.search(query=question, max_results=3)
    search_content = "\n".join([f"来源: {r['url']}\n内容: {r['content']}" for r in search_result['results']])
    
    return {"documents": [search_content], "question": question}

def generate(state: GraphState):
    print("--- 生成最终回答 ---")
    question = state["question"]
    documents = state["documents"]
    
    prompt = ChatPromptTemplate.from_template("""
    你是一个全能的文档分析与搜索助手。
    根据以下参考资料（可能是文档片段或搜索结果）回答问题。
    如果参考资料不足以回答，请根据你已有的知识回答并说明。
    
    资料来源：{context}
    
    用户问题：{question}
    """)
    chain = prompt | llm
    response = chain.invoke({"context": documents, "question": question})
    return {"generation": response.content}

# 构建有决策逻辑的图
def create_workflow(retriever):
    workflow = StateGraph(GraphState)
    
    workflow.add_node("retrieve", lambda state: retrieve(state, retriever))
    workflow.add_node("web_search", web_search)
    workflow.add_node("generate", generate)
    
    workflow.set_entry_point("retrieve")
    
    # 设置条件分支：如果 use_web_search 为 True，走 web_search 节点
    workflow.add_conditional_edges(
        "retrieve",
        lambda x: "web_search" if x["use_web_search"] else "generate",
        {
            "web_search": "web_search",
            "generate": "generate"
        }
    )
    
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()