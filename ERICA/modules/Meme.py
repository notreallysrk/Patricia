from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram import filters
from ERICA import pgram as bot
from pyrogram.types import Message
import requests

@bot.on_callback_query(filters.regex(pattern=r"meme"))
def callback_meme(_, query):
    if query.data.split(":")[1] == "next":
        query.message.delete()
        res = requests.get('https://nksamamemeapi.pythonanywhere.com').json()
        img = res['image']
        title = res['title']
        bot.send_photo(
            query.message.chat.id,
            img,
            caption=title,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Next", callback_data="meme:next")],
            ]))


@bot.on_message(filters.command('rmeme'))
def rmeme(_, message):
    res = requests.get('https://nksamamemeapi.pythonanywhere.com').json()
    img = res['image']
    title = res['title']
    bot.send_photo(message.chat.id,
                   img,
                   caption=title,
                   reply_markup=InlineKeyboardMarkup([[
                       InlineKeyboardButton("Next", callback_data="meme:next")
                   ]]))


@bot.on_message(filters.command('webss'))
async def webss(client, message):
    user = message.command[1]
    fuck = f'https://webshot.deam.io/{url}/?delay=2000'
    await client.send_document(message.chat.id, fuck, caption=f'{url}')


from ERICA.modules.language import gs

#def get_help(chat):
 #   return gs(chat, "meme_help")


#__mod_name__ = "Memes"
