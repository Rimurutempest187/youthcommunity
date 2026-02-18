from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from storage import read_json, write_json, read_text, write_text
from messages import START_MSG, HELP_MSG
from utils import ADMIN_IDS

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
    if len(context.args) < 2:
        await update.message.reply_text("အသုံး: /econtact <Name> <Phone>")
        return
    name = context.args[0]
    phone = context.args[1]
    contacts = read_json("contacts.json", {})
    contacts[name] = phone
    write_json("contacts.json", contacts)
    await update.message.reply_text("Contacts updated.")

async def verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    verses = read_json("verses.json", [])
    if not verses:
        await update.message.reply_text("ယနေ့ဖတ်ရန် ကျမ်းပိုဒ် မရှိသေးပါ။ (Admin များ /eabout ဖြင့် ထည့်ပါ)")
        return
    import datetime
    idx = datetime.date.today().toordinal() % len(verses)
    await update.message.reply_text(verses[idx])

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = read_json("events.json", [])
    if not events:
        await update.message.reply_text("လာမည့် အစီအစဉ် မရှိသေးပါ။")
        return
    lines = [f"{e.get('date','')} {e.get('time','')} - {e.get('title','')} @ {e.get('place','')}" for e in events]
    await update.message.reply_text("\n".join(lines))

async def eevents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        await update.message.reply_text("သင်သည် admin မဟုတ်ပါ။")
        return
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
        event = {"date": parts[0].strip(), "time": parts[1].strip(), "title": parts[2].strip(), "place": parts[3].strip() if len(parts) > 3 else ""}
        events.append(event)
        write_json("events.json", events)
        await update.message.reply_text("Event added.")
    elif cmd == "clear":
        write_json("events.json", [])
        await update.message.reply_text("Events cleared.")
    elif cmd == "list":
        await update.message.reply_text("\n".join([f"{i+1}. {ev.get('date','')} {ev.get('time','')} - {ev.get('title','')}" for i, ev in enumerate(events)]) or "No events.")
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

# Simple quiz (non-interactive)
QUIZ_Q = {
    "question": "ယေရှုခရစ်၏ မိဘများ၏ နာမည် ဘာလဲ?",
    "options": ["မရိယာနှင့် ယိုးဆေ့", "ယိုးနန်နှင့် မာရီယာ", "မရိယာနှင့် ယိုးနန်", "မရိယာနှင့် ယာကုပ်"],
    "answer_index": 2
}

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[opt] for opt in QUIZ_Q["options"]]
    await update.message.reply_text(QUIZ_Q["question"], reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

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
    await update.message.reply_text("ဘာသာစကားပြောင်းရန် feature မရှိသေးပါ။")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("အသုံး: /report <text>")
        return
    text = " ".join(context.args)
    reports = read_json("reports.json", [])
    reports.append({"user": update.effective_user.full_name, "text": text})
    write_json("reports.json", reports)
    await update.message.reply_text("Report received. ကျေးဇူးတင်ပါတယ်။")
