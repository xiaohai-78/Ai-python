from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# 第一步：初始化模型对象：LLM，Embedding
llm = Ollama(model="qwen2:latest")
embeddings = OllamaEmbeddings(model="qwen2:latest")
question = "帮我总结论文内容"
response1 = llm.invoke(question)
print(f"检索前：{response1}\n")
# 第二步：获取数据
loader = WebBaseLoader("https://www.lamini.ai/blog/lamini-memory-tuning")
docs = loader.load()

# 第三步：文本拆分，文本Vector化
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

# 第四步：准备Prompt，创建文档处理的LLMChain，检索Chain
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain) #建立检索

# 第五步：代码执行与测试
response2 = document_chain.invoke({
    "input": question,
    "context": [Document(page_content=question)]
})
print(f"检索前（运行测试）：{response2}\n")

response3 = retrieval_chain.invoke({"input": question})
print(f"检索后：{response3['answer']}")
