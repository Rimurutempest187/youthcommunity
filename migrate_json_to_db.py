# migrate_json_to_db.py
import asyncio
import os
import json
import logging
from pathlib import Path

# import db helpers
from db import init_db, import_quizzes_from_json, import_verses_from_json

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_DIR = Path(__file__).parent / "data"
QUIZZES_PATH = DATA_DIR / "quizzes.json"
VERSES_PATH = DATA_DIR / "verses.json"

async def migrate():
    # ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    logging.info("Initializing database (creating tables if needed)...")
    try:
        await init_db()
    except Exception as e:
        logging.exception("Failed to initialize DB: %s", e)
        return

    # import quizzes
    qcount = 0
    if QUIZZES_PATH.exists():
        logging.info("Found quizzes file: %s", QUIZZES_PATH)
        try:
            qcount = await import_quizzes_from_json(str(QUIZZES_PATH))
            logging.info("Imported %d quizzes.", qcount)
        except Exception as e:
            logging.exception("Failed to import quizzes: %s", e)
    else:
        logging.info("No quizzes.json found at %s — skipping quizzes import.", QUIZZES_PATH)

    # import verses
    vcount = 0
    if VERSES_PATH.exists():
        logging.info("Found verses file: %s", VERSES_PATH)
        try:
            vcount = await import_verses_from_json(str(VERSES_PATH))
            logging.info("Imported %d verses.", vcount)
        except Exception as e:
            logging.exception("Failed to import verses: %s", e)
    else:
        logging.info("No verses.json found at %s — skipping verses import.", VERSES_PATH)

    print(f"Imported {qcount} quizzes and {vcount} verses.")
    logging.info("Migration finished: %d quizzes, %d verses.", qcount, vcount)

if __name__ == "__main__":
    try:
        asyncio.run(migrate())
    except KeyboardInterrupt:
        logging.info("Migration cancelled by user.")
    except Exception as e:
        logging.exception("Unhandled error during migration: %s", e)
        raise
