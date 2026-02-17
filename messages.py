from config import CONFIG

POWERED_BY = CONFIG.get("powered_by", "@Enoch_777")

START_MSG = (
    "မင်္ဂလာပါ။ Church Community Bot သို့ ကြိုဆိုပါတယ်။\n\n"
    "အသုံးပြုနိုင်သော command များ -\n"
    "/help - အသုံးပြုနည်း\n"
    "/about - အသင်း၏ သမိုင်းနှင့် ရည်ရွယ်ချက်\n"
    "/contact - တာဝန်ခံများ၏ ဖုန်းနံပါတ်များ\n"
    "/verse - ယနေ့ဖတ်ရန် ကျမ်းပိုဒ်\n"
    "/events - လာမည့် အစီအစဉ်များ\n"
    "/birthday - ယခုလ မွေးနေ့များ\n"
    "/pray <text> - ဆုတောင်းခံချက်ရေးရန်\n"
    "/quiz - ကျမ်းစာ ဉာဏ်စမ်း\n"
    "/report <text> - အကြောင်းအရာတင်ပြရန်\n\n"
    f"powerby : {POWERED_BY}"
)

HELP_MSG = (
    "Bot ကို အသုံးပြုနည်း လမ်းညွှန်\n\n"
    "အသုံးပြုသူ command များ -\n"
    "/start - စတင်\n"
    "/help - လမ်းညွှန်\n"
    "/about - အသင်းအကြောင်း\n"
    "/contact - တာဝန်ခံ ဖုန်းနံပါတ်များ\n"
    "/verse - ယနေ့ဖတ်ရန် ကျမ်းပိုဒ်\n"
    "/events - အစီအစဉ်များ\n"
    "/birthday - ယခုလ မွေးနေ့များ\n"
    "/pray <text> - ဆုတောင်းပေးရန်\n"
    "/quiz - ဉာဏ်စမ်း\n"
    "/report <text> - အမှားတင်ပြရန်\n\n"
    "Admin-only commands -\n"
    "/eabout, /econtact, /eevents, /ebirthday, /broadcast, /stats\n"
)
