import os
import pandas as pd
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredURLLoader,Docx2txtLoader, UnstructuredFileLoader
from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter, CharacterTextSplitter
model_id = 'sentence-transformers/all-MiniLM-L6-v2'
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(
    model_name=model_id,
    model_kwargs=model_kwargs
)

def doc_process():
  documents =[]
  for file in os.listdir('/Users/akshayshendre/Desktop/rag_fastapi/data/'):
      if file.endswith('.pdf'):
          pdf_path = '/Users/akshayshendre/Desktop/rag_fastapi/data/' + file
          print(pdf_path)
          loader = PyPDFLoader(pdf_path)
          documents.extend(loader.load())
      else:
          pass
  text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
  documents = text_splitter.split_documents(documents)
  return documents

docs = doc_process()
embedding_dir = '/Users/akshayshendre/Desktop/rag_fastapi/embeddings'
vectordb = FAISS.from_documents(docs, embeddings)
vectordb.save_local(embedding_dir)