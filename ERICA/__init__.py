import logging
import os
import sys
import time
from typing import List
import spamwatch
from telethon.sessions import StringSession
import telegram.ext as tg
from telethon import TelegramClient
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pyrogram.types import Message
from pyrogram import Client, filters, errors
from telethon.sessions import MemorySession
from configparser import ConfigParser
from ptbcontrib.postgres_persistence import PostgresPersistence
from logging.config import fileConfig

StartTime = time.time()
CMD_HELP = {}


flag = """
\033[37m┌─────────────────────────────────────────────┐\033[0m\n\033[37m│\033[44m\033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[0m\033[91;101m#########################\033[0m\033[37m│\n\033[37m│\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m  \033[0m\033[97;107m:::::::::::::::::::::::::\033[0m\033[37m│\n\033[37m│\033[44m\033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[0m\033[91;101m#########################\033[0m\033[37m│\n\033[37m│\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m  \033[0m\033[97;107m:::::::::::::::::::::::::\033[0m\033[37m│\n\033[37m│\033[44m\033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[0m\033[91;101m#########################\033[0m\033[37m│\n\033[37m│\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m  \033[0m\033[97;107m:::::::::::::::::::::::::\033[0m\033[37m│\n\033[37m│\033[44m\033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[97m★\033[0m\033[44m \033[0m\033[91;101m#########################\033[0m\033[37m│      \033[1mUnited we stand, Divided we fall\033[0m\n\033[37m│\033[97;107m:::::::::::::::::::::::::::::::::::::::::::::\033[0m\033[37m│ \033[1mKigyo Project, a tribute to USS Enterprise.\033[0m\n\033[37m│\033[91;101m#############################################\033[0m\033[37m│\n\033[37m│\033[97;107m:::::::::::::::::::::::::::::::::::::::::::::\033[0m\033[37m│\n\033[37m│\033[91;101m#############################################\033[0m\033[37m│\n\033[37m│\033[97;107m:::::::::::::::::::::::::::::::::::::::::::::\033[0m\033[37m│\n\033[37m│\033[91;101m#############################################\033[0m\033[37m│\n\033[37m└─────────────────────────────────────────────┘\033[0m\n
"""

def get_user_list(key):
    # Import here to evade a circular import
    from ERICA.modules.sql import nation_sql
    royals = nation_sql.get_royals(key)
    return [a.user_id for a in royals]

# enable logging

fileConfig('logging.ini')

#print(flag)
log = logging.getLogger('[ERICA]')
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)
log.info("[ERICA] Erica is starting. | An Eagle Union Project. | Licensed under GPLv3.")
log.info("[ERICA] Not affiliated to Azur Lane or Yostar in any way whatsoever.")
log.info("[ERICA] Project maintained by: github.com/ITZ-ZAID (t.me/TIMESISNOTWAITING)")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    log.error(
        "[ZAID] You MUST have a python version of at least 3.7! Multiple features depend on this. Bot quitting."
    )
    quit(1)

parser = ConfigParser()
parser.read("config.ini")
kigconfig = parser["kigconfig"]

class KigyoINIT:
    def __init__(self, parser: ConfigParser):
        self.parser = parser
        self.SYS_ADMIN: int = self.parser.getint('SYS_ADMIN', 0)
        self.OWNER_ID: int = self.parser.getint('OWNER_ID')
        self.OWNER_USERNAME: str = self.parser.get('OWNER_USERNAME', None)
        self.APP_ID: str = self.parser.getint("APP_ID")
        self.API_HASH: str = self.parser.get("API_HASH")
        self.WEBHOOK: bool = self.parser.getboolean('WEBHOOK', False)
        self.URL: str = self.parser.get('URL', None)
        self.STRING_SESSION: str = self.parser.get('STRING_SESSION', None)
        self.CERT_PATH: str = self.parser.get('CERT_PATH', None)
        self.PORT: int = self.parser.getint('PORT', None)
        self.INFOPIC: bool = self.parser.getboolean('INFOPIC', False)
        self.DEL_CMDS: bool = self.parser.getboolean("DEL_CMDS", False)
        self.STRICT_GBAN: bool = self.parser.getboolean("STRICT_GBAN", False)
        self.ALLOW_EXCL: bool = self.parser.getboolean("ALLOW_EXCL", False)
        self.CUSTOM_CMD: List[str] = ['/', '!']
        self.BAN_STICKER: str = self.parser.get("BAN_STICKER", None)
        self.TOKEN: str = self.parser.get("TOKEN")
        self.DB_URI: str = self.parser.get("SQLALCHEMY_DATABASE_URI")
        self.LOAD = self.parser.get("LOAD").split()
        self.LOAD: List[str] = list(map(str, self.LOAD))
        self.MESSAGE_DUMP: int = self.parser.getint('MESSAGE_DUMP', None)
        self.GBAN_LOGS: int = self.parser.getint('GBAN_LOGS', None)
        self.NO_LOAD = self.parser.get("NO_LOAD").split()
        self.NO_LOAD: List[str] = list(map(str, self.NO_LOAD))
        self.spamwatch_api: str = self.parser.get('spamwatch_api', None)
        self.CASH_API_KEY: str = self.parser.get('CASH_API_KEY', None)
        self.TIME_API_KEY: str = self.parser.get('TIME_API_KEY', None)
        self.WALL_API: str = self.parser.get('WALL_API', None)
        self.LASTFM_API_KEY: str = self.parser.get('LASTFM_API_KEY', None)
        self.CF_API_KEY: str =  self.parser.get("CF_API_KEY", None)
        self.bot_id = 0 #placeholder
        self.bot_name = "Erica" #placeholder
        self.bot_username = "Mrs_Erica_Bot" #placeholder
        self.DEBUG: bool = self.parser.getboolean("IS_DEBUG", False)
        self.DROP_UPDATES: bool = self.parser.getboolean("DROP_UPDATES", True)
        self.BOT_API_URL: str = self.parser.get('BOT_API_URL', "https://api.telegram.org/bot")
        self.BOT_API_FILE_URL: str = self.parser.get('BOT_API_FILE_URL', "https://api.telegram.org/file/bot")


    def init_sw(self):
        if self.spamwatch_api is None:
            log.warning("SpamWatch API key is missing! Check your config.ini")
            return None
        else:
            try:
                sw = spamwatch.Client(spamwatch_api)
                return sw
            except:
                sw = None
                log.warning("Can't connect to SpamWatch!")
                return sw


KInit = KigyoINIT(parser=kigconfig)

SYS_ADMIN = KInit.SYS_ADMIN
OWNER_ID = KInit.OWNER_ID
OWNER_USERNAME = KInit.OWNER_USERNAME
APP_ID = KInit.APP_ID
API_HASH = KInit.API_HASH
WEBHOOK = KInit.WEBHOOK
URL = KInit.URL
CERT_PATH = KInit.CERT_PATH
PORT = KInit.PORT
INFOPIC = KInit.INFOPIC
DEL_CMDS = KInit.DEL_CMDS
ALLOW_EXCL = KInit.ALLOW_EXCL
CUSTOM_CMD = KInit.CUSTOM_CMD
BAN_STICKER = KInit.BAN_STICKER
TOKEN = KInit.TOKEN
DB_URI = KInit.DB_URI
STRING_SESSION = KInit.STRING_SESSION
LOAD = KInit.LOAD
MESSAGE_DUMP = KInit.MESSAGE_DUMP
GBAN_LOGS = KInit.GBAN_LOGS
NO_LOAD = KInit.NO_LOAD
SUDO_USERS = [OWNER_ID] + get_user_list("sudos")
DEV_USERS = [OWNER_ID] + get_user_list("devs")
SUPPORT_USERS = get_user_list("supports")
SARDEGNA_USERS = get_user_list("sardegnas")
WHITELIST_USERS = get_user_list("whitelists")
SPAMMERS = get_user_list("spammers")
spamwatch_api = KInit.spamwatch_api
CASH_API_KEY = KInit.CASH_API_KEY
TIME_API_KEY = KInit.TIME_API_KEY
WALL_API = KInit.WALL_API
LASTFM_API_KEY = KInit.LASTFM_API_KEY
CF_API_KEY = KInit.CF_API_KEY

STRING_SESSION = '1AZWarzoBu1UTbrldjbuCEY0WpSHa8J9Lk48Of-8qB_7CDcT4JtzyW-Mg1eRhtWhOlzzA9s6K3ZrxhbHqCcgAoMRJVhEQT9YJ_buacByEy3KNR2NdrDl-hi9e-MSmBFQEM_alrlDh0pay_87TxEkfczQCnCf1fe19HbAKK7gkBp5qf_aIQEnPgCVh30mfUnUaoPUjNEv44fGKhOBy7bK5C-C2d3ekuS2NJNI4wtthHwKCnWeZ4VGwZNMk4chsCi9IWuqmsKUwlPxQJzx4IMTsl1q4rQA0T1dLA03VqT1DZOlM8f69CowV2XElcfQ-9HhoYU-_8WrIE8cWmEMK4P9VXYPHQWyKLew='
API_ID = '6435225'
API_HASH = '4e984ea35f854762dcde906dce426c2d'
TOKEN = '1901951380:AAF3u3uHfxaomSr0e6o7F1St1D4uWDIMxuY'
WORKERS = 8
# SpamWatch
sw = KInit.init_sw()

from ERICA.modules.sql import SESSION
updaters = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
    
telethn = TelegramClient(MemorySession(), APP_ID, API_HASH)
dispatcher = updater.dispatcher

ubot2 = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot2.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)

pgram = Client("ZPyro", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

MONGO_DB = "ZaidRobot"
MONGO_DB_URL = "mongodb+srv://ZAID2:ZAID2@cluster0.plap4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongodb = MongoClient(MONGO_DB_URL, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)

aiohttpsession = ClientSession()

arq = ARQ("https://thearq.tech", "UIUXOY-NTKWDC-QHFFMD-DHHKVV-ARQ", aiohttpsession)



# Load at end to ensure all prev variables have been set
from ERICA.modules.helper_funcs.handlers import CustomCommandHandler

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler


def spamfilters(text, user_id, chat_id):
    # print("{} | {} | {}".format(text, user_id, chat_id))
    if int(user_id) not in SPAMMERS:
        return False

    print("This user is a spammer!")
    return True


print("Starting Pyrogram Client")
pgram.start()

print("Aquiring BOT Client Info")

bottie = pgram.get_me()

BOT_ID = 1901951380
BOT_USERNAME = 'Zaid2_Robot'
BOT_NAME = 'Zaid Robot'
BOT_MENTION = bottie.mention


# eor help sessions
async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
