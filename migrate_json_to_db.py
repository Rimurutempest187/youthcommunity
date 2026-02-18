# migrate_json_to_db.py
import asyncio
import os
import json
from db import init_db, import_quizzes_from_json, import_verses_from_json

async def migrate():
    await init_db()
    base = "data"
    qpath = os.path.join(base, "quizzes.json")
    vpath = os.path.join(base, "verses.json")
    qcount = await import_quizzes_from_json(qpath)
    vcount = await import_verses_from_json(vpath)
    print(f"Imported {qcount} quizzes and {vcount} verses.")

if __name__ == "__main__":
    asyncio.run(migrate())
