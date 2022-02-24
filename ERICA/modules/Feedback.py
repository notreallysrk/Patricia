import random

from telegram import ParseMode
from telethon import Button

from ShuKurenaiXRoBot import OWNER_ID, SUPPORT_CHAT
from ShuKurenaiXRoBot import telethn as tbot
from ShuKurenaiXRoBot.events import register

SHU1 = ( "https://telegra.ph/file/0a2abd13876ac59489c8a.jpg", 
      "https://telegra.ph/file/77eef7b0a5e354f257ff7.jpg", 
      "https://telegra.ph/file/898b10cf0ee3086c82def.jpg", 
      "https://telegra.ph/file/8fd1b2351135e778700a0.jpg", 
      "https://telegra.ph/file/d15dd2e8dbf15bd6b616c.jpg",
      "https://telegra.ph/file/ac980e9c880bc5d703b01.jpg",   
      ) 
SHU2 = "https://telegra.ph/file/3932bb5dbc221c22eb2d4.jpg"

@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    BUTTON = [[Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Service"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback**

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


__mod_name__ = "Feedback"
