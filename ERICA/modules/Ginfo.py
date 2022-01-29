
from pyrogram import Client, filters


@Client.on_message(filters.command("ginfo"))
def ginfo(client, message):
    id = message.from_user.id
    txt=message.text
    text = txt.split(" ", 1)
    chat_id=text[1]
    message = f"<b>Chat Name:</b> {bot.get_chat(chat_id)}"
    message += f"<b>Total Members:</b> {bot.get_chat_members_count(chat_id)}"
    message += f"<b>Photo:</b> {bot.get_profile_photos(chat_id, limit=1)}"
    message += f"<b>Link:</b> {bot.get_chat_invite_link(chat_id)}"
    try:
        message += f"<b>Pinned Message:</b> {bot.get_dialogs(chat_id, pinned_only=True)}"
    except TelegramError as e:
        return 
    message.reply_text(message)
