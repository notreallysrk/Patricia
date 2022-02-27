# plugins under @TeamDeeCode || No One Rather Than Blaze Had Permission To Use This Else May Accept Github Reported
# Licensed Under GNU Private License Mean Copyright Only To Plugins Creator


from pyrogram import filters
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ERICA import pgram as app, MONGO_DB_URL

client = MongoClient(MONGO_DB_URL)
dbd = client["new1"]
approved_users = dbd.approve
db = dbd

tagdb = db.tagdb1
nightmod = db.nightmode4

def get_info(id):
    return nightmod.find_one({"id": id})

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@app.on_message(filters.command(["tagalert"]))
async def locks_dfunc(_, message):
   lol = await message.reply("`Processing..`")
   if len(message.command) != 2:
      return await lol.edit("Usage: /tagalert [on | off]")
   parameter = message.text.strip().split(None, 1)[1].lower()
  
   if parameter == "on" or parameter=="ON":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit("Only users with usernames are eligible for tag alert service")
     uname=str(message.from_user.username)
     uname = uname.lower()
     isittrue = tagdb.find_one({f"teg": uname})
     if not isittrue:
          tagdb.insert_one({f"teg": uname})
          return await lol.edit(f"✅ **Tag alerts enabled.**\n\n»**__When someone tags you as @{uname} you will be notified.__**")
     else:
          return await lol.edit("**Tag alerts already enabled for you.**")
   if parameter == "off" or parameter=="OFF":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit("**Only users with usernames are eligible for tag alert service**")
     uname = message.from_user.username
     uname = uname.lower()
     isittrue = tagdb.find_one({f"teg": uname})
     if isittrue:
          tagdb.delete_one({f"teg": uname})
          return await lol.edit("❌ **Tag alerts removed for you.**")
     else:
          return await lol.edit("❌ **Tag alerts already disabled for you.**")
   else:
     await lol.edit("I only recognize `/tagalert on` and `/tagalert off` only. ")
     





     
@app.on_message(filters.incoming & ~filters.edited)
async def mentioned_alert(client, message):
    try:
        if not message:
            message.continue_propagation()
            return
        if not message.from_user:
            message.continue_propagation()
            return 
        input_str = message.text
        input_str = input_str.lower()
        if "@" in input_str:
            
            input_str = input_str.replace("@", "  |")
            Rose = input_str.split("|")[1]
            text = Rose.split()[0]
        try:
            chat_name = message.chat.title
            chat_id = message.chat.id
            msg = message.text
            tagged_msg_link = message.link
        except:
            return message.continue_propagation()
        user_ = message.from_user.mention or f"@{message.from_user.username}"
        
        final_tagged_msg = f"""
**💬 You Have Been Tagged**
**Group:-** {chat_name}
**By User:-** {user_}
**Message:-** `{msg}`
**Message:-** [Here]({tagged_msg_link})
        """
        button_s = InlineKeyboardMarkup([[InlineKeyboardButton("💬 View Message", url=tagged_msg_link)]])
        try:
            await client.send_message(chat_id=f"{text}", text=final_tagged_msg,reply_markup=button_s,disable_web_page_preview=True)
            
        except:
            return message.continue_propagation()
        message.continue_propagation()
    except:
        return message.continue_propagation()
    
__MODULE__ = "Tagalert"
__HELP__ = """
Too many mentions.. Cant you manage them all alone..
Here is the solution

If you are tagged/mentioned in a group where Rose is present
Rose will notify it to you via private message after enabling tag alerts

**Commands**
- /tagalert `on` : Turn tag alerts on
- /tagalert `off` : Turn tag alert off

**Example:**
If you are mentioned in a group Zaid will tell you who mentioned you, 
message that you are tagged in and which group is that.
"""
    
