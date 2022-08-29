import re
from telethon.tl.types import Message
from telethon.tl.custom import Button
from telethon import events
from telethon.events import NewMessage, CallbackQuery
import asyncio
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    UserBlockedError,
    ChatWriteForbiddenError,
)
from google_trans_new.constant import LANGUAGES
from google_trans_new import google_translator
translator = google_translator()
from ERICA.untils import Zbot, Zinline
from ERICA.modules.mongodb.lang import get_welcome, save_welcome
from ERICA import telethn as Zaid
from typing import Union, List, Dict, Callable, Generator, Any
import ERICA.modules.sql.language_sql as sql
from ERICA.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from ERICA.langs import get_string, get_languages, get_language

def gs(chat_id: Union[int, str], string: str) -> str:
    lang = sql.get_chat_lang(chat_id)
    return get_string(lang, string)


JSONDB = None

if not JSONDB:
    JSONDB = {"users": [], "language": {}}


def split_list(lis, index):
    new_ = []
    while lis:
        new_.append(lis[:index])
        lis = lis[index:]
    return new_


Buttons = [Button.inline(LANGUAGES[lang].upper(), f"st-{lang}") for lang in LANGUAGES]
# 2 Rows
Buttons = split_list(Buttons, 2)
# 5 Columns
Buttons = split_list(Buttons, 5)


def translate(text, sender, to_bing=False):
    if to_bing:
        return translator.translate(text, lang_tgt="en")
    get_ = get_welcome(str(sender))
    if get_:
        try:
            return translator.translate(text, lang_tgt=get_)
        except Exception as er:
            LOG.exception(er)
    return text






@Zaid.on(events.NewMessage(pattern="^/setlang"))
async def setlhng(event):
    if not event.is_private:
       try:
           _s = await event.client.get_permissions(event.chat_id, event.sender_id)
           if not _s.is_admin:
              return
       except Exception:
           pass
    bts = Buttons[0].copy()
    bts.append([Button.inline("Next ▶", "btsh"), Button.inline("Cancel ❌", "cncl")])
    await event.reply("Choose your desired language..", buttons=bts)



@Zinline(pattern=r"language")
async def setlang(event):
    if not event.is_private:
       try:
           _s = await event.client.get_permissions(event.chat_id, event.sender_id)
           if not _s.is_admin:
              return
       except Exception:
           pass
    bts = Buttons[0].copy()
    bts.append([Button.inline("Next ▶", "btsh"), Button.inline("Cancel ❌", "cncl")])
    await event.reply("Choose your desired language..", buttons=bts)


@Zinline(pattern=r"btsh(.*)")
async def click_next(event):
    data = event.data_match.group(1).decode("utf-8")
    if not event.is_private:
       try:
           _s = await event.client.get_permissions(event.chat_id, event.sender_id)
           if not _s.is_admin:
              return
       except Exception:
           pass
    if not data:
        val = 1
    else:
        prev_or_next = data[0]
        val = int(data[1:])
        if prev_or_next == "p":
            val -= 1
        else:
            val += 1
    try:
        bt = Buttons[val].copy()
    except IndexError:
        val = 0
        bt = Buttons[0].copy()
    if val == 0:
        bt.append([Button.inline("Next ▶", "btsh"), Button.inline("Cancel ❌", "cncl")])
    else:
        bt.extend(
            [
                [
                    Button.inline("◀ Prev", f"btshp{val}"),
                    Button.inline("Next ▶", f"btshn{val}"),
                ],
                [Button.inline("Cancel ❌", "cncl")],
            ]
        )
    await event.edit(buttons=bt)


@Zinline(pattern=r"cncl")
async def maggie(event):
    if not event.is_private:
       try:
           _s = await event.client.get_permissions(event.chat_id, event.sender_id)
           if not _s.is_admin:
              return
       except Exception:
           pass
    await event.delete()



@Zinline(pattern=r"st-(.*)")
async def set_lang(event):
    match = event.data_match.group(1).decode("utf-8")
    if not event.is_private:
       try:
           _s = await event.client.get_permissions(event.chat_id, event.sender_id)
           if not _s.is_admin:
              return
       except Exception:
           pass
    save_welcome(str(event.chat_id), str(match))
    code_lang = {code: name for code, name in LANGUAGES.items()}
    name = code_lang[match]
    name = name[0].upper() + name[1:]
    await event.edit(f"Language successfully changed to {name} !")
