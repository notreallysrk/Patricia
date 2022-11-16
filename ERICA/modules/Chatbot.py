from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import os
import asyncio
import re
from ERICA import pgram as bot

MONGO_URL = "mongodb+srv://Nia:Nia@cluster0.w4bqt7l.mongodb.net/?retryWrites=true&w=majority"
BOT_ID = int(5594511258)
AI_API_KEY = 'VVwV177Rz1QOibLD'
AI_BID = 162157

@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
   is_kuki = message.chat.id
   if is_kuki: 
       if int(message.reply_to_message.from_user.id) == 1669178360:
           await client.send_message(chat_id=1669178360, text=f"{message.link}")
       if int(message.reply_to_message.from_user.id) == BOT_ID:       
           await bot.send_chat_action(message.chat.id, "typing")
           if not message.text:
               msg = "/"
           else:
               msg = message.text
           try: 
               x = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={msg}").json()
               x = x["cnt"]
               await asyncio.sleep(0.01)
               await message.reply_text(x)
           except Exception as e:
               error = str(e)
