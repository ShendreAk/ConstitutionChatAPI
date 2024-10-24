import os
import openai

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain_ollama import ChatOllama

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_DEPLOYMENT_ENDPOINT')
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv('OPENAI_DEPLOYMENT_VERSION')



# llm = AzureChatOpenAI(deployment_name="gpt-35-turbo", temperature=0.5,streaming=True,openai_api_version="2023-05-15", openai_api_key=openai.api_key,  openai_api_base="https://swapai-prod01.openai.azure.com/" )
llm = ChatOllama(model="llama3.2",
    temperature=0,)
embedding_dir = '/Users/akshayshendre/Desktop/rag_fastapi/embeddings'

model_id = 'sentence-transformers/all-MiniLM-L6-v2'
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(
    model_name=model_id,
    model_kwargs=model_kwargs
)
vectordb = FAISS.load_local(embedding_dir, embeddings)

def llm_chain(input):
  question_gen_system_template = (
    "Given a chat history and the current user question which might be referencing to the context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, "
    "if current user question do not reference to the chat history just reformulate it if needed and otherwise return as it is.")

  q_prompt = ChatPromptTemplate.from_messages([
    ("system", question_gen_system_template),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")])
  
  qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professor of political science in india and have very firm understanding of indian constitution. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")])
  
  
  history_aware_retriever = create_history_aware_retriever(
    llm, vectordb, q_prompt)
  question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
  
  chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
  
  return chain
  
  
  