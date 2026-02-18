# main.py
import logging
import os
import datetime
import asyncio
from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# load .env if present
load_dotenv()

from utils import require_bot_token, BOT_TOKEN
import handlers
from db import init_db, get_random_verse, get_all_group_ids

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/bot.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

require_bot_token()

# ensure event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(init_db())

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def send_daily_verse(context):
    try:
        verse = await get_random_verse()
        if not verse:
            return
        groups = await get_all_group_ids()
        for gid in groups:
            try:
                await context.bot.send_message(chat_id=int(gid), text=f"📖 Daily Verse\n{verse}")
            except Exception:
                logging.exception("Failed to send daily verse to %s", gid)
                continue
    except Exception:
        logging.exception("Error in send_daily_verse job")

app.job_queue.run_daily(send_daily_verse, time=datetime.time(hour=8, minute=0))

# register handlers
app.add_handler(CommandHandler("start", handlers.start))
app.add_handler(CommandHandler("help", handlers.help_cmd))
app.add_handler(CommandHandler("about", handlers.about))
app.add_handler(CommandHandler("eabout", handlers.eabout))
app.add_handler(CommandHandler("contact", handlers.contact))
app.add_handler(CommandHandler("econtact", handlers.econtact))
app.add_handler(CommandHandler("verse", handlers.verse))
app.add_handler(CommandHandler("events", handlers.events))
app.add_handler(CommandHandler("eevents", handlers.eevents))
app.add_handler(CommandHandler("birthday", handlers.birthday))
app.add_handler(CommandHandler("ebirthday", handlers.ebirthday))
app.add_handler(CommandHandler("pray", handlers.pray))
app.add_handler(CommandHandler("quiz", handlers.quiz))
app.add_handler(CallbackQueryHandler(handlers.quiz_answer, pattern="^quiz_"))
app.add_handler(CommandHandler("leaderboard", handlers.leaderboard))
app.add_handler(CommandHandler("broadcast", handlers.broadcast))
app.add_handler(CommandHandler("stats", handlers.stats))
app.add_handler(CommandHandler("language", handlers.language))
app.add_handler(CommandHandler("report", handlers.report))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handlers.new_chat_member))

if __name__ == "__main__":
    print("Bot starting...")
    try:
        app.run_polling()
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped by user")
    except Exception:
        logging.exception("Unhandled exception in bot run")
