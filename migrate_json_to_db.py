# migrate_json_to_db.py
import asyncio
import logging
from pathlib import Path
from db import init_db, import_quizzes_from_json, import_verses_from_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
DATA_DIR = Path(__file__).parent / "data"
QUIZZES_PATH = DATA_DIR / "quizzes.json"
VERSES_PATH = DATA_DIR / "verses.json"

async def migrate():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Initializing database (creating tables if needed)...")
    await init_db()
    qcount = 0
    vcount = 0
    if QUIZZES_PATH.exists():
        logging.info("Found quizzes file: %s", QUIZZES_PATH)
        qcount = await import_quizzes_from_json(str(QUIZZES_PATH))
        logging.info("Imported %d quizzes.", qcount)
    else:
        logging.info("No quizzes.json found — skipping quizzes import.")
    if VERSES_PATH.exists():
        logging.info("Found verses file: %s", VERSES_PATH)
        vcount = await import_verses_from_json(str(VERSES_PATH))
        logging.info("Imported %d verses.", vcount)
    else:
        logging.info("No verses.json found — skipping verses import.")
    print(f"Imported {qcount} quizzes and {vcount} verses.")
    logging.info("Migration finished: %d quizzes, %d verses.", qcount, vcount)

if __name__ == "__main__":
    try:
        asyncio.run(migrate())
    except KeyboardInterrupt:
        logging.info("Migration cancelled by user.")
