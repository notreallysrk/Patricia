import re

from pyrogram import filters
from pyrogram.types import Message
from ERICA.data.defaults import Defaults
from .yui_base import Yui_Base
from ERICA import TOKEN, pgram
import ERICA.modules.sql.kuki_sql as sql

# Bot Id
yui_bot_id = int(TOKEN.split(":")[0])

# Chat
@pgram.on_message(~filters.command(["engine", "help", "restart"]) & ~filters.edited & ~filters.via_bot)
async def talk_with_yui(_, message: Message):
    c_type = message.chat.type
    r_msg = message.reply_to_message
    yui_base = Yui_Base()
    if sql.is_kuki:
        return
    # For Private chats
    if c_type == "private":
        quiz_text = message.text
    # For Public and private groups
    elif c_type == "supergroup" or "group":
        # Regex to find if "yui" or "Yui" in the message text
        if message.text and re.search(r'\bYui|yui\b', message.text):
            quiz_text = message.text
        # For replied message
        elif r_msg:
            if not r_msg.from_user:
                return
            # If replied message wasn't sent by the bot itself won't be answered
            if r_msg.from_user.id == yui_bot_id:
                if message.text:
                    quiz_text = message.text
                else:
                    quiz_text = None
            else:
                return
        else:
            return await message.stop_propagation()
    else:
        return await message.stop_propagation()
    # Arguments
    if quiz_text:
        quiz = quiz_text.strip()
    else:
        if message.photo:
            return await yui_base.reply_to_user(message, await yui_base.image_resp())
        elif message.video or message.video_note or message.animation:
            return await yui_base.reply_to_user(message, await yui_base.vid_resp())
        elif message.document:
            return await yui_base.reply_to_user(message, await yui_base.doc_resp())
        elif message.sticker:
            return await yui_base.reply_to_user(message, await yui_base.sticker_resp())
        else:
            return await message.stop_propagation()
    usr_id = message.from_user.id
    # Get the reply from Yui
    rply = await yui_base.get_answer_from_yui(quiz, usr_id)
    await yui_base.reply_to_user(message, rply)

