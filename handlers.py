from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from storage import read_json, write_json, read_text, write_text
from messages import START_MSG, HELP_MSG
from utils import ADMIN_IDS
import random
from telegram.ext import CallbackQueryHandler

# helper
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users = read_json("users.json", {})
    users[str(user.id)] = {"id": user.id, "name": user.full_name}
    write_json("users.json", users)
    await update.message.reply_text(START_MSG)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MSG)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = read_text("about.txt", "အသင်းအကြောင်း မရှိသေးပါ။ (Admin များ /eabout ဖြင့် ပြင်နိုင်သည်)")
    await update.message.reply_text(text)

async def eabout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return
    if not context.args:
        await update.message.reply_text("အသင်းအကြောင်းကို ထည့်ရန် /eabout <text> ရိုက်ပါ။")
        return
    text = " ".join(context.args)
    write_text("about.txt", text)
    await update.message.reply_text("အသင်းအကြောင်းကို သိမ်းဆည်းပြီးပါပြီ။")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contacts = read_json("contacts.json", {})
    if not contacts:
        await update.message.reply_text("တာဝန်ခံ ဖုန်းနံပါတ် မရှိသေးပါ။")
        return
    lines = [f"{name} - {phone}" for name, phone in contacts.items()]
    await update.message.reply_text("\n".join(lines))

async def econtact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return

    if not context.args:
        await update.message.reply_text(
            "အသုံး: /econtact add|list|delete|clear\n"
            "Examples:\n"
            "/econtact add Name Phone\n"
            "/econtact list\n"
            "/econtact delete Name\n"
            "/econtact clear confirm"
        )
        return

    sub = context.args[0].lower()
    contacts = read_json("contacts.json", {})

    if sub == "add":
        if len(context.args) < 3:
            await update.message.reply_text("အသုံး: /econtact add <Name> <Phone>")
            return
        name, phone = context.args[1], context.args[2]
        contacts[name] = phone
        write_json("contacts.json", contacts)
        await update.message.reply_text(f"Contact added: {name} - {phone}")

    elif sub == "list":
        if not contacts:
            await update.message.reply_text("Contacts မရှိသေးပါ။")
            return
        await update.message.reply_text("\n".join([f"{n} - {p}" for n, p in contacts.items()]))

    elif sub == "delete":
        if len(context.args) < 2:
            await update.message.reply_text("အသုံး: /econtact delete <Name>")
            return
        name = context.args[1]
        if name in contacts:
            contacts.pop(name)
            write_json("contacts.json", contacts)
            await update.message.reply_text(f"Deleted contact: {name}")
        else:
            await update.message.reply_text(f"No contact named {name} found.")

    elif sub == "clear":
        if len(context.args) >= 2 and context.args[1].lower() == "confirm":
            write_json("contacts.json", {})
            await update.message.reply_text("All contacts cleared.")
        else:
            await update.message.reply_text("သတိပေးချက်: Contacts အားလုံး ဖျက်မည်။ ဆက်လက်ရန် `/econtact clear confirm` ရိုက်ပါ။")

    else:
        await update.message.reply_text("Unknown subcommand. Use add|list|delete|clear.")


import random
from storage import read_json

async def verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    verses = read_json("verses.json", [])
    if not verses:
        await update.message.reply_text("ယနေ့ဖတ်ရန် ကျမ်းပိုဒ် မရှိသေးပါ။ Admin ထည့်ပေးပါ။")
        return
    # random choice
    v = random.choice(verses)
    await update.message.reply_text(v)


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = read_json("events.json", [])
    if not events:
        await update.message.reply_text("လာမည့် အစီအစဉ် မရှိသေးပါ။")
        return
    lines = [f"{e['date']} - {e.get('time','')} - {e['title']} - {e.get('place','')}" for e in events]
    await update.message.reply_text("\n".join(lines))

async def eevents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return
    # expect JSON-like single-line or simple format: date|time|title|place
    if not context.args:
        await update.message.reply_text("အသုံး: /eevents add|clear|list or /eevents add date|time|title|place")
        return
    cmd = context.args[0].lower()
    events = read_json("events.json", [])
    if cmd == "add":
        rest = " ".join(context.args[1:])
        parts = rest.split("|")
        if len(parts) < 3:
            await update.message.reply_text("အသုံး: /eevents add date|time|title|place")
            return
        event = {"date": parts[0].strip(), "time": parts[1].strip(), "title": parts[2].strip(), "place": parts[3].strip() if len(parts)>3 else ""}
        events.append(event)
        write_json("events.json", events)
        await update.message.reply_text("Event added.")
    elif cmd == "clear":
        write_json("events.json", [])
        await update.message.reply_text("Events cleared.")
    else:
        await update.message.reply_text("Unknown subcommand.")

async def birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    b = read_json("birthdays.json", [])
    if not b:
        await update.message.reply_text("မည်သူ့မွေးနေ့မှတ်တမ်း မရှိသေးပါ။")
        return
    lines = [f"{item['name']} - {item['date']}" for item in b]
    await update.message.reply_text("\n".join(lines))

async def ebirthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return
    if len(context.args) < 2:
        await update.message.reply_text("အသုံး: /ebirthday <Name> <YYYY-MM-DD>")
        return
    name = context.args[0]
    date = context.args[1]
    b = read_json("birthdays.json", [])
    b.append({"name": name, "date": date})
    write_json("birthdays.json", b)
    await update.message.reply_text("Birthday added.")

async def pray(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("အသုံး: /pray <text>")
        return
    text = " ".join(context.args)
    prayers = read_json("prayers.json", [])
    prayers.append({"user": update.effective_user.full_name, "text": text})
    write_json("prayers.json", prayers)
    await update.message.reply_text("သင်၏ ဆုတောင်းကို မှတ်တမ်းတင်ပြီးပါပြီ။")

# Simple quiz: one question example
QUIZ_Q = {
    "question": "ယေရှုခရစ်၏ မိဘများ၏ နာမည် ဘာလဲ?",
    "options": ["မရိယာနှင့် ယိုးဆေ့", "ယိုးနန်နှင့် မာရီယာ", "မရိယာနှင့် ယိုးနန်", "မရိယာနှင့် ယာကုပ်"],
    "answer_index": 2
}


import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from storage import read_json, write_json

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quizzes = read_json("quizzes.json", [])
    if not quizzes:
        await update.message.reply_text("Quiz မရှိသေးပါ။ Admin ထည့်ပေးပါ။")
        return

    q = random.choice(quizzes)
    context.user_data["current_quiz"] = q

    keyboard = [
        [InlineKeyboardButton(f"A) {q['options']['A']}", callback_data="quiz_A")],
        [InlineKeyboardButton(f"B) {q['options']['B']}", callback_data="quiz_B")],
        [InlineKeyboardButton(f"C) {q['options']['C']}", callback_data="quiz_C")],
        [InlineKeyboardButton(f"D) {q['options']['D']}", callback_data="quiz_D")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(q["question"], reply_markup=reply_markup)

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    q = context.user_data.get("current_quiz")
    if not q:
        await query.edit_message_text("Quiz မရှိပါ။ /quiz ဖြင့် စတင်ပါ။")
        return

    choice_letter = query.data.split("_")[1]  # "A","B","C","D"
    correct_letter = q["answer_letter"]

    users = read_json("users.json", {})
    uid = str(update.effective_user.id)
    if uid not in users:
        users[uid] = {"id": update.effective_user.id,
                      "name": update.effective_user.full_name,
                      "score": 0}

    if choice_letter == correct_letter:
        users[uid]["score"] += 1
        write_json("users.json", users)
        await query.edit_message_text(
            f"✅ မှန်ကန်ပါတယ်! အဖြေ: {correct_letter}) {q['options'][correct_letter]}\n\nသင့် score: {users[uid]['score']}"
        )
    else:
        await query.edit_message_text(
            f"❌ မှားသွားပါတယ်။ အမှန်အဖြေက {correct_letter}) {q['options'][correct_letter]} ဖြစ်ပါတယ်။\n\nသင့် score: {users[uid]['score']}"
        )

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = read_json("users.json", {})
    if not users:
        await update.message.reply_text("Leaderboard မရှိသေးပါ။")
        return
    sorted_users = sorted(users.values(), key=lambda u: u.get("score",0), reverse=True)
    lines = [f"{i+1}. {u['name']} - {u.get('score',0)} points" for i,u in enumerate(sorted_users)]
    await update.message.reply_text("🏆 Leaderboard\n" + "\n".join(lines))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return
    if not context.args:
        await update.message.reply_text("အသုံး: /broadcast <message>")
        return
    msg = " ".join(context.args)
    groups = read_json("groups.json", [])
    sent = 0
    for gid in groups:
        try:
            await context.bot.send_message(chat_id=int(gid), text=msg)
            sent += 1
        except Exception:
            continue
    await update.message.reply_text(f"Broadcast sent to {sent} groups.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return
    users = read_json("users.json", {})
    groups = read_json("groups.json", [])
    await update.message.reply_text(f"Users: {len(users)}\nGroups: {len(groups)}")

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # simple toggle example
    await update.message.reply_text("ဘာသာစကားပြောင်းရန် feature မရှိသေးပါ။")


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("အသုံး: /report <text>")
        return

    text = " ".join(context.args)
    reports = read_json("reports.json", [])
    reports.append({"user": update.effective_user.full_name, "text": text})
    write_json("reports.json", reports)

    # user confirmation
    await update.message.reply_text("Report received. ကျေးဇူးတင်ပါတယ်။")

    # send to owner/admins
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"📢 Report from {update.effective_user.full_name}:\n{text}"
            )
        except Exception:
            continue
