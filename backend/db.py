import sqlite3

conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        session_id TEXT,
        question TEXT,
        answer TEXT
    )
''')
conn.commit()

def save_chat(session_id, question, answer):
    cursor.execute("INSERT INTO chats (session_id, question, answer) VALUES (?, ?, ?)",
                   (session_id, question, answer))
    conn.commit()

def get_chat_history(session_id, limit=10):
    cursor.execute("SELECT question, answer FROM chats WHERE session_id=? ORDER BY ROWID DESC LIMIT ?", 
                   (session_id, limit))
    return cursor.fetchall()[::-1]
