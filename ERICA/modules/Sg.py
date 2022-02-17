from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from typing import Union, List, Dict, Callable, Generator, Any

from ERICA import telethn as tbot
from ERICA import ubot2 as ubot
from ERICA.events import register as shasa
from ERICA.modules.language import gs
from ERICA import dispatcher
import ERICA.modules.sql.language_sql as sql
from ERICA.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from ERICA.langs import get_string, get_languages, get_language

async def is_register_admin(chat, user):

    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response

def gs(chat_id: Union[int, str], string: str) -> str:
    lang = sql.get_chat_lang(chat_id)
    return get_string(lang, string)


@shasa(pattern="^/sg ?(.*)")
async def _(event):

    if event.fwd_from:

        return
    chat = update.effective_chat
    msg = update.effective_message

    if not event.reply_to_msg_id:

        await event.reply(gs(chat.id, "sg_search_text"))

        return

    reply_message = await event.get_reply_message()

    if not reply_message.text:

        await event.reply(gs(chat.id, "sg_give_text"))

        return

    chat = "Sangmatainfo_bot"
    uid = reply_message.sender_id
    reply_message.sender

    if reply_message.sender.bot:

        await event.edit(gs(chat.id, "sg_replyusers_text"))

        return

    lol = await event.reply(gs(chat.id, "sg_getting_text"))

    async with ubot.conversation(chat) as conv:

        try:

            # response = conv.wait_event(
            #   events.NewMessage(incoming=True, from_users=1706537835)
            # )

            await silently_send_message(conv, f"/search_id {uid}")

            # response = await response
            responses = await silently_send_message(conv, f"/search_id {uid}")
        except YouBlockedUserError:

            await event.reply("```Please unblock @Sangmatainfo_bot and try again```")

            return
        await lol.edit(f"```{responses.text}```")
        # await lol.edit(f"{response.message.message}")



def get_help(chat):
    return gs(chat, "sg_help")


__mod_name__ = "Sangamata"
