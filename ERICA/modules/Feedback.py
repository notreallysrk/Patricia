import random

from telegram import ParseMode
from telethon import Button

from ERICA import OWNER_ID
from ERICA import telethn as tbot
from ERICA.events import register
SUPPORT_CHAT = 'Superior_Support'
OWNER = "Timesisnotwaiting"

SHU1 = ( "https://telegra.ph/file/74c20b72b87b09549e257.jpg", 
      "https://telegra.ph/file/a4d1ff1616655428d657f.jpg", 
      "https://telegra.ph/file/3932bb5dbc221c22eb2d4.jpg",  
      "https://telegra.ph/file/0a2abd13876ac59489c8a.jpg",   
      ) 
SHU2 = "https://telegra.ph/file/3932bb5dbc221c22eb2d4.jpg"

@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Support"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback In Zaid**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=SHU2,
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(SHU1),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(SHU1), buttons=BUTTON)

@register(pattern="/report ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "Thanks For Your Reports, I will Work Soon in this Report 🔜"
    GIVE = "Provide Me Some Text issues with (Your Group username) ✨"
    logger_text = f"""
**New Report In Zaid**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=SHU2,
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(SHU1),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(SHU1), buttons=BUTTON)


@register(pattern="/hammer ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    BUTTON = [[Button.url("Go To Owner Pm, f"https://t.me/{OWNER_NAME}")]]
    TEXT = "Your Requested Message Has been sended to my Owner Inbox , Hope he will Solve Ur Issues Soon 🔜"
    GIVE = "Provide Me Some Text to send a hammer message to my Owner ✨"
    logger_text = f"""
**New Report In Zaid**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=SHU2,
        ),
        return

    await tbot.send_message(
        OWNER,
        f"{logger_text}",
        file=random.choice(SHU1),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(SHU1), buttons=BUTTON)


from ERICA.modules.language import gs

def get_help(chat):
    return gs(chat, "feed_help")

__mod_name__ = "Feedback"
