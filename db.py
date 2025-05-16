import sqlite3

DB_FILE = 'tag_data.db'


def init_db():
    """
    Khởi tạo database và bảng tags nếu chưa tồn tại
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS tags (
                  id TEXT PRIMARY KEY,
                  description TEXT,
                  last_cnt BIGINT,
                  last_seen TIMESTAMP
              )
              ''')
    conn.commit()
    conn.close()
