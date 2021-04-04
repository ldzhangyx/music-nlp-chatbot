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
            emotion TEXT,
            topic TEXT,
            content TEXT,
            melody TEXT,
            chord TEXT,
            drum TEXT,
            acc TEXT,
            lyrics TEXT 
        );
        '''
    )
    conn.commit()
    conn.close()


def message_logging(db_name, session_id, timestamp, message, is_user):
    # 记录一条新消息
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # 预防SQL注入
    c.execute("INSERT INTO MESSAGES (session_id, timestamp, text, is_user) VALUES (?, ?, ?, ?)", (session_id, timestamp, message, is_user))
    conn.commit()
    conn.close()

def new_creatiob_table_logging(db_name, session_id):
    # 创建一条新的creation table
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # 预防SQL注入
    c.execute("INSERT INTO CREATION (session_id) VALUES (?)", (session_id))
    conn.commit()
    conn.close()   

def creation_table_logging(db_name, session_id, column_name, content):
    # 修改现有的creation table
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM CREATION WHERE id = ?", (session_id))
    if len(c.fetchall()) == 0:
        new_creatiob_table_logging(db_name, session_id)
    # 预防SQL注入
    c.execute("UPDATE CREATION SET ? = ? where session_id = ?", (column_name, content, session_id))
    conn.commit()
    conn.close()   


# ===
# log_table_init('log.sqlite3')

# 临时改动用代码
# conn = sqlite3.connect('log.sqlite3')
# c = conn.cursor()
# c.execute("ALTER TABLE MESSAGES ADD is_user BOOLEAN")
# conn.commit()
# conn.close()

# logging('log.sqlite3', 123, 1323,'12312321', True)

