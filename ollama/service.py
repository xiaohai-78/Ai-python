from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

def send(str):
    promptStr = (
                "你是一名资深的新闻撰稿人，接下来你的工作是将我给你的文章起一个20字以内标题。然后将内容进行压缩同时需要尽量不丢失新闻中的主体，时间，地点等重要信息，字数控制在200字以内。请你以Json格式的内容给我返回信息。如：{\"title\":\"标题\",\"context\":\"内容\"}。需要以Json格式返回信息"
             + str)
    # 第一步：初始化模型对象：LLM，Embedding
    llm = Ollama(model="qwen2:latest")
    # embeddings = OllamaEmbeddings(model="qwen2:latest")
    response1 = llm.invoke(promptStr)
    print(f"ollama: {response1}\n")
    return response1