import sqlite3
from datetime import datetime
from db import init_db, DB_FILE


def process_log_line(line: str) -> None:
    """
    Xử lý một dòng log "TAG,<tag_id>,<cnt>,<timestamp>"
    Cập nhật SQLite DB nếu cnt thay đổi
    """
    try:
        prefix, tag_id, cnt_str, ts_str = line.strip().split(',')
        if prefix != 'TAG':
            return
        cnt = int(cnt_str)
        timestamp = datetime.strptime(ts_str, '%Y%m%d%H%M%S.%f')
        ts_iso = timestamp.isoformat()
    except Exception as e:
        print(f"Failed to parse line: {e}")
        return

    conn = sqlite3.connect(DB_FILE)
    init_db()
    c = conn.cursor()
    c.execute('SELECT last_cnt FROM tags WHERE id=?', (tag_id,))
    row = c.fetchone()
    if row:
        last_cnt = row[0] or 0
        if cnt != last_cnt:
            print(f"Tag {tag_id} cnt changed from {last_cnt} to {cnt} at {ts_iso}")
            c.execute(
                'UPDATE tags SET last_cnt=?, last_seen=? WHERE id=?',
                (cnt, ts_iso, tag_id)
            )
            conn.commit()
    conn.close()