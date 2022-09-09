import re
from time import sleep

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler,
    CommandHandler, Filters, MessageHandler, run_async,
)
import telegram.ext as tg
from time import perf_counter
from functools import wraps
from cachetools import TTLCache
from threading import RLock
DEL_CMDS = None

from telegram import Chat, ChatMember, ParseMode, Update
from telegram.ext import CallbackContext
DB_URI = "mongodb+srv://Anmol:Anmol@cluster0.icc3g.mongodb.net/?retryWrites=true&w=majority"
# stores admemes in memory for 10 min.
ADMIN_CACHE = TTLCache(maxsize=512, ttl=60 * 10, timer=perf_counter)
THREAD_LOCK = RLock()

from pymongo import MongoClient
import requests
import random
import os
import re
from re import IGNORECASE, escape, search
from ERICA import dispatcher

MONGO_URL = "mongodb+srv://Nia:Nia@cluster0.w4bqt7l.mongodb.net/?retryWrites=true&w=majority"

CHATBOT_ENABLED_CHATS = []

BOT_ID = int(1901951380)
AI_API_KEY = 'VVwV177Rz1QOibLD'
AI_BID = 162157

def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (
        chat.type == "private"
        or chat.all_members_are_administrators
        or user_id in [777000, 1087968824]
    ):  # Count telegram and Group Anonymous as admin
        return True
    if not member:
        with THREAD_LOCK:
            # try to fetch from cache first.
            try:
                return user_id in ADMIN_CACHE[chat.id]
            except KeyError:
                # keyerror happend means cache is deleted,
                # so query bot api again and return user status
                # while saving it in cache for future useage...
                chat_admins = dispatcher.bot.getChatAdministrators(chat.id)
                admin_list = [x.user.id for x in chat_admins]
                ADMIN_CACHE[chat.id] = admin_list

                return user_id in admin_list
    else:
        return member.status in ("administrator", "creator")

def user_admin(func):
    @wraps(func)
    def is_admin(update: Update, context: CallbackContext, *args, **kwargs):
        bot = context.bot
        user = update.effective_user
        chat = update.effective_chat

        if user and is_user_admin(chat, user.id):
            return func(update, context, *args, **kwargs)
        if not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            try:
                update.effective_message.delete()
            except:
                pass
        else:
            update.effective_message.reply_text(
                "Who dis non-admin telling me what to do? You want a punch?",
            )

    return is_admin

@run_async
@user_admin
def chatbot_toggle(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Enable", callback_data="chatbot_enable"),
            InlineKeyboardButton("Disable", callback_data="chatbot_disable"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)



def chatbot_handle_callq(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    vickdb = MongoClient(DB_URI)    
    vick = vickdb["VickDb"]["Vick"]
    action = query.data.split("_")[1]
    is_vick = vick.find_one({"chat_id": chat.id})
    if not is_user_admin(chat, user.id):
        return query.answer("This is not for you.")

    if action == "delete":
        query.message.delete()

    elif action == "enable":
        if not is_vick:
            return query.answer("Chatbot is already enabled")
        vick.delete_one({"chat_id": chat.id})
        query.answer("Chatbot enabled")
        query.message.delete()

    elif action == "disable":
        if is_vick:
            return query.answer("Chatbot is already disabled")
        vick.insert_one({"chat_id": chat.id})
        query.answer("Chatbot disabled")
        query.message.delete()

    else:
        query.answer()


def chatbot_response(query: str, user_id: int) -> str:
    data = requests.get(
        f"http://api.brainshop.ai/get?bid={AI_BID}&"
        + f"key={AI_API_KEY}&uid={user_id}&msg={query}",
    )
    response = data.json()["cnt"]
    return response


def check_message(context: CallbackContext, message):
    reply_msg = message.reply_to_message
    text = message.text
    if re.search("[.|\n]{0,}"+dispatcher.bot.first_name+"[.|\n]{0,}", text, flags=re.IGNORECASE):
        return True
    if reply_msg and reply_msg.from_user.id == BOT_ID:
        return True
    elif message.chat.type == 'private':
        return True
    else:
        return False



def chatbot(update: Update, context: CallbackContext):
   chat = update.effective_chat
   message = update.effective_message
   chat_id = chat.id
   vickdb = MongoClient(DB_URI)    
   vick = vickdb["VickDb"]["Vick"]
   is_vick = vick.find_one({"chat_id": chat.id})
   if is_vick:
       return
   try:
       if (
           message.text.startswith("!")
           or message.text.startswith("/")
           or message.text.startswith("?")
       ):
           return
   except Exception as e:
       pass
   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message:
       K = []  
       is_chat = chatai.find({"word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       if K:
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
       else:
           hey = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}").json()["cnt"]
           Yo = None
       if Yo == "sticker": 
           message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           message.reply_text(f"{hey}")
   if message.reply_to_message:                   
       if message.reply_to_message.from_user.id == 1901951380:                    
           K = []  
           is_chat = chatai.find({"word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           if K:
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
           else:
               hey = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}").json()["cnt"]
               Yo = None
           if Yo == "sticker":
               message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == 1901951380:
           if message.text:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})



CHATBOT_TOGGLE_COMMAND_HANDLER = CommandHandler(
    "chatbot",
    chatbot_toggle,
)
CHATBOT_TOGGLE_CALLBACK_HANDLER = CallbackQueryHandler(
    chatbot_handle_callq, pattern=r"chatbot_",
)

USER_HANDLER = MessageHandler(
    Filters.all, chatbot, run_async=True
)
USERS_GROUP = 1
dispatcher.add_handler(USER_HANDLER)

# Filters for ignoring #note messages, !commands and sed.

dispatcher.add_handler(CHATBOT_TOGGLE_COMMAND_HANDLER)
dispatcher.add_handler(CHATBOT_TOGGLE_CALLBACK_HANDLER)
