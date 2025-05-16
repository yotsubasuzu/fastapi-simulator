import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from db import DB_FILE

app = FastAPI()


class TagRegister(BaseModel):
    id: str
    description: str


class TagState(BaseModel):
    id: str
    description: str
    last_cnt: int
    last_seen: Optional[datetime] = None


def get_db():
    return sqlite3.connect(DB_FILE)


@app.post("/tags")
def register_tag(tag: TagRegister):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO tags(id, description, last_cnt, last_seen) VALUES(?,?,?,?)',
            (tag.id, tag.description, 0, None)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Tag already registered")
    conn.close()
    return {"message": "Tag registered"}


@app.get("/tags")
def get_tags():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, description, last_cnt, last_seen FROM tags')
    rows = c.fetchall()
    result = []
    for id, desc, last_cnt, last_seen in rows:
        result.append(TagState(
            id=id,
            description=desc,
            last_cnt=last_cnt,
            last_seen=datetime.fromisoformat(last_seen) if last_seen else None
        ))
    conn.close()
    return result


@app.get("/tag/{tag_id}")
def get_tag(tag_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, description, last_cnt, last_seen FROM tags WHERE id=?', (tag_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Tag not found")
    id, desc, last_cnt, last_seen = row
    return TagState(
        id=id,
        description=desc,
        last_cnt=last_cnt,
        last_seen=datetime.fromisoformat(last_seen) if last_seen else None
    )


@app.get("/health")
def health():
    return {"status": "ok"}
