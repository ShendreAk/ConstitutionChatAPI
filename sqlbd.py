import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Depends
def get_db():
  try:
    conn = psycopg2.connect(database="constitutionChat", user="postgres", password="ABss1998", host="localhost", port=5432, cursor_factory=RealDictCursor)
    
    print("success")
  except Exception as error:
    print(error)
  return conn
  
  
def session_logs(db = Depends(get_db)):
  cursor = db.cursor()
  cursor.execute('create table if not exists session_logs (id serial PRIMARY KEY , session_id TEXT, query TEXT,response TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
  db.commit()

def insert_logs(session_id, query, response):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO session_logs (session_id, query, response) VALUES (%s,%s,%s)',
                 (session_id, query, response))
    conn.commit()

def fetch_chat_history(session_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT query, response FROM session_logs WHERE session_id = %s ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role": "human", "content": row['query']},
            {"role": "ai", "content": row['response']}
        ])
    return messages
  
if __name__ == "__main__":
  session_logs()
  insert_logs("1234","abcd","xyzmno")