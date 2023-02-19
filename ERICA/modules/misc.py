import html
import time
import git
import requests
from io import BytesIO
from telegram import Update, MessageEntity, ParseMode
from telegram.error import BadRequest
from telegram.ext import Filters, CallbackContext
from telegram.utils.helpers import mention_html, escape_markdown
from subprocess import Popen, PIPE

from ERICA import (
    dispatcher,
    OWNER_ID,
    SUDO_USERS,
    SUPPORT_USERS,
    DEV_USERS,
    SARDEGNA_USERS,
    WHITELIST_USERS,
    INFOPIC,
    sw,
    StartTime,
    KInit
)
from ERICA.__main__ import STATS, USER_INFO, TOKEN
from ERICA.modules.sql import SESSION
from ERICA.modules.helper_funcs.chat_status import user_admin, sudo_plus
from ERICA.modules.helper_funcs.extraction import extract_user
import ERICA.modules.sql.users_sql as sql
from ERICA.modules.language import gs
from telegram import __version__ as ptbver, InlineKeyboardMarkup, InlineKeyboardButton
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
import datetime
import platform
from platform import python_version
from ERICA.modules.helper_funcs.decorators import kigcmd, kigcallback
INFOPIC = True

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

- <code>_italic_</code>: wrapping text with '_' will produce italic text
- <code>*bold*</code>: wrapping text with '*' will produce bold text
- <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
- <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
EG: <code>[test](example.com)</code>

- <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
EG: <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@kigcmd(command='gifid')
def gifid(update: Update, _):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")



@kigcmd(command='echo', pass_args=True, filters=Filters.chat_type.groups)
@user_admin
def echo(update: Update, _):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)

    message.delete()


def shell(command):
    process = Popen(command, stdout=PIPE, shell=True, stderr=PIPE)
    stdout, stderr = process.communicate()
    return (stdout, stderr)

@kigcmd(command='markdownhelp', filters=Filters.chat_type.private)
def markdown_help(update: Update, _):
    chat = update.effective_chat
    update.effective_message.reply_text((gs(chat.id, "markdown_help_text")), parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, `code`, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

stats_str = '''
'''
@kigcmd(command='stats', can_disable=False)
def stats(update, context):
    db_size = SESSION.execute("SELECT pg_size_pretty(pg_database_size(current_database()))").scalar_one_or_none()
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    botuptime = get_readable_time((time.time() - StartTime))
    status = "*╒═══「 Patricia Statistics: 」*\n\n"
    status += "*• System Start time:* " + str(uptime) + "\n"
    uname = platform.uname()
    status += "*• System:* " + str(uname.system) + "\n"
    status += "*• Node name:* " + escape_markdown(str(uname.node)) + "\n"
    status += "*• Release:* " + escape_markdown(str(uname.release)) + "\n"
    status += "*• Machine:* " + escape_markdown(str(uname.machine)) + "\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "*• CPU:* " + str(cpu) + " %\n"
    status += "*• RAM:* " + str(mem[2]) + " %\n"
    status += "*• Storage:* " + str(disk[3]) + " %\n\n"
    status += "*• Python version:* " + python_version() + "\n"
    status += "*• python-telegram-bot:* " + str(ptbver) + "\n"
    status += "*• Uptime:* " + str(botuptime) + "\n"
    status += "*• Database size:* " + str(db_size) + "\n"
    kb = [
          [
           InlineKeyboardButton('Ping', callback_data='pingCB')
          ]
    ]
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    status += f"*• Commit*: `{sha[0:9]}`\n"
    try:
        update.effective_message.reply_text(status +
            "\n*Bot Statistics*:\n"
            + "\n".join([mod.__stats__() for mod in STATS]) +
            "\n\n[Support](https://t.me/srkbotchat) | [Updates](https://t.me/SrkBots)\n\n" +
            "╘══「 [Creator](t.me/notreallysrk) 」\n",
        parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb), disable_web_page_preview=True)
    except BaseException:
        update.effective_message.reply_text(
            (
                (
                    (
                        "\n*Bot Statistics*:\n"
                        + "\n".join(mod.__stats__() for mod in STATS)
                    )
                    + "\n\n[Support](https://t.me/srkbotchat) | [Updates](https://t.me/SrkBots)\n\n"
                )
                + "╘══「 [Creator](t.me/notreallysrk) 」\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
        )


@kigcmd(command='status', can_disable=False)
@sudo_plus
def stats(update, context):
    kb = [
          [
           InlineKeyboardButton('Ping', callback_data='pingCB')
          ]
    ]
    status = "*╒═══「 System Statistics: 」*\n\n"
    try:
        update.effective_message.reply_text(status +
            "\n*Bot statistics*:\n"
            + "\n".join([mod.__stats__() for mod in STATS]) +
            "\n\n[Support](https://t.me/srkbotchat) | [Updates](https://t.me/SrkBots)\n\n" +
            "╘══「 [Creator](t.me/notreallysrk) 」\n",
        parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb), disable_web_page_preview=True)
    except BaseException:
        update.effective_message.reply_text(
            (
                (
                    (
                        "\n*Bot Statistics*:\n"
                        + "\n".join(mod.__stats__() for mod in STATS)
                    )
                    + "\n\n[Support](https://t.me/srkbotchat) | [Updates](https://t.me/SrkBots)\n\n"
                )
                + "╘══「 [Creator](t.me/notreallysrk) 」\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
        )

@kigcmd(command='ping')
def ping(update: Update, _):
    msg = update.effective_message
    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    message.edit_text(
        "*Pong!!!*\n`{}ms`".format(ping_time), parse_mode=ParseMode.MARKDOWN
    )


@kigcallback(pattern=r'^pingCB')
def pingCallback(update: Update, context: CallbackContext):
    query = update.callback_query
    start_time = time.time()
    requests.get('https://api.telegram.org')
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    query.answer('Pong! {}ms'.format(ping_time))


def get_help(chat):
    return gs(chat, "misc_help")



__mod_name__ = "Misc"
