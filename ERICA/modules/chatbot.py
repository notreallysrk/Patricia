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
from ERICA.modules.mongodb import MONGO_DB_URI as DB_URI
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




CHATBOT_TOGGLE_COMMAND_HANDLER = CommandHandler(
    "chatbot",
    chatbot_toggle,
)
CHATBOT_TOGGLE_CALLBACK_HANDLER = CallbackQueryHandler(
    chatbot_handle_callq, pattern=r"chatbot_",
)


dispatcher.add_handler(CHATBOT_TOGGLE_COMMAND_HANDLER)
dispatcher.add_handler(CHATBOT_TOGGLE_CALLBACK_HANDLER)
