#By Zaid (github.com/ITZ-ZAID ; t.me/Timesisnotwaiting)
#By @Superior_Bots Telegram

from ERICA import telethn as tbot
from telethon.errors import (
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import EditAdminRequest, EditPhotoRequest

from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from telethon import *
from telethon.tl import *
from telethon.errors import *

import os
from time import sleep
from telethon import events
from telethon.errors import FloodWaitError, ChatNotModifiedError
from telethon.errors import UserAdminInvalidError
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import *

from ERICA import *
from ERICA.events import register

from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest

from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError

sudo = 1669178360
BOT_ID = 1901951380
CMD_HELP = '/ !'





# ================================================

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True



@register(pattern="^/unbanall$")
async def _(event):
    chat_id = event.chat_id
    user = event.sender_id
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator
    if event.is_private:
      return await event.respond("__This command can be use in groups and channels!__")
  
    is_admin = False
    try:
      zaid = await tbot(GetParticipantRequest(
        event.chat_id,
        event.sender_id
      ))
    except UserNotParticipantError:
      is_admin = False
    else:
      if (
        isinstance(
          zaid.participant,
          (
            ChannelParticipantAdmin,
            ChannelParticipantCreator,
          )
        )
      ):
        is_admin = True
    if not is_admin:
      return await event.respond("__Only admins can Unmuteall!__")

    if not admin and not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    done = await event.reply("Searching Participant Lists.")
    p = 0
    async for i in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await tbot(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            logger.warn("sleeping for {} seconds".format(ex.seconds))
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No one is banned in this chat")
        return
    required_string = "Successfully unbanned **{}** users"
    await event.reply(required_string.format(p))


@register(pattern="^/unmuteall$")
async def _(event):
    chat_id = event.chat_id
    if event.is_private:
      return await event.respond("__This command can be use in groups and channels!__")
  
    is_admin = False
    try:
      zaid = await tbot(GetParticipantRequest(
        event.chat_id,
        event.sender_id
      ))
    except UserNotParticipantError:
      is_admin = False
    else:
      if (
        isinstance(
          zaid.participant,
          (
            ChannelParticipantAdmin,
            ChannelParticipantCreator,
          )
        )
      ):
        is_admin = True
    if not is_admin:
      return await event.respond("__Only admins can Unmuteall!__")
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator

    # Well
    if not admin and not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    done = await event.reply("Working ...")
    p = 0
    async for i in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsBanned, aggressive=True
    ):
        rights = ChatBannedRights(
            until_date=0,
            send_messages=False,
        )
        try:
            await tbot(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            logger.warn("sleeping for {} seconds".format(ex.seconds))
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No one is muted in this chat")
        return
    required_string = "Successfully unmuted **{}** users"
    await event.reply(required_string.format(p))




@register(pattern="^/users$")
async def get_users(show):
    if not show.is_group:
        return
    if show.is_group:
        if not await is_register_admin(show.input_chat, show.sender_id):
            return
    info = await tbot.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "Users in {}: \n".format(title)
    async for user in tbot.iter_participants(show.chat_id):
        if not user.deleted:
            mentions += f"\n[{user.first_name}](tg://user?id={user.id}) {user.id}"
        else:
            mentions += f"\nDeleted Account {user.id}"
    file = open("userslist.txt", "w+")
    file.write(mentions)
    file.close()
    await tbot.send_file(
        show.chat_id,
        "userslist.txt",
        caption="Users in {}".format(title),
        reply_to=show.id,
    )
    os.remove("userslist.txt")



__mod_name__ = "Advance"

from ERICA.modules.language import gs

def get_help(chat):
    return gs(chat, "group_help")
