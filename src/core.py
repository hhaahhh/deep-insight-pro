import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 替换为 HuggingFace 的导入
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def process_pdf(file_path):
    # 1. 加载 PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # 2. 切分文档
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    # 3. 使用免费的本地嵌入模型 (无需 API Key)
    # 这个模型很小，普通电脑 CPU 也能秒开
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    # 4. 创建向量库
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    return vectorstore.as_retriever()