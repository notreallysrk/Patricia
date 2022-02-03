#By Eviral (github.com/TeamEviral ; t.me/Eviral)
#By RoseLoverx Telegram

from ERICA import telethn as tbot
from telethon.errors import (
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)

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
CMD_HELP = '/'

# =================== CONSTANT ===================
PP_TOO_SMOL = "The image is too small"
PP_ERROR = "Failure while processing image"
NO_ADMIN = "I am not an admin"
NO_PERM = "I don't have sufficient permissions!"

CHAT_PP_CHANGED = "Chat Picture Changed"
CHAT_PP_ERROR = (
    "Some issue with updating the pic,"
    "maybe you aren't an admin,"
    "or don't have the desired rights."
)
INVALID_MEDIA = "Invalid Extension"


BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


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


async def can_promote_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.add_admins
    )


async def can_ban_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


async def can_del(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.delete_messages
    )


async def can_pin_msg(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.pin_messages
    )


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await tbot.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("You need to specify a user by replying, or providing a username or user id...!")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await tbot.get_entity(user_id)
                return user_obj
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj

async def rep(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("`Pass the user's username, id or reply!`")
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj, extra

def find_instance(items, class_or_tuple):
    for item in items:
        if isinstance(item, class_or_tuple):
            return item
    return None

@register(pattern="^/promote ?(.*)")
async def promote(promt):
    text = promt.pattern_match.group(1)
    if text == None:
      title = 'Aԃɱιɳ'
    else:
      title = text
    if promt.is_group:
      if not promt.sender_id == OWNER_ID:
        if not await is_register_admin(promt.input_chat, promt.sender_id):
           await promt.reply("Only admins can execute this command!")
           return
        
    else:
        return
    if not await can_promote_users(message=promt):
            await promt.reply("You are missing the following rights to use this command:CanPromoteMembers")
            return
    user = await get_user_from_event(promt)
    if user.id == BOT_ID:
       await promt.reply("I can't promote myself! Get an admin to do it for me.")
       return
    if promt.is_group:
        if await is_register_admin(promt.input_chat, user.id):
            await promt.reply("Why will i promote an admin ?")
            return
        pass
    else:
        return

    new_rights = ChatAdminRights(
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await tbot(EditAdminRequest(promt.chat_id, user.id, new_rights, title))
        await promt.reply("Promoted!")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except Exception:
        await promt.reply("Failed to promote.")
        return

@register(pattern="^/lowpromote ?(.*)")
async def lowpromote(promt):
    text = promt.pattern_match.group(1)
    if text == None:
      title = 'α∂мιи'
    else:
      title = text
    if promt.is_group:
      if not promt.sender_id == OWNER_ID:
        if not await is_register_admin(promt.input_chat, promt.sender_id):
           await promt.reply("Only admins can execute this command!")
           return
        
    else:
        return
    if not await can_promote_users(message=promt):
            await promt.reply("You are missing the following rights to use this command:CanPromoteMembers")
            return
    user = await get_user_from_event(promt)
    if user.id == BOT_ID:
       await promt.reply("I can't promote myself! Get an admin to do it for me.")
       return
    if promt.is_group:
        if await is_register_admin(promt.input_chat, user.id):
            await promt.reply("Why will i promote an admin ?")
            return
        pass
    else:
        return

    new_rights = ChatAdminRights(
        invite_users=True,
        change_info=True,
        delete_messages=True,
        pin_messages=True,
    )

    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await tbot(EditAdminRequest(promt.chat_id, user.id, new_rights, title))
        await promt.reply("Promoted!")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except Exception:
        await promt.reply("Failed to promote.")
        return



@register(pattern="^/unbanall$")
async def _(event):
    if not event.is_group:
        return

    if event.is_group:
        if not await can_ban_users(message=event):
            return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator

    # Well
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
    if not event.is_group:
        return
    if event.is_group:
        if not await can_ban_users(message=event):
            return

    # Here laying the sanity check
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



@register(pattern="^/permapin(?: |$)(.*)")
async def pin(msg):
    if msg.is_group:
      if not msg.sender_id == OWNER_ID:
        if not await can_pin_msg(message=msg):
            return
    else:
        return
    previous_message = await msg.get_reply_message()
    k = await tbot.send_message(
            msg.chat_id,
            previous_message
          )
    to_pin = k.id
    if not to_pin:
        await msg.reply("Reply to a message which you want to pin.")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False

    try:
        await tbot(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except Exception:
        await msg.reply("Failed to pin.")
        return







@register(pattern="^/setgrouppic$")
async def set_group_photo(gpic):
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    photo = None

    if gpic.is_group:
        if not await can_change_info(message=gpic):
            return
    else:
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await tbot.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await tbot.download_file(replymsg.media.document)
        else:
            await gpic.reply(INVALID_MEDIA)

    if photo:
        try:
            await tbot(EditPhotoRequest(gpic.chat_id, await tbot.upload_file(photo)))
            await gpic.reply(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.reply(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.reply(PP_ERROR)
        except:
            await gpic.reply("Failed to set group pic.")


@register(pattern="^/settitle ?(.*)")
async def settitle(promt):
    textt = promt.pattern_match.group(1)
    thatuser = textt.split(" ")[0]
    title_admin = textt.split(" ")[1]
    # print(thatuser)
    # print(title_admin)
    if thatuser:
        user = await tbot.get_entity(thatuser)
    else:
        await promt.reply("Pass the user's username or id or followed by title !")
        return

    if promt.is_group:
        if not await can_promote_users(message=promt):
            return
    else:
        return

    if promt.is_group:
        if not await is_register_admin(promt.input_chat, user.id):
            await promt.reply("How can i set title of a non-admin ?")
            return
        pass

    try:
        result = await tbot(
            functions.channels.GetParticipantRequest(
                channel=promt.chat_id,
                user_id=user.id,
            )
        )
        p = result.participant

        await tbot(
            EditAdminRequest(
                promt.chat_id,
                user_id=user.id,
                admin_rights=p.admin_rights,
                rank=title_admin,
            )
        )

        await promt.reply("Chat Title set successfully!")

    except Exception:
        await promt.reply("Failed to set title.")
        return


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





@register(pattern="^/kickthefools$")
async def _(event):
    if event.fwd_from:
        return

    if event.is_group:
        if not await can_ban_users(message=event):
            return
    else:
        return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator

    # Well
    if not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    c = 0
    KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
    done = await event.reply("Working ...")
    async for i in tbot.iter_participants(event.chat_id):

        if isinstance(i.status, UserStatusLastMonth):
            status = await tbot(EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
                return
            c = c + 1

        if isinstance(i.status, UserStatusLastWeek):
            status = await tbot(EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
                return
            c = c + 1

    if c == 0:
        await done.edit("Got no one to kick.")
        return

    required_string = "Successfully Kicked **{}** users"
    await event.reply(required_string.format(c))




@register(pattern="^/setgrouptitle (.*)")
async def set_group_title(gpic):
    input_str = gpic.pattern_match.group(1)

    if gpic.is_group:
        if not await can_change_info(message=gpic):
            return
    else:
        return

    try:
        await tbot(
            functions.messages.EditChatTitleRequest(
                chat_id=gpic.chat_id, title=input_str
            )
        )
    except BaseException:
        await tbot(
            functions.channels.EditTitleRequest(channel=gpic.chat_id, title=input_str)
        )

    if gpic.chat.title == input_str:
        await gpic.reply("Successfully set new group title.")
    else:
        await gpic.reply("Failed to set group title.")


@register(pattern=r"^/setdescription ([\s\S]*)")
async def set_group_des(gpic):
    input_str = gpic.pattern_match.group(1)
    # print(input_str)
    if gpic.is_group:
        if not await can_change_info(message=gpic):
            return
    else:
        return

    try:
        await tbot(
            functions.messages.EditChatAboutRequest(peer=gpic.chat_id, about=input_str)
        )
        await gpic.reply("Successfully set new group description.")
    except BaseException:
        await gpic.reply("Failed to set group description.")


@register(pattern="^/setsticker$")
async def set_group_sticker(gpic):
    if gpic.is_group:
        if not await can_change_info(message=gpic):
            return
    else:
        return

    rep_msg = await gpic.get_reply_message()
    if not rep_msg.document:
        await gpic.reply("Reply to any sticker plox.")
        return
    stickerset_attr_s = rep_msg.document.attributes
    stickerset_attr = find_instance(stickerset_attr_s, DocumentAttributeSticker)
    if not stickerset_attr.stickerset:
        await gpic.reply("Sticker does not belong to a pack.")
        return
    try:
        id = stickerset_attr.stickerset.id
        access_hash = stickerset_attr.stickerset.access_hash
        print(id)
        print(access_hash)
        await tbot(
            functions.channels.SetStickersRequest(
                channel=gpic.chat_id,
                stickerset=types.InputStickerSetID(id=id, access_hash=access_hash),
            )
        )
        await gpic.reply("Group sticker pack successfully set !")
    except Exception as e:
        print(e)
        await gpic.reply("Failed to set group sticker pack.")

async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await message.reply("Invalid time amount specified.")
            return ""

        if unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            return 
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return 




__help__ = """
 - /adminlist : list of admins in the chat
 - /pin <loud(optional)> | /unpin: pins/unpins the message in the chat
 - /permapin: permapin
 - /promote: promotes a user
 - /demote: demotes a user
 - /ban: bans a user
 - /dban: deletes and bans a user
 - /unban: unbans a user
 - /mute: mute a user
 - /dmute: deletes and mute a user
 - /unmute: unmutes a user
 - /tban <entity> | <time interval>: temporarily bans a user for the time interval.
 - /tmute <entity> | <time interval>: temporarily mutes a user for the time interval.
 - /kick: kicks a user
 - /dkick: deletes and kicks a user
 - /kickme: kicks yourself (non-admins)
 - /banme: bans yourself (non-admins)
 - /settitle <entity> <title>: sets a custom title for an admin. If no <title> provided defaults to "Admin"
 - /setdescription <text>: set group description
 - /setgrouptitle <text>: set group title
 - /setgpic: reply to an image to set as group photo
 - /setsticker: reply to a sticker pack to set as group stickers
 - /delgpic: deletes the current group pic
 - /lock <item)>: lock the usage of "item" for non-admins
 - /unlock <item(s)>: unlock "item". Everyone can use them again
 - /chatlocks: gives the lock status of the chat
 - /chatlocktypes: gets a list of all things that can be locked
 - /unbanall: Unbans all in the chat
 - /unmuteall: Unmutes all in the chat
 - /users: list all the users in the chat
 - /zombies: counts the number of deleted account in your group
 - /kickthefools: kicks all members inactive from 1 week
"""

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

