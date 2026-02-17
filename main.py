import logging, os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from utils import BOT_TOKEN
import handlers
from storage import read_json, write_json


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/bot.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Please set it in .env")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register commands
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

# Track groups when bot is added to a group
async def new_chat_member(update, context):
    chat = update.effective_chat
    groups = read_json("groups.json", [])
    if str(chat.id) not in groups:
        groups.append(str(chat.id))
        write_json("groups.json", groups)

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_member))

if __name__ == "__main__":
    print("Bot starting...")
    app.run_polling()
