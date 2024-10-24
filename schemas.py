from pydantic import BaseModel, Field
from datetime import datetime


class QueryInput(BaseModel):
  question: str
  
class QueryOutput(BaseModel):
  query: str
  answer: str
  
class DocumentInfo(BaseModel):
  filename: str = 'Constitutiion of india'
  
