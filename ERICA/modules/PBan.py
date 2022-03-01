import asyncio
from time import time
import os
from pyrogram import filters
from pyrogram.types import CallbackQuery, ChatPermissions, Message

from ERICA import BOT_ID, OWNER_ID as SUDOERS, pgram as app
from ERICA.core.decorators.errors import capture_err
from ERICA.core.keyboard import ikb
from ERICA.utils.dbfunctions import (add_warn, get_warn, int_to_alpha,
                                   remove_warns, save_filter)
from ERICA.utils.functions import (extract_user, extract_user_and_reason,
                                 time_converter)


__MODULE__ = "Admin"
__HELP__ = """
Make it easy to promote and demote users with the admin module!
- /ban - Ban A User
- /dban - Delete the replied message banning its sender
- /tban - Ban A User For Specific Time
- /unban - Unban A User
- /warn - Warn A User
- /dwarn - Delete the replied message warning its sender
- /rmwarns - Remove All Warning of A User
- /warns - Show Warning Of A User
- /kick - Kick A User
- /dkick - Delete the replied message kicking its sender
- /purge - Purge Messages
- /del - Delete Replied Message
- /promote - Promote A Member
- /fullpromote - Promote A Member With All Rights
- /demote - Demote A Member
- /pin - Pin A Message
- /mute - Mute A User
- /tmute - Mute A User For Specific Time
- /unmute - Unmute A User
- /ban_ghosts - Ban Deleted Accounts
- /report | @admins | @admin - Report A Message To Admins.
Sometimes, you promote or demote an admin manually, 
and Rose doesn't realise it immediately. This is because 
to avoid spamming telegram servers, admin status is cached locally.
"""


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from ERICA.core.decorators.permissions import adminsOnly

admins_in_chat = {}


async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.iter_chat_members(
                chat_id, filter="administrators"
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms





# Kick members


@app.on_message(
    filters.command(["kick", "dkick"]) & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "I can't kick myself, i can leave if you want."
        )
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Kick The Elevated One?")
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't kick an admin, You know the rules, so do i."
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


# Ban members


@app.on_message(
    filters.command(["ban", "dban", "tban"])
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text(
            "I can't ban myself, i can leave if you want."
        )
    if user_id in SUDOERS:
        return await message.reply_text(
            "You Wanna Ban The Elevated One?, RECONSIDER!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do i."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text("You can't use more than 99")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command("unban") & ~filters.edited & ~filters.private)
@adminsOnly("can_restrict_members")
async def unbanFunc(_, message: Message):
    # we don't need reasons for unban, also, we
    # don't need to get "text_mention" entity, because
    # normal users won't get text_mention if the the user
    # they want to unban is not in the group.
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    umention = (await app.get_users(user)).mention
    await message.reply_text(f"Unbanned! {umention}")






    


# Report


@app.on_message(
    (
        filters.command("report")
        | filters.command(["admins", "admin"], prefixes="@")
    )
    & ~filters.edited
    & ~filters.private
)
@capture_err
async def report_user(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to report that user."
        )

    if message.reply_to_message.from_user.id == message.from_user.id:
        return await message.reply_text("Why are you reporting yourself ?")

    list_of_admins = await list_admins(message.chat.id)
    if message.reply_to_message.from_user.id in list_of_admins:
        return await message.reply_text(
            "Do you know that the user you are replying is an admin ?"
        )

    user_mention = message.reply_to_message.from_user.mention
    text = f"Reported {user_mention} to admins!"
    admin_data = await app.get_chat_members(
        chat_id=message.chat.id, filter="administrators"
    )  # will it giv floods ?
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            # return bots or deleted admins
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"

    await message.reply_to_message.reply_text(text)

@app.on_message(filters.command("setgrouptitle") & ~filters.private)
@adminsOnly("can_change_info")
async def set_chat_title(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:**\n/set_chat_title NEW NAME")
    old_title = message.chat.title
    new_title = message.text.split(None, 1)[1]
    await message.chat.set_title(new_title)
    await message.reply_text(
        f"Successfully Changed Group Title From {old_title} To {new_title}"
    )


@app.on_message(filters.command("settitle") & ~filters.private)
@adminsOnly("can_change_info")
async def set_user_title(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to user's message to set his admin title"
        )
    if not message.reply_to_message.from_user:
        return await message.reply_text(
            "I can't change admin title of an unknown entity"
        )
    chat_id = message.chat.id
    from_user = message.reply_to_message.from_user
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n/set_user_title NEW ADMINISTRATOR TITLE"
        )
    title = message.text.split(None, 1)[1]
    await app.set_administrator_title(chat_id, from_user.id, title)
    await message.reply_text(
        f"Successfully Changed {from_user.mention}'s Admin Title To {title}"
    )


@app.on_message(filters.command("setgrouppic") & ~filters.private)
@adminsOnly("can_change_info")
async def set_chat_photo(_, message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text(
            "Reply to a photo to set it as chat_photo"
        )

    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(
            "Reply to a photo or document to set it as chat_photo"
        )

    if file.file_size > 5000000:
        return await message.reply("File size too large.")

    photo = await reply.download()
    await message.chat.set_photo(photo)
    await message.reply_text("Successfully Changed Group Photo")
    os.remove(photo)
