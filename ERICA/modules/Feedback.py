import random

from telegram import ParseMode
from telethon import Button
 
from ERICA import telethn as tbot
OWNER_ID = 5937170640
SUPPORT_CHAT = 'thedeadlybots'
OWNER = "wtf_blaze"

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    HOTTIE = (
        "https://telegra.ph/file/a4d1ff1616655428d657f.jpg",        
        "https://telegra.ph/file/3932bb5dbc221c22eb2d4.jpg",
    )
    FEED = ("https://telegra.ph/file/3932bb5dbc221c22eb2d4.jpg",)
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Support"
    GIVE = "Give Some Text For Feedback âœ¨"
    logger_text = f"""
**New Feedback**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if user_id == 1926801217:
        await e.reply("**Sry I Can't Identify ur Info**", parse_mode=ParseMode.MARKDOWN)
        return

    if user_id == 1087968824:
        await e.reply(
            "**Turn Off Ur Anonymous Mode And Try**", parse_mode=ParseMode.MARKDOWN
        )
        return

    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(FEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(HOTTIE),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(HOTTIE), buttons=BUTTON)

@register(pattern="/hammer ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    HOTTIE = (
        "https://telegra.ph/file/a4d1ff1616655428d657f.jpg",        
        "https://telegra.ph/file/3932bb5dbc221c22eb2d4.jpg",
    )
    FEED = ("https://te.legra.ph/file/404503e13fac593ada12d.jpg",)
    BUTTON = [[Button.url("Go To Owner Pm", f"https://t.me/{OWNER}")]]
    TEXT = "Thanks For Your Feedback, I Hope Your Issue will Fix Soon"
    GIVE = "Give Some Text For Send message âœ¨"
    logger_text = f"""
**New Feedback**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if user_id == 1926801217:
        await e.reply("**Sry I Can't Identify ur Info**", parse_mode=ParseMode.MARKDOWN)
        return

    if user_id == 1087968824:
        await e.reply(
            "**Turn Off Ur Anonymous Mode And Try**", parse_mode=ParseMode.MARKDOWN
        )
        return

    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(FEED),
        ),
        return

    await tbot.send_message(
        OWNER,
        f"{logger_text}",
        file=random.choice(HOTTIE),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(HOTTIE), buttons=BUTTON)





from ERICA.modules.language import gs

#def get_help(chat):
 #   return gs(chat, "feed_help")

#__mod_name__ = "Feedback"
