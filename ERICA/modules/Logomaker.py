import functools

import requests
from pyrogram import filters

from ERICA.function.pluginhelpers import get_text
from ERICA import pgram as pbot

API1 = "https://single-developers.up.railway.app/logo?name="
API2 = "https://single-developers.up.railway.app/hqlogo?name="



from ERICA.modules.language import gs

def get_help(chat):
    return gs(chat, "logo_help")


__mod_name__ = "Logos"


import os
import random
import glob
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterPhotos
from ERICA.events import register
from ERICA import telethn as tbot, ubot2


def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m


@register(pattern="^/logo ?(.*)")
async def logo_gen(event):
    xx = await event.reply("Preparing your logo...")
    name = event.pattern_match.group(1)
    if not name:
        await xx.edit("Provide some text to draw!\nExample: /logo <your name>!")
        return
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in ubot2.iter_messages(
            "@KenLogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob.glob("./Zaid/resources/fonts/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in ubot2.iter_messages(
            "@KenLogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("./Zaid/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 120
        strke = 10
    elif len(name) >= 9:
        fnt_size = 50
        strke = 5
    else:
        fnt_size = 100
        strke = 20
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text((x, y), name, font=font, fill="white",
              stroke_width=strke, stroke_fill="black")
    flnme = f"logo.png"
    img.save(flnme, "png")
    await xx.edit("Downloading")
    if os.path.exists(flnme):
        await tbot.send_file(
            event.chat_id,
            file=flnme,
            caption="Logo by [Zaid Robot](https://t.me/Zaid2_Robot)",
            force_document=False,
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_) 
    if os.path.exists(font_):
        if not font_.startswith("./Zaid/resources/fonts"):
            os.remove(font_)


@register(pattern="^/wlogo ?(.*)")
async def logo_(event):
    xx = await event.reply("Preparing your logo...")
    name = event.pattern_match.group(1)
    if not name:
        await xx.edit("`Provide some text to draw!\nExample: /wlogo <your name>!`")
        return
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in ubot2.iter_messages(
            "@kenlogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob.glob("./Zaid/resources/fonts/*")
        font_ = random.choice(fpath_)
    if not bg_:
        pics = []
        async for i in ubot2.iter_messages(
            "@kenlogopack", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("./Zaid/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 105
        strke = 8
    elif len(name) >= 9:
        fnt_size = 50
        strke = 4
    else:
        fnt_size = 95
        strke = 13
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text((x, y), name, font=font, fill="white",
              stroke_width=strke, stroke_fill="black")
    flnme = f"logo.png"
    img.save(flnme, "png")
    await xx.edit("`Uploading`")
    if os.path.exists(flnme):
        await tbot.send_file(
            event.chat_id,
            file=flnme,
            caption="Logo by [Zaid](https://t.me/Zaid2_Robot)",
            force_document=False,
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_) 
    if os.path.exists(font_):
        if not font_.startswith("./Zaid/resources/fonts"):
            os.remove(font_)



import functools

import requests
from pyrogram import filters

from ERICA.function.pluginhelpers import get_text
from ERICA import pgram as pbot

API1 = "https://single-developers.up.railway.app/logo?name="
API2 = "https://single-developers.up.railway.app/hqlogo?name="


def is_admin(func):
    @functools.wraps(func)
    async def oops(client, message):
        is_admin = False
        try:
            user = await message.chat.get_member(message.from_user.id)
            admin_strings = ("creator", "administrator")
            if user.status not in admin_strings:
                is_admin = False
            else:
                is_admin = True

        except ValueError:
            is_admin = True
        if is_admin:
            await func(client, message)
        else:
            await message.reply("**Only Admins can execute this command!**")

    return oops


@pbot.on_message(filters.command("bglogo") & ~filters.edited & ~filters.bot)
@is_admin
async def logo_maker(client, message):
    if message.reply_to_message:
        try:
            msg = await client.send_message(
                message.chat.id, "**Creating The Logo....**"
            )
        except:
            return
        try:
            text = get_text(message.reply_to_message)
        except:
            return
        if (
            message.reply_to_message.video
            or message.reply_to_message.document
            or message.reply_to_message.photo
            or message.reply_to_message.animation
            or message.reply_to_message.sticker
        ):
            try:
                await msg.edit("Sorry I can't get the text of replied message")
                return
            except:
                return
        if not text:
            try:
                await msg.edit("**Invalid Command Syntax**\n\n`/logo [name]`")
                return
            except:
                return
        try:
            req = requests.get(API1 + text.replace(" ", "%20"))
        except:
            return
        try:
            url = req.history[1].url
        except:
            return
        try:
            await msg.delete()
        except:
            return
        try:
            await message.reply_photo(
                url,
                caption=f"**Logo Generated Successfully** As {text}\n\nImage Link => {url}\n\n**By @Zaid2_Robot**",
            )
        except:
            return

    else:
        try:
            msg = await client.send_message(
                message.chat.id, "**Creating The Logo....**"
            )
        except:
            return
        try:
            text = get_text(message)
        except:
            return
        if not text:
            try:
                await msg.edit("**Invalid Command Syntax**\n\n`/logo [name]`")
                return
            except:
                return
        try:
            req = requests.get(API1 + text.replace(" ", "%20"))
        except:
            return
        try:
            url = req.history[1].url
        except:
            return
        try:
            await msg.delete()
        except:
            return
        try:
            await message.reply_photo(
                url,
                caption=f"**Logo Generated Successfully** As {text}\n\nImage Link => {url}\n\n**By @Zaid2_Robot**",
            )
        except:
            return


@pbot.on_message(filters.command(["logohq", "walllogo"]) & ~filters.edited & ~filters.bot)
@is_admin
async def logohq(client, message):
    if message.reply_to_message:
        try:
            msg = await client.send_message(
                message.chat.id, "**Creating The Logo....**"
            )
        except:
            return
        try:
            text = get_text(message.reply_to_message)
        except:
            return
        if (
            message.reply_to_message.video
            or message.reply_to_message.document
            or message.reply_to_message.photo
            or message.reply_to_message.animation
            or message.reply_to_message.sticker
        ):
            try:
                await msg.edit("Sorry I can't get the text of replied message")
                return
            except:
                return
        if not text:
            try:
                await msg.edit("**Invalid Command Syntax**\n\n`/logo [name]`")
                return
            except:
                return
        try:
            req = requests.get(API2 + text.replace(" ", "%20"))
        except:
            return
        try:
            url = req.history[1].url
        except:
            return
        try:
            await msg.delete()
        except:
            return
        try:
            await message.reply_photo(
                url,
                caption=f"**Logo Generated Successfully** As {text}\n\nImage Link => {url}\n\n**By @Zaid2_Robot**",
            )
        except:
            return

    else:
        try:
            msg = await client.send_message(
                message.chat.id, "**Creating The Logo....**"
            )
        except:
            return
        try:
            text = get_text(message)
        except:
            return
        if not text:
            try:
                await msg.edit("**Invalid Command Syntax**\n\n`/logo [name]`")
                return
            except:
                return
        try:
            req = requests.get(API2 + text.replace(" ", "%20"))
        except:
            return
        try:
            url = req.history[1].url
        except:
            return
        try:
            await msg.delete()
        except:
            return
        try:
            await message.reply_photo(
                url,
                caption=f"**Logo Generated Successfully** As {text}\n\nImage Link => {url}\n\n**By @Zaid2_Robot**",
            )
        except:
            return


