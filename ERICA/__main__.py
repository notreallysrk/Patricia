'''#TODO

Dank-del
2020-12-29
'''

import importlib
import re
from typing import Optional
from sys import argv
from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import (
    CallbackContext,
    Filters
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from ERICA import (
    KInit,
    dispatcher,
    updater,
    TOKEN,
    WEBHOOK,
    OWNER_ID,
    CERT_PATH,
    PORT,
    URL,
    log,
    telethn,
    KigyoINIT
)
from typing import Union, List, Dict, Callable, Generator, Any
import itertools
from collections.abc import Iterable
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from ERICA import dispatcher
import ERICA.modules.sql.language_sql as sql
from ERICA.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from ERICA.langs import get_string, get_languages, get_language

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from ERICA.modules import ALL_MODULES
from ERICA.modules.helper_funcs.chat_status import is_user_admin
from ERICA.modules.helper_funcs.misc import paginate_modules
from ERICA.modules.helper_funcs.decorators import kigcmd, kigcallback, kigmsg
from ERICA.modules.language import gs

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("ERICA.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "get_help") and imported_module.get_help:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    '''#TODO

    Params:
        chat_id  -
        text     -
        keyboard -
    '''

    if not keyboard:
        kb = paginate_modules(0, HELPABLE, "help")
        kb.append([InlineKeyboardButton(text='Back', callback_data='innexiahelp_')])
        keyboard = InlineKeyboardMarkup(kb)
    dispatcher.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )



def test(update: Update, context: CallbackContext):
    '''#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    '''
    # pprint(ast.literal_eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)



def start(update: Update, context: CallbackContext):  # sourcery no-metrics
    '''#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    '''
    chat = update.effective_chat
    args = context.args

    if hasattr(update, 'callback_query'):
        query = update.callback_query
        if hasattr(query, 'id'):
            first_name = update.effective_user.first_name
            update.effective_message.edit_text(
                text=gs(chat.id, "pm_start_text").format(
                    escape_markdown(first_name),
                    escape_markdown(context.bot.first_name),
                    OWNER_ID,
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "add_bot_to_group_btn"),
                                url="t.me/{}?startgroup=true".format(
                                    context.bot.username
                                ),
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "support_chat_link_btn"),
                                url='https://t.me/srkbotchat',
                            ),
                            InlineKeyboardButton(
                                text=gs(chat.id, "updates_channel_link_btn"),
                                url="https://t.me/SrkBots",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "helper_btn"),
                                callback_data="innexiahelp_",
                            ),
                            InlineKeyboardButton(
                                text=gs(chat.id, "chlang_btn"),
                                callback_data="callbacklang_",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "donation_btn"),
                                callback_data="donate",
                            ),
                        ],
                    ]
                ),
            )

            context.bot.answer_callback_query(query.id)
            return

    if update.effective_chat.type == "private":
        if args and len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, (gs(chat.id, "pm_help_text")))
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
            elif args[0].lower() == "nations":
                IMPORTED["nations"].send_nations(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(update, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(
                text=gs(chat.id, "pm_start_text").format(
                    escape_markdown(first_name),
                    escape_markdown(context.bot.first_name),
                    OWNER_ID,
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "add_bot_to_group_btn"),
                                url="t.me/{}?startgroup=true".format(
                                    context.bot.username
                                ),
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "support_chat_link_btn"),
                                url='https://t.me/srkbotchat',
                            ),
                            InlineKeyboardButton(
                                text=gs(chat.id, "updates_channel_link_btn"),
                                url="https://t.me/SrkBots",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "helper_btn"),
                                callback_data="innexiahelp_",
                            ),
                            InlineKeyboardButton(
                                text=gs(chat.id, "chlang_btn"),
                                callback_data="callbacklang_",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text=gs(chat.id, "donation_btn"),
                                callback_data="donate",
                            ),
                        ],
                    ]
                ),
            )

    else:
        update.effective_message.reply_text(gs(chat.id, "grp_start_text"))

    if hasattr(update, 'callback_query'):
        query = update.callback_query
        if hasattr(query, 'id'):
            context.bot.answer_callback_query(query.id)


# for test purposes
def error_callback(update, context):
    '''#TODO

    Params:
        update  -
        context -
    '''

    try:
        raise context.error
    except (Unauthorized, BadRequest):
        pass
        # remove update.message.chat_id from conversation list
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated as e:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors



def help_button(update, context):
    '''#TODO

    Params:
        update  -
        context -
    '''

    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    chat = update.effective_chat
    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            help_list = HELPABLE[module].get_help(update.effective_chat.id)
            if isinstance(help_list, list):
                help_text = help_list[0]
                help_buttons = help_list[1:]
            elif isinstance(help_list, str):
                help_text = help_list
                help_buttons = []
            text = (
                    "ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ɪɴꜰᴏ ᴀʙᴏᴜᴛ *{}* ᴍᴏᴅᴜʟᴇ:\n".format(
                        HELPABLE[module].__mod_name__
                    )
                    + help_text
            )
            help_buttons.append(
                [InlineKeyboardButton(text="Back", callback_data="help_back")])
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(help_buttons),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            kb = paginate_modules(curr_page - 1, HELPABLE, "help")
            kb.append([InlineKeyboardButton(text='Back', callback_data='innexiahelp_')])
            query.message.edit_text(
                text=gs(chat.id, "pm_help_text"),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            kb = paginate_modules(next_page + 1, HELPABLE, "help")
            kb.append([InlineKeyboardButton(text='Back', callback_data='innexiahelp_')])
            query.message.edit_text(
                text=gs(chat.id, "pm_help_text"),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb),
            )

        elif back_match:
            kb = paginate_modules(0, HELPABLE, "help")
            kb.append([InlineKeyboardButton(text='Back', callback_data='innexiahelp_')])
            query.message.edit_text(
                text=gs(chat.id, "pm_help_text"),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass



def get_help(update, context):
    '''#TODO

    Params:
        update  -
        context -
    '''

    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text(
            "Welcome to the help menu!",
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Fᴜʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ👩‍🔧", callback_data="help_back"),
                 ],
                 [
                    InlineKeyboardButton(text="💁Bᴀꜱɪᴄ", callback_data="basic_"),
                    InlineKeyboardButton(text="Aᴅᴠᴀɴᴄᴇᴅ🙋", callback_data="advance_"),
                 ],
                 [
                    InlineKeyboardButton(text="👩‍🎓 Exᴘᴇʀᴛꜱ", callback_data="expert_"),
                    InlineKeyboardButton(text="Dᴏɴᴀᴛɪᴏɴ 🎉", url="https://www.paypal.me/piroxpower"),
                 ],
                 [
                    InlineKeyboardButton(text="Cʟᴏꜱᴇ", callback_data="start_back"),
                 ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
                "Here is the available help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].get_help
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, (gs(chat.id, "pm_help_text")))


def send_settings(chat_id, user_id, user=False):
    '''#TODO

    Params:
        chat_id -
        user_id -
        user    -
    '''

    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    elif CHAT_SETTINGS:
        chat_name = dispatcher.bot.getChat(chat_id).title
        dispatcher.bot.send_message(
            user_id,
            text="Which module would you like to check {}'s settings for?".format(
                chat_name
            ),
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
            ),
        )
    else:
        dispatcher.bot.send_message(
            user_id,
            "Seems like there aren't any chat settings available :'(\nSend this "
            "in a group chat you're admin in to find its current settings!",
            parse_mode=ParseMode.MARKDOWN,
        )



def settings_button(update: Update, context: CallbackContext):
    '''#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    '''

    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                     "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            'Message is not modified',
            'Query_id_invalid',
            "Message can't be deleted",
        ]:
            log.exception('Exception in settings buttons. %s', str(query.data))



def get_settings(update: Update, context: CallbackContext):
    '''#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    '''

    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type == chat.PRIVATE:
        send_settings(chat.id, user.id, True)

    elif is_user_admin(update, user.id):
        text = "Click here to get this chat's settings, as well as yours."
        msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Settings",
                            url="t.me/{}?start=stngs_{}".format(
                                context.bot.username, chat.id
                            ),
                        )
                    ]
                ]
            ),
        )
    else:
        text = "Click here to check your settings."



def innexia_about_callback(update, context):
    query = update.callback_query
    if query.data == "innexiahelp_":
        query.message.edit_text(
            text="Welcome to the help menu!",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Fᴜʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ👩‍🔧", callback_data="help_back"),
                 ],
                 [
                    InlineKeyboardButton(text="💁Bᴀꜱɪᴄ", callback_data="basic_"),
                    InlineKeyboardButton(text="Aᴅᴠᴀɴᴄᴇᴅ🙋", callback_data="advance_"),
                 ],
                 [
                    InlineKeyboardButton(text="👩‍🎓 Exᴘᴇʀᴛꜱ", callback_data="expert_"),
                    InlineKeyboardButton(text="Dᴏɴᴀᴛɪᴏɴ 🎉", url="https://www.paypal.me/piroxpower"),
                 ],
                 [
                    InlineKeyboardButton(text="Cʟᴏꜱᴇ", callback_data="start_back"),
                 ]                
                ]
            ),
        )


def basic_about_callback(update, context):
    query = update.callback_query
    if query.data == "basic_":
        query.message.edit_text(
            text="Base Commands."
                 "\n\n👮🏻Available to Admins&Moderators."
                 "\n\n🕵🏻Available to Admins."
                 "\n\n👮🏻/reload updates the Admins list and their privileges."
                 "\n\n🕵🏻/settings lets you manage all the Bot settings in a group."
                 "\n\n👮🏻/ban lets you ban a user from the group without giving him the possibility to join again using the link of the group."
                 "\n\n👮🏻/mute puts a user in read-only mode. He can read but he can't send any messages."
                 "\n\n👮🏻 /kick bans a user from the group, giving him the possibility to join again with the link of the group."
                 "\n\n👮🏻/unban lets you remove a user from group's blacklist, giving them the possibility to join again with the link of the group."
                 "\n\n👮🏻/info gives information about a user."
                 "\n\n\n◽️/staff gives the complete List of group Staff!.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="innexiahelp_"),
                 ]
                ]
            ),
        )

def expert_about_callback(update, context):
    query = update.callback_query
    if query.data == "expert_":
        query.message.edit_text(
            text="*Expert commands*"
                 "\n\n👥 Available to all users"
                 "\n\n👮🏻 Available to Admins&Moderators."
                 "\n\n🕵🏻 Available to Admins"
                 "\n\n🕵🏻 /unbanall Unbanalll members from your groups"
                 "\n\n👮🏻 /unmuteall unmuteall all from Your Group"
                 "\n\n*Pinned Messages*"
                 "\n🕵🏻`/pin [message]` sends the message through the Bot and pins it."
                 "\n\n🕵🏻 /pin pins the message in reply"
                 "\n\n🕵🏻 /unpin removes the pinned message."
                 "\n\n🕵🏻 /adminlist list of all the special roles assigned to users."
                 "\n\n◽️/feedback: (message) to Send message and errors which you are facing \n ex:`/feedback Hey There Is a Something Error @username of chat`!.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="innexiahelp_"),
                 ]
                ]
            ),
        )

def donate_about_callback(update, context):
    query = update.callback_query
    if query.data == "donate":
        query.message.edit_text(
            text=gs(query.message.chat.id, "donation_text"),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="start_back"),
                 ]
                ]
            ),
        )

def advance_about_callback(update, context):
    query = update.callback_query
    if query.data == "advance_":
        query.message.edit_text(
            text="*Advanced Commands*"
                 "\n\n👮🏻Available to Admins&Moderators."
                 "\n\n🕵🏻Available to Admins."
                 "\n\n🛃 Available to Admins&Cleaners"
                 "\n\n*WARN MANAGEMENT*"
                 "\n👮🏻 /warn adds a warn to the user"
                 "\n\n👮🏻 /unwarn removes a warn to the user"
                 "\n\n👮🏻 /warns lets you see and manage user warns"
                 "\n\n🕵🏻 /delwarn deletes the message and add a warn to the user"
                 "\n\n🛃 /del deletes the selected message"
                 "\n\n🛃 /purge deletes from the selected message."
                 "\n\n◽️/feedback: (message) to Send message and errors which you are facing \n ex:`/feedback Hey There Is a Something Error @username of chat`!.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="innexiahelp_"),
                 ]
                ]
            ),
        )







@kigcmd(command='donate')
def donate(update: Update, context: CallbackContext):
    '''#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    '''

    update.effective_message.reply_text("https://www.paypal.me/piroxpower")





def paginate(
    iterable: Iterable, page_size: int
) -> Generator[List, None, None]:
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (
            itertools.islice(i1, page_size, None),
            list(itertools.islice(i2, page_size)),
        )
        if not page:
            break
        yield page


def gs(chat_id: Union[int, str], string: str) -> str:
    lang = sql.get_chat_lang(chat_id)
    return get_string(lang, string)


@user_admin
def set_language(update: Update, _) -> None:
    chat = update.effective_chat
    query = update.callback_query
    msg = update.effective_message

    msg_text = gs(chat.id, "curr_chat_lang").format(
        get_language(sql.get_chat_lang(chat.id))[:-3]
    )

    keyb = [InlineKeyboardButton(
                text=name,
                callback_data=f"setLanguage_{code}",
            ) for code, name in get_languages().items()]
    keyb = list(paginate(keyb, 2))
    keyb.append(
        [
            InlineKeyboardButton(text="Back", callback_data="start_back"),
        ]
    )
    query.message.edit_text(msg_text, reply_markup=InlineKeyboardMarkup(keyb))


@user_admin_no_reply
def lang_buttons(update: Update, _) -> None:
    query = update.callback_query
    chat = update.effective_chat

    query.answer()
    lang = query.data.split("_")[1]
    sql.set_lang(chat.id, lang)

    query.message.edit_text(
        gs(chat.id, "set_chat_lang").format(get_language(lang)[:-3])
    )

@kigmsg((Filters.status_update.migrate))
def migrate_chats(update: Update, context: CallbackContext):
    '''#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    '''

    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    log.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    log.info("Successfully migrated!")
    raise DispatcherHandlerStop

test_handler = CommandHandler("test", test)
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", get_help)
START_BACK = CallbackQueryHandler(start, pattern=r"start_back")
settings = CommandHandler("settings", get_settings)
SETING_HANDLER = CallbackQueryHandler(settings_button, pattern=r"stngs_")
HELP_HANDLER = CallbackQueryHandler(help_button, pattern=r"help_")
SETLANGUAGE_HANDLER = CallbackQueryHandler(set_language, pattern=r"callbacklang_")
SETLANGGUAGE_BUTTON_HANDLER = CallbackQueryHandler(lang_buttons, pattern=r"setLanguage_")
about_callback_handler = CallbackQueryHandler(
        innexia_about_callback, pattern=r"innexiahelp_", run_async=True
    )
basic_callback_handler = CallbackQueryHandler(
        basic_about_callback, pattern=r"basic_", run_async=True
    )
advance_callback_handler = CallbackQueryHandler(
        advance_about_callback, pattern=r"advance_", run_async=True
    )
expert_callback_handler = CallbackQueryHandler(
        expert_about_callback, pattern=r"expert_", run_async=True
    )
donate_callback_handler = CallbackQueryHandler(
        donate_about_callback, pattern=r"donate", run_async=True
    )
dispatcher.add_handler(test_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(START_BACK)
dispatcher.add_handler(settings)
dispatcher.add_handler(SETING_HANDLER)
dispatcher.add_handler(HELP_HANDLER)
dispatcher.add_handler(SETLANGUAGE_HANDLER)
dispatcher.add_handler(SETLANGGUAGE_BUTTON_HANDLER)
dispatcher.add_handler(about_callback_handler)
dispatcher.add_handler(basic_callback_handler)
dispatcher.add_handler(advance_callback_handler)
dispatcher.add_handler(expert_callback_handler)
dispatcher.add_handler(donate_callback_handler)


def main():
    dispatcher.add_error_handler(error_callback)
    # dispatcher.add_error_handler(error_handler)

    if WEBHOOK:
        log.info("Using webhooks.")
        updater.start_webhook(listen="127.0.0.1", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        log.info(f"Erica started, Using long polling. | BOT: [@{dispatcher.bot.username}]")
        KigyoINIT.bot_id = dispatcher.bot.id
        KigyoINIT.bot_username = dispatcher.bot.username
        KigyoINIT.bot_name = dispatcher.bot.first_name
        updater.start_polling(timeout=15, read_latency=4, allowed_updates=Update.ALL_TYPES, drop_pending_updates=KInit.DROP_UPDATES)
    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()
    updater.idle()


if __name__ == "__main__":
    log.info("[ERICA] Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    main()
