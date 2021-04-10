import sqlite3
from sqlite3.dbapi2 import connect

def log_table_init(db_name):
    # 初始化消息记录保存器
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE MESSAGES(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            timestamp INTEGER NOT NULL,
            is_user BOOLEAN NOT NULL,
            text TEXT
        );
        '''
    )
    conn.commit()
    conn.close()

def creation_table_init(db_name):
    # 初始化作曲系统进度表
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE CREATION(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            note_num INTEGER,
            note_var FLOAT,
            rhythm_var FLOAT,
            genre TEXT,
            keyword TEXT,
            melody_generated BOOLEAN,
            lyrics_generated BOOLEAN,
            state INTEGER
        );
        '''
    )
    conn.commit()
    conn.close()


def message_logging(db_name, session_id, timestamp, message, is_user, state):
    # 记录一条新消息
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # 预防SQL注入
    c.execute("INSERT INTO MESSAGES (session_id, timestamp, text, is_user, state) VALUES (?, ?, ?, ?, ?)",
              (session_id, timestamp, message, is_user, state))
    conn.commit()
    conn.close()

def creation_logging_new(db_name, session_id):
    # 创建一条新的creation table
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # 预防SQL注入
    c.execute("INSERT INTO CREATION (session_id, note_num, note_var, rhythm_var, genre, keyword, melody_generated, lyrics_generated, state) "
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (session_id, -1, -1, -1, "", "", False, False, 0))
    conn.commit()
    conn.close()   


def creation_logging_update(db_name, session_id, column_name, content):
    # 修改现有的creation table
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM CREATION WHERE id = ?", (session_id))
    # if len(c.fetchall()) == 0:
    #     new_creation_table_logging(db_name, session_id)
    # 预防SQL注入
    c.execute("UPDATE CREATION SET ? = ? where session_id = ?", (column_name, content, session_id))
    conn.commit()
    conn.close()

def check_table(db_name, table_name, session_id, column_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT ? FROM ? WHERE id = ?", (column_name, table_name, session_id))
    lines = c.fetchone()
    return lines[0]

# ===
# log_table_init(r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\log.sqlite3")
# creation_table_init(r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\log.sqlite3")

# 临时改动用代码
# conn = sqlite3.connect('log.sqlite3')
# c = conn.cursor()
# c.execute("ALTER TABLE MESSAGES ADD is_user BOOLEAN")
# conn.commit()
# conn.close()

# logging('log.sqlite3', 123, 1323,'12312321', True)

