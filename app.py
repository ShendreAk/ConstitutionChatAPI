from fastapi import Fastapi, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from . import schemas
from .llm_utils import llm_chain
import uuid
from .sqlbd import fetch_chat_history, insert_logs
#logging
logging.basicConfig(filename='app.log',level=logging.INFO)

app = Fastapi()

# middleware
origins = ["*"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True,
)

@app.get("/")
def root():
  return { "message": "Welcome to ConstitutionChat"}

@app.post("/chat", response_model = schemas.QueryOutput)
def chat(query: schemas.QueryInput):
  
  session_id = str(uuid.uuid4())
  logging.info(f"query:{query.question}, session_id: {session_id}")
  
  chat_history = fetch_chat_history(session_id)
  
  chain = llm_chain()
  answer = chain.invoke({
    "input": query.question,
    "chat_history": chat_history
  })['answer']
  insert_logs(session_id, query.question, answer),
  
  logging.info(f" query:{query.question}, query_response:{answer}, session_id: {session_id}")
  return {"query":query.question, "answer" : answer }