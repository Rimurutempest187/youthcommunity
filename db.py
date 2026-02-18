# db.py
import aiosqlite
import json
import os
from datetime import datetime

DB_PATH = os.path.join("data", "bot.db")
os.makedirs("data", exist_ok=True)

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    score INTEGER DEFAULT 0,
    created_at TEXT
);
"""

CREATE_GROUPS = """
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    title TEXT,
    added_at TEXT
);
"""

CREATE_QUIZZES = """
CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    options TEXT,
    answer_letter TEXT,
    difficulty TEXT,
    created_at TEXT
);
"""

CREATE_VERSES = """
CREATE TABLE IF NOT EXISTS verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    created_at TEXT
);
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_USERS)
        await db.execute(CREATE_GROUPS)
        await db.execute(CREATE_QUIZZES)
        await db.execute(CREATE_VERSES)
        await db.commit()

# Users
async def get_or_create_user(uid: int, name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id, name, score FROM users WHERE id = ?", (uid,))
        row = await cur.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "score": row[2]}
        now = datetime.utcnow().isoformat()
        await db.execute("INSERT INTO users(id,name,score,created_at) VALUES(?,?,?,?)", (uid, name, 0, now))
        await db.commit()
        return {"id": uid, "name": name, "score": 0}

async def increment_user_score(uid: int, delta: int = 1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET score = score + ? WHERE id = ?", (delta, uid))
        await db.commit()
        cur = await db.execute("SELECT score FROM users WHERE id = ?", (uid,))
        row = await cur.fetchone()
        return row[0] if row else None

async def get_leaderboard(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id, name, score FROM users ORDER BY score DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return [{"id": r[0], "name": r[1], "score": r[2]} for r in rows]

# Groups
async def add_group_if_not_exists(gid: int, title: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id FROM groups WHERE id = ?", (gid,))
        if await cur.fetchone():
            return
        now = datetime.utcnow().isoformat()
        await db.execute("INSERT INTO groups(id,title,added_at) VALUES(?,?,?)", (gid, title, now))
        await db.commit()

async def get_all_group_ids():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id FROM groups")
        rows = await cur.fetchall()
        return [r[0] for r in rows]

# Quizzes
async def insert_quiz(question: str, options: dict, answer_letter: str, difficulty: str = "normal"):
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.utcnow().isoformat()
        await db.execute(
            "INSERT INTO quizzes(question,options,answer_letter,difficulty,created_at) VALUES(?,?,?,?,?)",
            (question, json.dumps(options, ensure_ascii=False), answer_letter, difficulty, now)
        )
        await db.commit()

async def get_random_quiz():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id, question, options, answer_letter FROM quizzes ORDER BY RANDOM() LIMIT 1")
        row = await cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "question": row[1],
            "options": json.loads(row[2]),
            "answer_letter": row[3]
        }

# Verses
async def insert_verse(text: str):
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.utcnow().isoformat()
        await db.execute("INSERT INTO verses(text,created_at) VALUES(?,?)", (text, now))
        await db.commit()

async def get_random_verse():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT text FROM verses ORDER BY RANDOM() LIMIT 1")
        row = await cur.fetchone()
        return row[0] if row else None

# Migration helpers
async def import_quizzes_from_json(path: str):
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    count = 0
    for q in data:
        options = q.get("options")
        if isinstance(options, list):
            letters = ["A", "B", "C", "D"]
            opts = {letters[i]: options[i] for i in range(min(len(options), 4))}
        else:
            opts = options
        await insert_quiz(q.get("question"), opts, q.get("answer_letter", "A"), q.get("difficulty", "normal"))
        count += 1
    return count

async def import_verses_from_json(path: str):
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for v in data:
        await insert_verse(v)
    return len(data)
